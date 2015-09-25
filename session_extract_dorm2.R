# Extracts user sessions from HTTP log in csv format and 
library(data.table)
#library(sfsmisc)

pdate <- "20150419"
pnum <- 53
max.st <- 0.01  # in seconds

for (l in 1:length(pnum)) {
  for (m in 1:pnum[l]) {
    if (m < 10) {
      infname <- paste("~/data/dorm2/2015/DNL/", pdate[l], "0000/http/log_", pdate[l], "_DNL_p0", m, ".txt", sep="")
      outfname1 <- paste("~/data/dorm2/2015/DNL/", pdate[l], "0000/itime/itime_", max.st, "_", pdate[l], "_DNL_p0", m, ".txt", sep="")
      outfname2 <- paste("~/data/dorm2/2015/DNL/", pdate[l], "0000/size/size_", max.st, "_", pdate[l], "_DNL_p0", m, ".txt", sep="")
    } else {
      infname <- paste("~/data/dorm2/2015/DNL/", pdate[l], "0000/http/log_", pdate[l], "_DNL_p", m, ".txt", sep="")
      outfname1 <- paste("~/data/dorm2/2015/DNL/", pdate[l], "0000/itime/itime_", max.st, "_", pdate[l], "_DNL_p", m, ".txt", sep="")
      outfname2 <- paste("~/data/dorm2/2015/DNL/", pdate[l], "0000/size/size_", max.st, "_", pdate[l], "_DNL_p", m, ".txt", sep="")
    }
    hlog <- fread(infname)
    setnames(hlog, c("V1", "V2", "V3", "V4", "V5"), c("Time", "IP.Src", "IP.Dst", "IP.Proto", "Size"))
    
    All.IP.Dst <- hlog$IP.Dst[duplicated(hlog, by="IP.Dst") == FALSE]
    
    k <- 1
    for(i in 1:length(All.IP.Dst)) {
      hlogf <- subset(hlog, IP.Dst == All.IP.Dst[i])
      
      itime <- diff(hlogf$Time)
      itime1 <- c(0, itime)
      
      if (i == 1){ 
        ssize <- numeric(sum(itime1 > max.st)+1)
      } else {
        ssize <- c(ssize, numeric(sum(itime1 > max.st)+1))
      }
      
      for (j in 1:nrow(hlogf)) {
        if (itime1[j] > max.st) {
          k <- k+1
          ssize[k] <- hlogf$Size[j]
        } else {
          ssize[k] <- ssize[k] + hlogf$Size[j]
        }
      }
      k <- k+1
      
      # Calculate time between user sessions
      ifelse(i == 1, ses.it <- itime[itime > max.st], 
             ses.it <- c(ses.it, itime[itime > max.st]))
    }
    options(scipen = -100)
    write.table(ses.it, outfname1, row.names = FALSE, col.names = FALSE)
    options(scipen = 100)
    write.table(ssize, outfname2, row.names = FALSE, col.names = FALSE)
  }
}
#Fn <- ecdf(ses.it)
#x <- lseq(1e-6, 20, length=1000)
#ep <- 1-Fn(x)
#plot(x, ep, log="xy", type='l')
