import feedparser,os,pickle,json
from datetime import datetime
import shutil
import subprocess
import glob

from ya_tts_paid import *
from balaboba_helper import *
from chatGPT_helper import *

__dir=os.path.dirname(os.path.realpath(__file__))  


def get_prompt_from_news(feed_url,only_check=False):    
    NewsFeed = feedparser.parse(feed_url)
    news_date_fname=__dir+'/latest_news_date.dump'
    if os.path.exists(news_date_fname):
        with open(news_date_fname,'rb') as f:
            latest_date=pickle.load(f)
            if(NewsFeed.entries[0].published_parsed<=latest_date):
                return None
    if not only_check:        
        with open(news_date_fname,'wb') as f:
            pickle.dump(NewsFeed.entries[0].published_parsed, f)        
    return NewsFeed.entries[0].title


def synth_news_entire(etire):
    a=1

def synt_news(feed_url,max_news_count=10,source_every_x=3):    
    ya_conf=None
    think_conf= None
    with open(os.path.join(os.path.dirname(__file__),'ya_cloud_conf.json')) as json_file:
        ya_conf = json.load(json_file)
    with open(os.path.join(os.path.dirname(__file__),'config_think.json')) as json_file:
        think_conf = json.load(json_file)
    NewsFeed = feedparser.parse(feed_url)
    source_tts="Источник: 1777.ru"
    source_tts_file=os.path.join(__dir,'../sounds/source1777.mp3')
    news_dir=os.path.join(__dir,'../news_parts')
    arch_news(news_dir,os.path.join(__dir,'../news_arch'))
    news_count=0
    iamToken = ya_conf['token']
    iamToken = get_new_iam_token(ya_conf['oToken'])['iamToken']
    for entry in  NewsFeed.entries:        
        print(entry.title)
        print(entry.published)        
        timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", entry.published_parsed)  
        if not os.path.exists(f'{news_dir}/{timestamp}_a.mp3'):
            tts_to_lpcm(entry.title,f'{news_dir}/tmp_a.pcm',ya_conf['folder_id'],iamToken)
            result = subprocess.call(["lame",f'{news_dir}/tmp_a.pcm','-s','24', '--tt', f"{entry.title}", '-b', '256', '-r',f'{news_dir}/{timestamp}_a.mp3',],cwd=news_dir)
        if not os.path.exists(f'{news_dir}/{timestamp}_b.mp3'):
            tts_to_lpcm(entry.summary,f'{news_dir}/tmp_b.pcm',ya_conf['folder_id'],iamToken,voice='ermil')
            result = subprocess.call(["lame",f'{news_dir}/tmp_b.pcm','-s','24', '--tt', f"{entry.summary}", '-b', '256', '-r',f'{news_dir}/{timestamp}_b.mp3',],cwd=news_dir)
        if not os.path.exists(f'{news_dir}/{timestamp}_c.mp3'):
            if news_count%source_every_x==0:
                shutil.copy(source_tts_file,f'{news_dir}/{timestamp}_c.mp3')
        if not os.path.exists(f'{news_dir}/{timestamp}_d.mp3'):
            chatGPTThink=davincii003_query(entry.title)
            chatGPTThink = "Думаю что "+chatGPTThink
            print(chatGPTThink)
            tts_to_lpcm(chatGPTThink,f'{news_dir}/tmp_d.pcm',ya_conf['folder_id'],iamToken,voice='filipp')
            result = subprocess.call(["lame",f'{news_dir}/tmp_d.pcm','-s','24', '--tt', f"{entry.summary}", '-b', '256', '-r',f'{news_dir}/{timestamp}_d.mp3',],cwd=news_dir)
            
        # tts_to_mp3(source_tts,f'{news_dir}/{timestamp}_с.mp3',ya_conf['folder_id'],ya_conf['token'])
        # prompt_balaboba = sync_balaboba_old(entry.title,6,think_conf['balaboba_cookie'])
        # if prompt_balaboba['text']!='' and prompt_balaboba['text']!=entry.title:
        #     tts_to_mp3(prompt_balaboba['text'],f'{news_dir}/{timestamp}_b.mp3',ya_conf['folder_id'],ya_conf['token'],voice='ermil')
        news_count+=1
        if news_count>max_news_count:
            break
    shutil.copy(source_tts_file,f'{news_dir}/{timestamp}_c.mp3')
    if os.path.exists(f'{news_dir}/tmp_a.pcm'):
        os.remove(f'{news_dir}/tmp_a.pcm')
    if os.path.exists(f'{news_dir}/tmp_b.pcm'):
        os.remove(f'{news_dir}/tmp_b.pcm')
    if os.path.exists(f'{news_dir}/tmp_d.pcm'):
        os.remove(f'{news_dir}/tmp_d.pcm')

def concat_news(news_dir):
    a=1

def arch_news(news_dir,arch_dir):
    tracks=glob.glob(news_dir+"/*.mp3")
    # playlist={}
    # playlist["tracks"]=[]
    for track in tracks:
        c_date=datetime.fromtimestamp(os.path.getmtime(track))
        diff_dates = (datetime.today() - c_date)
        diff_dates_hours = (diff_dates.days*24 * 60 * 60+diff_dates.seconds)/3600
        if diff_dates_hours>=3.0:
            result = subprocess.call(["mv",track,arch_dir],cwd=__dir)
        # track_base_name=os.path.basename(track)
        # c_date=datetime.fromtimestamp(os.path.getmtime(track))
        # diff_dates = (datetime.today() - c_date)
        # diff_dates_hours = (diff_dates.days*24 * 60 * 60+diff_dates.seconds)/3600
        # if diff_dates_hours>=24.0:
        #     move_to_arch(track)
        #     continue

if __name__=='__main__':
    synt_news("https://news.1777.ru/rss/yandex")
    