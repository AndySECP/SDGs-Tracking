#wrapper 
#date: April 9, 2020
import requests
import re
from bs4 import BeautifulSoup
import json
import argparse
import time
from multiprocessing import Pool

#key items for search
SEARCH_URL = "https://google.com/search"
search_filter = 'filetype:pdf'
title = 'sarbecovirus lineage responsible for the COVID-19 pandemic'
scraper_api = 'http://api.scraperapi.com'
with open('api_key.json') as f:
    api_key = json.load(f)['api_key']

def extract_all_title(doc_txt, ret=False, authors=False):
	'''
	Extract all the title from the file and store them in a list
	'''
	title_list = []
	start = time.perf_counter()
	with open(doc_txt) as myfile:
	    i = 0
	    for line in myfile:
	        if authors:
		        try: 
		            nmes = [name for name in [dct['name'] for dct in eval(line)['authors']]]
		            #print('success')
		        except: nmes = ''
	        else:
	            nmes = ''
	        try: 
	            title = eval(line)['title'] + ' '.join(nmes)
	            title_list.append(title)
	        except: print('passing one')
	        if i % 100000 == 0:
	            print(i, ', time: ', time.perf_counter() - start)
	        else: pass
	        i+=1
	#dct =  {'titles': title_list}
	#with open('title_list_{}.json'.format(doc_txt[:-4]), 'w') as json_file:
	#    json.dump(dct, json_file)
	if ret:
	    return title_list
	else:
		return


def get_paper(title):
    '''
    Make requests and download papers from the web
    '''
    full_url = scraper_api + '?api_key=' + api_key +'&url=' + SEARCH_URL + '?q=' + search_filter + ' ' + title

    #make the request and get content as html
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, "html.parser")

    #use regex to extract relevant urls
    results = []
    for g in soup.find_all('div', class_='r')[:3]:
        anchors = g.find_all('a')
        if anchors:
            results.append(anchors[0]['href'])

    response = requests.get(results[0])
    content_type = response.headers.get('content-type')
    if 'application/pdf' in content_type:
        pass
    else:
        response = requests.get(results[1])
        content_type = response.headers.get('content-type')
        if 'application/pdf' in content_type:
            pass
        else:
            response = requests.get(results[2])
            content_type = response.headers.get('content-type')
            if 'application/pdf' in content_type:
                pass
            else:
                return
    #we save the downloaded pdf
    with open('{}.pdf'.format(title), 'wb') as f:
        f.write(response.content)

    return


if __name__ == '__main__':
	# Initialize the arguments
    prs = argparse.ArgumentParser()
    prs.add_argument('-t', '--num_threads', help='Number of Threads to use', type=int, default=8)
    prs.add_argument('-d', '--doc_txt', help='aminer txt with the info', type=str, default='aminer_papers_1.txt')
    prs = prs.parse_args()

    #running the extract_all_title function
    titles_list = extract_all_title(prs.doc_txt, ret=True, authors=False)
    print('titles extracted')
    p = Pool(prs.num_threads)
    start = time.perf_counter()
    p.map(get_paper, titles_list)
    end = time.perf_counter()
    print('Time to process the download part: ', end - start)

