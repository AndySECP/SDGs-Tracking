#Get Title
#Date: April 8, 2020
import argparse
import json
import time


def get_title(line):
    nmes = [name for name in [dct['name'] for dct in eval(line)['authors']]]
    title = eval(lines_list[0])['title'] + ' '.join(nmes)
    return title

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
	dct =  {'titles': title_list}
	with open('title_list_{}.json'.format(doc_txt[:-4]), 'w') as json_file:
	    json.dump(dct, json_file)
	if ret:
	    return title_list
	else:
		return


if __name__ == '__main__':
	# Initialize the arguments
    prs = argparse.ArgumentParser()
    prs.add_argument('-d', '--doc_txt', help='aminer txt with the info', type=str, default='aminer_papers_1.txt')
    prs = prs.parse_args()

    #running the extract_all_title function
    extract_all_title(prs.doc_txt, ret=False)