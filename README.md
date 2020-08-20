### Instagram_Production

In this project we tried to automate instagram using selenium. 

The project is divided into 2 parts. In first part we will be extracting user data like username, number of followers, post and followees and account type. The details of data extraction is given in following [notebook](https://github.com/abbi163/Instagram_Production/blob/master/PotentialFollowers.ipynb)

In second part, we will be using the extracted data to extract feature and give us a recommendation using machine learning classification model to which user is most likely to follow back if we interact with them by liking there picture and following them. The details are given in the following [notebook](https://github.com/abbi163/Instagram_Production/blob/master/notebbook/abbijeetanand/AutoScript-V1.1.ipynb)

#### Feature Extraction: 
Our raw data consists of 4 columns. Number of followers, number of following, number of posts and account type. 

Using these four columns we have extracted 7 featuers. They are :-
1. log(following count)
2. log(followees count)
3. Privacy category
4. Follower Category
5. Following Category
6. Post Category
7. Ratio of follower per unit following


To know more in details about the implementation please check out this pyton [script](https://github.com/abbi163/Instagram_Production/blob/master/src/FeatureExtraction.py)

#### Training Model. 

For training I extracted data of all my followers and all my followees.
All the people who followed me were labelled as 0 and all the people whom I followed but they didn't follow me were labelled as 1. I extracted raw data of both the group and extracted features and trained the model using lightgbm classifier to do binary classification. 

```python
from lightgbm import LGBMClassifier
lgm = LGBMClassifier(n_estimators= 500)
model = lgm..fit(X_train, Y_train)
```