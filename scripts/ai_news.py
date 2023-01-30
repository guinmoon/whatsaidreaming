import feedparser,os,pickle
from datetime import datetime

__dir=os.path.dirname(os.path.realpath(__file__))  

def get_prompt_from_news(feed_url):    
    NewsFeed = feedparser.parse(feed_url)
    news_date_fname=__dir+'/latest_news_date.dump'
    if os.path.exists(news_date_fname):
        with open(news_date_fname,'rb') as f:
            latest_date=pickle.load(f)
            # if(NewsFeed.entries[0].published_parsed<=latest_date):
            #     return None
            
    with open(news_date_fname,'wb') as f:
        pickle.dump(NewsFeed.entries[0].published_parsed, f)        
    return NewsFeed.entries[0].title


if __name__=='__main__':
    NewsFeed = feedparser.parse("https://news.1777.ru/rss/yandex")
    for entry in  NewsFeed.entries:
        print(entry.title)
        print(entry.published)