library(shiny)

shinyUI(pageWithSidebar(
  
  # Application title
  headerPanel("q-exponential distribution fit"),
  
  sidebarPanel(
  
  # Choose file
    fileInput('file1', 'Choose Data File',
            accept=c('text/plain', '.dat')),
    tags$hr(),
    
  helpText("Black circles represent empirical cumulative probability imported from data file, 
           red line - fit with q-exponential distribution."),
  
  # Data multiply input
  numericInput("mc", "Multiply by:", 1, min = 1e-6),
  
  # Fit parameters input
  numericInput("scale", "q-parameter:", 1, step = 0.01),
  numericInput("df", paste("Rate:"), 1, step = 0.01),
  
  # Sliders for axis limit change
  numericInput("x.max", "Max X:", min = 1e-6, value = 20),
  numericInput("y.low", "Min Y:", min = 1e-6, max = 0.99, value = 1e-4),
  downloadButton('downloadData', 'Download - NOT WORKING')  
  ),
  
  # Show a plot of the generated distribution
  mainPanel(
       plotOutput("distPlot")
    )
  )
)