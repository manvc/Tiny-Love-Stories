import pandas as pd
from requests_html import HTMLSession
from functools import lru_cache
from tiny_love_urls_util import get_nyt_tinylove_urls
session = HTMLSession()

# @lru_cache #its a decorator. Call decorator using @
def get_nyt_article(session, tls_url):
    nyt = session.get(tls_url)
    return nyt

tls_url_list, tls_pubdate_list  = get_nyt_tinylove_urls(return_urls=True, return_pubdate=True) #unpacking 
#tls_pubdate_list = get_nyt_tinylove_urls(return_urls=False, return_pubdate=True)

api_latest_date = tls_pubdate_list[0]
latest_date     = api_latest_date[0:10]
read_df = pd.read_csv('tinystories.csv')
if read_df.empty == False:
    csv_latest_date = read_df['Published Date'].iloc[0]
else:
    csv_latest_date = ""
#print(latest_date, csv_latest_date)

publishdatetime = []
subheading      = []
paragraph       = []
writtenby       = []

def split_author_from_story(x):
    #print(x)
    story =  x.split('. —')[0]+"."
    #author =  x.split('. —')[1]
    return story#, author

for url,pubdate in zip(tls_url_list,tls_pubdate_list):
    tls_url        = url
    nyt_data       = get_nyt_article(session=session, tls_url=tls_url)
    stories        = nyt_data.html.find('div.StoryBodyCompanionColumn > div.css-53u6y8', first = False)

    for story in stories:
        if csv_latest_date != "" and latest_date == csv_latest_date:
            break
        else :
            sub_heading     = story.find('h2.eoo0vm40', first = True)
            story_paragraph = story.find('p.evys1bk0', first = True)
            author          = story.find('em.e1gzwzxm0', first = True)
            if sub_heading != None and story_paragraph != None and author != None:
                subheading.append(sub_heading.text)
                paragraph.append(story_paragraph.text)
                writtenby.append(author.text)
                publishdatetime.append(pubdate)
    #pubdate.date()
    #print(len(publishdatetime), len(subheading), len(paragraph), len(writtenby)) 
    story_dict = {'Published Date':publishdatetime, 'Story Name':subheading, 'Story':paragraph, 'Author':writtenby}
    df = pd.DataFrame(story_dict)
    df['Published Date'] = pd.to_datetime(df['Published Date'])
    df['Published Date'] = df['Published Date'].dt.date
    df['Story'] = df['Story'].apply(split_author_from_story)
    df.to_csv('tinystories.csv')
