library(minpack.lm)
library(reliaR)
library(sfsmisc)



data <- read.table("D:/dorm2/20150921/session_extract_usask.txt") # read data from file session_extract_usask.txt
colnames(data) <- c("time","num_connection", "ssize") # Assign names for the column
Fn <- ecdf(data$time/mean(data$time))
ep <- 1 - Fn(x)
x <- lseq(7.96e-2, 1000,length = 100) # min(ep)= 0.007969651

out <- data.frame(x=x, ep=ep)
write.table(out, "ep_time_session_usk.txt", row.names = F, col.names = F)
plot(x,ep, type ="p", log="xy", xlab = "Time between sessions, seconds", ylab="Cumulative probability")
wf2 <- seq(1,10,length.out = length(x))^35
fit <- nlsLM(ep ~ pexp.ext(x, alpha,lambda, lower.tail = F), data = data, start = list(alpha=1, lambda=1),
             lower=c(1e-5, 1e-5), upper=c(20,20), weights = wf2)

yfit <-pexp.ext(x, coef(fit)[1], coef(fit)[2], lower.tail=F)
lines(x, yfit, col="red", lwd=2)


data1 <-read.table("D:/dorm2/20150921/ep_time/ep_time_20150416D.txt")
data2 <-read.table("D:/dorm2/20150921/ep_time/ep_time_20150417D.txt")
data3 <-read.table("D:/dorm2/20150921/ep_time/ep_time_20150418D.txt")
data4 <-read.table("D:/dorm2/20150921/ep_time/ep_time_20150418D.txt")
data5 <- read.table("D:/dorm2/20150921/ep_time/ep_time_1_2011D.txt")
data1$V1 <- data1$V1/mean(data1$V1)
data2$V1 <- data2$V1/mean(data2$V1)
data3$V1 <- data3$V1/mean(data3$V1)
data4$V1 <- data4$V1/mean(data4$V1)
data5$V1 <- data5$V1/mean(data5$V1)

  
points(data1$V1, data1$V2,col ="green")
points(data2$V1, data2$V2, col="blue")
points(data3$V1, data3$V2, col="brown")
points(data4$V1, data4$V2, col="coral")
points(data5$V1, data5$V2, col = "DarkGreen")
