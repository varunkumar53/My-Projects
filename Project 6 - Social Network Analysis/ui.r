######################################################################
#libraries to import 
######################################################################

library(shiny)
library(shinythemes)
library(networkD3)

####################
#Start UI.R code
####################

shinyUI(fluidPage(theme = shinytheme("united"),
  
  titlePanel("Varun Kumar Manohara Selvan_Social_Network_Analysis"),
 
  
  ########################
  #Side bar layout panels
  ########################
  
  sidebarLayout(
    sidebarPanel(
                 fileInput("File1", h5("Upload File 1"), multiple = FALSE, accept = NULL, width = NULL,
                           buttonLabel = "Browse...", placeholder = "No file selected"),
                 fileInput("File2", h5("Upload File 2"), multiple = FALSE, accept = NULL, width = NULL,
                           buttonLabel = "Browse...", placeholder = "No file selected"),
                 conditionalPanel(condition="input.tabselected==1",numericInput("Head",h5("Enter a number to display n connections"),value = "")),
                 conditionalPanel(condition="input.tabselected==2",
                 radioButtons("send_radio", label = h3("Top 10 Senders"),
                              choices = list("160" = 160, "82" = 82, "121" = 121, "107" = 107, "86" = 86, "62" = 62, "13" = 13, "249" = 249, "183" = 183, "434" = 434), 
                              selected = 160)),
                 conditionalPanel(condition="input.tabselected==3",
                 radioButtons("receive_radio", label = h3("Top 10 Receivers"),
                              choices = list("160" = 160, "62" = 62, "107" = 107, "121" = 121, "86" = 86, "434" = 434, "183" = 183, "129" = 129, "64" = 64, "128" = 128), 
                              selected = 160)),
                 conditionalPanel(condition="input.tabselected==4",
                                  radioButtons("centrality_radio", label = h3("Top 10 Degree Centrality"),
                                               choices = list("160" = 160, "121" = 121, "82" = 82, "107" = 107, "86" = 86, "62" = 62, "434" = 434, "13" = 13, "183" = 183, "249" = 249), 
                                               selected = 160)),
                 conditionalPanel(condition="input.tabselected==5",
                                  radioButtons("betweenness_radio", label = h3("Top 10 Betweeness Centrality"),
                                               choices = list("160" = 160, "86" = 86, "5" = 5, "121" = 121, "62" = 62, "107" = 107, "64" = 64, "82" = 82, "377" = 377, "129" = 129), 
                                               selected = 160)),
                 conditionalPanel(condition="input.tabselected==6",
                                  radioButtons("indegree_radio", label = h3("Top 10 InDegree Centrality"),
                                               choices = list("160" = 160, "62" = 62, "107" = 107, "121" = 121, "86" = 86, "434" = 434, "183" = 183, "129" = 129, "64" = 64, "128" = 128), 
                                               selected = 160))
                
                 ),
    
    ##############################
    #Main panel and tab panel code
    ##############################
    mainPanel(
      tabsetPanel(
        tabPanel(h5("3.Summary"),value=1,tableOutput("contents"),h4("Plot"),simpleNetworkOutput("simple")),
        tabPanel(h5("4.Mails Sent"),tableOutput("contents1")),
        tabPanel(h5("5.Mails Received"), tableOutput("contents2")),
        tabPanel(h5("Departments"),tableOutput("contents3")),
        tabPanel(h5("6.a Sender 2-hop"),value=2,forceNetworkOutput("contents6")),
        tabPanel(h5("6.b Receiver 2-hop"),value=3,forceNetworkOutput("contents5")),
        tabPanel(h5("7.Degree Centrality 2-hop"),value=4,forceNetworkOutput("contents8")),
        tabPanel(h5("8.Betweeness Centrality 2-hop"),value=5, forceNetworkOutput("contents10")),
        tabPanel(h5("9.Indegree Centrality 2-hop"),value=6,forceNetworkOutput("contents9")),
        tabPanel(h5("10.Department Mails"),tableOutput("contents4"),h4("Plot"),forceNetworkOutput("contents7")),
        tabPanel(h5("11.Observations"),tableOutput("contents11"),tableOutput("contents12"),tableOutput("contents13")),
        id = "tabselected"
        

      )
  )
)))
