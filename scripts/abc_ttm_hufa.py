import http.client
import json,time,os


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
payload = json.dumps({
  "inputs": "the fish about the method says that it is not necessary to run after the fish.",
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
data = res.read()
data=json.loads(data)[0]
__dir=os.path.dirname(os.path.realpath(__file__)) 
timestamp = time.strftime("%a_%d_%b_%Y_%H_%M_%S", time.localtime()) 
abc = "X:1\n"+data['generated_text'].replace('\\n','\n')
with open(__dir+'/../output_tunes/'+timestamp+'.abc', 'w') as f:
    f.write(abc)
print(abc)