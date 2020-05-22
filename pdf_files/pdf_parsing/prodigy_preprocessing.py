#Prodigy Preprocessing
#Date: May 22, 2020

import jsonlines
from datetime import datetime
import json
from multiprocessing import Pool
from os import listdir
import argparse

def prodigy_process(file_path):
    
    with open(file_path) as f:
        file = json.load(f)
        
    def process_paragraph(prg):
        d = {}
        d['text'] = prg
        d['meta'] = {'corpora_id': file_path.split('/')[-1][:-4], 'corpora_id':file_path.split('/')[-1][:-4]+str(datetime.now())}
        #print(d)
        generated_file.write(d)
        #print('done')
        
    list(map(process_paragraph, file))
    return


if __name__ == '__main__':
    prs = argparse.ArgumentParser()
    prs.add_argument('-p', '--path', help='Path to access the directory with the doc with keywords', type=str, default='data/sample_doc_with_keywords/')
    prs.add_argument('-t', '--num_threads', help='Number of Threads to use', type=int, default=8)
    prs.add_argument('-n', '--file_name', help='Name of the generated file', type=str, default='prodigy_processed_file.jsonl')
    prs = prs.parse_args()

    generated_file = jsonlines.open(prs.file_name, mode='w')
    p = Pool(prs.num_threads)
    print([''.join([prs.path, listdir(prs.path)[i]]) for i in range(len(listdir(prs.path))) if listdir(prs.path)[i][-4:]=='json'])
    p.map(prodigy_process, [''.join([prs.path, listdir(prs.path)[i]]) for i in range(len(listdir(prs.path))) if listdir(prs.path)[i][-4:]=='json'])
