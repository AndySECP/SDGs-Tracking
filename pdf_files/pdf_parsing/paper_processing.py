# Paper Processing
# Date: May 22, 2020

import pandas as pd
import numpy as np
import re
from tika import parser

import concurrent.futures
from multiprocessing import Pool
import argparse

import json
import os
from os import listdir
import time


class Paper:
    
    def __init__(self, path, keywords=['data', 'dataset', 'database'], random_state=42):

        self.path = path
        self.keywords = keywords
        #if not os.path.exists(self.dir): os.makedirs(self.dir, exist_ok=True)
        #self.log = Logger('/'.join([self.dir, 'logs.log']))
        #self.rnd = random_state
        
    def parse(self):
            
        self.raw_content = parser.from_file(self.path)['content']
        #splitting by paragraph
        try:
            paragraph_split = self.raw_content.split('\n\n')
            #removing noise, headers and urls links
            self.paragraph_split_cl = [el for el in paragraph_split if len(el)>50 and len(el.split(' '))>2]
            return True
        except:
        	return False

            
    def extract_paragraph_with_keywords(self, ret=False, save=False, file_path=None):
            
        self.paragraph_keywords = [el for el in self.paragraph_split_cl if 'data' in el or 'dataset' in el or 'database' in el]
        if save and len(self.paragraph_keywords)>0:
            with open(file_path, 'w') as json_file:
                json.dump(self.paragraph_keywords, json_file)
        if ret: return self.paragraph_keywords    



if __name__ == '__main__':
    prs = argparse.ArgumentParser()
    prs.add_argument('-p', '--path', help='Path to access the directory', type=str, default='data/')
    prs.add_argument('-i', '--inputDir', help='input directory', type=str, default='pdf_samples/')
    prs.add_argument('-o', '--outputDir', help='output directory', type=str, default='sample_doc_with_keywords')
    prs.add_argument('-t', '--num_threads', help='Number of Threads to use', type=int, default=8)
    prs = prs.parse_args()

    inputDir = prs.path + prs.inputDir
    print(inputDir)
    outputDir = prs.path + prs.outputDir

    def get_sample_with_keywords(path):
        Pap = Paper(path)
        bool_parse = Pap.parse()
        try:
            nme = path.split("/")[-1][:-4]
        except:
        	nme = path
        if bool_parse:
            Pap.extract_paragraph_with_keywords(ret=False, save=True, file_path='{}/{}.json'.format(outputDir, nme))

    p = Pool(prs.num_threads)
    p.map(get_sample_with_keywords, [''.join([inputDir,listdir(inputDir)[i]]) for i in range(len(listdir(inputDir)))])