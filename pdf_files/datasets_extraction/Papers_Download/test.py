import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


def get_url_to_download(url):
    
    r = requests.get(url)
    #get the urls 
    urls_found = re.findall('"https://([^"]*)"', r.text)
    sub_dl = 'dl.acm.org'
    sub_doi = 'doi.org'
    #get those that include the doi.org pattern
    urls_to_keep = [url for url in urls_found if sub_doi in url]
    #return the whole url list
    urls_found_complete = ['https://' + url for url in urls_to_keep]
    try:
        new_url = urls_found_complete[0]
    except: return
    
    url_doi = scraper_api + '?api_key=' + api_key +'&url=' + new_url
    r_doi = requests.get(url_doi)
    #get pdf link
    pdf_urls_found = re.findall('pdfUrl', r_doi.text)
    #get the index of it, as tuples (start, end), take the first result and the index of the end
    #of the substring
    end_substring = [(m.start(0), m.end(0)) for m in re.finditer('pdfUrl', r_doi.text)][0][1]
    #the +3 is because after the substring, there is ":" and then the pattern we want to extract
    new_ext = r_doi.text[end_substring+3:]
    #this pattern endind at the following quote, we are extracting the index of it
    end_index = new_ext.find('\"')
    matching_pattern = new_ext[:37]
    full_url = 'https://ieeexplore.ieee.org' + matching_pattern
    
    return full_url