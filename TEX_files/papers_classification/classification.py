#classification
#author: Andy Spezzatti
#date: December 18, 2019

import gzip
import re
import spacy
from spacy.lemmatizer import Lemmatizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer

import os
import json
import logging
import operator

mapping = {
	'SDG Goal 1':'No Povery',
	'SDG Goal 2':'Zero Hunger',
	'SDG Goal 3':'Good Health and Well Being',
	'SDG Goal 4':'Quality Education',
	'SDG Goal 5':'Gender Equality',
	'SDG Goal 6':'Clean Water and Sanitation',
	'SDG Goal 7':'Affordable and Clean Energy',
	'SDG Goal 8':'Decent Work and Economic Growth',
	'SDG Goal 9':'Industry, Innovation and Infrastructure',
	'SDG Goal 10':'Reduced Inequality',
	'SDG Goal 11':'Sustainable cities and communities',
	'SDG Goal 12':'Responsible consuption and production',
	'SDG Goal 13':'Climate Action',
	'SDG Goal 14':'Life Below Water',
	'SDG Goal 15':'Life on Land',
	'SDG Goal 16':'Peace and Justice Strong Institution',
	'SDG Goal 17':'Partnerships to achieve the goals'
}
	

def SDG_keywords():

    '''
    This function use the two keywords csv files to extract the list of keywords by SDG Goal
    '''
    #loading the keywords
    kw1 = pd.read_csv('Keywords.csv')
    kw2 = pd.read_csv('SDG_Keywords_June2019.csv')
    kw2 = kw2[['Goals', 'Words']].head(17)
    kw2['Words'] = kw2['Words'].map(lambda x: [y.strip().lower() for y in x.split(',')])
    kw2 = kw2.T
    kw2.columns = kw2.iloc[0]
    kw2 = kw2.drop(kw2.index[0])
    #getting, for each SDG goal, the set of corresponding keywords
    SDG = {}
    for i in range(17):
        SDG[i+1] = set(kw1['SDG{}'.format(i+1)].dropna().unique()).union(set(kw2.loc['Words', 'Goal {}'.format(i+1)]))

    return SDG


class Paper:

    def __init__(self, path, name_exp=str(int(time.time())), random_state=42):

        self._id = path
        self.dir = 'experiments/{}'.format(self._id)
        if not os.path.exists(self.dir): os.makedirs(self.dir, exist_ok=True)
        self.rnd = random_state
        self.path = path

    
    def get_metadata(self):

        '''
        This function extract the metadata from the paper and save it in a json file
        '''

        f = gzip.open(self.path, 'rb')
        self.text = f.read().decode('utf-8')

        metadata = {}
        try:
        	metadata['title'] = re.search('title\{(.*)\}', self.text).group()[6:-1]
        except: pass
        try:
        	metadata['author'] = re.search('author\{(.*)\}', self.text).group()[7:-1]
        except: pass
        try:
        	metadata['address'] = re.search('address\{[^)]+\}', self.text).group()[8:-1]
        except: pass
        try:
        	metadata['affiliation'] = re.search('affil\{[^)]+\}', self.text).group()[8:-1]
        except: pass

        nme = '/'.join([self.dir, 'metadata.json'])
        with open(nme, 'w') as raw: 
            json.dump(metadata, raw, indent=4, sort_keys=True)

        return metadata


    def get_cleaned_text(self):

        '''
        This function clean the text
        '''

        f = gzip.open(self.path, 'rb')
        self.text = f.read().decode('utf-8')

        #removing stop words and words with only one character
        nlp = spacy.load("en_core_web_sm")
        stop_words = set(nlp.Defaults.stop_words)
        self.text = self.text.lower().split(' ')
        self.text = [word for word in self.text if word not in stop_words if len(word)>1]

        #lemmatizing the words
        lemmatizer = Lemmatizer()
        self.text = [lemmatizer.lookup(word) for word in self.text]

        return self.text


    def get_stats(self, index=None, display=True, ret = False):

        '''
        Compute and display the score for each SDG Goal of the paper
        The score is computed by adding the number of occurence of each keyword related to the corresponding goal
        '''

        vectorizer = CountVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(self.text).todense()

        #dataframe of the words in the text with the count of their occurences, sorted by the count of occurence
        voc_top = pd.DataFrame.from_dict(vectorizer.vocabulary_, columns=['Count'], orient='index').sort_values(by='Count', ascending=False)

        SDG = SDG_keywords()
        SDG_score = {}
        for i in range(17):
            score = 0
            for element in SDG[i+1]:
                try:
                    score+=voc_top.T[element].values[0]
                except:
                    pass
                SDG_score['SDG Goal {}'.format(i+1)] = int(score)
        SDG_score['main_goal'] = max(SDG_score.items(), key = operator.itemgetter(1))[0]

        if index is None: nme = '/'.join([self.dir, 'stats.json'])
        else: nme = '/'.join([self.dir, 'stats_{}.json'.format(index)])
        with open(nme, 'w') as raw: 
        	json.dump(SDG_score, raw, indent=4, sort_keys=False)

        if display == True:
			#plot the score for each SDG Goal related to this paper
	        df = pd.DataFrame.from_dict(SDG_score, orient='index', columns=['count'])
	        plt.style.use('fivethirtyeight')
	        plt.figure(figsize=(18,4))
	        sns.barplot(x=list(mapping.values()), y=df['count'])
	        plt.xticks(rotation=90)
	        plt.ylabel('Score', size=15)
	        plt.title('Importance of the different SDG Goals in the paper, based on keywords', size=15)
        else: pass

        if ret:
            return SDG_score
        else: return







