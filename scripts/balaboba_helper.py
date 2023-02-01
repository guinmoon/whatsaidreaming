import asyncio
import json
import http.client
import ssl

from aiobalaboba import Balaboba


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
    try:
        conn.request("POST", "/lab/api/yalm/text3", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data=json.loads(data)
        return data
    except Exception as ee:
        print(ee)
        data = {'query':orig_text,'text':orig_text}
        return data