# This script extracts user session data using University of Saskatchewan WWW server log
#taken from the internet Traffic Archive (http://ita.ee.lbl.gov)

#Read log -------------------------------------------------------------------------------------------
infname <- "D:/dorm2/2016/data/extractdata/saskatchewan.txt" # Folder "extractdata" contains logs including 3 columns 
                                                         # "host" "time" "size" extracted from original logs
hlog <- read.table(infname)
colnames(hlog) <- c("host", "time", "size")


# User session extraction ---------------------------------------------------------------------------
h <- hlog$host             # host variable

index <- 1                 # session number
time_temp <- hlog$time[1]
size_temp <- hlog$size[1]
number_request <- 1        # number request from a host to server
time <- 0;                 # time between sessions (in seconds)
size <- 0;                 # session total size (in bytes)
n <- length(hlog$host)
i <- 2

#Main loop--------------------------------------------
while (index <5) {
  if (hlog$host[i] == hlog$host[i-1]){
    time_temp <- time_temp + hlog$time[i]
    size_temp <- size_temp + hlog$size[i]
    number_request <- number_request +1
  }
  else
  {
    h[index] <- hlog$host[i-1]
    time[index]<- time_temp
    size[index]<- size_temp
    index <- index +1
    time_temp <- hlog$time[i]
    size_temp <- hlog$size[i]
   }
  i <- i+1
}
# Find session size and number of connections for final sesssion
h[index] <- hlog$host[i]
time[index] <- time_temp
size[index]<- size_temp
h <- h[c(1:index)]

# Write variabls "host" "time of session" "size of session
ses <- data.frame(host = h , time = time, size= size)
write.table(ses, "D:/dorm2/2016/groupbysession/usask_session.txt", col.names = F, row.names = F)
