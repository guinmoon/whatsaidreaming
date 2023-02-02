######################## INPUT TEXT ########################

# This is a traditional Irish dance music.
# Note Length-1/8
# Meter-6/8
# Key-D


import requests
import json,time,os,sys
import http.client
import subprocess
from fix_abc import fix_abc

Config=None



def gen_abc(inputs):
    conn = http.client.HTTPSConnection("api-inference.huggingface.co")
    payload = json.dumps({
    "inputs": inputs+"\nNote Length-1/2",
    "parameters": {
        "top_p": 0.9,
        "max_length": 1024,
        # "num_tunes":2,
        "do_sample": True
    },
    "options":{
        "wait_for_model": True,
        "use_cache": False,
    }
    })
    headers = {"Authorization": f"Bearer {Config['API_TOKEN']}"}
    conn.request("POST", "/models/sander-wood/text-to-music", payload, headers)
    res = conn.getresponse()
    # output=output[0]
    data = res.read()
    output=json.loads(data)[0]
    abc = output['generated_text'].replace('\\n','\n')
    abc=fix_abc(abc)
    return abc

if __name__ == '__main__':
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    config_path = os.path.join(os.path.dirname(__file__),'config_hufa.json')
    with open(config_path) as json_file:
        Config = json.load(json_file)
    # if len(sys.argv)<2:
    #     print("enter text")
    #     exit(1)
    inputs=sys.argv[1]
    # inputs="To live is not to grieve, not to condemn anyone, not to annoy anyone, and all my respect."    
    full_abc=f"% {inputs}\n"
    for i in range(1,3):
        abc=gen_abc(inputs=inputs)
        full_abc+=f"\nX:{i}\n"+abc
        print(abc)

    __dir=os.path.dirname(os.path.realpath(__file__)) 
    timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())  
    abc_fname=__dir+'/../output_tunes/'+timestamp
    with open(abc_fname+'.abc', 'w') as f:
        f.write(full_abc)

    # abc_fname='/home/m_vs_m/whatsaidreaming/scripts/../output_tunes/2023-01-26_15_43_03'
    result = subprocess.call([f"{__dir}/mp3_from_abc.sh", abc_fname,inputs],cwd=__dir)
    
