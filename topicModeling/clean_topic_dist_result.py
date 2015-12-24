import numpy as np
import pandas as pd
import os
'''
preprocessing in command line
cat  /Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/topicDist.txt/part-00000 /Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/topicDist.txt/part-00001 > /Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/topicsDict.txt

sed 's/(//g' topicsDict.txt >topicsDict0.txt

sed 's/)//g' topicsDict0.txt>topicsDict1.txt

sed 's/\[//g' topicsDict1.txt>topicsDict2.txt

sed 's/\]//g' topicsDict2.txt>topicsDict3.txt

'''

path='/Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/'
os.system('cat  /Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/topicDist.txt/part-00000 /Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/topicDist.txt/part-00001 > /Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/topicsDict.txt')

os.system("sed 's/(//g' "+path+"topicsDict.txt >"+path+"topicsDict0.txt")
os.system("sed 's/)//g'  "+path+"topicsDict0.txt >"+path+"topicsDict1.txt")
os.system("sed 's/\[//g' "+path+"topicsDict1.txt >"+path+"topicsDict2.txt")
os.system("sed 's/\]//g' "+path+"topicsDict2.txt >"+path+"topicsDict3.txt")

topics=pd.read_csv(path+'/topicsDict3.txt', header=None)
topics.to_csv(path+'/topic_Distribution_for_each_doc.csv', sep=',')
# lda result is in the order of the documents stored in "parse" folder, so we should link the order with actural doc ID
data=pd.read_csv(path+'/topic_Distribution_for_each_doc.csv', header=0,index_col=0,sep=',')
# order of the documents in "parse" folder, actural doc ID
data_index=pd.read_csv(path+'parse_doc_ID.csv', sep=',',header=False)
# join the two tables
newdata=data_index.merge(data, left_on='Unnamed: 0',right_on='0',how='left')
newdata2=newdata.drop(['Unnamed: 0','0'], 1)
newdata2.to_csv(path+'doc_id_topic_doc_dist.csv',sep=',',header=0,index_col=0)