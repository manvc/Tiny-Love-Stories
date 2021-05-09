#This Utility is to get all the tiny love story URLS from New York Times website.
import pandas as pd
import requests
import time
from functools import lru_cache

@lru_cache #its a decorator. Call decorator using @
def get_nyt_tinylove_urls(return_urls, return_pubdate):
    seconds = 7
    urls    = []
    pubdate = []
    for page_no in range(14):
        api_url    = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fl=web_url%2C%20pub_date&fq=headline%3A(%22Tiny%20Love%20Stories%22)&page={}&q=tiny-modern-Love-stories&sort=newest&api-key=b1sSZOCjfGfJQDoU2o2pW5ytwgTnmQ8Y".format(page_no)
        #print(api_url)
        links      = requests.get(api_url, time.sleep(seconds))
        links_json = links.json()
        for docs in links_json['response']['docs']:
            url             = docs['web_url']
            published_date = docs['pub_date']
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





