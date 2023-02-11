# aaa
import http.client
import json
import time
import argparse
import random
import os
import pickle
import ssl


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
        display_freq = 0.5
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
        print(latest_task["state"])
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


def update_styles(styles_fname=None):
    conn = http.client.HTTPSConnection("paint.api.wombo.ai",context = _unverified_context)    
    conn.request("GET", f"/api/styles")
    data=conn.getresponse().read()        
    styles = json.loads(data)
    if styles_fname is None:
        print(json.dumps(styles,indent=4))
        return
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


def escape_prompt(in_prompt):
    prompt = in_prompt.replace("'","")
    prompt = prompt.replace("\n","")
    prompt = prompt.replace(":","")
    prompt = prompt.replace("  "," ")
    prompt = prompt.replace("\\","")
    return prompt