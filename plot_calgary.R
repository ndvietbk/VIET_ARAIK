# code to plot traffic in munite of server "calgary



infname <- "calgary_access_log.txt"
hlog_cal <- read.table(infname, fill = TRUE, stringsAsFactors = FALSE)
hlog_cal <- hlog_cal[ , c(1,4,8)]
colnames(hlog_cal) <- c("host", "time", "size")
hlog_cal$size <- replace(hlog_cal$size, hlog_cal$size == '-', NA)
hlog_cal$size <- replace(hlog_cal$size, hlog_cal$size == 0, NA)
hlog_cal$time <- substring(hlog_cal$time,2)
hlog_cal$time <- as.POSIXct(hlog_cal$time, format="%d/%B/%Y:%H:%M:%S")
# Get interarrival time
hlog_cal$time <- c(0,diff(as.numeric(hlog_cal$time)))
# Eliminate NAs and convert to numeric
hlog_cal <- hlog_cal[complete.cases(hlog_cal), ]
hlog_cal$size <- as.numeric(hlog_cal$size)



num_second <- 60        # number seconds in minute:  60s
size_paketinminute <- 0    # total traffic size per minute (in bytes)
n <- length(hlog_cal$host) 
index <- 1                # index of size_paketinminute 
size_paket <- hlog_cal$size[1]     # temporary variable of traffic per minute
time <- 0               # temporary time variable 

# Main loop to fize size of traffic in minute
for (i in 2:n) {
  time <- time + hlog_cal$time[i]
  size_paket <- size_paket + hlog_cal$size[i]

  if (time > num_second) {
    
    size_paketinminute[index] <- size_paket - hlog_cal$size[i]
    size_paket <- hlog_cal$size[i]   # reset size_paket
    time <- hlog_cal$time[i]   #reset time
    index <- index+1    #increase index
  }
}
size_paketinminute[index] <-  size_paket   # end size_paketinminute 


x <- seq(1,18000,1)
y <- size_paketinminute[x]
plot(x,y, xlim = c(0,18000), ylim = c(0,6e+6), type = "h" )
