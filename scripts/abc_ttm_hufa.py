import http.client
import json,time,os,sys

def init_load_model():
    conn = http.client.HTTPSConnection("api-inference.huggingface.co")
    payload = ''
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://huggingface.co',
    'Referer': 'https://huggingface.co/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }
    conn.request("GET", "/status/sander-wood/text-to-music", payload, headers)
    res = conn.getresponse()
    data = res.read()
    cookie_AWSALB = ''
    cookie_AWSALBCORS = ''
    for val in res.headers.values():
        if val.find('AWSALB')>=0:
            cookie_AWSALB = val
        if val.find('AWSALBCORS')>=0:
            cookie_AWSALBCORS = val
        a=1
    cookies = cookie_AWSALB+'; '+cookie_AWSALBCORS
    print(res.headers)
    return cookies


def gen_abc(cookies,inputs="ambient music",max_req=3):
    for i in range(max_req+1):
        conn = http.client.HTTPSConnection("api-inference.huggingface.co")
        payload = json.dumps({
        "inputs": inputs,
        "parameters": {
            "top_p": 0.9,
            "max_length": 1024,
            # "num_tunes":2,
            "do_sample": True
        }
        })
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        #   'Cookie': '_ga=GA1.2.702113307.1670589458; __stripe_mid=0d7fc89b-6244-4d48-8b9e-fdb0f1d2071dd984f2; intercom-id-hgve3glw=f7230dd0-355f-444a-86dd-53d08de89885; intercom-device-id-hgve3glw=4f27d8e9-0cff-4dff-8a00-92be34ff641b; _gid=GA1.2.951852636.1674127188; __stripe_sid=7a9d3f34-1bd4-4f96-8ef4-7f9af6e47ca42aac94; AWSALB=GbM9agCOV1l2i+0A3TqyL59OfDOizHEe6z/XboCUaMdx+Gf3RnpdhEI92FHbNcspW02PgkPttR83REHBMmZqNsh1ZD8bJrVCrhVIfykl3GyqTh4yB/ENtdHzDoH/; AWSALBCORS=GbM9agCOV1l2i+0A3TqyL59OfDOizHEe6z/XboCUaMdx+Gf3RnpdhEI92FHbNcspW02PgkPttR83REHBMmZqNsh1ZD8bJrVCrhVIfykl3GyqTh4yB/ENtdHzDoH/; intercom-session-hgve3glw=',
        'Cookie':cookies,
        'Origin': 'https://huggingface.co',
        'Referer': 'https://huggingface.co/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-use-cache': 'false'
        }
        conn.request("POST", "/models/sander-wood/text-to-music", payload, headers)
        res = conn.getresponse()
        if res.status==503:
            print(res)
            sleep(2)
            continue
        data = res.read()
        data=json.loads(data)[0]
        abc = data['generated_text'].replace('\\n','\n').replace('L1','L:1')
        return abc

cookies = init_load_model()
full_abc=""
if len(sys.argv)<2:
    print("enter text")
    exit(1)
inputs=sys.argv[1]
for i in range(1,3):
    abc=gen_abc(cookies,inputs=inputs,max_req=3)
    full_abc+=f"\nX:{i}\n"+abc
    print(abc)

__dir=os.path.dirname(os.path.realpath(__file__)) 
timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())     
with open(__dir+'/../output_tunes/'+timestamp+'.abc', 'w') as f:
    f.write(full_abc)
