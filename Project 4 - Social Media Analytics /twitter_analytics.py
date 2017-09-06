
# coding: utf-8

# In[1]:

import tweepy
import requests
import json
import operator


# In[2]:

# Downloading the json file starts here #

print("# Downloading the json file starts here #")

# ************************** Download the json file ***************************************** #

# Link To Download the json file #

json_datalink="http://kevincrook.com/utd/tweets.json"

# Request the response of the json file #

r=requests.get(json_datalink)

# Create "json_file.txt" and the write the contents of the URL in the TextFile #

json_file=open("tweets.json","wb")
json_file.write(r.content)
json_file.close()

print("# Downloading the json file ends here #")

# Downloading the training dataset ends here #


# In[3]:

# Downloading the json file starts here #

print("# Reading json datafile starts #")

f=open('tweets.json','rt')
json_data=json.load(f)
f.close()

print("# Reading json datafile ends #")

# Downloading the json file starts here #


# In[4]:

#  Create the twitter_analytics.txt and tweets.txt file#

Output_File1 = open("twitter_analytics.txt", "w")
Output_File2 = open("tweets.txt", "w")

# Tweet count = 0#
tweet_count=0
# Delete count = 0#
delete_count=0
lang_full_list=[]
for tweet in json_data:
    
    #  To write the tweets into tweets.txt file  #
    
    if 'text' in tweet:
        my_string=str(tweet['text'].encode('utf8'))
        Output_File2.write(my_string.split("'")[1]+'\n')
        
        #  To Count the numberof tweets  #
        
        tweet_count=tweet_count+1
        
    #  To Count the number of deleted tweets  #

    if 'delete' in tweet:
        delete_count=delete_count+1
        
    #  Append all occurences of languages in a list  #  
    
    if 'lang' in tweet:
        lang_full_list.append(tweet['lang'])
        
#  Create a dictionary with distinct languages and the number of occurences #   

lang_dict = {x:lang_full_list.count(x) for x in lang_full_list}

# Sort the laguage dictionary in descending order w.r.t number of occurences #

sorted_lang_dict = sorted(lang_dict.items(), key=operator.itemgetter(1),reverse=True)

#  No_Of_Events = Total Number Of Tweets + Total No Of Deleted Tweets #

No_Of_Events=tweet_count+delete_count

#  To write the number of events into twitter_analytics.txt file  #
        
Output_File1.write(str(No_Of_Events)+'\n')

#  To write the number of tweets into twitter_analytics.txt file  #

Output_File1.write(str(tweet_count)+'\n')

#  To write the count the frequency of Tweets for each language.  #

for x in sorted_lang_dict:
    Output_File1.write(x[0]+','+str(x[1])+'\n')
    
    
print(tweet_count)
print(delete_count)


Output_File2.close()
Output_File1.close()


# In[ ]:



