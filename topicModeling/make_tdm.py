# -*- coding: utf-8 -*-
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
sys.path.append('/Users/Zhen/Desktop/Courses/BigData/stackexchange/topicModeling/')
from Word2VecUtility import Word2VecUtility

# get the post data
post_tree=ET.parse('/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/Posts.xml')
post=[(i.attrib.get("PostTypeId"),i.attrib.get("CreationDate"),i.attrib.get("Body") ) for i in post_tree.getroot() if i.attrib.get("PostTypeId") in ['2']] 
post_frame=DataFrame(post,columns=['PostTypeId','CreationDate','Body'])
post_body=post_frame.loc[:,'Body']

# clean the posts and save the result in a folder named parse
clean_post = []
postID=[]
print "Cleaning and parsing the posts...\n"
for i in xrange( 0, len(post_body)):
		tmp=BeautifulSoup(post_body[i].replace('\n',""),'html.parser').get_text()
		if tmp=='':
			continue
        postID.append('')
		clean_post=" ".join(Word2VecUtility.review_to_wordlist(tmp, True))
		f = file('/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/parse/' + str(i), 'w');f.write(clean_post.encode('utf-8'))


import textmining
import os
xDIR = '/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/parse'
def termdocumentmatrix_example(xDIR):
    # Initialize class to create term-document matrix
    count=0
    tdm = textmining.TermDocumentMatrix()
    for i in os.listdir(xDIR):
    	Res = tdm.add_doc(open(os.path.join(xDIR,i)).read()) 


    # Write out the matrix to a csv file. Note that setting cutoff=1 means
    # that words which appear in 1 or more documents will be included in
    # the output (i.e. every word will appear in the output). The default
    # for cutoff is 2, since we usually aren't interested in words which
    # appear in a single document. For this example we want to see all
    # words however, hence cutoff=1.
    tdm.write_csv('/Users/Zhen/Desktop/Courses/BigData/stackexchange/topicModeling/result/matrix.csv',cutoff=1) #输出结果
    # Instead of writing out the matrix you can also access its rows directly.
    # Let's print them to the screen.
    for row in tdm.rows(cutoff=1):
            print row

termdocumentmatrix_example(xDIR)