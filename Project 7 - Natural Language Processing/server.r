
######################################################################
#libraries to import 
######################################################################

library(shiny)
library(dplyr)
library(sqldf)
library(rvest)
library(tidytext)
library(tidyverse)
library(tidytext)
library(stringr)

####################
#Server side code
####################

shinyServer(
  function(input,output){
    output$TrainingData <- renderTable(
      {
        
        
        ####################
        #Individual URL
        ####################
        
        a <- 'https://www.cars.com/research/toyota-camry-'
        c <-'/consumer-reviews/?nr=250&pg=1'
        sql_union <- data.frame(Id=character(),Year=character(),
                                Rating=character(), 
                                Review=character())
        
        ########################################
        #Years for the Training Data Set
        ########################################
        for (year in c(2012,2013,2014,2015,2016))
          
        {
          url<-paste0(a,year,c)
    
          
          ########################################
          #Scraping part for Reviews
          ########################################
          toyota_webpage <- read_html(url)
          description <- html_nodes(toyota_webpage,'.mmy-reviews__blurb div span')
          description_text <- html_text(description)
          description_text<-gsub("\n","",description_text)
  
          ########################################
          #Scraping part for years
          ########################################
          year <- html_nodes(toyota_webpage,'.consumer-reviews-social-share div  span')
          year_text <- html_text(year)
          year_text<-gsub("\n","",year_text)
          year_text[2]
          only_year<-substr(year_text[2], 1, 4)
          only_year<-rep.int(only_year, length(description_text))
            ########################################
            #Scraping part for Ratings
            ########################################
          
          ratings <- html_nodes(toyota_webpage, css='.mmy-reviews__review header noscript')
          ratings_text <- html_text(ratings)
          ratings_text<-gsub("\n","",ratings_text)
          
          only_ratings<-ratings_text[c(TRUE, FALSE)]
          only_ratings<-gsub(" ", "",only_ratings, fixed = TRUE)
          only_ratings<-substr(only_ratings, 0, 1)
          
            ################################################################################
            #making the Year,Rating and Review columns as a Data Frame
            ################################################################################
          
          desc_dataframe<-data.frame(description_text)
          ratings_dataframe<-data.frame(only_ratings)
          year_dataframe<-data.frame(only_year)
          
            ################################################################################
            #Adding row number to each data frame
            ################################################################################
          
          
          df1 <- desc_dataframe %>% mutate(id = row_number())
          df2 <- ratings_dataframe %>% mutate(id = row_number())
          df3 <- year_dataframe %>% mutate(id = row_number())
          
          ################################################################################
          #Merging all three Dataframes into a single Dataframe
          ################################################################################
          
          total_df <- merge(df2,df1,by="id")
          total_df <- merge(df3,total_df,by="id")
          colnames(total_df) <- c("Id","Year","Rating","Review")
          # total_2012
          sql <- sqldf("SELECT Id, Year, Rating, Review from total_df")
          
          ################################################################################
          #Combining all the years dataset with Union SQL operator
          ################################################################################
          sql_union <-sqldf("SELECT * FROM sql_union UNION SELECT * FROM sql")
        }
        sql_union<-sqldf("SELECT Year, Rating, Review from sql_union order by Year,Id asc")
      
         }
    )
    output$TestData <- renderTable(
      {
        
        ####################
        #Individual URL
        ####################
        a <- 'https://www.cars.com/research/toyota-camry-2017/consumer-reviews/?pg='
        c <-'&nr=250'
        sql_union <- data.frame(Id=character(),Year=character(),
                                Rating=character(), 
                                Review=character())
        for (page in c(1,2))
          
        {
          url<-paste0(a,page,c)
        
          ########################################
          #Scraping part for Reviews
          ########################################
          toyota_webpage <- read_html(url)
          description <- html_nodes(toyota_webpage,'.mmy-reviews__blurb div span')
          description_text <- html_text(description)
          description_text<-gsub("\n","",description_text)
          ########################################
          #Scraping part for years
          ########################################
      
          year <- html_nodes(toyota_webpage,'.consumer-reviews-social-share div  span')
          year_text <- html_text(year)
          year_text<-gsub("\n","",year_text)
          year_text[2]
          only_year<-substr(year_text[2], 1, 4)
          only_year<-rep.int(only_year, length(description_text))
          ########################################
          #Scraping part for Ratings
          ########################################
          
          ratings <- html_nodes(toyota_webpage, css='.mmy-reviews__review header noscript')
          ratings_text <- html_text(ratings)
          ratings_text<-gsub("\n","",ratings_text)
          
          only_ratings<-ratings_text[c(TRUE, FALSE)]
          only_ratings<-gsub(" ", "",only_ratings, fixed = TRUE)
          only_ratings<-substr(only_ratings, 0, 1)
          
          ################################################################################
          #making the Year,Rating and Review columns as a Data Frame
          ################################################################################
          desc_dataframe<-data.frame(description_text)
          ratings_dataframe<-data.frame(only_ratings)
          year_dataframe<-data.frame(only_year)
          
          ################################################################################
          #Adding row number to each data frame
          ################################################################################
          
          df1 <- desc_dataframe %>% mutate(id = row_number())
          df2 <- ratings_dataframe %>% mutate(id = row_number())
          df3 <- year_dataframe %>% mutate(id = row_number())
          
          ################################################################################
          #Merging all three Dataframes into a single Dataframe
          ################################################################################
          
          total_df <- merge(df2,df1,by="id")
          total_df <- merge(df3,total_df,by="id")
          colnames(total_df) <- c("Id","Year","Rating","Review")
          # total_2012
          sql <- sqldf("SELECT Id, Year, Rating, Review from total_df")
          ################################################################################
          #Combining all the years dataset with Union SQL operator
          ################################################################################
          sql_union <-sqldf("SELECT * FROM sql_union UNION SELECT * FROM sql")
        }
        sql_union<-sqldf("SELECT Year, Rating, Review from sql_union order by Year,Id asc")
        
      }
    )
    
    output$NormalizedTrainingData <- renderTable(
      {
        a <- 'https://www.cars.com/research/toyota-camry-'
        c <-'/consumer-reviews/?nr=250&pg=1'
        sql_union <- data.frame(Id=character(),
                                Year=character(),
                                Rating=character(), 
                                Review=character(),
                                Normalized_review=character(),
                                Score=integer())
        for (year in c(2012,2013,2014,2015,2016))
          
        {
          url<-paste0(a,year,c)
          #url <- 'https://www.cars.com/research/toyota-camry-2013/consumer-reviews/?nr=250&pg=1'
          toyota_webpage <- read_html(url)
          description <- html_nodes(toyota_webpage,'.mmy-reviews__blurb div span')
          description_text <- html_text(description)
          description_text<-gsub("\n","",description_text)
          
          ################################################################################
          #Removing the Punctuation and converting from Upper case to Lower Case
          ################################################################################
          description_text_normalized<-tolower(description_text)
          description_text_normalized<-gsub("[[:punct:]]", "", description_text_normalized)  
          
          # #
          year <- html_nodes(toyota_webpage,'.consumer-reviews-social-share div  span')
          year_text <- html_text(year)
          year_text<-gsub("\n","",year_text)
          year_text[2]
          only_year<-substr(year_text[2], 1, 4)
          only_year<-rep.int(only_year, length(description_text))
          #
          
          ratings <- html_nodes(toyota_webpage, css='.mmy-reviews__review header noscript')
          ratings_text <- html_text(ratings)
          ratings_text<-gsub("\n","",ratings_text)
          
          only_ratings<-ratings_text[c(TRUE, FALSE)]
          only_ratings<-gsub(" ", "",only_ratings, fixed = TRUE)
          only_ratings<-substr(only_ratings, 0, 1)
          
          desc_dataframe<-data.frame(description_text)
          ratings_dataframe<-data.frame(only_ratings)
          year_dataframe<-data.frame(only_year)
          desc_norm_dataframe<-data.frame(description_text_normalized)
          
          AFINN <- sentiments %>%
            filter(lexicon == "AFINN") %>%
            select(word, afinn_score = score)
          
          score_char=character()
          for (i in 1:length(description_text_normalized))
          {
            text_df <- data_frame(text = description_text_normalized[i])
            
            aa<-text_df %>%
              unnest_tokens(word, text) %>%
              left_join(AFINN, by = "word")
            
            bb<-as.data.frame(aa)
            
            score_char[i]<-sqldf("SELECT SUM(afinn_score) from bb")
            score_char[is.na(score_char)] <- 0
          }
          score_dataframe<-data.frame(score_char)
          score_dataframe <- t(score_dataframe)
          score_dataframe<-as.data.frame(score_dataframe)
          
          df1 <- desc_dataframe %>% mutate(id = row_number())
          df2 <- ratings_dataframe %>% mutate(id = row_number())
          df3 <- year_dataframe %>% mutate(id = row_number())
          df4 <- desc_norm_dataframe %>% mutate(id = row_number())
          df5 <- score_dataframe %>% mutate(id = row_number())
          
          total_df <- merge(df2,df1,by="id")
          total_df <- merge(df3,total_df,by="id")
          total_df <- merge(total_df,df4,by="id")
          total_df <- merge(total_df,df5,by="id")
          colnames(total_df) <- c("Id","Year","Rating","Review","Normalized_Review","Score")
          sql <- sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from total_df")
          sql_union <-sqldf("SELECT * FROM sql_union UNION SELECT * FROM sql")
        }
          sql_union<-sqldf("SELECT Year, Rating, Review, Normalized_Review, Score from sql_union order by Year,Id asc")
          sql_union <- sql_union %>% mutate(Id = row_number())
          service_char=character()
          service_logical<-grepl("service|Service", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(service_logical))
          {
            if (service_logical[i]==TRUE)
            { 
              service_char[i]="service"
            }
            else
            {
              service_char[i]=""
            }
          }
          service_dataframe<-data.frame(service_char)
          
          ## price data frame ##
          price_char=character()
          price_logical<-grepl("price|Price", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(price_logical))
          {
            if (price_logical[i]==TRUE)
            { 
              price_char[i]="price"
            }
            else
            {
              price_char[i]=""
            }
          }
          price_dataframe<-data.frame(price_char)
          
          ## handling data frame
          
          handling_char=character()
          handling_logical<-grepl("handling|Handling", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(handling_logical))
          {
            if (handling_logical[i]==TRUE)
            { 
              handling_char[i]="handling"
            }
            else
            {
              handling_char[i]=""
            }
          }
          handling_dataframe<-data.frame(handling_char)
          
          ## interior dataframe
          
          interior_char=character()
          interior_logical<-grepl("interior|Interior", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(interior_logical))
          {
            if (interior_logical[i]==TRUE)
            { 
              interior_char[i]="interior"
            }
            else
            {
              interior_char[i]=""
            }
          }
          interior_dataframe<-data.frame(interior_char)
          
          df1 <- service_dataframe %>% mutate(id = row_number())
          df2 <- price_dataframe %>% mutate(id = row_number())
          df3 <- handling_dataframe %>% mutate(id = row_number())
          df4 <- interior_dataframe %>% mutate(id = row_number())
         # df5 <- score_dataframe %>% mutate(id = row_number())
          
          words_df <- merge(df1,df2,by="id")
          words_df <- merge(words_df,df3,by="id")
          words_df <- merge(words_df,df4,by="id")
          colnames(words_df) <- c("Id","service","price","handling","interior")
          words_df$new<- with(words_df, paste(service, price, handling, interior))
    
          
          sql_final <- merge(sql_union,words_df,by="Id")
          sql_final <-sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, new AS Tags, Score from sql_final order by Id asc")
        
      }
    )
    
    output$PredictiveData <- renderTable(
      {
        
        ####################
        #Individual URL
        ####################
        a <- 'https://www.cars.com/research/toyota-camry-'
        c <-'/consumer-reviews/?nr=250&pg=1'
        sql_union <- data.frame(Id=character(),
                                Year=character(),
                                Rating=character(), 
                                Review=character(),
                                Normalized_review=character(),
                                Score=integer())
        for (year in c(2012,2013,2014,2015,2016))
          
        {
          url<-paste0(a,year,c)
          #url <- 'https://www.cars.com/research/toyota-camry-2013/consumer-reviews/?nr=250&pg=1'
          toyota_webpage <- read_html(url)
          description <- html_nodes(toyota_webpage,'.mmy-reviews__blurb div span')
          description_text <- html_text(description)
          description_text<-gsub("\n","",description_text)
          
          ################################################################################
          #Removing the Punctuation and converting from Upper case to Lower Case
          ################################################################################
          description_text_normalized<-tolower(description_text)
          description_text_normalized<-gsub("[[:punct:]]", "", description_text_normalized)  
          
          # #
          year <- html_nodes(toyota_webpage,'.consumer-reviews-social-share div  span')
          year_text <- html_text(year)
          year_text<-gsub("\n","",year_text)
          year_text[2]
          only_year<-substr(year_text[2], 1, 4)
          only_year<-rep.int(only_year, length(description_text))
          #
          
          ratings <- html_nodes(toyota_webpage, css='.mmy-reviews__review header noscript')
          ratings_text <- html_text(ratings)
          ratings_text<-gsub("\n","",ratings_text)
          
          only_ratings<-ratings_text[c(TRUE, FALSE)]
          only_ratings<-gsub(" ", "",only_ratings, fixed = TRUE)
          only_ratings<-substr(only_ratings, 0, 1)
          
          desc_dataframe<-data.frame(description_text)
          ratings_dataframe<-data.frame(only_ratings)
          year_dataframe<-data.frame(only_year)
          desc_norm_dataframe<-data.frame(description_text_normalized)
          
          AFINN <- sentiments %>%
            filter(lexicon == "AFINN") %>%
            select(word, afinn_score = score)
          
          score_char=character()
          for (i in 1:length(description_text_normalized))
          {
            text_df <- data_frame(text = description_text_normalized[i])
            
            aa<-text_df %>%
              unnest_tokens(word, text) %>%
              left_join(AFINN, by = "word")
            
            bb<-as.data.frame(aa)
            
            score_char[i]<-sqldf("SELECT SUM(afinn_score) from bb")
            score_char[is.na(score_char)] <- 0
          }
          score_dataframe<-data.frame(score_char)
          score_dataframe <- t(score_dataframe)
          score_dataframe<-as.data.frame(score_dataframe)
          
          df1 <- desc_dataframe %>% mutate(id = row_number())
          df2 <- ratings_dataframe %>% mutate(id = row_number())
          df3 <- year_dataframe %>% mutate(id = row_number())
          df4 <- desc_norm_dataframe %>% mutate(id = row_number())
          df5 <- score_dataframe %>% mutate(id = row_number())
          
          total_df <- merge(df2,df1,by="id")
          total_df <- merge(df3,total_df,by="id")
          total_df <- merge(total_df,df4,by="id")
          total_df <- merge(total_df,df5,by="id")
          colnames(total_df) <- c("Id","Year","Rating","Review","Normalized_Review","Score")
          sql <- sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from total_df")
          sql_union <-sqldf("SELECT * FROM sql_union UNION SELECT * FROM sql")
        }
        sql_union<-sqldf("SELECT Year, Rating, Review, Normalized_Review, Score from sql_union order by Year,Id asc")
        sql_union <- sql_union %>% mutate(Id = row_number())
        service_char=character()
        service_logical<-grepl("service|Service", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(service_logical))
        {
          if (service_logical[i]==TRUE)
          { 
            service_char[i]="service"
          }
          else
          {
            service_char[i]=""
          }
        }
        service_dataframe<-data.frame(service_char)
        
        ## price data frame ##
        price_char=character()
        price_logical<-grepl("price|Price", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(price_logical))
        {
          if (price_logical[i]==TRUE)
          { 
            price_char[i]="price"
          }
          else
          {
            price_char[i]=""
          }
        }
        price_dataframe<-data.frame(price_char)
        
        ## handling data frame
        
        handling_char=character()
        handling_logical<-grepl("handling|Handling", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(handling_logical))
        {
          if (handling_logical[i]==TRUE)
          { 
            handling_char[i]="handling"
          }
          else
          {
            handling_char[i]=""
          }
        }
        handling_dataframe<-data.frame(handling_char)
        
        ## interior dataframe
        
        interior_char=character()
        interior_logical<-grepl("interior|Interior", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(interior_logical))
        {
          if (interior_logical[i]==TRUE)
          { 
            interior_char[i]="interior"
          }
          else
          {
            interior_char[i]=""
          }
        }
        interior_dataframe<-data.frame(interior_char)
        
        df1 <- service_dataframe %>% mutate(id = row_number())
        df2 <- price_dataframe %>% mutate(id = row_number())
        df3 <- handling_dataframe %>% mutate(id = row_number())
        df4 <- interior_dataframe %>% mutate(id = row_number())
        # df5 <- score_dataframe %>% mutate(id = row_number())
        
        words_df <- merge(df1,df2,by="id")
        words_df <- merge(words_df,df3,by="id")
        words_df <- merge(words_df,df4,by="id")
        colnames(words_df) <- c("Id","service","price","handling","interior")
        words_df$new<- with(words_df, paste(service, price, handling, interior))
        
        
        sql_final <- merge(sql_union,words_df,by="Id")
        training_sql_final <-sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, new AS Tags, Score from sql_final order by Id asc")
        
      
      
        ####################
        #Individual URL
        ####################

      
        a <- 'https://www.cars.com/research/toyota-camry-2017/consumer-reviews/?pg='
        c <-'&nr=250'
        sql_union <- data.frame(Id=character(),
                                Year=character(),
                                Rating=character(),
                                Review=character(),
                                Normalized_Review=character(),
                                Score=integer())
        for (page in c(1,2))

        {
          url<-paste0(a,page,c)
          
          ########################################
          #Scraping part for Reviews
          ########################################
          
          toyota_webpage <- read_html(url)
          description <- html_nodes(toyota_webpage,'.mmy-reviews__blurb div span')
          description_text <- html_text(description)
          description_text<-gsub("\n","",description_text)
          description_text_normalized<-tolower(description_text)
          description_text_normalized<-gsub("[[:punct:]]", "", description_text_normalized)

          ########################################
          #Scraping part for years
          ########################################
          
          # #
          year <- html_nodes(toyota_webpage,'.consumer-reviews-social-share div  span')
          year_text <- html_text(year)
          year_text<-gsub("\n","",year_text)
          year_text[2]
          only_year<-substr(year_text[2], 1, 4)
          only_year<-rep.int(only_year, length(description_text))
          #
          ########################################
          #Scraping part for Ratings
          ########################################
          

          ratings <- html_nodes(toyota_webpage, css='.mmy-reviews__review header noscript')
          ratings_text <- html_text(ratings)
          ratings_text<-gsub("\n","",ratings_text)

          only_ratings<-ratings_text[c(TRUE, FALSE)]
          only_ratings<-gsub(" ", "",only_ratings, fixed = TRUE)
          only_ratings<-substr(only_ratings, 0, 1)
          ################################################################################
          #making the Year,Rating and Review columns as a Data Frame
          ################################################################################
          

          desc_dataframe<-data.frame(description_text)
          ratings_dataframe<-data.frame(only_ratings)
          year_dataframe<-data.frame(only_year)
          desc_norm_dataframe<-data.frame(description_text_normalized)
          ################################################################################
          #finding the Affin Score
          ################################################################################
          
          AFINN <- sentiments %>%
            filter(lexicon == "AFINN") %>%
            select(word, afinn_score = score)

          score_char=character()
          for (i in 1:length(description_text_normalized))
          {
            text_df <- data_frame(text = description_text_normalized[i])

            aa<-text_df %>%
              unnest_tokens(word, text) %>%
              left_join(AFINN, by = "word")

            bb<-as.data.frame(aa)

            score_char[i]<-sqldf("SELECT SUM(afinn_score) from bb")
            score_char[is.na(score_char)] <- 0
          }
          score_dataframe<-data.frame(score_char)
          score_dataframe <- t(score_dataframe)
          score_dataframe<-as.data.frame(score_dataframe)
          ################################################################################
          #Adding row number to each data frame
          ################################################################################
          

          df1 <- desc_dataframe %>% mutate(id = row_number())
          df2 <- ratings_dataframe %>% mutate(id = row_number())
          df3 <- year_dataframe %>% mutate(id = row_number())
          df4 <- desc_norm_dataframe %>% mutate(id = row_number())
          df5 <- score_dataframe %>% mutate(id = row_number())
          
          ################################################################################
          #Merging all three Dataframes into a single Dataframe
          ################################################################################
          

          total_df <- merge(df2,df1,by="id")
          total_df <- merge(df3,total_df,by="id")
          total_df <- merge(total_df,df4,by="id")
          total_df <- merge(total_df,df5,by="id")
          colnames(total_df) <- c("Id","Year","Rating","Review","Normalized_Review","Score")
          sql <- sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from total_df")
          ################################################################################
          #Combining all the years dataset with Union SQL operator
          ################################################################################
          
          sql_union <-sqldf("SELECT * FROM sql_union UNION SELECT * FROM sql")

        }
        sql_union$Id<-NULL
        sql_union <- sql_union %>% mutate(Id = row_number())
        sql_union<-sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from sql_union order by Year,Id asc")

        ################################################################################
        #Tag the Service Key words
        ################################################################################
        
        service_char=character()
        service_logical<-grepl("service|Service", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(service_logical))
        {
          if (service_logical[i]==TRUE)
          {
            service_char[i]="service"
          }
          else
          {
            service_char[i]=""
          }
        }
        service_dataframe<-data.frame(service_char)

        ## price data frame ##
        ################################################################################
        #Tag the Price Key words
        ################################################################################
        price_char=character()
        price_logical<-grepl("price|Price", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(price_logical))
        {
          if (price_logical[i]==TRUE)
          {
            price_char[i]="price"
          }
          else
          {
            price_char[i]=""
          }
        }
        price_dataframe<-data.frame(price_char)

        ## handling data frame
        ################################################################################
        #Tag the handling Key words
        ################################################################################

        handling_char=character()
        handling_logical<-grepl("handling|Handling", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(handling_logical))
        {
          if (handling_logical[i]==TRUE)
          {
            handling_char[i]="handling"
          }
          else
          {
            handling_char[i]=""
          }
        }
        handling_dataframe<-data.frame(handling_char)

        ## interior dataframe
        
        ################################################################################
        #Tag the interior Key words
        ################################################################################
        interior_char=character()
        interior_logical<-grepl("interior|Interior", sql_union$Review,ignore.case = FALSE)
        for (i in 1:length(interior_logical))
        {
          if (interior_logical[i]==TRUE)
          {
            interior_char[i]="interior"
          }
          else
          {
            interior_char[i]=""
          }
        }
        interior_dataframe<-data.frame(interior_char)

        df1 <- service_dataframe %>% mutate(id = row_number())
        df2 <- price_dataframe %>% mutate(id = row_number())
        df3 <- handling_dataframe %>% mutate(id = row_number())
        df4 <- interior_dataframe %>% mutate(id = row_number())
        # df5 <- score_dataframe %>% mutate(id = row_number())

        words_df <- merge(df1,df2,by="id")
        words_df <- merge(words_df,df3,by="id")
        words_df <- merge(words_df,df4,by="id")
        colnames(words_df) <- c("Id","service","price","handling","interior")
        words_df$new<- with(words_df, paste(service, price, handling, interior))


        sql_final <- merge(sql_union,words_df,by="Id")
       test_sql_final <-sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, new AS Tags, Score from sql_final order by Id asc")
       
       ################################################################################
       #Training the Model with Linear Regression Technique
       ################################################################################
       trainingData <- data.frame(training_sql_final$Score,training_sql_final$Rating) 
       colnames(trainingData) <- c("Score","Rating")# model training data
       testData <- data.frame(test_sql_final$Score)
       colnames(testData) <- c("Score")# test data
       lmMod <- lm(Rating ~ Score, data=trainingData)  # build the model
       
       ################################################################################
       #predicting the Star Ratingds for Test Values
       ################################################################################
       RatingPred <- as.integer(predict(lmMod, testData))
       
      
       RatingPred <- as.data.frame(RatingPred) %>% mutate(Id = row_number())
       colnames(RatingPred) <- c("Predicted_Rating","Id")
       test_sql_final<-merge(test_sql_final,RatingPred,by="Id")
     
       

      }

      
    )
    
    output$Tfidf <- renderTable(
      {
        
        ####################
        #Individual URL
        ####################
        a <- 'https://www.cars.com/research/toyota-camry-'
        c <-'/consumer-reviews/?nr=250&pg=1'
        sql_union <- data.frame(Id=character(),
                                Year=character(),
                                Rating=character(), 
                                Review=character(),
                                Normalized_review=character(),
                                Score=integer())
        for (year in c(2012,2013,2014,2015,2016))
          
        {
          url<-paste0(a,year,c)
          toyota_webpage <- read_html(url)
          description <- html_nodes(toyota_webpage,'.mmy-reviews__blurb div span')
          description_text <- html_text(description)
          description_text<-gsub("\n","",description_text)
          description_text_normalized<-tolower(description_text)
          description_text_normalized<-gsub("[[:punct:]]", "", description_text_normalized)  
          
          # #
          year <- html_nodes(toyota_webpage,'.consumer-reviews-social-share div  span')
          year_text <- html_text(year)
          year_text<-gsub("\n","",year_text)
          year_text[2]
          only_year<-substr(year_text[2], 1, 4)
          only_year<-rep.int(only_year, length(description_text))
          #
          
          ratings <- html_nodes(toyota_webpage, css='.mmy-reviews__review header noscript')
          ratings_text <- html_text(ratings)
          ratings_text<-gsub("\n","",ratings_text)
          
          only_ratings<-ratings_text[c(TRUE, FALSE)]
          only_ratings<-gsub(" ", "",only_ratings, fixed = TRUE)
          only_ratings<-substr(only_ratings, 0, 1)
          
          desc_dataframe<-data.frame(description_text)
          ratings_dataframe<-data.frame(only_ratings)
          year_dataframe<-data.frame(only_year)
          desc_norm_dataframe<-data.frame(description_text_normalized)
          
          AFINN <- sentiments %>%
            filter(lexicon == "AFINN") %>%
            select(word, afinn_score = score)
          
          score_char=character()
          for (i in 1:length(description_text_normalized))
          {
            text_df <- data_frame(text = description_text_normalized[i])
            
            aa<-text_df %>%
              unnest_tokens(word, text) %>%
              left_join(AFINN, by = "word")
            
            bb<-as.data.frame(aa)
            
            score_char[i]<-sqldf("SELECT SUM(afinn_score) from bb")
            score_char[is.na(score_char)] <- 0
          }
          score_dataframe<-data.frame(score_char)
          score_dataframe <- t(score_dataframe)
          score_dataframe<-as.data.frame(score_dataframe)
          
          df1 <- desc_dataframe %>% mutate(id = row_number())
          df2 <- ratings_dataframe %>% mutate(id = row_number())
          df3 <- year_dataframe %>% mutate(id = row_number())
          df4 <- desc_norm_dataframe %>% mutate(id = row_number())
          df5 <- score_dataframe %>% mutate(id = row_number())
          
          total_df <- merge(df2,df1,by="id")
          total_df <- merge(df3,total_df,by="id")
          total_df <- merge(total_df,df4,by="id")
          total_df <- merge(total_df,df5,by="id")
          colnames(total_df) <- c("Id","Year","Rating","Review","Normalized_Review","Score")
          sql <- sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from total_df")
          sql_union <-sqldf("SELECT * FROM sql_union UNION SELECT * FROM sql")
        }
          sql_union$Id<-NULL
          sql_union <- sql_union %>% mutate(Id = row_number())
          sql_union<-sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from sql_union order by Year,Id asc")
          
          service_char=character()
          j=1
          service_logical<-grepl("service|Service", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(service_logical))
          {
            if (service_logical[i]==TRUE)
            { 
              service_char[j]=sql_union$Review[i]
              j=j+1
            }
            else
            {}
            
          }
          service_dataframe<-data.frame(service_char)
          
          ######
          final_table <- data.frame(reviews=character(),
                                    word=character(),
                                    n=character())
          for (i in 1:length(service_dataframe$service_char))
          {
            text_df <- data_frame(text = as.character(service_dataframe$service_char[i]))
            first<-text_df %>%
              unnest_tokens(word, text)  %>%
              count(service_dataframe$service_char[i], word, sort = TRUE) %>%
              ungroup()
            
            first_nostop <- first %>%
              anti_join(get_stopwords())
            
            colnames(first_nostop) <-c("reviews","word","n")
            
            loop_table<-sqldf("select * from first_nostop")
            final_table<-sqldf("select * from loop_table union select * from final_table")
          }
          
          service_final_table_tfidf <- final_table %>%
            bind_tf_idf(reviews,word, n) %>%
            arrange(desc(tf_idf))
          
          
          price_char=character()
          j=1
          price_logical<-grepl("price|Price", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(price_logical))
          {
            if (price_logical[i]==TRUE)
            { 
              price_char[j]=sql_union$Review[i]
              j=j+1
            }
            else
            {}
            
          }
          
          price_dataframe<-data.frame(price_char)
          
          ######
          final_table <- data.frame(reviews=character(),
                                    word=character(),
                                    n=character())
          for (i in 1:length(price_dataframe$price_char))
          {
            text_df <- data_frame(text = as.character(price_dataframe$price_char[i]))
            first<-text_df %>%
              unnest_tokens(word, text)  %>%
              count(price_dataframe$price_char[i], word, sort = TRUE) %>%
              ungroup()
            
            first_nostop <- first %>%
              anti_join(get_stopwords())
            
            colnames(first_nostop) <-c("reviews","word","n")
            
            loop_table<-sqldf("select * from first_nostop")
            final_table<-sqldf("select * from loop_table union select * from final_table")
          }
          
          price_final_table_tfidf <- final_table %>%
            bind_tf_idf(reviews,word, n) %>%
            arrange(desc(tf_idf))
          
          handling_char=character()
          j=1
          handling_logical<-grepl("handling|Handling", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(handling_logical))
          {
            if (handling_logical[i]==TRUE)
            { 
              handling_char[j]=sql_union$Review[i]
              j=j+1
            }
            else
            {}
            
          }
          
          handling_dataframe<-data.frame(handling_char)
          
          ######
          final_table <- data.frame(reviews=character(),
                                    word=character(),
                                    n=character())
          for (i in 1:length(handling_dataframe$handling_char))
          {
            text_df <- data_frame(text = as.character(handling_dataframe$handling_char[i]))
            first<-text_df %>%
              unnest_tokens(word, text)  %>%
              count(handling_dataframe$handling_char[i], word, sort = TRUE) %>%
              ungroup()
            
            first_nostop <- first %>%
              anti_join(get_stopwords())
            
            colnames(first_nostop) <-c("reviews","word","n")
            
            loop_table<-sqldf("select * from first_nostop")
            final_table<-sqldf("select * from loop_table union select * from final_table")
          }
          
          handling_final_table_tfidf <- final_table %>%
            bind_tf_idf(reviews,word, n) %>%
            arrange(desc(tf_idf))
          
          interior_char=character()
          j=1
          interior_logical<-grepl("interior|Interior", sql_union$Review,ignore.case = FALSE)
          for (i in 1:length(interior_logical))
          {
            if (interior_logical[i]==TRUE)
            { 
              interior_char[j]=sql_union$Review[i]
              j=j+1
            }
            else
            {}
            
          }
          
          interior_dataframe<-data.frame(interior_char)
          
          ######
          final_table <- data.frame(reviews=character(),
                                    word=character(),
                                    n=character())
          for (i in 1:length(interior_dataframe$interior_char))
          {
            text_df <- data_frame(text = as.character(interior_dataframe$interior_char[i]))
            first<-text_df %>%
              unnest_tokens(word, text)  %>%
              count(interior_dataframe$interior_char[i], word, sort = TRUE) %>%
              ungroup()
            
            first_nostop <- first %>%
              anti_join(get_stopwords())
            
            colnames(first_nostop) <-c("reviews","word","n")
            
            loop_table<-sqldf("select * from first_nostop")
            final_table<-sqldf("select * from loop_table union select * from final_table")
          }
          
          interior_final_table_tfidf <- final_table %>%
            bind_tf_idf(reviews,word, n) %>%
            arrange(desc(tf_idf))
          final_tfidf_table<-sqldf("select 'service' AS Tag,reviews,word,n,tf,idf,tf_idf from service_final_table_tfidf
                         union
                                   select 'price' AS Tag,reviews,word,n,tf,idf,tf_idf from price_final_table_tfidf
                                   union
                                   select 'handling' AS Tag,reviews,word,n,tf,idf,tf_idf from handling_final_table_tfidf
                                   union
                                   select 'interior' AS Tag,reviews,word,n,tf,idf,tf_idf from interior_final_table_tfidf
                                   order by Tag, tf_idf desc
                                   ")
      }
    )
    
    output$Plot <- renderPlot(
      
    {
      
      ####################
      #Individual URL
      ####################
    
      a <- 'https://www.cars.com/research/toyota-camry-'
      c <-'/consumer-reviews/?nr=250&pg=1'
      sql_union <- data.frame(Id=character(),
                              Year=character(),
                              Rating=character(), 
                              Review=character(),
                              Normalized_review=character(),
                              Score=integer())
      
      ########################################
      #Years for the Training Data Set
      ########################################
      
      
      for (year in c(2012,2013,2014,2015,2016))
        
      {
        
        ########################################
        #Scraping part for Reviews
        ########################################
        
        url<-paste0(a,year,c)
        toyota_webpage <- read_html(url)
        description <- html_nodes(toyota_webpage,'.mmy-reviews__blurb div span')
        description_text <- html_text(description)
        description_text<-gsub("\n","",description_text)
        description_text_normalized<-tolower(description_text)
        description_text_normalized<-gsub("[[:punct:]]", "", description_text_normalized)  
        
        ########################################
        #Scraping part for years
        ########################################
        
        # #
        year <- html_nodes(toyota_webpage,'.consumer-reviews-social-share div  span')
        year_text <- html_text(year)
        year_text<-gsub("\n","",year_text)
        year_text[2]
        only_year<-substr(year_text[2], 1, 4)
        only_year<-rep.int(only_year, length(description_text))
        #
        ########################################
        #Scraping part for Ratings
        ########################################
        
        
        ratings <- html_nodes(toyota_webpage, css='.mmy-reviews__review header noscript')
        ratings_text <- html_text(ratings)
        ratings_text<-gsub("\n","",ratings_text)
        
        only_ratings<-ratings_text[c(TRUE, FALSE)]
        only_ratings<-gsub(" ", "",only_ratings, fixed = TRUE)
        only_ratings<-substr(only_ratings, 0, 1)
        
        ################################################################################
        #making the Year,Rating and Review columns as a Data Frame
        ################################################################################
        
        desc_dataframe<-data.frame(description_text)
        ratings_dataframe<-data.frame(only_ratings)
        year_dataframe<-data.frame(only_year)
        desc_norm_dataframe<-data.frame(description_text_normalized)
        
        ################################################################################
        #Finding the Affin score for each review
        ################################################################################
        
        
        AFINN <- sentiments %>%
          filter(lexicon == "AFINN") %>%
          select(word, afinn_score = score)
        
        score_char=character()
        for (i in 1:length(description_text_normalized))
        {
          text_df <- data_frame(text = description_text_normalized[i])
          
          aa<-text_df %>%
            unnest_tokens(word, text) %>%
            left_join(AFINN, by = "word")
          
          bb<-as.data.frame(aa)
          
          score_char[i]<-sqldf("SELECT SUM(afinn_score) from bb")
          score_char[is.na(score_char)] <- 0
        }
        score_dataframe<-data.frame(score_char)
        score_dataframe <- t(score_dataframe)
        score_dataframe<-as.data.frame(score_dataframe)
        
        ################################################################################
        #Adding row number to each data frame
        ################################################################################
        
        
        df1 <- desc_dataframe %>% mutate(id = row_number())
        df2 <- ratings_dataframe %>% mutate(id = row_number())
        df3 <- year_dataframe %>% mutate(id = row_number())
        df4 <- desc_norm_dataframe %>% mutate(id = row_number())
        df5 <- score_dataframe %>% mutate(id = row_number())
        
        ################################################################################
        #Merging all three Dataframes into a single Dataframe
        ################################################################################
        
        
        total_df <- merge(df2,df1,by="id")
        total_df <- merge(df3,total_df,by="id")
        total_df <- merge(total_df,df4,by="id")
        total_df <- merge(total_df,df5,by="id")
        colnames(total_df) <- c("Id","Year","Rating","Review","Normalized_Review","Score")
        sql <- sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from total_df")
        sql_union <-sqldf("SELECT * FROM sql_union UNION SELECT * FROM sql")
      }
      sql_union$Id<-NULL
      sql_union <- sql_union %>% mutate(Id = row_number())
      ################################################################################
      #Combining all the years dataset with Union SQL operator
      ################################################################################
      
      sql_union<-sqldf("SELECT Id, Year, Rating, Review, Normalized_Review, Score from sql_union order by Year,Id asc")
      
      
      
      ################################################################################
      #Finding the review which are tagged as Service
      ################################################################################
      
      service_char=character()
      j=1
      service_logical<-grepl("service|Service", sql_union$Review,ignore.case = FALSE)
      for (i in 1:length(service_logical))
      {
        if (service_logical[i]==TRUE)
        { 
          service_char[j]=sql_union$Review[i]
          j=j+1
        }
        else
        {}
        
      }
      service_dataframe<-data.frame(service_char)
      
      ######
      final_table <- data.frame(reviews=character(),
                                word=character(),
                                n=character())
      ################################################################################
      #Tokenizing the Review
      ################################################################################
      for (i in 1:length(service_dataframe$service_char))
      {
        text_df <- data_frame(text = as.character(service_dataframe$service_char[i]))
        first<-text_df %>%
          unnest_tokens(word, text)  %>%
          count(service_dataframe$service_char[i], word, sort = TRUE) %>%
          ungroup()
        
        ################################################################################
        #Removing the Stop Words
        ################################################################################
        
        first_nostop <- first %>%
          anti_join(get_stopwords())
        
        colnames(first_nostop) <-c("reviews","word","n")
        
        loop_table<-sqldf("select * from first_nostop")
        final_table<-sqldf("select * from loop_table union select * from final_table")
      }
      ################################################################################
      #Finding the TF-IDF Score
      ################################################################################
      
      service_final_table_tfidf <- final_table %>%
        bind_tf_idf(reviews,word, n) %>%
        arrange(desc(tf_idf))
      
      ################################################################################
      #Finding the review which are tagged as Price
      ################################################################################   
      price_char=character()
      j=1
      price_logical<-grepl("price|Price", sql_union$Review,ignore.case = FALSE)
      for (i in 1:length(price_logical))
      {
        if (price_logical[i]==TRUE)
        { 
          price_char[j]=sql_union$Review[i]
          j=j+1
        }
        else
        {}
        
      }
      
      price_dataframe<-data.frame(price_char)
      
      ######
      final_table <- data.frame(reviews=character(),
                                word=character(),
                                n=character())
      
      ################################################################################
      #Tokenizing the Review
      ################################################################################
      for (i in 1:length(price_dataframe$price_char))
      {
        text_df <- data_frame(text = as.character(price_dataframe$price_char[i]))
        first<-text_df %>%
          unnest_tokens(word, text)  %>%
          count(price_dataframe$price_char[i], word, sort = TRUE) %>%
          ungroup()
        
        ################################################################################
        #Removing the Stop Words
        ################################################################################
        
        first_nostop <- first %>%
          anti_join(get_stopwords())
        
        colnames(first_nostop) <-c("reviews","word","n")
        
        loop_table<-sqldf("select * from first_nostop")
        final_table<-sqldf("select * from loop_table union select * from final_table")
      }
      
      ################################################################################
      #Finding the TF-IDF Score
      ################################################################################
      price_final_table_tfidf <- final_table %>%
        bind_tf_idf(reviews,word, n) %>%
        arrange(desc(tf_idf))
      
      ################################################################################
      #Finding the review which are tagged as Handling
      ################################################################################
      
      handling_char=character()
      j=1
      handling_logical<-grepl("handling|Handling", sql_union$Review,ignore.case = FALSE)
      for (i in 1:length(handling_logical))
      {
        if (handling_logical[i]==TRUE)
        { 
          handling_char[j]=sql_union$Review[i]
          j=j+1
        }
        else
        {}
        
      }
      
      handling_dataframe<-data.frame(handling_char)
      
      ######
      final_table <- data.frame(reviews=character(),
                                word=character(),
                                n=character())
      ################################################################################
      #Tokenizing the Review
      ################################################################################
      for (i in 1:length(handling_dataframe$handling_char))
      {
        text_df <- data_frame(text = as.character(handling_dataframe$handling_char[i]))
        first<-text_df %>%
          unnest_tokens(word, text)  %>%
          count(handling_dataframe$handling_char[i], word, sort = TRUE) %>%
          ungroup()
        
        ################################################################################
        #Removing the Stop Words
        ################################################################################
        
        first_nostop <- first %>%
          anti_join(get_stopwords())
        
        colnames(first_nostop) <-c("reviews","word","n")
        
        loop_table<-sqldf("select * from first_nostop")
        final_table<-sqldf("select * from loop_table union select * from final_table")
      }
      
      ################################################################################
      #Finding the TF-IDF Score
      ################################################################################
      handling_final_table_tfidf <- final_table %>%
        bind_tf_idf(reviews,word, n) %>%
        arrange(desc(tf_idf))
      
      ################################################################################
      #Finding the review which are tagged as Interior
      ################################################################################
      
      interior_char=character()
      j=1
      interior_logical<-grepl("interior|Interior", sql_union$Review,ignore.case = FALSE)
      for (i in 1:length(interior_logical))
      {
        if (interior_logical[i]==TRUE)
        { 
          interior_char[j]=sql_union$Review[i]
          j=j+1
        }
        else
        {}
        
      }
      
      interior_dataframe<-data.frame(interior_char)
      
      ######
      final_table <- data.frame(reviews=character(),
                                word=character(),
                                n=character())
      ################################################################################
      #Tokenizing the Review
      ################################################################################
      for (i in 1:length(interior_dataframe$interior_char))
      {
        text_df <- data_frame(text = as.character(interior_dataframe$interior_char[i]))
        first<-text_df %>%
          unnest_tokens(word, text)  %>%
          count(interior_dataframe$interior_char[i], word, sort = TRUE) %>%
          ungroup()
        
        ################################################################################
        #Removing the Stop Words
        ################################################################################
        
        first_nostop <- first %>%
          anti_join(get_stopwords())
        
        colnames(first_nostop) <-c("reviews","word","n")
        
        loop_table<-sqldf("select * from first_nostop")
        final_table<-sqldf("select * from loop_table union select * from final_table")
      }
      
      ################################################################################
      #Finding the TF-IDF Score
      ################################################################################
      interior_final_table_tfidf <- final_table %>%
        bind_tf_idf(reviews,word, n) %>%
        arrange(desc(tf_idf))
      final_tfidf_table<-sqldf("select 'service' AS Tag,reviews,word,n,tf,idf,tf_idf from service_final_table_tfidf
                               union
                               select 'price' AS Tag,reviews,word,n,tf,idf,tf_idf from price_final_table_tfidf
                               union
                               select 'handling' AS Tag,reviews,word,n,tf,idf,tf_idf from handling_final_table_tfidf
                               union
                               select 'interior' AS Tag,reviews,word,n,tf,idf,tf_idf from interior_final_table_tfidf
                               order by Tag, tf_idf desc
                               "
                               )
      
      ##########################################################################
      #Visualization for each of the tags - Price, Interior, Handling and Service
      ###########################################################################
      
      final_tfidf_table %>%
        arrange(desc(tf_idf)) %>%
        #mutate(Position = fct_reorder(Position, n, .desc = TRUE)) %>%
        #mutate(word = factor(word, levels = rev(unique(word)))) %>% 
        group_by(Tag) %>% 
        top_n(10) %>% 
        ungroup %>% 
        ggplot(aes(word, tf_idf,fill=Tag)) +
        geom_col(show.legend = TRUE) +
        labs(x = NULL, y = "tf-idf") +
        facet_wrap(~Tag, ncol = 2, scales = "free") +
        coord_flip()
    }
    ) 
    ########################################################
    #Comparison of average sentiment score vs Average Rating
    ########################################################
    output$Text <- renderText({
      print("The average sentiment rating in the training data set is 7.25  and the average star rating in training dataset is 4.52619 \n \n")
    })
    
    ########################################
    #Linear Regression Model Output
    ########################################
    output$Text1 <- renderText({
      print("Built a linear regression model with a intercept of 4.22615 and a slope of 0.04139 \n \n")
    })
  }
)

