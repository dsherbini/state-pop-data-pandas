# PPHA 30537: Python Programming for Public Policy
# Spring 2023
# HW4: Data Manipulation in Pandas
# Author: Danya Sherbini

##################

# To answer these questions, you will use the csv document included in
# your repo.  In nst-est2022-alldata.csv: SUMLEV is the level of aggregation,
# where 10 is the whole US, and other values represent smaller geographies. 
# REGION is the fips code for the US region. STATE is the fips code for the 
# US state.  The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2022/NST-EST2022-ALLDATA.pdf
# Note that each question will build on the modified dataframe from the
# question before.  Make sure the SettingWithCopyWarning is not raised.

# Question 1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.

import pandas as pd
import os

base_path = '/Users/danya/Documents/GitHub/personal github/homework-4-dsherbini'
path = os.path.join(base_path, 'NST-EST2022-ALLDATA.csv')

df = pd.read_csv(path)


# Question 2: Your data only includes fips codes for states.  Use the us
# library to crosswalk fips codes to state abbreviations.  Keep only the
# state abbreviations in your data.

import us
   
# creating a function to convert fips code to state abbreviation
def abbr_state(fips):
    if len(fips) == 1:
        fips = '0' + fips
    state = us.states.lookup(str(fips))
    return state.abbr if state else 'N/A'

# abbreviating STATE column
df['STATE'] = df['STATE'].map(lambda x: abbr_state(str(x)))
        

# Question 3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize for them. Show the relevant 
# exploration output with print() statements.

# getting summary statistics
df.describe()
   
# calculating average population, birth rate, and death rate for 2022
for state in df[['STATE']]:
    if state != 'N/A':
        mean_pop_2022 = df['POPESTIMATE2022'].mean()
        mean_birthrate_2022 = df['RBIRTH2022'].mean()
        mean_deathrate_2022 = df['RDEATH2022'].mean()
        print(mean_pop_2022,
              mean_birthrate_2022,
              mean_deathrate_2022)
        
# creating a summary table of 2022 population, birth rate, and death rate by state
state_summary = df.loc[14:, ['STATE', 'POPESTIMATE2022', 'RBIRTH2022', 'RDEATH2022']]


# Question 4: Subset the data so that only observations for individual
# US states remain, and only state names and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.

state_pop = df.loc[14:, ['STATE', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']]


# removing DC and PR because they are not US states
state_pop = state_pop.drop([22, 65])


# Question 5: Show only the 10 largest states by 2021 population estimates, in
# decending order.

state_pop.sort_values(by = ['POPESTIMATE2021'], ascending = False).head(10)


# Question 6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?

# adding POPCHANGE column
state_pop['POPCHANGE'] = state_pop.loc[:, 'POPESTIMATE2022'] - state_pop.loc[:, 'POPESTIMATE2020']

# states that gained population
len(state_pop[state_pop['POPCHANGE'] > 0])

# states that lost population
len(state_pop[state_pop['POPCHANGE'] < 0])


# Question 7: Show all the states that had an estimated change of smaller 
# than 1000 people. (hint: look at the standard abs function)

state_pop[state_pop['POPCHANGE'].abs() < 1000]

 
# Question 8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.

# finding the standard deviation
sd_pop_change = round(state_pop['POPCHANGE'].std(), 2)

# calling states with growth more than the sd
state_pop[state_pop['POPCHANGE'].abs() > sd_pop_change]

