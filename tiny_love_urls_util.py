#This Utility is to get all the tiny love story URLS from New York Times website.
import pandas as pd
import requests
import time
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv('.env')

SECRET_KEY = os.getenv("SECRET_KEY")

@lru_cache #its a decorator. Call decorator using @
def get_nyt_tinylove_urls(return_urls, return_pubdate):

    seconds         = 7
    urls            = []
    pubdate         = []
    
    
    dummy_api_url   = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fl=web_url%2C%20pub_date&fq=headline%3A(%22Tiny%20Love%20Stories%22)&page=0&q=tiny-modern-Love-stories&sort=newest&api-key={SECRET_KEY}".format(SECRET_KEY=SECRET_KEY)
    dummy_link      = requests.get(dummy_api_url)
    dummy_link_json = dummy_link.json()
    meta_hits       = dummy_link_json['response']['meta']['hits']
    # api_latest_date = dummy_link_json['response']['docs'][0]['pub_date']
    # latest_date     = api_latest_date[0:10]
    if (meta_hits % 10) == 0:
        pages = (meta_hits // 10)
    if (meta_hits % 10) > 0:
        pages = (meta_hits // 10) + 1
     
    # read_df = pd.read_csv('C:/Users/Madhuri/Documents/Python/Project - TLS/tinystories.csv')
    # csv_latest_date = read_df['Published Date'].iloc[0] 

    for page_no in range(pages):
        # if latest_date == csv_latest_date:
        #     break
        # else:
        api_url    = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fl=web_url%2C%20pub_date&fq=headline%3A(%22Tiny%20Love%20Stories%22)&page={page_no}&q=tiny-modern-Love-stories&sort=newest&api-key={SECRET_KEY}".format(page_no=page_no, SECRET_KEY=SECRET_KEY)
        links      = requests.get(api_url, time.sleep(seconds))
        links_json = links.json()
        # meta_hits   = links_json['response']['meta']['hits']
        # meta_offset = links_json['response']['meta']['offset']
        # if (meta_hits - meta_offset) < 0:
        #     break
        # else:
        for docs in links_json['response']['docs']:
            url             = docs['web_url']
            published_date  = docs['pub_date']
            urls.append(url)
            pubdate.append(published_date)
    urls_dict = {'Tiny Love Stories URLs': urls, 'Published Date': pubdate}
    urls_df   = pd.DataFrame(urls_dict)
    urls_df.to_csv("TinyLoveStories_urls.txt", index=False) 
    if return_urls == True and return_pubdate == True:
        return(urls, pubdate)
    elif return_urls == True and return_pubdate == False:
        return(urls)
    elif return_urls == False and return_pubdate == True:
        return(pubdate)
