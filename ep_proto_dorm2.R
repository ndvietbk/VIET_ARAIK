library(data.table)

fdate <- 20150417
proto <- "HTTP"
pnum <- 43
for (i in 1:pnum) {
  if (i < 10) {
    infile <- paste("~/data/dorm2/2015/DNL/", fdate, "/", proto, "/", proto, "_", fdate, "_DNL_p0", i, ".txt", sep="")
  } else {
    infile <- paste("~/data/dorm2/2015/DNL/", fdate, "/", proto, "/", proto, "_", fdate, "_DNL_p", i, ".txt", sep="")
  }
  if (i == 1) {
    dlog <- fread(infile)
  } else {
    dlog1 <- fread(infile)
    dlog1$V1 <- dlog$V1+dlog$V1[length(dlog$V1)]
    dlog <- rbind(dlog, dlog1)
  }
}

int.time <- diff(dlog$V1)
Fn <- ecdf(int.time/mean(int.time))
x <- lseq(.1, 100, length = 1000)
ep <- 1-Fn(x)
plot(x, ep, log="xy", type="l", main = paste("DORM2", fdate, proto, sep="-"),
     xlim=c(.1,100), ylim=c(1e-5,1),
     xlab = "Time betweeb packets, seconds",
     ylab = "Exceedance probability")

