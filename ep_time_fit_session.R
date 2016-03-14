library(minpack.lm)
library(reliaR)
library(sfsmisc)
library(ggplot2)
library(scales)
source("ptsal.R")



data <- read.table("D:/dorm2/2015/paper/extractdata/ses_20081013.txt") # read data1 from file session_extract_usask.txt
colnames(data) <- c("time","ip", "numcon", "size") # Assign names for the column
data$time <- c(0,diff(as.numeric(data$time)))
Fn <- ecdf(data$time/mean(data$time))
x <- lseq(0.01, 1e+6,length = 200) # min(ep)= 0.007969651
ep <- 1 - Fn(x)



wf<- seq(1,10,length.out = length(x))^40
fit <- nlsLM(ep ~ pts.qexp(x, shape,scale, lower.tail =F ), data = data, start = list(shape=1, scale=1),
             lower=c(1e-5, 1e-5), upper=c(20,20), weights = wf)
yfit <-pts.qexp(x, coef(fit)[1], coef(fit)[2], lower.tail=F)

datap <- data.frame(x=x, ep=ep,  epf=yfit)
p <- ggplot(datap, aes(x))
p + geom_point(aes(y = ep, shape="a"), colour="black", size=5)+
  geom_line(aes(y = epf), colour="black", size=1)+
  scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(0.01,100))+
  scale_y_log10(breaks = c(10^-4, 10^-3,10^-2,10^-1, 1), labels = trans_format("log10", math_format(10^.x)))+
  coord_cartesian(xlim = c(10^-2, 110), ylim = c(10^-4, 1.2))+
  theme_bw()+
  theme(panel.grid.major=element_blank(), legend.position="none",
        text=element_text(size=25),
        panel.border = element_rect(colour = "black", fill=NA))+
  
 ylab("Cumulative probability\n")+xlab("\nInter-request time (normalized)")





