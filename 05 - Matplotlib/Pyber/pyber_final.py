#!/usr/bin/env python
# coding: utf-8

# # Report on Ride Sharing Data

# ### Compiled by Andrew Boring, Data Scientist 
# (which is way sexier than saying, "Statistician")

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# File to Load (Remember to change these)
city_data_to_load = "data/city_data.csv"
ride_data_to_load = "data/ride_data.csv"

# Read the City and Ride Data
city_data = pd.read_csv(city_data_to_load)
ride_data = pd.read_csv(ride_data_to_load)
#ride_data.head(),  city_data.head()

# Combine the data into a single dataset
combined_data = pd.merge(city_data, ride_data, on="city")
# Display the data table for preview
combined_data.head(10)


# ## Data Set Description
# The example above is a 10-row sample of the information in the raw data set, and includes the following:
# * Ride ID, 
# * Date, 
# * Fare
# * No of available drivers at the time of fare, 
# * City,
# * Classification of city (urban, suburban, or rural)
# 
# 
# ### Trends:
# Urban rides account for the largest percentage of revenue, followed by suburban and rural rides respectively. 
# 
# Urban markets have a higher population density, which in turn provides a larger supply of drivers and a larger number of customers to consume them. 
# 
# Rural areas had higher fare costs in comparison to the urban or suburban areas.

# In[3]:


organized_data = combined_data[["city", "date", "fare", "ride_id", "driver_count", "type"]]
#organized_data.head()


# In[12]:


# Let's get some basic throwaway output to warm up with.

# Counts by city
city_count = organized_data["city"].value_counts()
#city_count.head

# How many cities
number_of_cities = len(organized_data["city"].unique())
#number_of_cities

city_types = organized_data["type"].unique()
#city_types

sum_rides = combined_data["ride_id"].count()


print(f"There are {sum_rides} total rides across {number_of_cities} cities in this data set.")

# Check our data for missing rows
#organized_data.count()


# ## Average Fares and Number of Rides By City
# The following illustrates the number of rides per city and the average (mean) fare.

# In[13]:


#grouped_data_by_city = organized_data.groupby(["city"])
#grouped_data_by_city.mean().head()

#Average Fare per city
#avg_fare_per_city = round(grouped_data_by_city["fare"].mean(), 2)
#avg_fare_per_city.head()
# Rides per city
#rides_per_city = grouped_data_by_city["ride_id"].count().head()
#rides_per_city.head()

#driver_count = organized_data["driver_count"]
#driver_count.head()

# we now have our four plot points, i think:
#print(city_types)
#print(avg_fare_per_city)
#print(rides_per_city)
#print(driver_count)

#driver_df = organized_data["city","driver_count"]
driver_df = organized_data[["city", "driver_count"]]
#driver_df.head()

#Nope. I need to groupby city and city type, don't I?
agg_data_by_city = organized_data.groupby(["type","city"]).aggregate({'ride_id':'count',
                                                                          'fare':'mean',
                                                                          })
agg_data_by_city
agg_data_by_city.sort_index()


# ## Bubble Plot of Ride Sharing Data

# In[14]:


# Obtain the x and y coordinates for each of the three city types

x_limit = agg_data_by_city["ride_id"].max() + 1

agg_df = agg_data_by_city.reset_index()
agg_df = agg_df.rename(columns={"ride_id":"Total Rides",
                        "fare":"Average Fare"
                       })

df = pd.merge(agg_df, driver_df, on="city", how="outer")
#df.head()


#rural_x = pd.Series[df.loc[df['type'] == "Rural"]
rural_x = df.loc[df['type'] == "Rural", 'Total Rides']
suburban_x = df.loc[df['type'] == "Suburban", 'Total Rides']
urban_x = df.loc[df['type'] == "Urban", 'Total Rides']


rural_y = df.loc[df['type'] == "Rural", 'Average Fare']
suburban_y = df.loc[df['type'] == "Suburban", 'Average Fare']
urban_y = df.loc[df['type'] == "Urban", 'Average Fare']

rural_s = df.loc[df['type'] == "Rural", 'driver_count']
suburban_s = df.loc[df['type'] == "Suburban", 'driver_count']
urban_s = df.loc[df['type'] == "Urban", 'driver_count']

bubble_size = 10




# Build the scatter plots for each city types
plt.scatter(rural_x, rural_y, s=rural_s * bubble_size, edgecolors="black", linewidth=1, c="#fade59", alpha=0.3, marker="o", label="Rural")
plt.scatter(suburban_x, suburban_y, s=suburban_s * bubble_size, edgecolors="black", linewidth=1, c="#95cae4", alpha=0.1, marker="o", label="Suburban")
plt.scatter(urban_x, urban_y, s=urban_s * bubble_size, edgecolors="black", linewidth=1, c="#ef865d", alpha=0.1, marker="o", label="Urban")


# Incorporate the other graph properties
plt.title("Pyber Ride Sharing Data 2016")
plt.xlabel("Total Number of Rides (per City)") 
plt.ylabel("Average Fair ($)")

import seaborn as sns
plt.style.use('seaborn-whitegrid')

# Create a legend
plt.legend(framealpha=1, frameon=True, title="City Types")

# Incorporate a text label regarding circle size


# Save Figure
plt.savefig('Pyber_Ride_Sharing_data-2016.png', bbox_inches='tight')


# 

# In[6]:


# Show plot
plt.show()


# In[68]:


new_agg_df = organized_data.groupby(["type"]).aggregate({'fare':'sum'})
new_agg_df.sort_index()

total_fares = new_agg_df["fare"].sum()

rural_fares = (new_agg_df.loc["Rural", "fare"] / total_fares) * 100
suburban_fares = (new_agg_df.loc["Suburban", "fare"] / total_fares) * 100
urban_fares = (new_agg_df.loc["Urban", "fare"] / total_fares) * 100




# ## Total Fares by City Type

# In[69]:


# Calculate Type Percents
#rural_fares = round((rural_y.sum() / sum_rides) * 100, 2)
#urban_fares = round((urban_y.sum() / sum_rides) * 100, 2)
#suburban_fares = round((suburban_x.sum() / sum_rides) * 100, 2)



fares_labels = ["Rural", "Urban", "Suburban"]

# The values of each section of the pie chart
fares = [rural_fares, urban_fares, suburban_fares]

# The colors of each section of the pie chart
colors = ["gold", "lightcoral", "lightskyblue"]

# Tells matplotlib to seperate the "Python" section from the others
explode = (0, 0.1, 0)

plt.pie(fares, explode=explode, labels=fares_labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140)
plt.title("Total Fares by City Type")


# Build Pie Chart

# Save Figure
plt.savefig("Total_fares_by_city_type.png", bbox_inches="tight")


# In[17]:


# Show Figure
plt.show()


# ## Total Rides by City Type

# In[18]:


# Calculate Ride Percents
rural_rides = round((rural_x.count() / sum_rides) * 100, 2)
urban_rides = round((urban_x.count() / sum_rides) * 100, 2)
suburban_rides = round((suburban_x.count() / sum_rides) * 100, 2)

# Build Pie Chart
# Labels for the sections of our pie chart
rides_labels = ["Rural", "Urban", "Suburban"]

# The values of each section of the pie chart
rides = [rural_rides, urban_rides, suburban_rides]

# The colors of each section of the pie chart
colors = ["gold", "lightcoral", "lightskyblue"]

# Tells matplotlib to seperate the "Python" section from the others
explode = (0, 0.1, 0)

plt.pie(rides, explode=explode, labels=rides_labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140)
plt.title("Total Rides by City Type")
# Save Figure
plt.savefig("Total_rides_by_city_type.png", bbox_inches="tight")


# In[15]:


# Show Figure
plt.show()


# ## Total Drivers by City Type

# In[32]:


# Calculate Driver Percents
# Calculate Ride Percents
rural_drivers = round((rural_s.count() / sum_rides) * 100, 2)
urban_drivers = round((urban_s.count() / sum_rides) * 100, 2)
suburban_drivers = round((suburban_s.count() / sum_rides) * 100, 2)

# Build Pie Chart
# Labels for the sections of our pie chart
drivers_labels = ["Rural", "Urban", "Suburban"]

# The values of each section of the pie chart
drivers = [rural_drivers, urban_drivers, suburban_drivers]

# The colors of each section of the pie chart
colors = ["gold", "lightcoral", "lightskyblue"]

# Tells matplotlib to seperate the "Python" section from the others
explode = (0, 0.1, 0)

plt.pie(rides, explode=explode, labels=rides_labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140)
plt.title("Total Drivers by City Type")
# Save Figure
plt.savefig("Total_drivers_by_city_type.png", bbox_inches="tight")


# In[31]:


# Show Figure
plt.show()


# In[ ]:




