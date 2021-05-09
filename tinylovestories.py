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

publishdatetime = []
subheading      = []
paragraph       = []
writtenby       = []


for url,pubdate in zip(tls_url_list,tls_pubdate_list) :
    tls_url        = url
    nyt_data       = get_nyt_article(session=session, tls_url=tls_url)
    stories        = nyt_data.html.find('div.css-1fanzo5.StoryBodyCompanionColumn > div.css-53u6y8', first = False)

    for story in stories:
        sub_heading     = story.find('h2.css-ow6j0y.eoo0vm40', first = True)
        story_paragraph = story.find('p.css-axufdj.evys1bk0', first = True)
        author          = story.find('em.css-2fg4z9.e1gzwzxm0', first = True)
        if sub_heading != None and story_paragraph != None and author != None:
            subheading.append(sub_heading.text)
            paragraph.append(story_paragraph.text)
            writtenby.append(author.text)
            publishdatetime.append(pubdate)
    #print(len(publishdatetime), len(subheading), len(paragraph), len(writtenby)) 
    story_dict = {'Published Date': publishdatetime, 'Story Name':subheading, 'Story':paragraph, 'Author':writtenby}
    df = pd.DataFrame(story_dict)
    df['publishdatetime'] = pd.to_datetime(df.publishdatetime)
    df['publishdate'] = df['publishdatetime'].dt.strftime['%m%d%y']
    df.to_csv('tinystories.csv')

