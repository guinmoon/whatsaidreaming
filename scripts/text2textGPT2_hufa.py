######################## INPUT TEXT ########################

# This is a traditional Irish dance music.
# Note Length-1/8
# Meter-6/8
# Key-D


import requests
import json,time,os,sys
import http.client
import subprocess

Config=None



def gpt2_text2text(inputs,API_TOKEN):
    conn = http.client.HTTPSConnection("api-inference.huggingface.co")
    payload = json.dumps({
    "inputs": inputs,
    "parameters": {
        "top_p": 0.9,
        # "num_tunes":2,
        "do_sample": True
    },
    "options":{
        "wait_for_model": True,
        "use_cache": False,
    }
    })
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    conn.request("POST", "/models/gpt2", payload, headers)
    res = conn.getresponse()
    # output=output[0]
    data = res.read()
    output=json.loads(data)[0]
    gen_text = output['generated_text'].replace('\\n','\n')
    return gen_text

if __name__ == '__main__':
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    config_path = os.path.join(os.path.dirname(__file__),'config_hufa.json')
    with open(config_path) as json_file:
        Config = json.load(json_file)
    # if len(sys.argv)<2:
    #     print("enter text")
    #     exit(1)
    # inputs=sys.argv[1]
    inputs = "To live is not to grieve, not to condemn anyone, not to annoy anyone, and all my respect."    
    gen_text = gpt2_text2text(inputs,Config['API_TOKEN'])
    print(gen_text)
    
    
