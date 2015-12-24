import xml.etree.ElementTree as ET
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr
from datetime import datetime
import time
from time import mktime
import sys
sys.path.insert(0, '/Users/Zhen/Desktop/Courses/BigData/stackexchange/')
from Word2VecUtility import Word2VecUtility
import sklearn
import sklearn.feature_extraction

post_tree=ET.parse('/Users/Zhen/Desktop/Courses/BigData/stackexchange/data/Posts.xml')
post=[(i.attrib.get("PostTypeId"),i.attrib.get("CreationDate"),i.attrib.get("Body") ) for i in post_tree.getroot()] 
post_frame=DataFrame(post,columns=['PostTypeId','CreationDate','Body'])
post_body=post_frame.loc[:,'Body']

clean_post = []
print "Cleaning and parsing the posts...\n"
for i in xrange( 0, len(post_body)):
	clean_post.append(" ".join(Word2VecUtility.review_to_wordlist(post_body[i], True)))
clean_postdf=pd.DataFrame(clean_post)
clean_postdf.to_csv('post_body.csv',sep=',',encoding = 'utf-8')


 # Initialize the "CountVectorizer" object, which is scikit-learn's
 # bag of words tool.
vectorizer = sklearn.feature_extraction.text.CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000,min_df=1)
# fit_transform() does two functions: First, it fits the model
# and learns the vocabulary; second, it transforms our training data
# into feature vectors. The input to fit_transform should be a list of
# strings.
data_features = vectorizer.fit_transform(clean_post)

# Numpy arrays are easy to work with, so convert the result to an
# array
data_features = data_features.toarray()

print('data_features: {0}'.format(data_features))
print('vectorizer.vocabulary_: {0}'.format(vectorizer.vocabulary_))



##################################

from pyspark import SparkContext
from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.feature import HashingTF
data = sc.textFile("/Users/Zhen/desktop/Courses/BigData/stackexchange/data/post_body2.csv")
parsedData = data.map(lambda line: line.split(" "))
hashingTF = HashingTF()
tf = hashingTF.transform(parsedData)

ldaModel = LDA.train(tf, k=3)

inp =data.map(lambda row: row.split(" "))
word2vec = Word2Vec()
model = word2vec.fit(inp)

schema = sqlContext.inferSchema(data)

def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


from pyspark.mllib.feature import Word2Vec
word2vec = Word2Vec()
model = word2vec.fit(parsedData)


sqlContext = SQLContext(sc)
df = sqlContext.DataFrame(parsedData)


# Load and parse the data
sc =SparkContext()
corpus = sc.parallelize(data_features)

ldaModel = LDA.train(corpus, k=3)

# Output topics. Each is a distribution over words (matching word count vectors)
print("Learned topics (as distributions over vocab of " + str(ldaModel.vocabSize()) + " words):")
topics = ldaModel.topicsMatrix()
for topic in range(3):
    print("Topic " + str(topic) + ":")
    for word in range(0, ldaModel.vocabSize()):
        print(" " + str(topics[word][topic]))
    
# Save and load model
model.save(sc, "myModelPath")
sameModel = LDAModel.load(sc, "myModelPath")

ldaModel = LDA.train(corpus, k=3)

# Output topics. Each is a distribution over words (matching word count vectors)
print("Learned topics (as distributions over vocab of " + str(ldaModel.vocabSize()) + " words):")
topics = ldaModel.topicsMatrix()
for topic in range(3):
    print("Topic " + str(topic) + ":")
    for word in range(0, ldaModel.vocabSize()):
        print(" " + str(topics[word][topic]))
    
# Save and load model
model.save(sc, "myModelPath")
sameModel = LDAModel.load(sc, "myModelPath")

