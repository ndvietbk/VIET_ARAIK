# This script extracts user session data using University of Saskatchewan WWW server log
# taken from The Internet Traffic Archive (http://ita.ee.lbl.gov)

# Read log ------------------------------------------------------------------------------
infname <- "UofS_access_log.txt"
hlog <- read.table(infname, fill = TRUE, stringsAsFactors = FALSE)
# Select only host, time and size fields
hlog <- hlog[, c(1, 4, 8)]
colnames(hlog)<- c("host", "time", "size")
# Eliminate NAs
hlog$size <- replace(hlog$size, hlog$size == '-', NA)
hlog$size <- replace(hlog$size, hlog$size == 0, NA)
hlog$time <- substring(hlog$time,2)
# Date conversion
hlog$time <- as.POSIXct(hlog$time, format="%d/%B/%Y:%H:%M:%S")
# Get interarrival time
hlog$time <- c(0,diff(as.numeric(hlog$time)))
# Eliminate NAs and convert to numeric
hlog <- hlog[complete.cases(hlog), ]
hlog$size <- as.numeric(hlog$size)

# User session extraction ---------------------------------------------------------------------------
max.ts <- 30                # maximum time between packets allowed in session
k <- 1                      # session number
sum_packet <-0              # total rows to final session 
t_session <- 0              # time between sessions (in seconds)
size_session <- 0           # session total size (in bytes)
size_paket <- 0
number_paketinsession <- 0  # number of connections in session 
number_paket <- 0
n<- 11

# Main loop
for(i in 2:n) {
  number_paket <- number_paket +1
  size_paket <- size_paket +hlog$size[i-1]
 
  if (hlog$host[i] != hlog$host[i-1]| hlog$time[i] > max.ts)
  {
    t_session[k] <- hlog$time[i]
    
    size_session[k] <- size_paket
    size_paket <- 0
    
    number_paketinsession[k] <- number_paket
    sum_packet <- sum_packet + number_paket
    number_paket <- 0
    k <- k+1
  }
}

# Find session size and number of connections for final sesssion
num_diff <- n - sum_packet 
number_paketinsession[k] <- num_diff
size_session[k] <- 0
for (i in 1:num_diff) {
  size_session[k] <- size_session[k] + hlog$size[sum_packet+i]
}

# Assemble results in dataframe
size_session <- size_session[2:length(size_session)]
number_paketinsession <- number_paketinsession[2:length(number_paketinsession)]
ses <- data.frame(time = t_session, ncon = number_paketinsession, size = size_session)

x <- ses$time
Fn <- ecdf(x)
x <- seq(1,100,length.out = 100)
ep <- 1 - Fn(x)
plot(x, ep, type = "l", log="xy") 
