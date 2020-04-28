from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
import re

class InstagramBot:
    def __init__(self,username,password, user = None):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path = 'C:\\Users\\PC\\Desktop\\Instagram_production\\driver\\geckodriver.exe')
        
        
    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)
        email = bot.find_element_by_name('username').send_keys(self.username)
        password = bot.find_element_by_name('password').send_keys(self.password + Keys.RETURN)

        time.sleep(3)

    def searchHashtag(self,hashtag):
        bot = self.bot

        bot.get('https://www.instagram.com/explore/tags/' + hashtag)
        
    def profile(self, user):
        ''' '''
        time.sleep(3)
        bot = self.bot
        bot.get('https://www.instagram.com/{}'.format(user))
        time.sleep(3)
               
    def likePhotos(self,amount, user):
        ''' This program likes the picture'''
        bot = self.bot
        try:
            bot.find_element_by_class_name('v1Nh3').click()

            i = 1
            while i <= amount:
                time.sleep(4 + np.random.randint(1,6))
                bot.find_element_by_class_name('fr66n').click()
                time.sleep(1 + np.random.randint(2, 5))
                bot.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
                time.sleep(1 + np.random.randint(3,5))
                i += 1
            return 0
        
        except NoSuchElementException:
            return print(user)
      
    def transformation(t2):
        '''  transform text into the number and return it. '''
        assert type(t2) == str
        try:
            t3 = int(t2)
            return t3
        except(ValueError):
            if t2.endswith('k'):
                t3 = re.sub('k', '', t2)
                t3 = re.sub(',','', t3)
                t3 = int(float(t3) * 1000)
                return t3
            elif t2.endswith('m'):
                t3 = re.sub('m', '', t2)
                t3 = re.sub(',','', t3)
                t3 = int(float(t3) * 1000000)
                return t3
            else:
                t3 = re.sub(',','', t2)
                t3 = int(t3)
                return t3

    def countPostsFollowingFollowers(self, user):
        '''returns the number of containing post count by user instagram'''
        bot = self.bot
        try:
            # suppose the username doesnot exits then try and exist will handle the case with non existant user return 0.
            bot.get('https://www.instagram.com/{}'.format(user))
            post = bot.find_element_by_class_name('k9GMp ').text
            t1 = re.split("\n", post)
            posts = InstagramBot.transformation(re.split(" ", t1[0])[0])
            following = InstagramBot.transformation(re.split(" ", t1[2])[0])
            followers = InstagramBot.transformation(re.split(" ", t1[1])[0])
            return posts, following, followers
        except NoSuchElementException:
            return 0, 0, 0
    
    
    def unfollow(self, user):
        'give profile detail , i.e user detail'
        bot = self.bot
        bot.get('https://www.instagram.com/{}'.format(user))
        time.sleep(2)
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button').click()
        time.sleep(2)
        bot.find_element_by_xpath('//button[text()="Unfollow"]').click()
        time.sleep(4)
        
    def follow(self, user):
        ''' Given profile detail, this program follows. '''
        bot = self.bot
        bot.get('https://www.instagram.com/{}'.format(user))
        time.sleep(4)
        bot.find_element_by_xpath('//button[text()="Follow"]').click()
        time.sleep(2)

    def directMessage(self, user, message = ''):
        ''' This function takes user and message as an input and sends direct message as an output. '''
        assert type(message) == str
        bot = self.bot
        bot.get('https://www.instagram.com/direct/new/')
        time.sleep(2)
        bot.find_element_by_name("queryBox").send_keys(user)
        time.sleep(2)
        bot.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div/div[3]/button').click()
        time.sleep(2)
        bot.find_element_by_xpath('//button[text()="Next"]').click()
        time.sleep(2)
        bot.find_elements_by_xpath("*//textarea")[0].send_keys(message)
        time.sleep(3)
        bot.find_element_by_xpath('//button[text()="Send"]').click()
        time.sleep(2)
         
   
    def accountPrivacy(self, user):
        ''' This function returns either true or false. If it's an open account, it returns True, If it's locked. It will return False.   '''
        time.sleep(1)
        posts, following, followers = InstagramBot.countPostsFollowingFollowers(self, user)
        time.sleep(1 + np.random.randint(2,3))
        bot = self.bot
        if posts == 0:
            return user, 'unknown', posts, following, followers
        else:
            try:
                bot.find_element_by_class_name('v1Nh3').click()
                return user, 'Open', posts, following, followers
            
            except NoSuchElementException:
                return user, 'Private', posts, following, followers
        