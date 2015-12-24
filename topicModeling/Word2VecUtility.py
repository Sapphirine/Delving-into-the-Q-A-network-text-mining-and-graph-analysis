#!/usr/bin/env python

import re
import nltk

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import *
from gensim.models.doc2vec import LabeledSentence

class Word2VecUtility(object):

    @staticmethod
    def review_to_wordlist( review, remove_stopwords=False ):
        # Function to convert a document to a sequence of words,
        # optionally removing stop words.  Returns a list of words.
        #
        # Removes any accents  
        # review_text = utils.deaccent(review_text)  
        # Replace hypens with spaces  
        review_text = re.sub(r"-", " ", review)
        # Remove non-letters
        review_text = re.sub("[^a-zA-Z!?0-9]"," ", review_text)
        review_text = re.sub("[!]", " !", review_text)
        review_text = re.sub("[?]", " ?", review_text)
        # Removes email addresses  
        review_text = re.sub(r"[\w]+@[\.\w]+", "", review_text)  
        # Removes web addresses  
        review_text = re.sub(r"/[a-zA-Z]*[:\/\/]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", review_text) 
        # Convert words to lower case and split them
        words = review_text.lower().split()
        # Optionally remove stop words (false by default)
        if remove_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]
        #Implement porter stemmer
        stemmer = PorterStemmer()
        words = [stemmer.stem(w) for w in words]
        # Return a list of words
        return(words)

    # Define a function to split a review into parsed sentences
    @staticmethod
    def review_to_sentences( review, tokenizer, remove_stopwords=False ):
        # Function to split a review into parsed sentences. Returns a
        # list of sentences, where each sentence is a list of words
        # 1. Use the NLTK tokenizer to split the paragraph into sentences
        raw_sentences = tokenizer.tokenize(review.decode('utf8').strip())
        # 2. Loop over each sentence
        sentences = []
        for i in range(len(raw_sentences)):
            # If a sentence is empty, skip it
            if len(raw_sentences[i]) > 0:
                # Otherwise, call review_to_wordlist to get a list of words
                sentences.append(LabeledSentence(Word2VecUtility.review_to_wordlist(raw_sentences[i], remove_stopwords), ['sentence%d' %i]))

        # for raw_sentence in raw_sentences:
        #     # If a sentence is empty, skip it
        #     if len(raw_sentence) > 0:
        #         # Otherwise, call review_to_wordlist to get a list of words
        #         sentences.append(LabeledSentence(Word2VecUtility.review_to_wordlist( raw_sentence, \
        #           remove_stopwords ),['']))
        #
        # Return the list of sentences (each sentence is a list of words,
        # so this returns a list of lists
        return sentences