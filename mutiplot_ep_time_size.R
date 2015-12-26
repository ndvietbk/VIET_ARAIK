# This script multiplot graphics ep_time, ep_size of sessions
library(minpack.lm)
library(reliaR)
library(sfsmisc)
library(ggplot2)
library(gridExtra)
library(scales)
source("ptsal.R")

#Read log-------------------------------------------------
data1 <- read.table("D:/dorm2/2016/Extract_session/usask_extract_session_3000.txt")
colnames(data1)<- c("host", "time", "size")
data2 <- read.table("D:/dorm2/2016/Extract_session/nasa_extract_session_3000.txt")
colnames(data2)<- c("host", "time", "size")



Fn1_time <- ecdf(data1$time/mean(data1$time, na.rm = T))
Fn1_size<- ecdf(data1$size/mean(data1$size, na.rm = T))

Fn2_time <- ecdf(data2$time/mean(data2$time, na.rm = T))
Fn2_size<- ecdf(data1$size/mean(data2$size, na.rm = T))


x <- lseq(0.01, 100,length = 30) 
ep1_time <- 1 - Fn1_time(x)
ep2_time <- 1-Fn2_time(x)

ep1_size <- 1 - Fn1_size(x)
ep2_size <- 1-Fn2_size(x)





datap <- data.frame(x,ep1_time = ep1_time, ep2_time = ep2_time, ep1_size = ep1_size, ep2_size=ep2_size)

# Graphic ccdf of session time for DORM2 (only example)
p1 <- ggplot(datap,aes(x=x,y=ep1_time)) + 
geom_point(size=2.5, color="red") +
theme_bw()+
theme(panel.grid.major=element_blank(), legend.position="none", text=element_text(size=25))+
theme(axis.title.x = element_blank()) +
#theme(axis.title.y = element_blank()) +
theme(axis.text.x = element_blank()) + 
#theme(axis.text.y = element_blank()) +
theme(legend.position="none",plot.margin=unit(c(0,0,0,0), "cm")) +
ylab("CCDF of session time")+
labs(title = "DORM2") +
theme(plot.title = element_text(size = rel(1), colour = "black"))+
scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(0.01,100))+
scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(1e-4,1)) +
coord_cartesian(xlim = c(10^-2, 300), ylim = c(10^-4, 1.2))


# Graphic ccdf of session time for WIDE (only example)
p2 <- ggplot(datap,aes(x=x,y=ep1_time)) +  
  geom_point(size=2.5, color="red") +
  theme_bw()+
  theme(panel.grid.major=element_blank(), legend.position="none", text=element_text(size=25))+
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  theme(axis.text.x = element_blank()) + 
  theme(axis.text.y = element_blank()) +
  theme(plot.margin=unit(c(0,0,0,0), "cm"))+
  labs(title = "WIDE")+
  theme(plot.title = element_text(size = rel(1), colour = "black"))+
  scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
              labels = trans_format("log10", math_format(10^.x)),
              limits=c(0.01,100))+
  scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(1e-4,1)) +
  coord_cartesian(xlim = c(10^-2, 300), ylim = c(10^-4, 1.2))


# Graphic ccdf of session time for USASK and NASA
p3 <- ggplot(datap,aes(x=x)) + 
  geom_point(aes(y = ep1_time, shape="a"), colour="red", size=3)+
  geom_point(aes(y = ep2_time, shape="b"), colour="blue", size=3)+
  theme_bw()+
  theme(panel.grid.major=element_blank(), legend.position="none", text=element_text(size=25))+
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  theme(axis.text.x = element_blank()) + 
  theme(axis.text.y = element_blank()) +
  theme(plot.margin=unit(c(0,0,0,0), "cm"))+
  labs(title = "USASK + NASA", size =2)+
  theme(plot.title = element_text(size = rel(1), colour = "black"))+
  scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
              labels = trans_format("log10", math_format(10^.x)),
              limits=c(0.01,100))+
  scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(1e-4,1))+
  coord_cartesian(xlim = c(10^-2, 300), ylim = c(10^-4, 1.2))


#CCDF of session size for DORM2 (only example)
p4 <- ggplot(datap,aes(x=x,y=ep1_time)) + 
  geom_point(size=2.5, color="red") +
  theme_bw()+
  theme(panel.grid.major=element_blank(), legend.position="none", text=element_text(size=25))+
  theme(axis.title.x = element_blank()) +
  # theme(axis.title.y = element_blank()) +
  # theme(axis.text.x = element_blank()) + 
  # theme(axis.text.y = element_blank()) +
  theme(plot.margin=unit(c(0,0,0,0), "cm")) +
  ylab("CCDF of session size") +
  scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
              labels = trans_format("log10", math_format(10^.x)),
              limits=c(0.01,100))+
  scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(1e-4,1))+
  coord_cartesian(xlim = c(10^-2, 300), ylim = c(10^-4, 1.2))


#CCDF of session size for WIDE (only example)
p5 <- ggplot(datap,aes(x=x,y=ep1_time)) +  
  geom_point(size=2.5, color="red") +
  theme_bw()+
  theme(panel.grid.major=element_blank(), legend.position="none", text=element_text(size=25))+
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
 #theme(axis.text.x = element_blank()) + 
  theme(axis.text.y = element_blank()) +
  theme(legend.position="none",plot.margin=unit(c(0,0,0,0), "cm"))+
  scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
              labels = trans_format("log10", math_format(10^.x)),
              limits=c(0.01,100))+
  scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(1e-4,1))+
  coord_cartesian(xlim = c(10^-2, 300), ylim = c(10^-4, 1.2))


#CCDF of session size for USASK and NASA
p6 <- ggplot(datap,aes(x=x)) + 
  geom_point(aes(y = ep1_size, shape="a"), colour="red", size=3)+
  geom_point(aes(y = ep2_size, shape="b"), colour="blue", size=3)+
  theme_bw()+
  theme(panel.grid.major=element_blank(), legend.position="none", text=element_text(size=25))+
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  # theme(axis.text.x = element_blank()) + 
  theme(axis.text.y = element_blank()) +
  theme(legend.position="none",plot.margin=unit(c(0,0,0,0), "cm"))+
  scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(0.01,100))+
  scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x)),
                limits=c(1e-4,1))+
  coord_cartesian(xlim = c(10^-2, 300), ylim = c(10^-4, 1.2))
 

# Multiplot graphics
grid.arrange(p1, p2, p3, p4,p5,p6,ncol=3,
             widths = unit(c(1.2, 1, 1), "null"),heights = unit(c(1, 1), "null"),
             bottom="Bottom title"
             )



           
 
