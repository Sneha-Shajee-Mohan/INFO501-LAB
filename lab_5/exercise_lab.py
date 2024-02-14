import requests
import os
import sys

from multiprocessing import Pool
from time import sleep

# user-installed
import pandas as pd

from tqdm import tqdm
from numpy.random import uniform
from dotenv import load_dotenv

load_dotenv()

# constants
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
NAME_DEMO = __name__
dfs = []
n = 10

def genius(search_term, per_page=15):

    try:
        
        genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                            f"access_token={ACCESS_TOKEN}&per_page={per_page}"
        response = requests.get(genius_search_url)
        json_data = response.json()
        if response.status_code == 200:
            print(f"STATUS CODE OF SEARCH TERM:{search_term} : {json_data['meta']['status']}")
            return json_data['response']['hits']
        else:
              print(f"Failed to fetch data. Status code:{json_data['meta']['status']}")
              return None
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
        
    

def genius_to_df(search_term, n_results_per_term=10):

    
    json_data = genius(search_term, per_page=n_results_per_term)
    hits = [hit['result'] for hit in json_data]
    df = pd.DataFrame(hits)

    # expand dictionary elements
    df_stats = df['stats'].apply(pd.Series)
    df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns},
                    inplace=True)
    
    df_primary = df['primary_artist'].apply(pd.Series)
    df_primary.rename(columns={c:'primary_artist_' + c for c in df_primary.columns},
                      inplace=True)
    
    df = pd.concat((df, df_stats, df_primary), axis=1)
    
    
    return df

def genius_calling(search_terms):
    if type(search_terms) == list:
        for search_term in tqdm(search_terms):
            df = genius_to_df(search_term, n_results_per_term=n)
    
            # add to list of DataFrames
            dfs.append(df)
        df_genius = pd.concat(dfs)
        df_genius.to_csv('/Users/sneha/IUPUI-INFORMATICS/INFO501-LAB/lab_5/genius_data_mp.csv', index=False)


    else:
        df = genius_to_df(search_term, n_results_per_term=n)
        df_genius.to_csv('/Users/sneha/IUPUI-INFORMATICS/INFO501-LAB/lab_5/genius_data_mp.csv', index=False)




