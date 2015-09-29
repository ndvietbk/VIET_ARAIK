library(reliaR)

n <- 1e+5
alpha <- 0.33
lambda <- 20
data1 <- rexp.ext(n, alpha, lambda)
data2 <- rexp.ext(n, alpha, lambda)
data3 <- rexp.ext(n, alpha, lambda)
data4 <- rexp.ext(n, alpha, lambda)

data <- cbind(matrix(data1), matrix(data2), matrix(data3), matrix(data4))

# main loop for swap data$V1,...,data$V4
for (i in 1:n) {
  if (i == 1) {
    x <- 0
  }
  j <- sample(1:4,4,replace = F) #generate random number in 1:4
  k <- 0
  x <- c(x, data[i,j])
}

x <- x[2:length(x)]
