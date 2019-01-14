#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
#purchase_data["SN"].value_counts().head()


# In[2]:


# Summary / cross-reference data cell
#purchase_data.dtypes
purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[3]:


#player_count = purchase_data["Purchase ID"].value_counts()
#player_count = len(purchase_data)
player_count = len(purchase_data["SN"].unique())
print ("Total Players: " + str(player_count))


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[4]:


numgames = len(purchase_data["Item ID"].unique())
#uniq_games = purchase_data["Item Name"].value_counts
#uniq_games
avgprice = round(purchase_data["Price"].mean(),2)
numpurchase = len(purchase_data["Purchase ID"])
sumpurchase = purchase_data["Price"].sum()
summary_table = pd.DataFrame({"Number of Unique Items": numgames, "Average Price": avgprice,"Number of Purchases":numpurchase, "Total Revenue $":sumpurchase}, index=[0])
summary_table


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[5]:


#genders = purchase_data.groupby(["Gender"])
#genders = purchase_data["Gender"].value_counts()
#genders
# No good. This gives me 780 players (total rows). I need uniq screennames, then get value counts.
# total_players is my total. I need to get the males, femals, other via uniq.
#players = purchase_data["SN"].unique()
#males = purchase_data.loc[purchase_data["Gender"] == "Male", :]
#print(males).value_counts()
#purchase_data['Gender'].value_counts()
genders = pd.DataFrame(purchase_data.groupby('Gender')['SN'].nunique())
males =  genders.loc["Male","SN"]
females = genders.loc["Female","SN"]
other =  genders.loc["Other / Non-Disclosed","SN"]
mperc = round((males / player_count) * 100)
fperc = round((females / player_count) * 100)
operc = round((other / player_count) * 100)
gtable = pd.DataFrame({"Total":[males,females,other],
                      "Percentage":[mperc,fperc,operc]},
                      index=["Male","Female","Other / NA"],)
gtable


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[6]:


# Groups
grouped_data = purchase_data.groupby(["Gender"])

#Determine Purchase Counts 
purchase_counts = purchase_data["Gender"].value_counts()

# Average Price
averages = grouped_data.mean()
averages["Price"] = pd.to_numeric(averages["Price"])
avg_purchase_price = round(averages["Price"],2)

#Purchase Value = Purchase Count * Avg Purchase Price
purchase_value = purchase_counts * avg_purchase_price

#Fem Purchase per person = tpv / females
#Mal Purchase per person = avg_purchase_price / males
#Oth purhcase per person = avg_purchase_price / other

purchase_analysis = pd.DataFrame({"Purchase Count": purchase_counts,
                                  "Average Purchase Price": avg_purchase_price,
                                  "Total Purchase Value": purchase_value
                                 })

app_f = round(purchase_analysis.loc["Female", "Total Purchase Value"] / females, 2)
app_m = round(purchase_analysis.loc["Male", "Total Purchase Value"] / males, 2)
app_o = round(purchase_analysis.loc["Other / Non-Disclosed", "Total Purchase Value"] / other, 2)

rowIndex = purchase_analysis.index[0]
rowIndex
purchase_analysis.loc[purchase_analysis.index[0], "Average Total Purchase Per Person"] = app_f
purchase_analysis.loc[purchase_analysis.index[1], "Average Total Purchase Per Person"] = app_m
purchase_analysis.loc[purchase_analysis.index[2], "Average Total Purchase Per Person"] = app_o
purchase_analysis


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[7]:


# I need help with this one. My numbers don't look correct, 
# but I can't seem to get the counts to match the expected output.
# I know there are multiple entries for several screen names, but 
# it appears I'm operating on a total count of SN, rather than .nunique
# even though it appeared to work correctly above.
#
# EDIT: After I wrote the above, I added "right=False" to the binning line.
# I did that in a previous attempt, but it did not yield the correct
# numbers.

bins = [0, 10, 15, 20, 25, 30, 35, 40, 100]
age_brackets = ["<10", "10-14", "15-19", "20-24", "25-29","30-34","35-39","40+"]

# I had to do the following, as there were weird NaNs, even though 
# all Age entries were dtype: int64. I don't understand why I had to do this.
purchase_data["Age"].astype(int)

purchase_data["Age Bracket"] = pd.cut(purchase_data["Age"], bins, labels=age_brackets, right=False)
sn_clean_data = purchase_data.drop_duplicates("SN")
age_summary = pd.DataFrame(sn_clean_data.groupby('Age Bracket')['SN'].nunique())

age_summary = age_summary.rename(columns={"SN":"Total Count"})
#age_summary
age_percentage = round(age_summary["Total Count"] / player_count * 100, 2)
age_summary["Percentage of Players"] = age_percentage
age_summary


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[8]:


purchase_data.head()
#age_counts = pd.DataFrame(sn_clean_data.groupby('Age Bracket')['Purchase ID'])
grouped_ages = purchase_data.groupby(["Age Bracket"])
age_purchase_counts = purchase_data["Age Bracket"].value_counts()
#age_purchase_counts

age_averages = grouped_ages.mean()
age_averages["Price"] = pd.to_numeric(age_averages["Price"])
age_avg_purchase_price = round(age_averages["Price"],2)
#age_avg_purchase_price

age_purchase_value = age_purchase_counts * age_avg_purchase_price
#age_purchase_value

age_summary_table = pd.DataFrame({"Purchase Count": age_purchase_counts,
                                  "Average Purchase Price": age_avg_purchase_price,
                                  "Total Purchase Value": age_purchase_value,
                                  "Total Count": age_summary["Total Count"],
                                 })
avg_purchase_per_person = round(age_summary_table["Total Purchase Value"]/age_summary_table["Total Count"], 2)
age_summary_table["Average Total Purchase Per Person"] = avg_purchase_per_person

age_summary_table


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[9]:




spenders_df = purchase_data.groupby(["SN"])

# Why does this work differently when I use Purchase ID instead of SN? 
# sn_purchase_counts = spenders_df["Purchase ID"].value_counts()
sn_purchase_counts = spenders_df["SN"].value_counts()
#sn_purchase_counts.head()




sn_avg_purchase_price = spenders_df["Price"].sum() / sn_purchase_counts
#sn_avg_purchase_price.head()
sn_purchase_value = sn_purchase_counts * sn_avg_purchase_price
spenders_summary = pd.DataFrame({"Purchase Count":sn_purchase_counts,
                                 "Average Purchase Price":sn_avg_purchase_price,
                                 "Total Purchase Value":sn_purchase_value
                                })
sorted_spenders_summary = spenders_summary.sort_values("Total Purchase Value", ascending=False)
sorted_spenders_summary.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[14]:


## I couldn't get this one working. 
## I will need some assistance here.


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[10]:


# I can sort, but not if the one above is incomplete. :-/

