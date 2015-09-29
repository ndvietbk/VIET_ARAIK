library(reliaR)

n <- 1e+5
alpha <- 0.33
lambda <- 20
nthr <- 2

# Generate threads
for (i in 1:nthr) {
  one.thr <- rexp.ext(n, alpha, lambda)
  if (i == 1) {
    all.thr <- one.thr
  } else {
    all.thr <- cbind(all.thr, matrix(one.thr))
  }
}

# Combine threads to one thread using random mix
for (i in 1:n) {
  if (i == 1) {
    comb.thr <- 0
  }
  j <- sample(1:4, 4) #generate random number in 1:4
  comb.thr <- c(comb.thr, all.thr[i, j])
}
comb.thr <- x[2:length(comb.thr)]
