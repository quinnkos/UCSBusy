## EDA Alex Morifusa

### Data Cleaning and Sorting
```py
import pandas as pd
import datetime

df = pd.read_csv('RecCen_Fall2022.csv')

# Fix Date Formatting
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert 'Date' to datetime

# Fix Time Formatting
df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p', errors='coerce').dt.time  # Convert 'Time' to time

# Handle Missing Values
# Decide how to handle missing values in 'Visits' column, e.g., fill with 0
df['Visits'].fillna(0, inplace=True)

# Convert Data Types
df['Visits'] = df['Visits'].astype(int)  # Convert 'Visits' to integer

# Remove Inconsistent Values

df = df[df['Visits'] >= 0]

# Remove any NaT
df = df.dropna()

# Remove Closed Days
# 11/11 Veterans Day Closure
df = df[df['Date'] != '2022-11-11']
# 11/24-27 Thanksgiving Break Closure
df = df[df['Date'] != '2022-11-24']
df = df[df['Date'] != '2022-11-25']
df = df[df['Date'] != '2022-11-26']
df = df[df['Date'] != '2022-11-27']

# Remove Reduced Hours
# 9/18 Open 1-10 (But Data Begins at 12 PM so set 12PM as Open Time)
start_time = datetime.time(6, 0, 0)  # 6 AM
end_time = datetime.time(12, 0, 0)   # 12 PM

mask = ~((df['Date'] == ('2022-9-18')) & (df['Time'] >= start_time) & (df['Time'] < end_time))
df = df[mask]

# 11/23 Open 6-3
start_time = datetime.time(15, 0, 0)  
end_time = datetime.time(23, 0, 0)   

mask = ~((df['Date'] == ('2022-11-23')) & (df['Time'] >= start_time) & (df['Time'] < end_time))
df = df[mask]

# 12/10 Open 11-7
start_time = datetime.time(6, 0, 0)  
end_time = datetime.time(11, 0, 0)   

mask = ~((df['Date'] == ('2022-12-10')) & (df['Time'] >= start_time) & (df['Time'] < end_time))
df = df[mask]

start_time = datetime.time(19, 0, 0)  
end_time = datetime.time(23, 0, 0)   

mask = ~((df['Date'] == ('2022-12-10')) & (df['Time'] >= start_time) & (df['Time'] < end_time))
df = df[mask]

# Sort Day to Monday to Sunday format
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['Day'] = pd.Categorical(df['Day'], categories=days_of_week, ordered=True)

# Sort the Data
df.sort_values(by=['Date', 'Time'], inplace=True)

df.head(15)

# Data is Cleaned and Sorted
print(df)
```
<img width="362" alt="Screenshot 2024-03-02 at 4 21 44 PM" src="https://github.com/amorifusa/UCSBusy/assets/147006654/bf2bc60d-2690-4643-86cb-cc018a72a5c3">

### Overall Summary
```python
df.describe()
```
<img width="143" alt="Screenshot 2024-03-02 at 4 22 23 PM" src="https://github.com/amorifusa/UCSBusy/assets/147006654/f53649c9-9780-4ccf-bf6f-298a9a5d51e9">

```python
# Plotting Clean Data
import os
import numpy as np
from matplotlib import pyplot as plt 
import seaborn as sns
%matplotlib inline

import sys

sns.set(rc={'figure.figsize':(15,15)})

# Horizontal Categories Boxplot, Time is not in order

df = df.sort_values(by= ['Day', 'Time'])

ax = sns.boxplot(x = 'Day', y = 'Visits', data = df, color = 'red', hue = 'Time')
```
<img width="1145" alt="Screenshot 2024-03-02 at 4 36 05 PM" src="https://github.com/amorifusa/UCSBusy/assets/147006654/efde492d-3d18-44e4-8f01-6a29fda99613">

Through the given graph, we are able to observe how busy each day of the week is and the trend via time using averages of the Fall Quarter. 
Certain days of the week are busier than others, same with certain times. We plan to take the data and create a model to approximate by the day and hour.

Next, I analyzed the visits per hour of the day since we want to focus on each hour.

```python
# Boxplot Time vs Visits
sns.set(rc={'figure.figsize':(14,9)})

df_sorted = df.sort_values(by='Time')

ax = sns.boxplot(x = 'Time', y = 'Visits', data = df)![Uploading Screenshot 2024-03-02 at 4.59.40 PM.png…]()

```
<img width="1161" alt="Screenshot 2024-03-02 at 4 41 14 PM" src="https://github.com/amorifusa/UCSBusy/assets/147006654/4261f2d5-05de-4c9a-b4b5-469991ad0a95">

Using this visual, we can approximate the average number of students at the rec center per time of day by the hour.

```python
df['Time'] = df['Time'].astype(str)

# Create a FacetGrid 
g = sns.FacetGrid(df, col='Day', col_order=days_of_week, height=5, aspect=2.2, col_wrap=2)
# Map scatter plots to each day of the week
g.map(sns.scatterplot, 'Time', 'Visits')

g.set_axis_labels('Time', 'Visits')
g.set_titles('{col_name}')
plt.tight_layout()
plt.show()
```
<img width="1172" alt="Screenshot 2024-03-02 at 5 04 05 PM" src="https://github.com/amorifusa/UCSBusy/assets/147006654/c3a9074b-2c14-4045-9f46-2890062597e0">
<img width="599" alt="Screenshot 2024-03-02 at 5 04 28 PM" src="https://github.com/amorifusa/UCSBusy/assets/147006654/270cd06b-aabf-4f49-b11d-dad911c5ffc3">

I made FacetGrid graphs to visually see each day and how the trend for the students in the rec cen looks like by the hour. 

### Summary
