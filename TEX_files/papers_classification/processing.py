#multiprocessing
#author: Andy Spezzatti
#date: December 19, 2019

import time
import six
import concurrent.futures
import functools
import cufflinks as cf
from classification import *

mapping = {
    1 :'No Povery',
    2 :'Zero Hunger',
    3 :'Good Health and Well Being',
    4 :'Quality Education',
    5 :'Gender Equality',
    6 :'Clean Water and Sanitation',
    7 :'Affordable and Clean Energy',
    8 :'Decent Work and Economic Growth',
    9 :'Industry, Innovation and Infrastructure',
    10 :'Reduced Inequality',
    11 :'Sustainable cities and communities',
    12 :'Responsible consuption and production',
    13 :'Climate Action',
    14 :'Life Below Water',
    15 :'Life on Land',
    16 :'Peace and Justice Strong Institution',
    17 :'Partnerships to achieve the goals'
}

def dtf_to_img(dtf, row_height=0.6, font_size=11, ax=None):
    '''
    Display a pd.DataFrame as an image
    '''

    # Round columns
    for key in dtf.columns: 
        try: dtf[key] = np.round(dtf[key].values, 3)
        except: pass

    # Basic needed attributes
    header_color, row_colors, edge_color = '#40466e', ['#f1f1f2', 'w'], 'w'
    bbox, header_columns = [0, 0, 1, 1], 0

    if ax is None:
        size = (18, dtf.shape[0]*row_height)
        fig, ax = plt.subplots(figsize=(size))
        ax.axis('off')

    mpl_table = ax.table(cellText=dtf.values, bbox=bbox, colLabels=dtf.columns, cellLoc='center')
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors)])

    return ax

def process_paper(path, direct='Papers'):
    '''    
    Extract the information out of the considered paper

    Args:
        path: the path of the paper we are currently analysing

    Returns:
        nothing, but create a json file to gather statistics about this paper and update the 
        global_summary json file that gather statistics about the whole set of papers
    '''
    path_ = '/'.join([direct, path])
    paper_4 = Paper(path_)
    try:		
        paper_4.get_metadata()
        _ = paper_4.get_cleaned_text()
        SDG_score = paper_4.get_stats(display=False, ret=True)
    except: return

    #adding all the score per SDG
    with open('stats/global_summary.json', 'r') as jsonFile:
        dat = json.load(jsonFile)
        for i in range(17):
            dat['SDG Goal {}'.format(i+1)] += SDG_score['SDG Goal {}'.format(i+1)]
        #get the main SDG Goal from the paper
        dat['Main {}'.format(int(SDG_score['main_goal'][-2:]))] += 1

        jsonFile.seek(0)  # rewind
        nme = 'stats/global_summary.json'
        with open(nme, 'w') as raw: 
        	json.dump(dat, raw, indent=4, sort_keys=False)
        	#json.dump(dat, jsonFile)
       # jsonFile.truncate()

    return 


def get_global_stats(direct='Papers'):
    '''
    Run the above process_paper function for all the papers in the directory using concurrent thread (multiprocessing)
    This create:
    - two json file per paper (one with the metadata and one with the statistics about the SDG Goals based on keywords)
    - one json file with global information about all the papers that have been processed

    Args:
        direct: the directory where are the papers in latex format

    Returns:
        nothing, but create json files with statistics about the papers processed
    '''

    #create the json file that will contains the global information
    global_summary = {}
    for i in range(17):
        #SDG Goal i: cumulative score for the ith SDG Goal
        #Main i: Number of papers that have the ith goal as main topic
        global_summary['SDG Goal {}'.format(i+1)] = 0
        global_summary['Main {}'.format(i+1)] = 0

    if not os.path.exists('stats'): os.makedirs('stats', exist_ok=True)
    nme = 'stats/global_summary.json'
    with open(nme, 'w') as raw: 
        json.dump(global_summary, raw, indent=4, sort_keys=False)
        print('done')

    directory = direct
    papers_paths = [filename for filename in os.listdir(directory)]

    for path in papers_paths:
        process_paper(path, direct='Papers')


def display_global_stats(keywords_occ = False, main_sdg = True, display_df = False):

    if keywords_occ:
        with open('stats/global_summary.json', 'r') as jsonFile:
            dct = json.load(jsonFile)
            dct_ = {key: dct[key] for key in ['SDG Goal {}'.format(i) for i in range(1, 18)]}
            df = pd.DataFrame.from_dict(dct_, orient='index', columns=['count']).sort_values(by='count', ascending=False)
            df['SDGs'] = df.index.map(lambda x: mapping[int(x[-2:])])   
            plt.style.use('fivethirtyeight')
            plt.figure(figsize=(18,4))
            sns.barplot(x=df['SDGs'], y=df['count'])
            plt.xticks(rotation=90)
            plt.ylabel('Score', size=15)
            plt.title('Importance of the different SDG Goals in the papers, based on keywords appearances', size=15)
    else: pass 

    if main_sdg:
        with open('stats/global_summary.json', 'r') as jsonFile:
            dct = json.load(jsonFile)
            dct_ = {key: dct[key] for key in ['Main {}'.format(i) for i in range(1, 18)]}
            df = pd.DataFrame.from_dict(dct_, orient='index', columns=['count']).sort_values(by='count', ascending=False)
            df['SDGs'] = df.index.map(lambda x: mapping[int(x[-2:])])
            df = df.set_index('SDGs')
            plt.style.use('fivethirtyeight')
            explode = [0.1 for _ in range(13)] + [2, 2, 2, 2]
            df.plot.pie(y='count', figsize=(15,15), explode=explode)
            plt.legend(fontsize='large', bbox_to_anchor=(1, 1))
            plt.ylabel('')
            plt.title('Part of the papers that have the corresponding SGD Goal as main topic', size=30)
    else: pass 

    if display_df:
        #visualization of the dataframe as an image
        with open('stats/global_summary.json', 'r') as jsonFile:
            dct_1 = {key: dct[key] for key in ['SDG Goal {}'.format(i) for i in range(1, 18)]}
            dct_2 = {key: dct[key] for key in ['Main {}'.format(i) for i in range(1, 18)]}
            df_1 = pd.DataFrame.from_dict(dct_1, orient='index', columns=['Score from keywords']).reset_index(drop=False)
            df_2 = pd.DataFrame.from_dict(dct_2, orient='index', columns=['Main topic in papers'])
            df_1['Main topic in papers'] = df_2.reset_index()['Main topic in papers']
            df_1['SDG Goal'] = pd.Series(mapping[int(df_1.loc[i, 'index'][-2:])] for i in range(17))
            dtf_to_img(df_1[['SDG Goal', 'Score from keywords', 'Main topic in papers']], row_height=0.6, font_size=11, ax=None)
            #dtf_to_img(df_2.reset_index(), row_height=0.6, font_size=11, ax=None)
    else: pass

    return


