library(data.table)
library(ggplot2)
library(scales)
library(sfsmisc)
library(minpack.lm)
source("ptsal.R")

ftype='D'
fdate <- c(20150317, 20150318, 20150416, 20150417, 20150418, 20150419, 20160426, 20160427, 20160428, 20160429)
fdate <- fdate[1:2]

fcol <- c("red", "blue", "green3", "violet", "orange", "cyan", "brown", "purple", "maroon", "grey")
fshp <- seq(1,10, by=1)
start=1
for (i in 1:length(fdate)) {
  fyear <- substr(fdate[i],1,4)
  fmonth <- substr(fdate[i],5,6)
  fday <- substr(fdate[i], 7, 8)
  times <-  gsub(":", "", substr(seq(ISOdatetime(fyear,fmonth,fday,0,0,0), ISOdatetime(fyear,fmonth,fday,23,45,0), length.out=96), 12, 16))
  timestamp <- paste(fdate[i], "_", times, sep="")
  fnum <- 96
  # For Windows download zcat.exe and replace "zcat" with "<path_to_zcat>\zcat.exe"
  infile <- paste("zcat ses/", ftype, substr(timestamp, 1, 8) ,"/ses_", ftype, timestamp, ".txt.gz", sep="")
  avtime <- numeric(fnum)
  for (j in 1:fnum) {
    data <- fread(infile[j])
    data1 <-  data[with(data, order(-V4)), ]
    data1 <-  data1[with(data1, order(V1)), ]
    var1 <- data1$V4
    var1 <- var1[!is.na(var1)]
    avtime[j] <- mean(var1)
    if (j == 1) {
      var <- var1
    } else {
      var <- c(var, var1)
    }
  }
  
  nvar <- var/mean(var)
  p <- density(nvar, to=80, n = 64, adjust = 12)
  out <- data.frame(x = p$x, p = p$y)
  
  if (i == 1) {
    pl <- ggplot()
    pl <- pl + scale_x_continuous(limits = c(0, 35))+
              scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x, n = 4),
                            labels = trans_format("log10", math_format(10^.x)),limits=c(1e-3, 1.5))+
              theme_bw()+
              theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), 
                    legend.position="none", text=element_text(size=20), axis.text=element_text(size=20),
                    axis.title=element_text(size=25, face="bold"))+
  
              ylab(bquote(paste(~bar(italic(v)), " ", ~italic(p), "(", ~italic(v), ")", sep=""))) +
              xlab(bquote(paste(~italic(v), "/", ~bar(italic(v)))))
             # 
  }
   pl <- pl + geom_point(data=out, aes(x=x, y=p), shape=1, size=3, colour=fcol[i])
}

x <-seq(0, 50, length.out=100)
q <- 1.5
lam <- 1.25
wf <- (seq(1, 1, length.out=length(out$x)))^3
fit <- nlsLM(p ~ dts.qexp(x, q, p2), start = list(p2 = 1),
             data = out, lower = 0.01, upper = 100, weights = wf)
pf <- dts.qexp(x, q, lam)
out<- data.frame(x, pf)

qtext <- paste("italic(q) == ", q)
ltext <- paste("lambda == ", lam)
pl <- pl + geom_line(data=out,aes(x=x, y=pf), linetype=2, size=2, colour="black") +
      geom_text(aes(label = qtext, x = 31, y = 1.2), size=8, parse = TRUE)+
      geom_text(aes(label = ltext, x = 31, y = 0.6), size=8, parse = TRUE)
print(pl)


