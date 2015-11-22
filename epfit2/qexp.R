library(VGAM)

dqexp <- function(x, shape, rate) {
  y <- dgpd(x, 0, shape=(shape-1)/(2-shape),
            scale=1/(rate*(2-shape)))
    return(y)
}

# pqexp <- function(q, shape, rate, lower.tail=FALSE) {
#   y <- pgpd(q, 0, shape=(shape-1)/(2-shape),
#             scale=1/(rate*(2-shape)))
#   if (lower.tail==FALSE) {
#     y <- 1-y
#   }
#   return(y)
# }

qqexp <- function(p, shape, rate) {
  y <- qgpd(p, 0, shape=(shape-1)/(2-shape),
                 scale=1/(rate*(2-shape)))
  return(y)
}

rqexp <- function(n, shape, rate) {
  y <- rgpd(n, 0, shape=(shape-1)/(2-shape),
                 scale=1/(rate*(2-shape)))
  return(y)
}

tsqexp <- function(x, q) {
  if (q == 1) {
    y <- exp(x)
  } else {
    ifelse(1 + (1 - q)*x > 0, (1 + (1 - q)*x)^(1/(1 - q)), 0)
  }
}

pqexp <- function(q, shape, rate, lower.tail = FALSE) {
  shape1 <- 1/(2 - shape)
  if (lower.tail) {
    y <- 1 - tsqexp(-rate*q/shape1, shape1)
  } else {
    y <- tsqexp(-rate*q/shape1, shape1)
  }
}

dqweibull <- function(x, qshape, shape, scale) {
  y <- ifelse(x >= 0, (2 - qshape)*shape/scale*(x/scale)^(shape-1)*tsqexp(-(x/scale)^shape, qshape), 0)
  return(y)
}

pqweibull <- function(q, qshape, shape, scale, lower.tail = TRUE) {
  scale1 <- scale/(2 - qshape)^(1/shape)
  qshape1 <- 1/(2 - qshape)
  if (lower.tail) {
    ifelse(q >= 0, 1 - tsqexp(-(q/scale1)^shape, qshape1), 0)
  } else {
    ifelse(q >= 0, tsqexp(-(q/scale1)^shape, qshape1), 0)
  }
}