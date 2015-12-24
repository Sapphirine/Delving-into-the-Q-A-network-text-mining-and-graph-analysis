
# coding: utf-8

# In[2]:

import xml.etree.ElementTree as ET
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr
from datetime import datetime
import time
from time import mktime
import sys
from bs4 import BeautifulSoup
import sklearn
import sklearn.feature_extraction
import re
from bs4 import BeautifulSoup
from Word2VecUtility import Word2VecUtility
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import random
# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 
from sklearn import metrics


# In[3]:

from numpy import genfromtxt
aaId = genfromtxt('/Users/XW/Desktop/datascience.stackexchange.com/answerId.csv', delimiter=',')
aaId = np.array(aaId).tolist()
aaId = [str(int(i)) for i in aaId]
delId = genfromtxt('/Users/XW/Desktop/datascience.stackexchange.com/deletedId.csv', delimiter=',')
delId = np.array(delId).tolist()
delId = [str(int(i)) for i in delId]


# In[4]:

matrix = pd.read_csv('/Users/XW/Desktop/datascience.stackexchange.com/accept.csv')
matrix1 = pd.read_csv('/Users/XW/Desktop/datascience.stackexchange.com/answer.csv')
length = matrix.sum(axis=1)
length1 = matrix1.sum(axis = 1)


# In[5]:

post_tree=ET.parse('/Users/XW/Desktop/datascience.stackexchange.com/Posts.xml')
post=[(i.attrib.get("PostTypeId"),i.attrib.get("CreationDate"),i.attrib.get("Body") ) for i in post_tree.getroot() if i.attrib.get("Id") in aaId]
post_frame=DataFrame(post,columns=['PostTypeId','CreationDate','Body'])
post_body=post_frame.loc[:,'Body']


post1=[(i.attrib.get("PostTypeId"),i.attrib.get("CreationDate"),i.attrib.get("Body") ) for i in post_tree.getroot() if i.attrib.get("PostTypeId") =='2' 
       and i.attrib.get("Id") not in aaId and i.attrib.get("Id") not in delId]
post_frame1=DataFrame(post1,columns=['PostTypeId','CreationDate','Body'])
post_body1=post_frame1.loc[:,'Body']


# In[60]:

clean = []
for i in xrange( 0, len(post_body)):
    tmp=BeautifulSoup(post_body[i].replace('\n',""),'html.parser').get_text()
    if tmp=='':
        continue
    clean.append(tmp)


# In[64]:

clean1 = []
for i in xrange( 0, len(post_body1)):
    tmp=BeautifulSoup(post_body1[i].replace('\n',""),'html.parser').get_text()
    if tmp=='':
        continue
    clean1.append(tmp)


# In[67]:

from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
alchemyapi = AlchemyAPI()


# In[68]:

sentiment_score = []
for i in clean[]:
    response = alchemyapi.sentiment('text', i)
    if response['status'] == 'OK' and 'score' in response['docSentiment'].keys(): 
        flag = response['docSentiment']['score']
        sentiment_score.append(flag)
    else:
        sentiment_score.append(0)


# In[70]:

sentiment_score1 = []
for i in clean1:
    response = alchemyapi.sentiment('text', i)
    if response['status'] == 'OK' and 'score' in response['docSentiment'].keys(): 
        flag = response['docSentiment']['score']
        sentiment_score1.append(flag)
    else:
        sentiment_score1.append(0)


# In[190]:

end = genfromtxt('/Users/XW/Desktop/datascience.stackexchange.com/sentiment_score_result.csv', delimiter=',')


# In[193]:

len(end)


# In[205]:

from decimal import Decimal
senti = [float(Decimal(lat)) for lat in sentiment_score] 
senti1 = [float(Decimal(lat)) for lat in sentiment_score1] 
senti1[0:615].extend(end)


# In[121]:

URL = []
for i in post_body:
    a = re.findall(r"/[a-zA-Z]*[:\/\/]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", i)
    URL.append(len(list(a)))
URL1 = []
for i in post_body1:
    a = re.findall(r"/[a-zA-Z]*[:\/\/]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", i)
    URL1.append(len(list(a)))


# In[248]:

#get answerer's reputation
users_tree=ET.parse('/Users/XW/Desktop/datascience.stackexchange.com/Users.xml')
userId=[i.attrib.get("OwnerUserId") for i in post_tree.getroot() if i.attrib.get("Id") in aaId]
userId1 = [i.attrib.get("OwnerUserId") for i in post_tree.getroot() if i.attrib.get("PostTypeId") =='2' 
       and i.attrib.get("Id") not in aaId and i.attrib.get("Id") not in delId]


# In[312]:

[item for item in userId1 if item not in Id_ ]


# In[282]:

rep = [[i.attrib.get("Id"),i.attrib.get("Reputation")] for i in users_tree.getroot()]


# In[291]:

reputation = []
for i in userId:
    for j in rep:
        if i == j[0]:
            reputation.append(int(j[1]))
            break     


# In[315]:

reputation1 = []
for i in userId1:
    if i == None:
        reputation1.append(0)
    else:
        for j in rep:
            if i == j[0]:
                reputation1.append(int(j[1]))


# In[10]:

#get votes 
score=[i.attrib.get("Score") for i in post_tree.getroot() if i.attrib.get("Id") in aaId]
comment=[i.attrib.get("CommentCount") for i in post_tree.getroot() if i.attrib.get("Id") in aaId]
score1=[i.attrib.get("Score") for i in post_tree.getroot() if i.attrib.get("PostTypeId") =='2' 
        and i.attrib.get("Id") not in aaId and i.attrib.get("Id") not in delId]

comment1=[ i.attrib.get("CommentCount") for i in post_tree.getroot() if i.attrib.get("PostTypeId") =='2' 
        and i.attrib.get("Id") not in aaId and i.attrib.get("Id") not in delId]


# In[11]:

score = [int(i) for i in score]
score1 = [int(i) for i in score1]
comment = [int(i) for i in comment]
comment1 = [int(i) for i in comment1]


# In[ ]:

QueId=[i.attrib.get("ParentId")  for i in post_tree.getroot() if i.attrib.get("Id") in aaId]
QueId1=[i.attrib.get("ParentId")  for i in post_tree.getroot() if i.attrib.get("PostTypeId") =='2' 
        and i.attrib.get("Id") not in aaId and i.attrib.get("Id") not in delId]


# In[12]:

QCreatTime = [i.attrib.get("CreationDate") for i in post_tree.getroot() if i.attrib.get("Id") in QueId]   


# In[13]:

QCreatTime1 = [[i.attrib.get("Id"),i.attrib.get("CreationDate")]  
               for i in post_tree.getroot() if i.attrib.get("Id") in QueId1] 


# In[14]:

ACreatTime = [i.attrib.get("CreationDate")  for i in post_tree.getroot() if i.attrib.get("Id") in aaId]  
ACreatTime1 = [[i.attrib.get("ParentId") ,i.attrib.get("CreationDate")]  for i in post_tree.getroot() 
               if i.attrib.get("PostTypeId") =='2' and i.attrib.get("Id") not in aaId and i.attrib.get("Id") not in delId]  


# In[15]:

import datetime
Time = []
for i in range(len(ACreatTime)):
    gap = pd.to_datetime(ACreatTime[i]) - pd.to_datetime(QCreatTime[i])
    Time.append(gap)
Time1 = []
for i in ACreatTime1:
    for j in QCreatTime1:
        if i[0] == j[0]:

            gap = pd.to_datetime(i[1]) - pd.to_datetime(j[1])
            Time1.append(gap)
            break
            


# In[16]:

from datetime import timedelta
time = [i.total_seconds() for i in Time]
time1 = [i.total_seconds() for i in Time1]


# In[108]:

#get topic features
topic = pd.read_csv('/Users/XW/Desktop/datascience.stackexchange.com/doc_id_topic_doc_dist.csv', sep=',',index_col=0, header=None)
inter=[i.attrib.get("Id") for i in post_tree.getroot() 
      if i.attrib.get("PostTypeId") =='2' and i.attrib.get("Id") not in aaId and i.attrib.get("Id") not in delId ]
index = [int(i) for i in aaId]
index1 = [int(i) for i in inter]
accept_feature = topic.ix[index]
answer_feature = topic.ix[index1]


# In[17]:

#matrix.index = np.arange(1, len(matrix)+1)


# In[18]:

#matrix1.index = np.arange(len(matrix)+1, len(matrix)+len(matrix1)+1)


# In[318]:

result= accept_feature.append(answer_feature)
result.index = np.arange(1, len(result)+1)


# In[319]:

result = result.fillna(0)


# In[330]:

result.shape


# In[320]:

#result1.drop([col for col, val in result1.sum().iteritems() if val <= 1], axis=1, inplace=True)


# In[384]:

result1 = result.copy()


# In[376]:

#result1 = pd.DataFrame()


# In[377]:

#result1


# In[385]:

result1['url'] = Series(np.array(URL + URL1),index=result1.index)
result1['count'] = Series(np.array(length.tolist()+length1.tolist()), index=result1.index)
result1['delta'] = Series(np.array(time+time1), index=result1.index)
result1['score'] = Series(np.array(score+score1), index=result1.index)
result1['comment'] = Series(np.array(comment+comment1), index=result1.index)
#result1['sentiment'] = Series(np.array(senti+senti1), index=result1.index)
result1['rep'] = Series(np.array(reputation+reputation1), index=result1.index)
result1['target'] = Series(np.array([1] * 386 + [0]*1500), index=result1.index)


# In[386]:

result1.shape


# In[387]:

msk = np.random.rand(len(result1)) < 0.8
train = result1[msk]
test = result1[~msk]


# In[388]:


# Create the random forest object which will include all the parameters
# for the fit
forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit(train.drop('target', 1), train.target)


# In[389]:

output = forest.predict(test.drop('target', 1))
right = test.target

print(metrics.classification_report(right, output))
print(metrics.confusion_matrix(right,output))


# In[390]:

false_positive_rate, true_positive_rate, thresholds = roc_curve(right, output)
roc_auc = auc(false_positive_rate, true_positive_rate)
roc_auc


# In[225]:

plt.title('ROC')
plt.plot(false_positive_rate, true_positive_rate, 'b',
label='AUC = %0.2f'% roc_auc)
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'r--')
plt.xlim([-0.1,1.2])
plt.ylim([-0.1,1.2])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()

