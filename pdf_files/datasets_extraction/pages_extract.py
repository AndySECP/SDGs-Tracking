#pages_extract
#Extraction of relevant pages from papers
#date: 03/02/2020

import concurrent.futures
from multiprocessing import Pool
from urllib.request import urlretrieve
import re
from googlesearch import search
import PyPDF4
import json
import os

os.chdir(os.curdir)
os.chdir("..")


def get_pages(path):
    '''
    This function look at each page of the paper and if it find the occurence of 
    the word data in the corresponding page, it will store it in the json file so we can
    later on, hand label it as relevant or unrelevant to our task
    path: the path of the paper we are interested in
    '''
    doc_ = open(path, mode='rb')
    doc = PyPDF4.PdfFileReader(doc_)
    for i in range(doc.getNumPages()):
        page = doc.getPage(i)
        page = re.sub(r'\n', '', page.extractText())
        if 'data' in page or 'dataset' in page or 'datasets' in page:
            if not os.path.exists('pages_selected_ter'): os.makedirs('pages_selected_ter', exist_ok=True)
            nme = 'pages_selected_bis/{}_page_{}.json'.format(path, i)
            with open(nme, 'w') as raw: 
                json.dump(page, raw, indent=4, sort_keys=False)
    return

def process_paper(fileline):
    '''
    This function extract the relevant pages from the papers
    fileline: the file of the file that we are currently considering
    '''
    title = eval(fileline)['title']
    print(title)
    query = 'filetype:pdf ' + title
    url_list = [url for url in search(query, tld="com", num=5, stop=5, pause=2) if url[-3:]=='pdf']
    
    #if there is at least one pdf link among the top 5 google search results, we can extract it 
    try: url_to_download = url_list[0]
    except: return
    
    #download pdf from online url
    urlretrieve(url_to_download, '{}.pdf'.format(title))
    print('doc_downloaded')
    #we extract the relevant pages
    try:
        get_pages(path='{}.pdf'.format(title))
        print('pages_parsed')
        #finally, we remove the downloaded document
        os.remove('{}.pdf'.format(title))
        print('doc_removed')
    except: pass
    return

def get_count(doc_text):
    '''
    This function return the number of lines in the text file considered
    '''
    count = 0
    for line in open(doc_txt): count += 1
    return count


if __name__=='__main__':
	doc_text = 'aminer_papers_0/aminer_papers_1.txt'
	count = get_count(doc_text)
	with open(doc_txt) as myfile: lines_list = [next(myfile) for x in range(count)]
	p = Pool(8)
	start = time.perf_counter()
	p.map(process_paper, lines_list)
	end = time.perf_counter()
	print('Time to process: ', end - start)