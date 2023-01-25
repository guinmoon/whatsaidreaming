import requests
import json,time,os,sys

Config=None

def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/sander-wood/text-to-music"    
    headers = {"Authorization": f"Bearer {Config['API_TOKEN']}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def gen_abc(inputs):
    output = query({
        "inputs": inputs,
        "parameters": {
                "top_p": 0.9,
                "max_length": 1024,
                # "num_tunes":2,
                "do_sample": True
        }
    })
    output=output[0]
    abc = output['generated_text'].replace('\\n','\n').replace('L1','L:1')
    return abc

if __name__ == '__main__':
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    config_path = os.path.join(os.path.dirname(__file__),'config_hufa.json')
    with open(config_path) as json_file:
        Config = json.load(json_file)
    full_abc=""
    if len(sys.argv)<2:
        print("enter text")
        exit(1)
    inputs=sys.argv[1]
    for i in range(1,3):
        abc=gen_abc(inputs=inputs)
        full_abc+=f"\nX:{i}\n"+abc
        print(abc)

    __dir=os.path.dirname(os.path.realpath(__file__)) 
    # timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())     
    # with open(__dir+'/../output_tunes/'+timestamp+'.abc', 'w') as f:
    #     f.write(full_abc)