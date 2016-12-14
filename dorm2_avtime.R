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

ftype <- "D"
fdate <- c(20150317, 20150318, 20150416, 20150417, 20150418, 20150419, 20160426, 20160427, 20160428, 20160429)
fdate <- fdate[1:2]
a=0.1
b=15
ind <- c(2, seq(4, 7, by=1), 9, 10)
for (i in 1:length(fdate)) {
  fyear <- substr(fdate[i],1,4)
  fmonth <- substr(fdate[i],5,6)
  fday <- substr(fdate[i], 7, 8)
  times <-  gsub(":", "", substr(seq(ISOdatetime(fyear,fmonth,fday,0,0,0), ISOdatetime(fyear,fmonth,fday,23,45,0), length.out=96), 12, 16))
  timestamp <- paste(fdate[i], "_", times, sep="")
  fnum <- 96
  infile <- paste("ses/", ftype, substr(timestamp, 1, 8) ,"/ses_", ftype, timestamp, ".txt.gz", sep="")
  avtime <- numeric(fnum)
  for (j in 1:fnum) {
    if (file.exists(infile[j])) {
      data <- fread(paste("C:/zcat.exe ", infile[j], sep=""))
      data1 <-  data[with(data, order(-V4)), ]
      data1 <-  data1[with(data1, order(V1)), ]
      var1 <- diff(data1$V1)
      avtime[j] <- mean(var1)
      if (j == 1) {
        var <- var1
      } else {
        var <- c(var, var1)
      }
    } else {
      avtime[j] <- avtime[j-1]
    }
  }
  nn <- 100
  nvar <- mean(avtime)/avtime
  print(sum(nvar[nvar<0]))
  p <- density(nvar, from=0,  n = nn)
  out <- data.frame(x = p$x, p = p$y)
  
  if (i == 1) {
    pl <- ggplot()
    pl <- pl + #scale_x_continuous(limits = c(0, 3))+
      scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x, n=3),
                    labels = trans_format("log10", math_format(10^.x)),
                    limits=c(1e-3, 1))+
      theme_bw()+
      theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), 
            legend.position="none", text=element_text(size=20), axis.text=element_text(size=20))+ 
      ylab(bquote(paste(~bar(beta), " ", ~italic(p), "(", ~beta, ")", sep=""))) + 
      xlab(bquote(paste(~beta, "/", ~bar(beta))))+
      geom_text(aes(label = "c", x = 3, y = 0.8), size=8, parse = TRUE)
  }
  pl <- pl + geom_point(data=out, aes(x = x, y = p), shape=1, color = "red", size = 3)
}


xf <- seq(0, 3, length.out=100)
pf <- dnorm(xf, 1.3, .45)
outf <- data.frame(xf = xf, pf = pf)
pl <- pl+geom_line(data=outf, aes(x = xf, y = pf), linetype = 2, color = "black", size=1)

print(pl)

