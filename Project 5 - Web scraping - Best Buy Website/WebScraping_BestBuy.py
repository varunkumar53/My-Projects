
# coding: utf-8

# In[1]:

#-Importing packages and modules for Web Scraping-#

import bs4
import json
import smtplib
import time
import email
import email.mime.application
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# In[2]:

#-Specify the Website from which data has to be extracted-#

my_url ='https://www.bestbuy.com/site/digital-slr-cameras/body-lens/pcmcat180400050000.c?id=pcmcat180400050000'


# In[3]:

#-Open the connection and grabing the response of the website-#

uClient = uReq(my_url)
page_html=uClient.read()
uClient.close()


# In[4]:

#-Parse the response of the website as a HTML file-#

page_soup = soup(page_html,'html.parser')


# In[5]:

#-Grabs each product/item in the container-#

containers = page_soup.findAll("div",{"class":"list-item"})


# In[6]:

#-Open the connection for a new csv file to write the contents of the web page-#

filename="cameras_"+time.strftime("%m-%d-%Y")+".csv"
f=open(filename,"w")

#-Specify the header of the csv file-#
headers ="Brand,Model,Regular Price,Discount,Offer Price,Ratings,No Of Reviewers \n"
f.write(headers)

#-Starting the loop for each item in the container-#
for container in containers:
    
    #-"Brand"-#
    string=container['data-brand']
    dict_data_brand = json.loads(string)
    model_brand = dict_data_brand['brand']
    
    #-"Model Name"-#
    model_name=container["data-name"]
    
    #-"Current Price"-#
    string=container['data-price-json']
    dict_data_price = json.loads(string)
    model_current_price = dict_data_price['priceDomain']['currentPrice']
    
    #-"Discounts"-#
    if 'instantSavings' in dict_data_price['priceDomain'].keys():
        model_discount = dict_data_price['priceDomain']['instantSavings']
    else:
        model_discount=0
        
    #-"Regular Price"-#
    model_old_price =dict_data_price['priceDomain']['regularPrice']
    
    #-"Ratings"-#
    if (container["data-average-rating"]==""):
        model_rating="No Rating"
    else:
        model_rating=container["data-average-rating"]
        
    #-"Reviewers"-#
    if (model_rating=="No Rating"):
        model_review_count="Not Reviewed"
    else:
        model_review_count=container["data-review-count"] 
    
    #-Write the attribute into the csv file-#
    f.write(model_brand+","+model_name.replace(",","|")+","+ str(model_old_price)+","+ str(model_discount)+","+ str(model_current_price)+","+model_rating+","+model_review_count+"\n")
    
#-Close the connection of the csv file-#    
f.close()
    


# In[7]:

#-Add the From & To address-#

fromaddr = "varunkumar.utd@gmail.com"
toaddr ="varunkumar.msec@gmail.com"

#-Create the container (outer) email message-#
msg=MIMEMultipart()
msg['from'] = fromaddr
msg['to'] = toaddr
msg['subject']= "Current status as on " + time.strftime("%m/%d/%Y")
body="Hello! Please find attached the status of the DSLR cameras as on "+ time.strftime("%m/%d/%Y")
msg.attach(MIMEText(body,'plain'))

#-Excel File attachment-#
filename="cameras_"+time.strftime("%m-%d-%Y")+".csv"
fp=open(filename,'rb')
att = email.mime.application.MIMEApplication(fp.read())
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)


# In[9]:

#-Send the message via SMTP gmail server-#

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("varunkumar.utd@gmail.com","******")
server.sendmail(fromaddr,toaddr,msg.as_string())
print("Email Successfull")
server.quit()


# In[ ]:



