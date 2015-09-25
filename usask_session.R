
infname <- "C:/Users/Araik/Documents/Research/server_log/data/UofS_access_log.txt"
hlog <- read.table(infname, fill = TRUE, stringsAsFactors = FALSE)
hlog <- hlog[,c(1,4,8)]
colnames(hlog)<- c("host", "time", "size")
hlog$size <- replace(hlog$size, hlog$size == '-', NA)
hlog$size <- replace(hlog$size, hlog$size == 0, NA)
hlog$time <- substring(hlog$time,2)

hlog$time <- as.POSIXct(hlog$time, format="%d/%B/%Y:%H:%M:%S")
hlog$time <- c(0,diff(as.numeric(hlog$time)))
hlog <- hlog[complete.cases(hlog), ]
hlog$size <- as.numeric(hlog$size)

max.ts <- 30
k <- 1 #number session
sum_packet <-0  #total rows to final session 
t_session <- 0
size_session <- 0 #size of session
size_paket <- 0
number_paketinsession <- 0 #number paket in session 
number_paket <- 0
n<- 11

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

#------------find parameters size and "number paket in session " for final sesssion -------#
num_diff <- n - sum_packet 
number_paketinsession[k] <- num_diff
size_session[k] <- 0
for (i in 1:num_diff)
{
  size_session[k] <- size_session[k] + hlog$size[sum_packet+i]
}
#--------------------------------------------------------------------------------------------


size_session <- size_session[2:length(size_session)]
number_paketinsession <- number_paketinsession[2:length(number_paketinsession)]
 
ses <- data.frame(time = t_session, ncon = number_paketinsession, size = size_session)

x <- ses$time
Fn <- ecdf(x)
x <- seq(1,100,length.out = 100)
ep <- 1 - Fn(x)
plot(x, ep, type = "l", log="xy")