#Papers Download
#Date: April 8, 2020
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
    api_key = json.load(f)['api_key']
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {"user-agent" : USER_AGENT}


def get_paper(title):
    '''
    Make requests and download papers from the web
    '''
    full_url = scraper_api + '?api_key=' + api_key +'&url=' + SEARCH_URL + '?q=' + search_filter + ' ' + title

    #make the request and get content as html
    r = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    #use regex to extract relevant urls
    results = []
    for g in soup.find_all('div', class_='r')[:3]:
        anchors = g.find_all('a')
        if anchors:
            results.append(anchors[0]['href'])

    response = requests.get(results[0], headers=headers)
    content_type = response.headers.get('content-type')
    if 'application/pdf' in content_type:
        pass
    else:
        response = requests.get(results[1], headers=headers)
        content_type = response.headers.get('content-type')
        if 'application/pdf' in content_type:
            pass
        else:
            response = requests.get(results[2], headers=headers)
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
    prs.add_argument('-p', '--titles_list', help='List of the paper titles we want to download', type=str, default='title_list_1.json')
    prs = prs.parse_args()
    #getting the list of titles from the json file
    with open(prs.titles_list) as file:
        titles_list = json.load(file)['titles']
    #running the get_paper function on the given number of threads
    p = Pool(prs.num_threads)
    start = time.perf_counter()
    p.map(get_paper, titles_list)
    end = time.perf_counter()
    print('Time to process: ', end - start)


