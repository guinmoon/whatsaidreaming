# aaa
import http.client
import json
import time
import argparse
import random
import os
import pickle
import ssl
import asyncio
import sys

from aiobalaboba import Balaboba

_unverified_context = ssl._create_unverified_context()

def identify(identify_key):    
    conn = http.client.HTTPSConnection("identitytoolkit.googleapis.com",context = _unverified_context)    
    payload = json.dumps(
        {"key": identify_key}
    )
    headers = {}
    conn.request("POST", f"/v1/accounts:signUp?key={identify_key}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data=json.loads(data)
    id_token = data["idToken"]
    local_id = ""
    return {"id_token": id_token, "local_id": local_id}



def create(id_token: str, prompt: str, style: int, ID=None,one=False, full=False):    
    conn = http.client.HTTPSConnection("paint.api.wombo.ai",context = _unverified_context)    
    headers={
            "Authorization": "bearer " + id_token,
            "Origin": "https://paint.api.wombo.ai/",
            "Referer": "https://paint.api.wombo.ai/",
            "User-Agent": "Mozilla/5.0",
        }
    
    body = '{"input_spec":{"prompt":"' + prompt + '","style":' + str(style)+ ',"display_freq":10}}'        

    id=ID
    display_freq = 1
    if ID is None:        
        conn.request("POST", f"/api/tasks", '{"premium": false}', headers)
        data=conn.getresponse().read()        
        id=json.loads(data)["id"]
        conn.request("PUT", f"/api/tasks/{id}", body, headers)
        data=conn.getresponse().read()        
        r=json.loads(data)                     
        print(f"Status: {r['state']}")
        display_freq = r["input_spec"]["display_freq"] / 10
        with open('headers.dump', 'wb') as f:
            pickle.dump(headers, f)
        with open('id.dump', 'w') as f:
            f.write(id)
        with open('prompt.dump', 'w') as f:
            f.write(prompt)
        print(prompt)
        if not full:
            exit(0)        
    else:
        with open('headers.dump', 'rb') as f:
            headers = pickle.load(f)
        with open('id.dump', 'r') as f:
            id = f.readline()
   
    conn.request("GET", f"/api/tasks/{id}", body, headers)
    data=conn.getresponse().read()        
    latest_task=json.loads(data)     
    if latest_task["state"] != "completed" and one:
            print("pending")
            exit(0)
    while latest_task["state"] != "completed":
        time.sleep(display_freq)
        conn.request("GET", f"/api/tasks/{id}", body, headers)
        data=conn.getresponse().read()        
        latest_task=json.loads(data)         

    
    conn.request("POST", f"/api/tradingcard/{id}", body, headers)
    data=conn.getresponse().read()        
    img_uri=json.loads(data) 
    return img_uri


def get_random_style(styles_fname,styles_blist_fname=None):
    styles = open(styles_fname).read().splitlines()
    style = styles[random.randint(0,len(styles)-1)] 
    if styles_blist_fname is not None:
        styles_blist = open(styles_blist_fname).read().splitlines()        
        while style in styles_blist:
            style = styles[random.randint(0,len(styles)-1)] 
    return style

def generate_prompt(prompttext1,prompttext2):
    prompt1 = open(prompttext1).read().splitlines()
    prompt2 = open(prompttext2).read().splitlines()
    return prompt1[random.randint(0,len(prompt1)-1)]+" "+prompt2[random.randint(0,len(prompt2)-1)]+" "+prompt1[random.randint(0,len(prompt1)-1)]


def update_styles(styles_fname):
    conn = http.client.HTTPSConnection("paint.api.wombo.ai",context = _unverified_context)    
    conn.request("GET", f"/api/styles")
    data=conn.getresponse().read()        
    styles = json.loads(data)
    lines = []
    for style in styles:
        lines.append(str(style["id"]))
    with open(styles_fname, 'w') as f:
        f.write("\n".join(lines))
    return styles

def translate(to_translate, to_language="auto", from_language="auto"):
    import re
    import html    
    from urllib.parse import quote
    agent = {'User-Agent':
         "Mozilla/4.0 (\
        compatible;\
        MSIE 6.0;\
        Windows NT 5.1;\
        SV1;\
        .NET CLR 1.1.4322;\
        .NET CLR 2.0.50727;\
        .NET CLR 3.0.04506.30\
        )"}
    base_link = "/m?tl=%s&sl=%s&q=%s"        
    to_translate = quote(to_translate, safe="")
    link = base_link % (to_language, from_language, to_translate)    
    conn = http.client.HTTPSConnection("translate.google.com",context = _unverified_context)    
    conn.request("GET", link,headers=agent)
    data=conn.getresponse().read().decode("utf-8")    
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = html.unescape(re_result[0])
    return (result)

async def async_balaboba(orig_text,text_type):
    bb = Balaboba()
    # text_types = await bb.get_text_types(language="ru")
    # intros = await bb.get_text_types(language="ru")
    response = await bb.balaboba(orig_text, text_type=text_type)
    # if response.find('http')>=0:
    #     response = orig_text
    # if response=='':
    #     response = orig_text
    return response



def sync_balaboba(orig_text,text_type=32):            
    return asyncio.run(async_balaboba(orig_text,text_type))

def sync_balaboba_urlib(orig_text,text_type=32,cookie=''):            
    import urllib.request
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Origin': 'https://yandex.ru',
    'Referer': 'https://yandex.ru/',
    }
    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": orig_text, "intro": text_type, "filter": 1}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    res = urllib.request.urlopen(req)
    data = res.read()
    data=json.loads(data)
    return data

def sync_balaboba_old(orig_text,text_type=32,cookie=''):            
    conn = http.client.HTTPSConnection("yandex.ru",context = ssl._create_unverified_context())    
    payload = json.dumps({
        "query": orig_text,
        "intro": text_type,
        "filter": 1
    })
    headers = {
        'authority': 'yandex.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6',
        'content-type': 'application/json',   
        'cookie': cookie,     
        'origin': 'https://yandex.ru',        
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }    
    conn.request("POST", "/lab/api/yalm/text3", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data=json.loads(data)
    return data

def escape_prompt(in_prompt):
    prompt = in_prompt.replace("'","")
    prompt = prompt.replace("\n","")
    prompt = prompt.replace(":","")
    prompt = prompt.replace("  "," ")
    prompt = prompt.replace("\\","")
    return prompt