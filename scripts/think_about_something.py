
#!/usr/bin/python3

import os,subprocess,time,argparse,pickle
import json, random
import ssl, urllib.request,http.client   
from datetime import datetime
from PIL import Image

from sqlalchemy import create_engine, ForeignKey,select
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship, backref,Session
from sqlalchemy.ext.declarative import declarative_base

from wombo import *
from balaboba_helper import *
from thinks_model import *
from ai_news import *
from text2textGPT2_hufa import *

DEBUG=False



Config={}
Config_hufa={}

identify_key = "AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw"

style = "r"
prompt_en = "r"
task_id = None


parser = argparse.ArgumentParser(
                    prog = 'wombo create',
                    description = 'get image from wombo',
                    epilog = 'Enjoy.')
parser.add_argument('-k','--key')
parser.add_argument('-u','--update',action='store_true')          
parser.add_argument('-n','--news',action='store_true')
# parser.add_argument('-i','--iterations',action='store_true')
# parser.add_argument('-o','--one',action='store_true')
# parser.add_argument('-c','--crop',action='store_true')
# parser.add_argument('-d','--download',action='store_true')          
# parser.add_argument('-r','--rename',action='store_true')
# parser.add_argument('-b','--blacklist',action='store_true')
# parser.add_argument('-s', '--style')      
# parser.add_argument('-t', '--translate',action='store_true')
# parser.add_argument('-p', '--prompt')      
args = parser.parse_args()


out_dir = '../new/'

def get_random_think(engine):
    rand_think_query=select(Think).order_by(func.random())
    with Session(engine) as session:   
        rand_think=session.execute(rand_think_query).first()
        return rand_think

if __name__ == '__main__':
    # exit(0)
    __dir=os.path.dirname(os.path.realpath(__file__))         
    with open(os.path.join(os.path.dirname(__file__),'config_think.json')) as json_file:
        Config = json.load(json_file)
    with open(os.path.join(os.path.dirname(__file__),'config_hufa.json')) as json_file:
        Config_hufa = json.load(json_file)
    sqlite_filepath = os.path.join(__dir,"thinks_map.db")

    if args.update:
        update_styles("styles.txt")
        print("done")
        exit(0)


    engine = create_engine('sqlite:///'+sqlite_filepath, echo=True)
    Base.metadata.create_all(engine)    

    numberList = ['mutate','new']
    choice=random.choices(numberList, weights=(60, 40), k=1)[0]
    
    # choice='mutate'

    print(choice)
    
    prompt = generate_prompt(__dir+"/words1.txt",__dir+"/words2.txt")    
    base_id= None
    if choice=='mutate':
        rand_think=get_random_think(engine)
        prompt = rand_think[0].base_text+' '+rand_think[0].balaboba_text
        base_id = rand_think[0].id


    if args.news:
        news_prompt = get_prompt_from_news("https://news.1777.ru/rss/yandex")
        if news_prompt is not None:
            prompt= news_prompt
    # prompt_balaboba = sync_balaboba_urlib(prompt,11)
    # prompt_en=translate(prompt, 'en')
    prompt_balaboba = {'query':prompt,'text':prompt}
    if not args.news:
        # prompt_balaboba['text']=translate(gpt2_text2text(translate(prompt, 'en'),Config_hufa['API_TOKEN']),'ru')
        prompt_balaboba = sync_balaboba_urlib(prompt,11)
        # prompt_balaboba = sync_balaboba_old(prompt,11,Config['balaboba_cookie'])
    if prompt_balaboba['text'].find('www')>=0:
        print("[bad balaboba]")
        exit(0)
    print(prompt_balaboba['query'])
    print(prompt_balaboba['text'])
    # prompt_balaboba = sync_balaboba(prompt,27)
    with open('balaboba.dump', 'wb') as f:
        pickle.dump(prompt_balaboba, f)

    tmp_think_id=-1
    if not args.news:
        tmp_think = Think(prompt_balaboba['query'],prompt_balaboba['text'],base_id=base_id)                    
        with Session(engine) as session:        
            session.add(tmp_think)        
            res=session.commit()
            tmp_think_id = tmp_think.id
    
    # ##PICKLE
    # prompt_balaboba = {}
    # with open('balaboba.dump', 'rb') as f:
    #     prompt_balaboba = pickle.load(f)    
    prompt_ru = prompt_balaboba['query']+prompt_balaboba['text']
    if prompt_ru=='':
        print("empty balaboba")
        exit(1)

    if args.news:
        prompt_ru=prompt_balaboba['query']

    if choice=='mutate':
        prompt_ru=prompt_balaboba['text']
    
    
    prompt_ru = prompt_ru.replace('\n','')
    prompt_ru = prompt_ru.replace('+','')
    prompt_en=translate(prompt_ru, 'en')
    prompt_en = escape_prompt(prompt_en)


    if prompt_en!='':
        result = subprocess.run(["python3",f"{__dir}/abc_ttm_hufa_api.py", prompt_en],cwd=__dir)

    style = get_random_style(__dir+"/styles.txt",__dir+"/styles_blist.txt")
    res = identify(identify_key=identify_key)
    img_uri = create(res["id_token"], prompt_en, style,None,False,full=True)
    # img_uri='https://images.wombo.art/exports/f4fca3bc-f2d3-4ae9-95ba-da203ab6661b/blank_tradingcard.jpg?Expires=1680405084&Signature=FbSsHfOE~wdpaAtmTAJpcGjZqpUxXchfQ3vemmwKQH1d~NUOYcwgML8WLHtxSFxTLgZx37XDbfcDIdS29jIyMg7mzEuI2y94GQwVgzgUJce2YIZLLRhZ-hWKC8Gp3JyxL01h5jA6jYDRLuDGzMI-5bixsJwiR7Tpx6o3Ijc2yp-QLNXkGGjIk18~1YZZ0by8yWC6sve0IQ5eeyFHOVmQVS1n2FawqO5-2pqRYRVBzPw89yOw-96hJz57c5H90l~hPR-JD4LgUgrGb2C5k4p~5oH6vnw9AFI59VjfBPr1wrcI46wUlALRrsP-zFCINEQHfzAxx9KuENLacgXU8F~Qjw__&Key-Pair-Id=K1ZXCNMC55M2IL'    
    ssl._create_default_https_context = ssl._create_unverified_context                 
    dt_string = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    res_f_name = os.path.join(__dir,out_dir)
    res_f_name = os.path.join(res_f_name,f'{dt_string}.jpg')
    urllib.request.urlretrieve(img_uri, res_f_name)
    print("download img done")       
    im = Image.open(res_f_name)
    width, height = im.size
    left = 62
    top = 215
    right = width-62
    bottom = height-154
    im = im.crop((left, top, right, bottom))        
             
    # with open(res_f_name+'.txt', 'w') as f:
    #     f.writelines(prompt_en)

    im.save(res_f_name)
    print("crop done")

    img_info={"db_id":tmp_think_id,"prompt":prompt_ru,"prompt_en":prompt_en,"prompt_query":prompt_balaboba['query'],"prompt_text":prompt_balaboba['text']}
    with open(res_f_name+'.json', 'w') as f:
        f.write(json.dumps(img_info,indent=4,ensure_ascii=False))

    result = subprocess.run(["python3.9",f"{__dir}/make_galery.py"],cwd=__dir)
    a=1
    