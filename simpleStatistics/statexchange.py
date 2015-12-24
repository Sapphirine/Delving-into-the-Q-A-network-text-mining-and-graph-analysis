import xml.etree.ElementTree as ET
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr
from datetime import datetime
import time
from time import mktime
import sys
sys.path.append('/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/')
pathdata='/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/'
tag_tree=ET.parse('tags.xml')
tag=[(i.attrib.get("TagName"),i.attrib.get("Count") ) for i in tag_tree.getroot()] 
tag_frame=DataFrame(tag,columns=['TagName','Count'])
tag_frame['Count']=tag_frame['Count'].astype(int)

# Get the top 5 tags
popular_tag=tag_frame.loc[tag_frame['Count'].order()[-5:].index.get_values()]
popular_tag_list=list()
for s in popular_tag['TagName']:
	popular_tag_list.append("<%s>" %s)
pattern='|'.join(popular_tag_list)

post_tree=ET.parse(pathdata+'Posts.xml')
post_tag=[(i.attrib.get('Id'), i.attrib.get('PostTypeId'),i.attrib.get('AcceptedAnswerId'),i.attrib.get('CreationDate'),i.attrib.get('Tags'), i.attrib.get('Score'), i.attrib.get('OwnerUserId'),i.attrib.get('FavoriteCount')) for i in post_tree.getroot()]
post_frame=DataFrame(post_tag,columns=['Id','PostTypeId','AcceptedAnswerId','CreationDate','Tags','Score','userId','FavoriteCount'])
post_sort=post_frame.sort(columns='CreationDate')
# fraction of top 5 tags
n=post_frame.shape[0]
post_dropna=post_frame.dropna(axis=0, how='any')
fraction_pop_tag=round(float(sum(post_dropna['Tags'].str.contains(pattern)))/float(n),10)
print fraction_pop_tag

# score difference of ask and answer
post_frame['Score']=post_frame['Score'].astype(float)
post_frame['FavoriteCount']=post_frame['FavoriteCount'].astype(float)
ask=post_frame.loc[post_frame['PostTypeId']=='1']
answer=post_frame.loc[post_frame['PostTypeId']=='2']
score_diff=round(answer['Score'].mean()-ask['Score'].mean(),10)
print score_diff

# pearson_corr 
user_tree=ET.parse('Users.xml')
user=[(i.attrib.get('Id'), i.attrib.get('Reputation'),i.attrib.get('UpVotes'),i.attrib.get('DownVotes') ) for i in user_tree.getroot()] 
user_frame=DataFrame(user,columns=['userId','Reputation','UpVotes','DownVotes'])
group_post=post_frame.groupby('userId').sum()
group_post['userId']=group_post.index
join_post_user=pd.merge(group_post, user_frame, on='userId', how='inner')
join_post_user['Reputation']=join_post_user['Reputation'].astype(float)
pearson_corr = round(pearsonr(join_post_user['Score'], join_post_user['Reputation'])[0],10)
print pearson_corr

# upvotes difference 
upvote_diff=round(np.nansum(answer['FavoriteCount'])/answer.shape[0]-np.nansum(ask['FavoriteCount'])/ask.shape[0],10)
print upvote_diff

#time difference
ask_react=ask[['CreationDate','AcceptedAnswerId']]
ask_react.columns=[['CreationDate_ask','Id']]
answer_react=answer[['Id','CreationDate']]
join_ask_answer=pd.merge(ask_react, answer_react, on='Id', how='inner')
ask_react_time=[datetime.fromtimestamp(mktime(time.strptime(i,'%Y-%m-%dT%H:%M:%S.%f') )) for i in join_ask_answer['CreationDate_ask'] ]
answer_react_time=[datetime.fromtimestamp(mktime( time.strptime(i,'%Y-%m-%dT%H:%M:%S.%f') )) for i in join_ask_answer['CreationDate'] ]

diff=list()
for i in range(len(ask_react_time)):
	temp=(answer_react_time[i]-ask_react_time[i]).total_seconds()/360
	diff.append(temp)
ask_post_hour=[i.hour for i in ask_react_time]
respond_frame=DataFrame({'ask_hour':ask_post_hour,'diff':diff},columns=['ask_hour','diff'])
group=respond_frame.groupby('ask_hour')
group_hour_median=group.median()
response_diff=group_hour_median.max()-group_hour_median.min()
print response_diff

# users behaviors
comment_tree=ET.parse('Comments.xml')
comment=[(i.attrib.get("CreationDate"),i.attrib.get("UserId") ) for i in comment_tree.getroot()] 
comment_frame=DataFrame(comment,columns=['CreationDate','userId'])
comment_frame['PostTypeId']='3'
post_frame2=post_frame.loc[(post_frame['PostTypeId']=='1') |(post_frame['PostTypeId']=='2'),['CreationDate','userId','PostTypeId']]
behavior=pd.concat([post_frame2,comment_frame],ignore_index=True)

behavior['CreationDate']=[datetime.fromtimestamp(mktime( time.strptime(i,'%Y-%m-%dT%H:%M:%S.%f')) ) for i in behavior['CreationDate'] ]
behavior=behavior.dropna(axis=0, how='any')
total=behavior.shape[0]
[prob_ask,prob_answer,prob_comment]=[float(behavior.loc[behavior['PostTypeId']==i].shape[0])/total for i in ['1','2','3']]
behavior=behavior.sort(['CreationDate'])
behavior_group=behavior.groupby('userId')
unique_user=set(behavior['userId'])


count=0
for user in unique_user:
	temp=behavior_group.get_group(user)
	if temp.shape[0]<=1:
		continue
	temp.loc[temp.index,'PostTypeId2']=temp.PostTypeId.shift(-1)
	temp=temp.dropna(axis=0, how='any')
	temp_group=temp.groupby(['PostTypeId','PostTypeId2']).size()
	if count==0:
		conditional=temp_group
	count+=1
	conditional=pd.concat([conditional,temp_group])

conditional=conditional.add_suffix('').reset_index()
conditional_group=conditional.groupby(['PostTypeId','PostTypeId2']).sum()