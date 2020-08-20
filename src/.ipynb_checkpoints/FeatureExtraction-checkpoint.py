import pandas as pd
import numpy as np

class featureExtraction():
    def __init__(self, dataframe):
        '''   '''
        self.username = dataframe['username'].values
        self.post = dataframe['post'].values
        self.privacy = dataframe['privacy'].values
        self.following = dataframe['followings'].values
        self.followers = dataframe['followers'].values
        self.ln_followings = np.log(dataframe['followings'].values)
        self.ln_followers = np.log(dataframe['followers'].values)
        
        # For modelling we use output. While using model disable it
        # self.output = dataframe['Output'].values

    def _following(self):
        """ categorically dividing following into  """
        category = []
        for count in self.following :
            if count > 10000 :
                category.append(5)
            elif count > 1000 :
                category.append(4)
            elif count > 500:
                category.append(3)
            elif count > 100:
                category.append(2)
            else:
                category.append(1)
        return category

    def _follower(self):
        """ return the category  """
        category = []
        for count in self.followers :
            if count > 10000 :
                category.append(5)
            elif count > 1000 :
                category.append(4)
            elif count > 500:
                category.append(3)
            elif count > 100:
                category.append(2)
            else:
                category.append(1) 
        return category

    def _post(self):
        """ return the category  """
        category = []
        for count in self.post :
            if count > 500 :
                category.append(5)
            elif count > 100 :
                category.append(4)
            elif count > 50:
                category.append(3)
            elif count > 10:
                category.append(2)
            elif count >= 1:
                category.append(1)
            else:
                category.append(0)
        return category

    def _privacy(self):
        ''' 
        2: Open Account
        1: Close Account
        0: unknown account
        '''
        category = []
        for privacy in self.post :
            if privacy == "Open" :
                category.append(2)
            elif privacy == "Private" :
                category.append(1)
            else:
                category.append(0)
        return category
    def _ratioFollowingFollower(self):
        ''' number of followers per followings'''
        return self.following/self.followers

    def exeFeatureExtraction(self):
        df = pd.DataFrame(data = self.ln_followings, columns = ['ln_following'])
        df['ln_follower'] = self.ln_followers
        df['post_category'] = self._post()
        df['privacy_category'] = self._privacy()
        df['follower_category'] = self._follower()
        df['following_category'] = self._following()
        df['ratio_Follower_Following'] = self._ratioFollowingFollower()
        
        # while modelling for a new user we use output, 
        # df['output'] = self.output
        return df