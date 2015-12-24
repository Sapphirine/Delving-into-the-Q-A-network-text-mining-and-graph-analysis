import xml.etree.ElementTree as ET
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr
from datetime import datetime
import time
from time import mktime
import sys
sys.path.insert(0, '/Users/Zhen/Desktop/Courses/BigData/stackexchange/topicModeling')
from Word2VecUtility import Word2VecUtility
import sklearn
import sklearn.feature_extraction
from bs4 import BeautifulSoup
path='/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/'
# post_tree=ET.parse('/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/Posts.xml')
# post_tree=ET.parse('/Users/Zhen/Desktop/Courses/BigData/stackexchange/Posts.xml')
# post=[(i.attrib.get("PostTypeId"),i.attrib.get("CreationDate"),i.attrib.get("Body") ) for i in post_tree.getroot()] 
# post_frame=DataFrame(post,columns=['PostTypeId','CreationDate','Title','Body'])
# a=[i.attrib.get("Tags").replace('<','').split('>')[:-1] for i in post_tree.getroot() if ((i.attrib.get("PostTypeId") in ['1','2']) & (i.attrib.get("Tags") is not None))] 


# read post data
post_tree=ET.parse(path+'Posts.xml')
###### psot node
post=[(i.attrib.get("Id"), i.attrib.get("PostTypeId"),\
		i.attrib.get("CreationDate"),\
		i.attrib.get("Title"),\
		BeautifulSoup(i.attrib.get("Body").replace('\n',''),'html.parser').get_text() ,\
		post_tree.getroot()[1].attrib.get("Tags").replace('<','').split('>')[:-1] if i.attrib.get("Tags") is not None else None,
		i.attrib.get("ViewCount"),\
		i.attrib.get("FavoriteCount"))\
		for i in post_tree.getroot() if i.attrib.get("PostTypeId") in ['1','2']]
post_frame=DataFrame(post,columns=['ID','Type','CreationDate','Title','Body','Tags','ViewCount','FavoriteCount'])
post_frame.to_csv('/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/post.csv',sep=';',encoding = 'utf-8',index=False)

# ####### 简易版
# post=[(i.attrib.get("Id"), \
# 		i.attrib.get("CreationDate"),\
# 		post_tree.getroot()[1].attrib.get("Tags").replace('<','').split('>')[:-1] if i.attrib.get("Tags") is not None else None,
# 		i.attrib.get("ViewCount"),\
# 		i.attrib.get("FavoriteCount"),
# 		i.attrib.get("PostTypeId"))\
# 		 for i in post_tree.getroot() if i.attrib.get("PostTypeId") in ['1','2']]
# post_frame=DataFrame(post,columns=['ID','CreationDate','Tags','ViewCount','FavoriteCount','Type'])
# post_frame.to_csv('post2.csv',sep=';',encoding = 'utf-8',index=False)

# print(np.where(post_frame.iloc[0,:] is None)[0])
# ##########



####### User
user_tree=ET.parse(path+'Users.xml')
user=[(i.attrib.get("Id"), i.attrib.get("Reputation"),\
		i.attrib.get("CreationDate"),\
		i.attrib.get("Location"),\
		i.attrib.get("UpVotes"),
		i.attrib.get("DownVotes"),\
		i.attrib.get("Age")) for i in user_tree.getroot()] 
user_frame=DataFrame(user,columns=['ID','Reputation','CreationDate','Location','UpVotes','DownVotes','Age'])
user_frame.to_csv(path+'user.csv',sep=';',encoding = 'utf-8',index=False)

###### Tags
tag_tree=ET.parse(path+'Tags.xml')
tag=[(i.attrib.get("Id"),i.attrib.get("TagName"),i.attrib.get("Count")) for i in tag_tree.getroot()]
tag_frame = DataFrame(tag,columns=['ID',"TagName",'Count'] )
tag_frame.to_csv(path+'tag.csv',sep=';',encoding = 'utf-8',index=False)

###### post relationship
post_relation=[(i.attrib.get("Id"), 
		i.attrib.get("ParentId"))\
		 for i in post_tree.getroot() if i.attrib.get("PostTypeId") in ['2']]
post_relation_frame=DataFrame(post_relation,columns=['START_ID','END_ID'])
post_relation_frame.to_csv(path+'post_relation.csv',sep=';',encoding = 'utf-8',index=False)


###### User post relationship
up=[(i.attrib.get("Id"),\
	i.attrib.get("OwnerUserId"),\
	'ask' if i.attrib.get("PostTypeId") =='1' else 'answer')\
	for i in post_tree.getroot() if i.attrib.get("PostTypeId") in ['1','2']]
up_frame = 	DataFrame(up, columns=['Id',"OwnerUserId",'Type'])
up_frame.to_csv(path+'userPost.csv',sep=';',encoding = 'utf-8',index=False)

###### post tag relations  
post_tree.getroot()[1].attrib.get("Tags").replace('<','').split('>')[:-1]
post_tag_relation=list()
for i in post_tree.getroot():
	if ((i.attrib.get("PostTypeId") in ['1']) & (i.attrib.get("Tags") is not None)):
		for j in i.attrib.get("Tags").replace('<','').split('>')[:-1]:
			post_tag_relation.append((i.attrib.get("Id"),j))
post_tag_relation_frame = DataFrame(post_tag_relation, columns=['ID','Tag'])
post_tag_relation_frame.to_csv(path+'post_tag_relation_frame.csv',sep=';',encoding = 'utf-8',index=False)


# post_tag_relation=[(i.attrib.get("Id"),j) \
# 		for j in i.attrib.get("Tags").replace('<','').split('>')[:-1] \
# 		for i in post_tree.getroot() \
# 		if ((i.attrib.get("PostTypeId") in ['1']) & (i.attrib.get("Tags") is not None)) ]
