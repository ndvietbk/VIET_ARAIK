library(data.table)
library(doParallel)
library(minpack.lm)
library(pracma)
library(ggplot2)
library(scales)
library(VGAM)
source("ptsal.R")

beck_model <- function(tvec, b1) {
  p <- numeric(length(tvec))
  den <- density(b1, n = 1000)
  b <- den$x
  fb <- den$y
  
  for (i in 1:length(tvec)) {
    p[i] <- trapz(b, fb*b*exp(-b*tvec[i]))
  }
  print(trapz(tvec, p))
  return(p)
}


ses.flow <- function(n, lambda) {
  #n <- round(tsim/lambda)
  time <- rexp(n, lambda)
  #timeline <- cumsum(time)
  return(time)
}

beck_sim <- function(n, lambda) {
  # Calculate the number of cores
  no_cores <- detectCores() - 1
  
  # Initiate cluster
  cl <- makeCluster(no_cores)
  
  # Calculate session flows
  timeline <- clusterMap(cl, ses.flow, lambda,  MoreArgs=list(n=n))
  
  # Stop cluster
  stopCluster(cl)
  
  timeline <- unlist(timeline)
#  timeline <- sort(timeline)
#  time.flow <- diff(timeline)
  return(timeline)
}

ftype <- ""
fdate <- c(20080318, 20080319, 20080320, 20090330, 20090331, 20090401, 20090402, 20100413, 20100414, 20100415)
#fdate <- 20080318
a=0.1
b=15
for (i in 1:10) {
  fyear <- substr(fdate[i],1,4)
  fmonth <- substr(fdate[i],5,6)
  fday <- substr(fdate[i], 7, 8)
  times <-  gsub(":", "", substr(seq(ISOdatetime(fyear,fmonth,fday,0,0,0), ISOdatetime(fyear,fmonth,fday,23,45,0), length.out=96), 12, 16))
  timestamp <- paste(fdate[i], times, sep="")
  fnum <- 96
  infile <- paste("ses/", ftype, substr(timestamp, 1, 8) ,"/ses_", ftype, timestamp, ".txt.gz", sep="")
  avtime <- numeric(fnum)
  for (j in 1:fnum) {
    if (file.exists(infile[j])) {
      data <- fread(paste("zcat ", infile[j], sep=""))
      data1 <-  data[with(data, order(-V4)), ]
      data1 <-  data1[with(data1, order(V1)), ]
      var1 <- diff(data1$V1)
      avtime[j] <- mean(var1)
      if (j == 1) {
        var <- var1
      } else {
        var <- c(var, var1)
      }
    }
  }
  nn <- 100
  nvar <- var/mean(var)
  p <- density(nvar, from = a, to=b, n = nn)
  out <- data.frame(x = p$x, p = p$y)
  # Fit with q-exponential distribution
  wf <- (seq(1, 10, length.out=length(p$x)))^10
  fit <- nlsLM(p ~ dts.qexp(x, p1, p2), start = list(p1 = 1, p2 = 1),
               data = out, lower = c(0.01, 0.01), upper = c(100, 100), weights = wf)
  print(fit)
  pf <- dts.qexp(out$x, coef(fit)[1], coef(fit)[2])
  
  #lam1 <- 1/rweibull(10000, 7, 1.1)
  lam1 <- rnorm(10000, 1.02, 0.1)
  x2 <- seq(a, b, length.out = nn)
  pb <- beck_model(x2, lam1)
  out$pb <- pb

  svar <- beck_sim(10000, lam1)
  svar <- svar/mean(svar)
  ps <- density(svar, from=a, to=b, n=50)
  outs <- data.frame(xs=ps$x, ps=ps$y)
  
  
  out <- cbind(out, pf)
  out <- cbind(out, pb)
  out <- cbind(out, outs)
  
  qtext <- paste("italic(q) == ", round(coef(fit)[1], 2))
  ltext <- paste("lambda == ", round(coef(fit)[2], 2))
  

  pl <- ggplot(out)
  pl <- pl + geom_point(aes(x = x, y = p), shape=1, color = "red", size = 3)+
            geom_line(aes(x = x, y = pf), linetype = 2, color = "black", size=1)+
            geom_line(aes(x = x, y = pb), color = "blue", size=1)+
            geom_point(aes(x = xs, y = ps), shape=0, color = "green3", size=3)+
            scale_x_continuous(limits = c(0, 15))+
            scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                          labels = trans_format("log10", math_format(10^.x)),
                          limits=c(1e-5, 1))+
            theme_bw()+
            theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), 
                  legend.position="none", text=element_text(size=20), axis.text=element_text(size=20))+ 
            ggtitle(bquote(paste(.(fday), "/", .(fmonth), "/", .(fyear), sep="")))+
            
            ylab(bquote(paste(~bar(tau), " ", ~italic(p), "(", ~tau, ")", sep=""))) + 
            xlab(bquote(paste(~tau, "/", ~bar(tau))))+
            geom_text(aes(label = qtext, x = 14, y = .8), size=8, parse = TRUE)+
            geom_text(aes(label = ltext, x = 14, y = .3), size=8, parse = TRUE)
  setEPS()
  postscript(paste("~/Dropbox/paper_new/paper_new/fig2_", i, ".eps", sep=""))
  print(pl)
  dev.off()
}




