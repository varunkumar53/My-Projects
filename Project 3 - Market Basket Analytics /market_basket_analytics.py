
# coding: utf-8

# In[1]:

# Include all packages starts #

print("# Include all packages starts #")

import requests
import pandas as pd
import numpy as np
import re
import itertools

print("# Include all packages ends #")

# Include all packages ends #


# In[2]:

# Downloading the training dataset starts here #

print("# Downloading the training dataset starts here #")



# ************************** Download the training dataset ***************************************** #

# Link To Download the training dataset #

training_datalink="http://kevincrook.com/utd/market_basket_training.txt"

# Request the response of the training dataset #

r=requests.get(training_datalink)

# Create "market_basket_training.txt" and the write the contents of the URL in the TextFile #

training_dataset=open("market_basket_training.txt","wb")
training_dataset.write(r.content)
training_dataset.close()

print("# Downloading the training dataset ends here #")

# Downloading the training dataset ends here #


# In[3]:

# Downloading the test dataset starts here #

print("# Downloading the test dataset starts here #")

# ************************** Download the training dataset ***************************************** #

# Link To Download the test dataset #

test_datalink="http://kevincrook.com/utd/market_basket_test.txt"

# Request the response of the test dataset #

r=requests.get(test_datalink)

# Create "market_basket_test.txt" and the write the contents of the URL in the TextFile #

test_dataset=open("market_basket_test.txt","wb")
test_dataset.write(r.content)
test_dataset.close()

print("# Downloading the test dataset ends here #")

# Downloading the test dataset ends here #


# In[4]:

# Creating training dataframe starts here  #

print("# Creating training dataframe starts here  #")


# Creating a dataframe using the  training_dataset #

ColNames = ["A", "B", "C", "D","E"]
Train_DataFrame = pd.read_csv('market_basket_training.txt', sep=",", names = ColNames,index_col=0)

print("# Creating training dataframe ends here  #")

# Creating training dataframe ends here  #


# In[5]:

# Creating support dataframe starts here  #

print("# Creating support dataframe starts here  #")


Initial_Support=1
# Step to convert into 1s,0s dataframe based on occurence from the tea #
OnesZeros_DataFrame=pd.get_dummies(Train_DataFrame.unstack().dropna()).groupby(level=1).sum()
# To get the shape(dimensions) of the dataframe #
RowLength,ColumnLength  =OnesZeros_DataFrame.shape
pattern = []
for NoOfCombinations in range(1, ColumnLength+1):
    for cols in itertools.combinations(OnesZeros_DataFrame, NoOfCombinations):
        NoOfOccurences = OnesZeros_DataFrame[list(cols)].all(axis=1).sum()
        #Probability=float(NoOfOccurences)/RowLength
        pattern.append([",".join(cols), NoOfOccurences])
sdf = pd.DataFrame(pattern, columns=["Pattern", "Support"])
Support_DataFrame=sdf[sdf.Support >= Initial_Support]


print("# Creating support dataframe ends here  #")

# Creating support dataframe ends here  #


# In[6]:

abc = Train_DataFrame.loc[Train_DataFrame['E'].isnull()]
efg = abc.loc[abc['D'].notnull()]
xyz = Train_DataFrame.loc[Train_DataFrame['D'].isnull()]


# In[7]:

# Creating support dataframe starts here  #

print("# Creating support dataframe starts here  #")


Initial_Support=1
# Step to convert into 1s,0s dataframe based on occurence from the tea #
OnesZeros_DataFrame=pd.get_dummies(xyz.unstack().dropna()).groupby(level=1).sum()
# To get the shape(dimensions) of the dataframe #
RowLength,ColumnLength  =OnesZeros_DataFrame.shape
pattern = []
for NoOfCombinations in range(1, ColumnLength+1):
    for cols in itertools.combinations(OnesZeros_DataFrame, NoOfCombinations):
        NoOfOccurences = OnesZeros_DataFrame[list(cols)].all(axis=1).sum()
        #Probability=float(NoOfOccurences)/RowLength
        pattern.append([",".join(cols), NoOfOccurences])
sdf = pd.DataFrame(pattern, columns=["Pattern", "Support"])
Support_DataFrame_xyz=sdf[sdf.Support >= Initial_Support]


print("# Creating support dataframe ends here  #")

# Creating support dataframe ends here  #


# In[8]:

# Creating support dataframe starts here  #

print("# Creating support dataframe starts here  #")


Initial_Support=1
# Step to convert into 1s,0s dataframe based on occurence from the tea #
OnesZeros_DataFrame=pd.get_dummies(efg.unstack().dropna()).groupby(level=1).sum()
# To get the shape(dimensions) of the dataframe #
RowLength,ColumnLength  =OnesZeros_DataFrame.shape
pattern = []
for NoOfCombinations in range(1, ColumnLength+1):
    for cols in itertools.combinations(OnesZeros_DataFrame, NoOfCombinations):
        NoOfOccurences = OnesZeros_DataFrame[list(cols)].all(axis=1).sum()
        #Probability=float(NoOfOccurences)/RowLength
        pattern.append([",".join(cols), NoOfOccurences])
sdf = pd.DataFrame(pattern, columns=["Pattern", "Support"])
Support_DataFrame_efg=sdf[sdf.Support >= Initial_Support]


print("# Creating support dataframe ends here  #")

# Creating support dataframe ends here  #


# In[9]:

# Creating Bundling dataframe starts here  #

print("# Creating Bundling dataframe starts here  #")

TwoProductBundle=Support_DataFrame_xyz.loc[Support_DataFrame_xyz['Pattern'].str.len() ==7]
ThreeProductBundle=Support_DataFrame_efg.loc[Support_DataFrame_efg['Pattern'].str.len() ==11]
FourProductBundle=Support_DataFrame.loc[Support_DataFrame['Pattern'].str.len() ==15]

print("# Creating Bundling dataframe ends here  #")

# Creating Bundling dataframe ends here  #


# In[10]:

# Creating market_basket_recommendations starts here  #

print("# Creating market_basket_recommendations starts here  #")


TestData_File = open( "market_basket_test.txt", "r" )
Output_File = open("market_basket_recommendations.txt", "w")
lines = []
Products=[]
for line in TestData_File:
    Products=(line[4:-1])
    ProductsList = re.sub("[^\w]", " ",  Products).split()
    #print(line[:4],ProductsList)
    if len(ProductsList)==1:
        x=TwoProductBundle.loc[TwoProductBundle['Pattern'].str.contains(ProductsList[0])]
        y=x.loc[x['Support'].idxmax()]
        my_list = y.values[0]
        my_list = my_list.split(",")
        if ProductsList[0]==my_list[0]:
            #text_file = open("demo_numpy.txt", "w")
            #strr =(line[:4],my_list[1])
            Output_File.write(line[:4]+my_list[1]+ "\n" )
            #text_file.close()
        else:
            #text_file = open("demo_numpy.txt", "w")
            Output_File.write(line[:4]+my_list[0]+ "\n" )
            #text_file.close()
            
            
            
    elif len(ProductsList)==2:
        x=ThreeProductBundle.loc[ThreeProductBundle['Pattern'].str.contains(ProductsList[0])]
        y=x.loc[x['Pattern'].str.contains(ProductsList[1])]
        #print(y.shape[0])
        if y.shape[0]!=0:
            z=y.loc[y['Support'].idxmax()]
            #print(line[:4],ProductsList)
            my_list = z.values[0]
            my_list = my_list.split(",")
            if (ProductsList[0]==my_list[0] and ProductsList[1]==my_list[1]) :
                Output_File.write(line[:4]+my_list[2]+ "\n" )
            elif (ProductsList[0]==my_list[0] and ProductsList[1]==my_list[2]):
                Output_File.write(line[:4]+my_list[1]+ "\n" )
            elif (ProductsList[0]==my_list[1] and ProductsList[1]==my_list[2]):
                Output_File.write(line[:4]+my_list[0]+ "\n" )
        else:
            #print(line[:4],ProductsList)
            if 'P04' in ProductsList: ProductsList.remove('P04')
            if 'P08' in ProductsList: ProductsList.remove('P08')
            #print(line[:4],ProductsList)
            x=TwoProductBundle.loc[TwoProductBundle['Pattern'].str.contains(ProductsList[0])]
            #print(x)
            y=x.loc[x['Support'].idxmax()]
            #print(y)
            my_list = y.values[0]
            my_list = my_list.split(",")
            #print(my_list)
            #print(ProductsList)
            if ProductsList[0]==my_list[0]:
                #text_file = open("demo_numpy.txt", "w")
                #strr =(line[:4],my_list[1])
                #print(111)
                Output_File.write(line[:4]+my_list[1]+ "\n" )
                #print(line[:4]+my_list[1])
                #print(222)
            else:
                #print(333)
                Output_File.write(line[:4]+my_list[0]+ "\n" )
                #print(444)
                
            
    elif len(ProductsList)==3:
        x=FourProductBundle.loc[FourProductBundle['Pattern'].str.contains(ProductsList[0])]
        y=x.loc[x['Pattern'].str.contains(ProductsList[1])]
        z=y.loc[y['Pattern'].str.contains(ProductsList[2])]
        #print(z)
        if z.shape[0]!=0:
            #print("3")
            w=z.loc[z['Support'].idxmax()]
            my_list = w.values[0]
            my_list = my_list.split(",")
            if (ProductsList[0]==my_list[0] and ProductsList[1]==my_list[1] and ProductsList[2]==my_list[2]) :
                Output_File.write(line[:4]+my_list[3]+ "\n" )
            elif (ProductsList[0]==my_list[0] and ProductsList[1]==my_list[2] and ProductsList[2]==my_list[3]) :
                Output_File.write(line[:4]+my_list[1]+ "\n" )
            elif (ProductsList[0]==my_list[0] and ProductsList[1]==my_list[1] and ProductsList[2]==my_list[3]) :
                Output_File.write(line[:4]+my_list[2]+ "\n" )
            elif (ProductsList[0]==my_list[1] and ProductsList[1]==my_list[2] and ProductsList[2]==my_list[3]) :
                Output_File.write(line[:4]+my_list[0]+ "\n" )
        else:
            #print(line[:4])
            if 'P04' in ProductsList: ProductsList.remove('P04')
            if 'P08' in ProductsList: ProductsList.remove('P08')
            if len(ProductsList)==2:
                x=ThreeProductBundle.loc[ThreeProductBundle['Pattern'].str.contains(ProductsList[0])]
                y=x.loc[x['Pattern'].str.contains(ProductsList[1])]
                if y.shape[0]!=0:
                    z=y.loc[y['Support'].idxmax()]
                    my_list = z.values[0]
                    my_list = my_list.split(",")
                    if (ProductsList[0]==my_list[0] and ProductsList[1]==my_list[1]) :
                        Output_File.write(line[:4]+my_list[2]+ "\n" )
                    elif (ProductsList[0]==my_list[0] and ProductsList[1]==my_list[2]):
                        Output_File.write(line[:4]+my_list[1]+ "\n" )
                    elif (ProductsList[0]==my_list[1] and ProductsList[1]==my_list[2]):
                        Output_File.write(line[:4]+my_list[0]+ "\n" )
            else:
                #print(line[:4])
                x=TwoProductBundle.loc[TwoProductBundle['Pattern'].str.contains(ProductsList[0])]
                y=x.loc[x['Support'].idxmax()]
                my_list = y.values[0]
                my_list = my_list.split(",")
                if ProductsList[0]==my_list[0]:
                #text_file = open("demo_numpy.txt", "w")
                #strr =(line[:4],my_list[1])
                    Output_File.write(line[:4]+my_list[1]+ "\n" )
                        #text_file.close()
                else:
                        #text_file = open("demo_numpy.txt", "w")
                    Output_File.write(line[:4]+my_list[0]+ "\n" )
                                                       
TestData_File.close()
Output_File.close()

print("# Creating  market_basket_recommendations ends here  #")

# Creating market_basket_recommendations ends here  #

