
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
import sklearn.feature_extraction
from Word2VecUtility import Word2VecUtility


# In[3]:

post = ET.parse('Posts.xml')
root = post.getroot()


# In[4]:

total = [i.attrib.get("Id") for i in root]


# In[5]:

#get answers, where the "PostTypeId" == 2 
answers_info = [[i.attrib.get("Id"),i.attrib.get("ParentId"),i.attrib.get("OwnerUserId"),i.attrib.get("LastEditDate")] 
                for i in root if i.attrib.get("PostTypeId") == '2']


# In[6]:

question_info = [[i.attrib.get("Id"), i.attrib.get("OwnerUserId"), i.attrib.get("AcceptedAnswerId")] for i in root if i.attrib.get("PostTypeId") == '1']


# In[7]:

# question_info contains questions without accepted answers 
qwa_info = [x for x in question_info if x[2] is not None] # "Id" "OwnerUserId" "AcceptedAnswerId"


# In[8]:

# get accepted answers Id 
accepted_answers = [i.attrib.get("AcceptedAnswerId") for i in root if i.attrib.get("PostTypeId") == '1']
accepted_answers = [x for x in accepted_answers if x is not None] # post "Id" of accepted answers


# In[9]:

accepted_ans_info = []
for i in answers_info:
    if i[0] in accepted_answers:
        accepted_ans_info.append(i) #"Id" "ParentId" "OwnerUserId" "LastEditDate"


# In[10]:

# filter the Users who accepted their own answers 
self_answers = []
selfans_Id = []
for i in accepted_ans_info:
    for j in qwa_info:
        if i[1] == j[0] and i[2] == j[1]:
            self_answers.append(i)
            selfans_Id.append(i[0])
            break
#len(self_answers) = 22 


# In[12]:

ans_without_info = [x for x in accepted_ans_info if x not in self_answers] 
#len(ans_without_info) = 442
ans_without_id = [x for x in accepted_answers if x not in selfans_Id]


# In[13]:

#delet answers that have edited after accept vote 
vote = ET.parse('Votes.xml')
root2 = vote.getroot()
ans_accepted_date = [[i.attrib.get("PostId"),i.attrib.get("CreationDate"),i.attrib.get("OwnerUserId")] for i in root2 
                     if (i.attrib.get("VoteTypeId") == '1' and i.attrib.get("PostId") in ans_without_id)]


# In[14]:

#get accepted answers last edit date 
date_Id = []
ans_without_info_flag = [x for x in ans_without_info if x[3] is not None]
for i in ans_without_info_flag:
    for j in ans_accepted_date:
        if i[0] == j[0] and pd.to_datetime(i[3]) > pd.to_datetime(j[1]):
            date_Id.append(i[0])
            break
# len(date_Id) = 56 


# In[16]:

#filter the answers edited after accepted
all_cleared_Id = [x for x in ans_without_id if x not in date_Id] 
# len(all_cleared_Id) = 386


# In[28]:

df = pd.DataFrame(all_cleared_Id)
df.to_csv("answerId.csv", index=False, header=False)


# In[17]:

deletedId = selfans_Id + date_Id


# In[19]:

df1 = pd.DataFrame(deletedId)
df1.to_csv("deletedId.csv", index=False, header=False)


# In[ ]:



