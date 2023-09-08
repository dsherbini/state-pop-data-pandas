# PPHA 30537: Python Programming for Public Policy
# Spring 2023
# HW5: Data Manipulation in Pandas
# Author: Danya Sherbini

##################

# To answer these questions, you will continue from where you left off in
# homework 4, by using the included file named hw4_data.csv.

import pandas as pd
import os

base_path = '/Users/danya/Documents/GitHub/personal github/homework-5-dsherbini'
path = os.path.join(base_path, 'hw4_data.csv')
df = pd.read_csv(path)

# Question 1a: Reshape the data from wide to long, using the wide_to_long function,
# making sure you reset the index to the default values if any of your data is located 
# in the index.  What happened to the POPCHANGE column, and why should it be dropped?

# reshaping 
df_long = pd.wide_to_long(df, stubnames='POPESTIMATE', i='STATE', j='YEAR')

# popchange column no longer makes sense because its recording each year's row as having a pop change; 
# it's no langer comparing different years to each other 

# removing popchange column
df_long = df_long.loc[:, ['POPESTIMATE']]

# Question 1b: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 1a (without the POPCHANGE column).

df_long2 = df.melt(id_vars = 'STATE', value_vars = None, var_name = 'YEAR', value_name = 'POPESTIMATE')
                        

# Question 2: Open the state-visits.xlsx file, and fill in the VISITED column
# with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original long-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.

# reading in data
path2 = os.path.join(base_path, 'state-visits.xlsx')
df_state_visits = pd.read_excel(path2)

# merging the data
df_merged = df.merge(df_state_visits, on = 'STATE', how = 'inner')

# investigating which observations were dropped
df_merged_outer = df.merge(df_state_visits, on = 'STATE', how = 'outer', indicator = True)
df_merged_outer[df_merged_outer['_merge'] != 'both']
# 2 obs were dropped: GU and PR


# Question 3a: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.

# reading in data
path3 = os.path.join(base_path, 'policy_uncertainty.xlsx')
df_pol_un = pd.read_excel(path3)

# taking mean by state and year
df_pol_un = df_pol_un.groupby(['state', 'year'], as_index=False)['EPU_Composite'].mean()


# Question 3b) Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. 

# filtering by years 2020 - 2022
df_pol_un = df_pol_un[df_pol_un['year'] > 2019]

# reshaping
df_pol_un = df_pol_un.pivot(index = 'state', columns ='year', values ='EPU_Composite')


# Question 3c) Finally, merge this data into your merged data from question 2, 
# making sure the merge does what you expect.

# changing state column from index to column
df_pol_un.reset_index(inplace=True)

# abbreviating states in df_pol_un
import us
   
def abbr_state(state):
    state = us.states.lookup(state)
    return state.abbr if state else 'NA'
    
df_pol_un['state'] = df_pol_un['state'].map(lambda x: abbr_state(x))

# merging data
df_full = df_merged.merge(df_pol_un, left_on='STATE', right_on='state', how = 'left')
df_full = df_full.drop(columns = 'state', axis=1)



# Question 4: Using groupby on the VISITED column in the dataframe resulting 
# from the previous question, answer the following questions and show how you  
# calculated them: a) what is the single smallest state by 2022 population  
# that you have visited, and not visited?  b) what are the three largest states  
# by 2022 population you have visited, and the three largest states by 2022 
# population you have not visited? c) do states you have visited or states you  
# have not visited have a higher average EPU-C value in 2022?

# grouping by visited
df_full1 = df_full.groupby(['VISITED', 'STATE'], as_index=False)['POPESTIMATE2022'].mean()

# a) 
# smallest state visited
df_full1[df_full1['VISITED']==1].sort_values('POPESTIMATE2022').head(1)

# smallest state not visited
df_full1[df_full1['VISITED']==0].sort_values('POPESTIMATE2022').head(1)


# b)
# three largest states visited
df_full1[df_full1['VISITED']==1].sort_values('POPESTIMATE2022', ascending = False).head(3)

# three largest states not visited
df_full1[df_full1['VISITED']==0].sort_values('POPESTIMATE2022', ascending = False).head(3)

# c)
# states visited have higher avg EPU-C in 2022
df_full2 = df_full.groupby(['VISITED'], as_index=False)[2022].mean()


# Question 5: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 3a and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore.

# writing a function
def zscore(x):
    zscore = x - x.mean() / x.std()
    return zscore


# calling original df from 3a
path3 = os.path.join(base_path, 'policy_uncertainty.xlsx')
df_z = pd.read_excel(path3)
df_zs = df_z.groupby(['state', 'year'], as_index=False)['EPU_Composite'].mean()

# creating mean column
df_mean = df_zs.groupby('state', as_index = False)['EPU_Composite'].mean()
df_mean.rename(columns = {'EPU_Composite':'EPU_mean'}, inplace = True)

# creating sd column
df_std = df_zs.groupby('state', as_index = False)['EPU_Composite'].std()
df_std.rename(columns = {'EPU_Composite':'EPU_std'}, inplace = True)

# merging data
df_zs = df_zs.merge(df_mean, on = 'state', how = 'inner')
df_zs = df_zs.merge(df_std, on = 'state', how = 'inner')
    
# creating new column 
df_zs['EPU_C_zscore'] = (df_zs.loc[:, 'EPU_Composite'] - df_zs.loc[:, 'EPU_mean']) / df_zs.loc[:,'EPU_std']

# grouping by state
df_zs = df_zs.groupby('state', as_index = False)['EPU_C_zscore'].mean()

