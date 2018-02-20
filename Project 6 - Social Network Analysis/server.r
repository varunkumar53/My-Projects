
######################################################################
#libraries to import 
######################################################################

library(shiny)
library(dplyr)
library(sqldf)
library(networkD3)
library(igraph)

####################
#Server side code
####################

shinyServer(
  function(input,output){
    
######################################################################
#display any n connections from the file, ???email-Eu-core.txt???; 
######################################################################
    
    ##############################################
    #Display the tables with Sender and Receiver
    ##############################################
    
    output$contents <- renderTable(
      {
        inFile <- input$File1
        inFile2 <- input$File2
        header <- input$Head
        if (is.null(inFile))
          return(NULL)
        if (is.null(inFile2))
          return(NULL)
        if (is.na(header))
          return(NULL)
        else read.table(inFile$datapath,sep = " ",col.names = c("Sender","Receiver"),nrows = header)
        }
      )
    
    #############################################
    #Display the tables with Simple Network Graph
    ##############################################
    output$simple <- renderSimpleNetwork(
      {
        inFile <- input$File1
        inFile2 <- input$File2
        header <- input$Head
        if (is.null(inFile))
          return(NULL)
        if (is.null(inFile2))
          return(NULL)
        if (is.na(header))
          return(NULL)
        else read.table(inFile$datapath,sep = " ",col.names = c("Sender","Receiver"),nrows = header)
        df_simple <- read.table(inFile$datapath,sep = " ",col.names = c("Sender","Receiver"),nrows = header)
        simpleNetwork(df_simple, fontSize = 20, opacity = 0.9, zoom=T, nodeColour = "#ff5319")
      }
    )
    
    
######################################################################
#display the table with sender id and the number of emails sent
######################################################################
    output$contents1 <- renderTable(
      {
        inFile <- input$File1
        SenderDataFrame <- read.table(inFile$datapath,sep = " ")[,1]
        FindFreq <- as.data.frame(table(unlist(SenderDataFrame)))
        colnames(FindFreq) <- c("Sender", "Mails_Sent")
        arrange(FindFreq, desc(Mails_Sent))

      }
    )
    
######################################################################
#display the table with receiver id and the number of emails received
######################################################################
    output$contents2 <- renderTable(
      {
        inFile <- input$File1
        ReceiverDataFrame <- read.table(inFile$datapath,sep = " ")[,2]
        FindFreq <- as.data.frame(table(unlist(ReceiverDataFrame)))
        colnames(FindFreq) <- c("Receiver", "Mails_Received")
        arrange(FindFreq, desc(Mails_Received))
        #sqldf("SELECT COUNT(*) FROM FindFreq ")
    
        
      }
    )
    
######################################################################
#display the table with people id and the department they belong to
######################################################################
    output$contents3 <- renderTable(
      {
        inFile <- input$File2
        read.table(inFile$datapath,sep = " ",col.names = c("People","Department"))
        
      }
    )
    
######################################################################
#display how many mails are sent from one department to the other
######################################################################   
    output$contents4 <- renderTable(
      {
        
        inFile1 <- input$File1
        inFile2 <- input$File2
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        sql <- sqldf("SELECT df2.Department AS Sender_Department,df3.Department AS Receiver_Department,count(*) AS Mails_Received
              FROM df1 
              join df2 on df1.Sender = df2.People 
              join df3 on df1.Receiver = df3.People 
              GROUP BY df2.Department,df3.Department
              ORDER by count(*) DESC
              ")
         }
     )
    
######################################################################
#Visualize how many mails are sent from one department to the other
######################################################################   
  
    output$contents7 <- renderForceNetwork(
      {
        
        inFile1 <- input$File1
        inFile2 <- input$File2
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        sql <- sqldf("SELECT df2.Department AS Sender_Department,df3.Department AS Receiver_Department,count(*) AS Mails_Received
                     FROM df1 
                     join df2 on df1.Sender = df2.People 
                     join df3 on df1.Receiver = df3.People 
                     GROUP BY df2.Department,df3.Department
                     ORDER by count(*) DESC
                
                     ")
        forceNetwork(Links = sql,Nodes = sql,NodeID = "Sender_Department",Group = "Sender_Department",Source = "Sender_Department", Target = "Receiver_Department",opacity = 0.9, zoom = TRUE, fontSize = 15)
        
      }
      
   )
######################################################################
#Display up to 2-hop neighbors of the top 10 from (4) 
######################################################################   

        
    output$contents5 <- renderForceNetwork(
      {
        inFile <- input$File1
        inFile2 <- input$File2
        radios <- input$receive_radio
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3<- as.data.frame(df2)
        ReceiverDataFrame <- read.table(inFile$datapath,sep = " ")[,2]
        FindFreq <- as.data.frame(table(unlist(ReceiverDataFrame)))
        colnames(FindFreq) <- c("Receiver", "Mails_Received")
        df <- head(arrange(FindFreq, desc(Mails_Received)),n=10)
        x <- df[,1, drop=FALSE]
        inFile1 <- input$File1
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))

        sql1 <- sqldf(sprintf("SELECT Sender,Receiver FROM df1 where df1.Sender = '%s'", radios))
        sql2 <- sqldf(sprintf("Select distinct Receiver from df1 where df1.Sender= '%s'", radios))
        sql3 <- sqldf("SELECT Sender,Receiver FROM df1 where df1.Sender IN (SELECT Distinct Receiver FROM sql2) and df1.receiver NOT IN (SELECT Distinct Receiver FROM sql2)")
        sql4 <- sqldf ("SELECT Sender,Receiver FROM sql1
                       union
                       SELECT Sender,Receiver FROM sql3")
        
        forceNetwork(Links = sql4,Nodes = df3,NodeID = "People",Group = "Department",Source = "Sender", Target = "Receiver",opacity = 0.9, zoom = TRUE, fontSize = 30)
      }
    )
    
######################################################################
#Display up to 2-hop neighbors of the top 10 from (5) 
######################################################################   
    output$contents6 <- renderForceNetwork(
      {
        inFile <- input$File1
        inFile2 <- input$File2
        radios <- input$send_radio
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3<- as.data.frame(df2)
        SenderDataFrame <- read.table(inFile$datapath,sep = " ")[,1]
        FindFreq <- as.data.frame(table(unlist(SenderDataFrame)))
        colnames(FindFreq) <- c("Sender", "Mails_Sent")
        df <- head(arrange(FindFreq, desc(Mails_Sent)),n=10)
        x <- df[,1, drop=FALSE]
        inFile1 <- input$File1
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))
        sql1 <- sqldf(sprintf("SELECT Sender,Receiver FROM df1 where df1.Sender = '%s'", radios))
        sql2 <- sqldf(sprintf("Select distinct Receiver from df1 where df1.Sender= '%s'", radios))
        sql3 <- sqldf("SELECT Sender,Receiver FROM df1 where df1.Sender IN (SELECT Distinct Receiver FROM sql2) and df1.receiver NOT IN (SELECT Distinct Receiver FROM sql2)")
        sql4 <- sqldf ("SELECT Sender,Receiver FROM sql1
                        union
                       SELECT Sender,Receiver FROM sql3")

        forceNetwork(Links = sql4,Nodes = df3,NodeID = "People",Group = "Department",Source = "Sender", Target = "Receiver",opacity = 0.9, zoom = TRUE, fontSize = 30)

      }
    )
    
##################################################################################
#Display/visualize up to 2-hop neighbors of 10 people with the highest centrality.
################################################################################## 
    
    output$contents8 <- renderForceNetwork(
      {
        inFile <- input$File1
        inFile2 <- input$File2
        radios <- input$centrality_radio
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3<- as.data.frame(df2)
        ReceiverDataFrame <- read.table(inFile$datapath,sep = " ")[,2]
        FindFreq <- as.data.frame(table(unlist(ReceiverDataFrame)))
        colnames(FindFreq) <- c("Receiver", "Mails_Received")
        df <- head(arrange(FindFreq, desc(Mails_Received)),n=10)
        x <- df[,1, drop=FALSE]
        inFile1 <- input$File1
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))
        sql4 <- sqldf ("SELECT Receiver,Sender FROM df1 where df1.receiver in(select * from x) order by receiver")
        inFile <- input$File1
        inFile2 <- input$File2
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3<- as.data.frame(df2)
        SenderDataFrame <- read.table(inFile$datapath,sep = " ")[,1]
        FindFreq <- as.data.frame(table(unlist(SenderDataFrame)))
        colnames(FindFreq) <- c("Sender", "Mails_Sent")
        df <- head(arrange(FindFreq, desc(Mails_Sent)),n=10)
        x <- df[,1, drop=FALSE]
        inFile1 <- input$File1
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))
        sql5 <- sqldf ("SELECT Sender,Receiver FROM df1 where df1.sender in(select * from x) order by Sender")
        
        sql6 <- sqldf( "SELECT Sender AS A,Receiver AS B FROM sql5
                        union
                       SELECT Receiver,Sender FROM sql4")
        sql7 <- sqldf("select A,count(*) from sql6 group by A order by count(*) desc limit 10")
        
        sql1 <- sqldf(sprintf("SELECT Sender,Receiver FROM df1 where df1.Sender = '%s'", radios))
        sql2 <- sqldf(sprintf("Select distinct Receiver from df1 where df1.Sender= '%s'", radios))
        sql3 <- sqldf("SELECT Sender,Receiver FROM df1 where df1.Sender IN (SELECT Distinct Receiver FROM sql2) and df1.receiver NOT IN (SELECT Distinct Receiver FROM sql2)")
        sql4 <- sqldf ("SELECT Sender,Receiver FROM sql1
                       union
                       SELECT Sender,Receiver FROM sql3")
        
        forceNetwork(Links = sql4,Nodes = df3,NodeID = "People",Group = "Department",Source = "Sender", Target = "Receiver",opacity = 0.9, zoom = TRUE, fontSize = 30)
        
        
      }
    )
    
##########################################################################################
#Display/visualize up to 2-hop neighbors of 10 people with the highest indegree centrality.
##########################################################################################
    
    output$contents9 <- renderForceNetwork(
      {
        inFile <- input$File1
        inFile2 <- input$File2
        radios <- input$indegree_radio
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3<- as.data.frame(df2)
        ReceiverDataFrame <- read.table(inFile$datapath,sep = " ")[,2]
        FindFreq <- as.data.frame(table(unlist(ReceiverDataFrame)))
        colnames(FindFreq) <- c("Receiver", "Mails_Received")
        df <- head(arrange(FindFreq, desc(Mails_Received)),n=10)
        x <- df[,1, drop=FALSE]
        inFile1 <- input$File1
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))
        sql1 <- sqldf(sprintf("SELECT Sender,Receiver FROM df1 where df1.Sender = '%s'", radios))
        sql2 <- sqldf(sprintf("Select distinct Receiver from df1 where df1.Sender= '%s'", radios))
        sql3 <- sqldf("SELECT Sender,Receiver FROM df1 where df1.Sender IN (SELECT Distinct Receiver FROM sql2) and df1.receiver NOT IN (SELECT Distinct Receiver FROM sql2)")
        sql4 <- sqldf ("SELECT Sender,Receiver FROM sql1
                       union
                       SELECT Sender,Receiver FROM sql3")
        
        forceNetwork(Links = sql4,Nodes = df3,NodeID = "People",Group = "Department",Source = "Sender", Target = "Receiver",opacity = 0.9, zoom = TRUE, fontSize = 30)
      }
    )
    
    
##########################################################################################
#Display/visualize up to 2-hop neighbors of 10 people with the highest betweeness centrality.
##########################################################################################
    
    output$contents10 <- renderForceNetwork(
      {
        inFile1 <- input$File1
        inFile2 <- input$File2
        df1 <- read.table(inFile1$datapath,sep = " ",col.names = c("Sender","Receiver"))
        df2 <- read.table(inFile2$datapath,sep = " ",col.names = c("People","Department"))
        df3<- as.data.frame(df2)
        gra = graph.data.frame(df1)
        b <- betweenness(gra)
        c <- as.data.frame(b)
        radios <- input$betweenness_radio
        sql1 <- sqldf(sprintf("SELECT Sender,Receiver FROM df1 where df1.Sender = '%s'", radios))
        sql2 <- sqldf(sprintf("Select distinct Receiver from df1 where df1.Sender= '%s'", radios))
        sql3 <- sqldf("SELECT Sender,Receiver FROM df1 where df1.Sender IN (SELECT Distinct Receiver FROM sql2) and df1.receiver NOT IN (SELECT Distinct Receiver FROM sql2)")
        sql4 <- sqldf ("SELECT Sender,Receiver FROM sql1
                       union
                       SELECT Sender,Receiver FROM sql3")
        
        forceNetwork(Links = sql4,Nodes = df3,NodeID = "People",Group = "Department",Source = "Sender", Target = "Receiver",opacity = 0.9, zoom = TRUE, fontSize = 30)
        
        
      }
    )
    
    
    ## Inference ##
    
    output$contents11 <- renderPrint({ "The degree centrality of a node(person) i, can be defined as the total number of nodes connected to node ni. From Degree Centrality results we infer that nodes 160, 121, 82, 107, 86, 62, 434, 13, 183, 249 have the top 10 degree centrality" })

    output$contents12 <- renderPrint({ "The betweeness centrality tells about information flow through a node. From iGraph package the betweeness measure was calculated and  we infer that nodes 160, 86, 5, 121, 62, 107, 64, 82, 377, 129 have the top 10 betweeness centrality" })
                                                                                                                                                                                           
    output$contents13 <- renderPrint({ "From InDegree Centrality results we infer that nodes 160, 62, 107, 121, 86, 434, 183, 129, 64, 128 have the top 10 indegree centrality" })

    
    
  }
  
)

