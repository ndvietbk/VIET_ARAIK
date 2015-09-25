library(minpack.lm)
library(reliaR)
library(sfsmisc)
source("qexp.R")

pstrgamma <- function(q, gamma_eff, lambda, lower.tail = TRUE) {
  if (lower.tail) {
    y <- 1 - exp(-lambda*(q)^gamma_eff)
  } else {
    y <- exp(-lambda*(q)^gamma_eff)
  }
  return(y)
}

powerlawcutoff <- function(x, alpha, lambda) {
  y <- x^(-alpha)*exp(-lambda*x)
  return(y)
}

pbipareto <- function(q, alpha, beta, k, b, lower.tail = TRUE) {
  y <- numeric(length(q))
  y[q > k] <- (q[q > k]/k)^(-alpha)*((q[q > k]+k*b)/(k+k*b))^(alpha-beta)
  y[q <= k] <- 1
  if(lower.tail) {
    y <- 1-y
  }
  return(y)
}

ppower <- function(q, shape, scale, lower.tail = TRUE) {
  if (lower.tail) {
    y <- 1 - (x/scale)^(1 - shape)
  } else {
    y <- (x/scale)^(1 - shape)
  }
  return(y)
}

dpowercutoff <- function(x, alpha, lambda, xmin) {
  y <- lambda^(1-alpha)/dgamma(x, 1-alpha, lambda*xmin)
}

ppowercutoff <- function(q, alpha, lambda, xmin, lower.tail = TRUE) {
  y <- cumsum(dpowercutoff(q, alpha, lambda, xmin))
  if(!lower.tail) {
    y <- 1-y
  }
}

timestamp <- "20150416"
pnum <- 43
aggr <- 10  # in ms
for (i in 1:pnum) {
  if (i < 10) {
    filename <- paste("/data/araik/dorm2/2015/DNL/", timestamp, "0000/itime/itime_0.01_", timestamp, "_DNL_p0", i, ".txt", sep="")
  } else {
    filename <- paste("/data/araik/dorm2/2015/DNL/", timestamp, "0000/itime/itime_0.01_", timestamp, "_DNL_p", i, ".txt", sep="")
  }
  if (i == 1) {
    data <- read.table(filename, col.names="itime")
  } else {
    data1 <-  read.table(filename, col.names="itime")
    data <- rbind(data, data1)
  }
}

Fn <- ecdf(data$itime)
x <- lseq(1e-2, 1000, length = 100)
ep <- 1-Fn(x)
out <- data.frame(x=x, ep=ep)
write.table(out, paste("~/data/dorm2/ep/time/time_0.01_", timestamp, ".txt", sep=""), row.names = FALSE, col.names = FALSE)
plot(x, ep, type="p", log="xy",
     main = paste(timestamp, ", aggr = ", aggr, " ms", sep=""),
     xlab = "Time between sessions, seconds",
     ylab = "Cumulative probability")

#wfdeg <- 20
#wf <- (seq(1, 10, length.out=length(ep)))^wfdeg
#fit <- nlsLM(ep.av ~ ptsal(x, p1, p2, lower.tail = FALSE), start=list(p1 = 1, p2 = 1),
#             lower=c(0.01, 0.01), upper=c(10, 10), weights=wf)
#ep.fit <- ptsal(x, coef(fit)[1], coef(fit)[2], lower.tail = FALSE)
#lines(x, ep.fit, col="red")

