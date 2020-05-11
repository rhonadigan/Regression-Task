# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from collections import Counter 
#Consider only the rows with country_id = "BDV" (there are 844 such rows). 
#For each site_id, we can compute the number of unique user_id's found in 
#these 844 rows. Which site_id has the largest number of unique users? 
#And what's the number?

# read in data
df = pd.read_csv(r'/Users/rhonadigan/Downloads/Moloco1.csv')
 #%%

#create new data frame from data with country ID BDV
DF_BVD = df[df.country_id=='BDV']

# group by site id and count the number of unique user ids for each site
users_by_site_id = {ref:data['user_id'].nunique() for ref,data in DF_BVD.groupby(['site_id'])}

# print the site id with the highest number of users
print('The site_id with the largest number of users is {}. It has {} users.'.format(max(users_by_site_id, key=users_by_site_id.get),max(users_by_site_id.values())))


 #%%
#Between 2019-02-03 00:00:00 and 2019-02-04 23:59:59, there are four users who 
#visited a certain site more than 10 times. Find these four users & which sites 
#they (each) visited more than 10 times. (Simply provides four triples in the form 
#(user_id, site_id, number of visits) in the box below.)

# get the data for the required time frame
new_df = df[((df.ts<'2019-02-04 23:59:59') & (df.ts>'2019-02-03 00:00:00'))]

# list of triples (user_id,site_id,visits) of all users with more than 10 site visits
users = [(ref,data.site_id.iloc[0],data.site_id.count()) for ref,data in new_df.groupby(['user_id']) if data.site_id.count()>10]

print(users)

 #%%

#For each site, compute the unique number of users whose last visit (found in 
#the original data set) was to that site. For instance, user "LC3561"'s last visit 
#is to "N0OTG" based on timestamp data. Based on this measure, what are top three 
#sites? (hint: site "3POLC" is ranked at 5th with 28 users whose last visit in the 
#data set was to 3POLC; simply provide three pairs in the form (site_id, number of 
#users).)

# group data by user id
grouped_users = df.groupby(['user_id'])

#create empty dataframe to store all users last site visit
latest_visits = pd.DataFrame()

#loop over all user groups and get their last visit
for ref, data in grouped_users:
    latest_visit = data[data.ts == data.ts.max()]
    latest_visits = latest_visits.append(latest_visit)

#group latest visits by site_id and get the count of each site
site_count = {ref:data.user_id.count() for ref,data in latest_visits.groupby(['site_id']) }

# get 3highest values in the site_count dictionary
k = Counter(site_count) 
high = k.most_common(3)  

#print values 
print("3 highest values:") 
for i in high: 
    print("(",i[0]," ,",i[1],")") 
 
 #%%
    
#For each user, determine the first site he/she visited and the last site 
#he/she visited based on the timestamp data. Compute the number of users 
#whose first/last visits are to the same website. What is the number?
    
# group data by user id
grouped_users = df.groupby(['user_id'])

count = 0

#loop over all user groups and get their first and last visit
for ref, data in grouped_users:
    
    last_visit = data[data.ts == data.ts.max()]
    first_visit = data[data.ts == data.ts.min()]
    
    # if the first and last vists for that user are the same then increment count
    if last_visit.site_id.iloc[0] == first_visit.site_id.iloc[0]:
        count+=1
        
print('The number of users whose first/last visits are to the same website is {}'.format(count))
    
