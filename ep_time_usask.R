library(minpack.lm)
library(reliaR)
library(sfsmisc)



data <- read.table("D:/dorm2/20150921/session_extract_usask.txt") # read data from file session_extract_usask.txt
colnames(data) <- c("time","num_connection", "ssize") # Assign names for the column

Fn <- data$time
x <- seq(1,100,length.out = 100)
ep <- 1-Fn(x)
out <- data.frame(x=x, ep=ep)
write.table(out, "ep_time_session_usk.txt", row.names = F, col.names = F)
plot(x,ep, type ="p", log="xy", xlab = "Time between sessions, seconds", ylab="Cumulative probability")


