######################################################################
#libraries to import 
######################################################################

library(shiny)
library(shinythemes)
library(networkD3)

####################
#Start UI.R code
####################

shinyUI(fluidPage(theme = shinytheme("flatly"),
                  
                  titlePanel("Varun Kumar Manohara Selvan_Natural Language Processing"),
                  
                  
                  ########################
                  #Side bar layout panels
                  ########################
                  
                
                    mainPanel(
                      tabsetPanel(
                         tabPanel(h4("1.Training Data"),tableOutput("TrainingData")),
                         tabPanel(h4("2.Test Data"),tableOutput("TestData")),
                         tabPanel(h4("3,4,5,6,7,8.Normalized Training Data"),textOutput("Text"),tableOutput("NormalizedTrainingData")),
                         tabPanel(h4("3,4,5,7,8.Normalized Test Data"),textOutput("Text1"),tableOutput("PredictiveData")),
                         tabPanel(h4("9.TF-IDF scores"),plotOutput("Plot"),tableOutput("Tfidf"))
                      )
                    )
                  )
)
