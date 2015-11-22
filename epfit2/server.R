library(shiny)
library(sfsmisc)
library(magicaxis)
library(minpack.lm)
source("qexp.R")

options(shiny.maxRequestSize=20*1024^2)

shinyServer(function(input, output, clientData, session) {
  
  importData <- reactive ({
    inFile <- input$file1
    
    if (is.null(inFile))
      return(NULL)
    
    data <- read.table(inFile$datapath)
  })
  

  output$distPlot <- renderPlot({
    tryCatch({
      data <- importData()
      x <- input$mc*data$V1
      y <- data$V2
      
      scale <- input$scale
      wfdeg <- 100
      x.max <- input$x.max
      y.low <- input$y.low
      wf <- (seq(1, 10, length.out=length(y)))^wfdeg
      fit <- nlsLM(y ~ pqexp(x-min(x), p1, p2, lower.tail = FALSE), start=list(p1 = scale, p2 = 1),
                  lower=c(scale - 0.0001, 0.01), upper=c(scale + 0.0001, 100), weights=wf)
      
      updateNumericInput(session, "df", value = round(as.numeric(coef(fit)[2]), 2))
      
      y.fit <- pqexp(x-min(x), scale, coef(fit)[2], lower.tail=FALSE)
      
      magplot(x, y, type="p", col="black", log="xy", 
              xlim=c(min(x), x.max), ylim=c(y.low, 1), xaxs = "i", yaxs = "i",
              labels=c(1, 1), xlab="Random variable", ylab="Cumulative probability")
      lines(x, y.fit, type="l", col="red")
      
    }, error=function(warn){
     text(0, 0, "Unable to plot and fit exceedance probability. \nLoad file with empirical data.")
   })
  })
  
  output$downloadData <- downloadHandler(
    filename = function() { paste("f", input$file1, sep='') },
    content = function(file) {
      x <- filedata()$V1
      y <- filedata()$V2
      y.fit <- pt(input$scale*x, df=input$df, lower.tail=FALSE)
      data <- data.frame(x=x, y=y, y.fit=y.fit)
      write.table(data, file, row.names=FALSE, col.names=FALSE)
    }
  )
})