
#     1. Enter Hash tag using hashtag file of src
#     2. Extract 300 user per hashtag
#     3. Check whether those users are in UsersData table. 
#     4. Extract for only those whose data is not in the table.
#     5. Recall back the userdata into dataframe, where date is today's date. 

# Change directory
import os
os.chdir('C:\\Users\\PC\\Desktop\\Instagram_production')

from src.data import data
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
from numpy import random
from selenium.common.exceptions import TimeoutException, WebDriverException

hashtags = data.hashtagAfrica()
user_pwd = data.user_pwd()

for key in user_pwd.keys():
    try:
        t = random.randint(0, len(hashtags))
        hashtag = hashtags[t]

        # Step 2
        L = Instaloader()
        data = []
        posts = L.get_hashtag_posts(hashtag)
        likes = set()

        today = datetime.today()
        tomorrow = datetime.today() + timedelta(days = 2)
        yesterday = datetime.today() + timedelta(days = -1)

        # Since is big | less past 
        SINCE = tomorrow
        # Until is small | past
        UNTIL = yesterday

        # Extract the list of people to send request to, note : We are selecting the users who are recently active. 

        for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
            print(post.date)
            likes = post.get_likes()
            for like in likes:
                data.append(like.username)
            users = np.unique(data)
            if len(users) >= 100: 
                break;
            else:
                pass

        # Step 3
        # Connect to a database (or create one if it doesn't exist) for saving the list in database
        conn = db.connect('data/sqldb/Ig_Data.db')
        # Create a 'cursor' for executing commands
        c = conn.cursor()

        query_db = ''' SELECT * FROM UsersData'''
        usersDB = pd.read_sql(query_db, conn)

        alreadySaved = usersDB['username'].values

        toCheck = []
        for user in users:
            if user in alreadySaved:
                pass
            else: 
                toCheck.append(user)

        del alreadySaved
        del usersDB
        del data
        del likes

        # Step 4
        ## Login using my account and checking for profile information
        username = key
        _pass = user_pwd[key]

        insta = InstagramBot(username, _pass)
        insta.login()

        for user in toCheck[:100]:
            try:
                user, AccountType, posts, following, followers = insta.accountPrivacy(user)
                query_insert = '''INSERT INTO UsersData VALUES ({}{}{},{}{}{},{}{}{},{},{},{})'''\
                            .format("'", today.date() ,"'", "'", user, "'","'", AccountType,"'", posts, following, followers)
                c.execute(query_insert)
                conn.commit()
            # adding web driver exception 
            except WebDriverException:
                pass

        # Step 5
        query = '''SELECT * FROM UsersData WHERE date = {}{}{}'''.format("'", today.date(), "'")
        df = pd.read_sql(query, conn)
        # assert len(df) == len(toCheck)
    except TimeoutException:
        pass