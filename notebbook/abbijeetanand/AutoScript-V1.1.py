#     This script will automatically select the username to whom to send request everyday! The input will be the hashtag. 
#     This script will do the following things. 
    
#     1. Extract the list of people to send request from SQL file, 
#     2. Extract my followers and followee list 
#     3. Look through these list to confirm that the person I am sending request to is not in this list
#     4. Check if the account is open or close. I will send request only to open account. 
#     5. Check the model I created and tell whether I should follow them or not.
#     6. Follow them
#     7. Like there picture
#     8. Save the list in database (date, username). 
#     9. Use this list to unfollow the person where date is of 7 day before the current date. 
    
# Change directory
import os
os.chdir('C:\\Users\\PC\\Desktop\\Instagram_production')

# Necessary imports
from datetime import datetime, timedelta
from itertools import dropwhile, takewhile
from instaloader import Instaloader, Profile
from src.insta import InstagramBot
from sklearn.externals.joblib import load
from src.FeatureExtraction import featureExtraction
import sqlite3 as db
import numpy as np
import pandas as pd

# today date
today = datetime.today()

# Connect to a database (or create one if it doesn't exist) for saving the list in database
conn = db.connect('data/sqldb/Ig_Data.db')
# Create a 'cursor' for executing commands
c = conn.cursor()

query = '''SELECT * FROM UsersData WHERE date = {}{}{}'''.format("'", today.date(), "'")
dataframe = pd.read_sql(query, conn)
users = dataframe['username'].values


print('Step 1 Completed...')

L = Instaloader()
USER = 'deliacarras' # user with login done
PASSWORD = 'Abhijeet@163' # password of user
USERNAME = 'abbijeetanand' # the username whose details we need to search. 
L.login(USER, PASSWORD)
# Extracting list of my follower and followees !!
profile = Profile.from_username(L.context, USERNAME)

followers = []
for follower in profile.get_followers():
    followers.append(follower.username)
    
followees = []
for followee in profile.get_followees():
    followees.append(followee.username)
    
print('Step 2 completed...')
    
## Look through the list and confirm that the person I am sending request is not in the list !
# We will only consider toFollow list and will delete other list
# TODO: Below make a program where check the user name of the person to whom I followed in SQL File
###     If he is also in users, remove him. 
 

toFollow = []
for user in users:
    if user in followers or user in followees:
        pass
    else: 
        toFollow.append(user)

print('Step 3 completed...')
        

del users
del followers
del followees

## Login using my account and checking for profile information
username = 'abbijeetanand'
_pass = 'Abhi@163'

insta = InstagramBot(username, _pass)
insta.login()

model = load('model/lgm.model')
for user in toFollow:
    # Cleaning the data , removing zero count for follower and followings .
    data = pd.DataFrame()
    data = dataframe[dataframe['username'] == user]
    data = data[['username', 'privacy', 'post', 'followings', 'followers']]
    data = data[(data.followings != 0) & (data.followers != 0) & (data.privacy == "Open")]
    if len(data) == 0:
        pass
    else:
        feature = featureExtraction(data)
        df = feature.exeFeatureExtraction()
        X = df.iloc[:, :7].values
        model_flag = model.predict(X)[0]
        if model_flag == 0:
            insta.follow(user)
            insta.likePhotos(2 + np.random.randint(2, 5), user)
            query = 'INSERT INTO Hernando_Follow_request VALUES ({}{}{}, {}{}{})'.format("'",today.date(),"'", '"',user,'"')
            c.execute(query)
            conn.commit()
            loop_break_flag = 0
            if loop_break_flag == 30:
                print('loop Broken : The End')
                break
            else:
                loop_break_flag += 1
        else:
            pass

# For unfollowing the users who was followed 7 days before. 
sevenDayBefore = datetime.today() + timedelta(days = -7)
query = '''SELECT * FROM Abhijeet_Follow_request WHERE requestDate = "{}"'''.format(sevenDayBefore.date())
unfollow = pd.read_sql_query(query, conn)
toUnfollow = unfollow['username'].values
for user in toUnfollow:
    insta.unfollow(user)
    
print('process completed ......')