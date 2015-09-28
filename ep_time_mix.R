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
colnames(data) <- c("V1", "V2", "V3", "V4")

# main loop for swap data$V1,...,data$V4
for (i in 1:10000) {
  n <- sample(1:4,4,replace = F) #generate random number in 1:4
  data_temp <- data[i,]
  data[i, ]$V1 <- data_temp[n[1]] 
  data[i, ]$V2 <- data_temp[n[2]]
  data[i, ]$V3 <- data_temp[n[3]]
  data[i, ]$V4 <- data_temp[n[4]]
}
