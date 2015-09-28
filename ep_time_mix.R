library(minpack.lm)
library(reliaR)
library(sfsmisc)


data1 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150416D.txt")
data2 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150417D.txt")
data3 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150418D.txt")
data4 <- read.table("D:/dorm2/20150921/ep_time/ep_time_20150419D.txt")



data1$V1 <- NULL
data2$V1 <- NULL
data3$V1 <- NULL
data4$V1 <- NULL
data1 <- head(data1,10000)
data2 <- head(data2,10000)
data3 <- head(data3,10000)
data4 <- head(data4,10000)
data <- cbind(data1, data2, data3, data4)



