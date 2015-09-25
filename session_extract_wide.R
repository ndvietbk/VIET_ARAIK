# Extracts user sessions from HTTP log in csv format and 
library(data.table)
#library(sfsmisc)

pdate <- c("20071015", "20071016", "20071017", "20071018", "20071019")
max.st <- 1  # in seconds

for (l in 1:length(pdate)) {
    infname <- paste("~/data/wide/", substring(pdate[l], 1, 4), "/http/log_", pdate[l],".txt", sep="")
    outfname1 <- paste("~/data/wide/", substring(pdate[l], 1, 4), "/itime/itime_", max.st, "_", pdate[l], ".txt", sep="")
    outfname2 <- paste("~/data/wide/", substring(pdate[l], 1, 4), "/size/size_", max.st, "_", pdate[l], ".txt", sep="")
    hlog <- fread(infname)
    setnames(hlog, c("V1", "V2", "V3", "V4", "V5"), c("Time", "IP.Src", "IP.Dst", "IP.Proto", "Size"))
    
    All.IP.Dst <- hlog$IP.Dst[duplicated(hlog, by="IP.Dst") == FALSE]
    All.IP.Dst <- All.IP.Dst[1:1000]
    pb <- txtProgressBar(min = 0, max = length(All.IP.Dst), style = 3)
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
      setTxtProgressBar(pb, i)
    }
    options(scipen = -100)
    write.table(ses.it, outfname1, row.names = FALSE, col.names = FALSE)
    options(scipen = 100)
    write.table(ssize, outfname2, row.names = FALSE, col.names = FALSE)
}
