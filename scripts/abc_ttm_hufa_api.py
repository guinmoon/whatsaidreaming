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
import random

Config={}
Config_synth={}



def gen_abc(inputs,use_cache=False):
    conn = http.client.HTTPSConnection("api-inference.huggingface.co")
    payload = json.dumps({
    "inputs": inputs,
    "parameters": {
        "top_p": 0.9,
        "max_length": 1024,
        # "num_tunes":2,
        "do_sample": True
    },
    "options":{
        "wait_for_model": True,
        "use_cache": use_cache,
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
    with open(os.path.join(__dir,'config_hufa.json')) as json_file:
        Config = json.load(json_file)
    with open(os.path.join(__dir,'../synth/synth_conf.json')) as json_file:
        Config_synth = json.load(json_file)
    with open(os.path.join(__dir,'../synth/cur_prog.txt'),'w') as f:
        prog_0 = Config_synth['prog0'][random.randint(0,len(Config_synth['prog0'])-1)]
        prog_1 = Config_synth['prog1'][random.randint(0,len(Config_synth['prog1'])-1)]
        prog_2 = Config_synth['prog2'][random.randint(0,len(Config_synth['prog2'])-1)]
        f.write(f"prog 0 {prog_0}\nprog 1 {prog_1}\nprog 2 {prog_2} ")

    # if len(sys.argv)<2:
    #     print("enter text")
    #     exit(1)
    if len(sys.argv)>1:
        inputs=sys.argv[1]
    else:
        inputs="To live is not to grieve, not to condemn anyone, not to annoy anyone, and all my respect."    
    full_abc=f"% {inputs}\n"
    for i in range(1,4):
        # if i==3:
        #     abc=gen_abc(inputs=inputs,use_cache=True)
        # else:
        abc=gen_abc(inputs=inputs+"\nNote Length-1/2")
        full_abc+=f"\nX:{i}\n"+abc
        print(abc)

    __dir=os.path.dirname(os.path.realpath(__file__)) 
    timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())  
    abc_fname=__dir+'/../output_tunes/'+timestamp

    full_abc =  full_abc.replace('L:1/4','L:1/2')
    full_abc =  full_abc.replace('L:1/8','L:1/2')
    full_abc =  full_abc.replace('M:4/4','M:2/2')
    full_abc =  full_abc.replace('M:3/4','M:2/2')

    with open(abc_fname+'.abc', 'w') as f:
        f.write(full_abc)

    # abc_fname='/home/m_vs_m/whatsaidreaming/scripts/../output_tunes/2023-01-26_15_43_03'
    result = subprocess.call([f"{__dir}/mp3_from_abc.sh", abc_fname,inputs],cwd=__dir)
    
