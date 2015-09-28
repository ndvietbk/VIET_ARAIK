library(minpack.lm)
library(reliaR)
library(sfsmisc)

data1 <- read.table("D:/dorm2/20150921/ep_time_session_usk.txt")
data2 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150416D.txt")
data3 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150417D.txt")
data4 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150418D.txt")
data5 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150419D.txt")
data6 <- read.table("D:/dorm2/20150921/ep_time/ep_time_1_2011D.txt")


data1$V1 <- NULL
data2$V1 <- NULL
data3$V1 <- NULL
data4$V1 <- NULL
data5$V1 <- NULL
data6$V1 <- NULL
x <- lseq(7.96e-2, 1000, length = 10000)
data <- cbind(x,data1, data2, data3, data4, data5, nrow=10000)



