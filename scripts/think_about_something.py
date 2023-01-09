
#!/usr/bin/python3

import http.client
import json
import time
import argparse
import random
import os
import pickle
import ssl
import urllib.request    
from datetime import datetime
from PIL import Image

import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship, backref,Session
from sqlalchemy.ext.declarative import declarative_base

from wombo import *
from thinks_model import *

DEBUG=False





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
parser.add_argument('-i','--iterations',action='store_true')
parser.add_argument('-o','--one',action='store_true')
parser.add_argument('-c','--crop',action='store_true')
parser.add_argument('-d','--download',action='store_true')          
parser.add_argument('-r','--rename',action='store_true')
parser.add_argument('-b','--blacklist',action='store_true')
parser.add_argument('-s', '--style')      
parser.add_argument('-t', '--translate',action='store_true')
parser.add_argument('-p', '--prompt')      
args = parser.parse_args()


out_dir = '../new/'

if __name__ == '__main__':
    
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    sqlite_filepath = os.path.join(__dir,"thinks.db")

    if args.update:
        update_styles("styles.txt")
        print("done")
        exit(0)

    prompt = generate_prompt(__dir+"/words1.txt",__dir+"/words2.txt")
    prompt_balaboba = sync_balaboba_old(prompt,11)
    print(prompt_balaboba['query'])
    print(prompt_balaboba['text'])
    # prompt_balaboba = sync_balaboba(prompt,27)
    with open('balaboba.dump', 'wb') as f:
        pickle.dump(prompt_balaboba, f)

    engine = create_engine('sqlite:///'+sqlite_filepath, echo=True)
    Base.metadata.create_all(engine)    
    tmp_think = Think(prompt_balaboba['query'],prompt_balaboba['text'])    
    with Session(engine) as session:
        session.add(tmp_think)        
        session.commit()
    
    # ##PICKLE
    # prompt_balaboba = {}
    # with open('balaboba.dump', 'rb') as f:
    #     prompt_balaboba = pickle.load(f)    
    prompt_ru = prompt_balaboba['query']+prompt_balaboba['text']
    prompt_ru = prompt_ru.replace('\n','')
    prompt_ru = prompt_ru.replace('+','')
    prompt_en=translate(prompt_ru, 'en')
    prompt_en = escape_prompt(prompt_en)
    style = get_random_style(__dir+"/styles.txt",__dir+"/styles_blist.txt")
    res = identify(identify_key=identify_key)
    img_uri = create(res["id_token"], prompt_en, style,None,False,full=True)
    # img_uri='https://images.wombo.art/exports/f4fca3bc-f2d3-4ae9-95ba-da203ab6661b/blank_tradingcard.jpg?Expires=1680405084&Signature=FbSsHfOE~wdpaAtmTAJpcGjZqpUxXchfQ3vemmwKQH1d~NUOYcwgML8WLHtxSFxTLgZx37XDbfcDIdS29jIyMg7mzEuI2y94GQwVgzgUJce2YIZLLRhZ-hWKC8Gp3JyxL01h5jA6jYDRLuDGzMI-5bixsJwiR7Tpx6o3Ijc2yp-QLNXkGGjIk18~1YZZ0by8yWC6sve0IQ5eeyFHOVmQVS1n2FawqO5-2pqRYRVBzPw89yOw-96hJz57c5H90l~hPR-JD4LgUgrGb2C5k4p~5oH6vnw9AFI59VjfBPr1wrcI46wUlALRrsP-zFCINEQHfzAxx9KuENLacgXU8F~Qjw__&Key-Pair-Id=K1ZXCNMC55M2IL'    
    ssl._create_default_https_context = ssl._create_unverified_context    
    now = datetime.now()               
    dt_string = now.strftime("%Y-%m-%d_%H_%M_%S")
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
             
    with open(res_f_name+'.txt', 'w') as f:
        f.writelines(prompt_en)
    im.save(res_f_name)
    print("crop done")
    a=1
    