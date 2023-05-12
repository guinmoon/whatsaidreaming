######################## INPUT TEXT ########################

# This is a traditional Irish dance music.
# Note Length-1/8
# Meter-6/8
# Key-D
import os

import requests
import json,time,sys
import http.client
import subprocess
try:
    from fix_abc import fix_abc
except Exception as eee:
    from scripts.fix_abc import fix_abc
import random

Config={}
Config_synth={}



def gen_abc(inputs,api_token,use_cache=False):
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
    headers = {"Authorization": f"Bearer {api_token}"}
    conn.request("POST", "/models/sander-wood/text-to-music", payload, headers)
    res = conn.getresponse()
    # output=output[0]
    data = res.read()
    output=json.loads(data)[0]
    abc = output['generated_text'].replace('\\n','\n')
    abc=fix_abc(abc)
    return abc

def gen_music(inputs,music_options="Note Length-1/2",track_count=3,user_id=-1,synth=True):
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

    inputs=inputs.lower()
    if inputs.find("verse")>=0:
        splited_by_verse=inputs.lstrip().split("verse")
        inputs = splited_by_verse[1]
        inputs=inputs[inputs.find("\n"):]
        inputs=inputs.strip()
        if inputs.find("chorus")>=0:
            inputs=inputs.split("chorus")[0]
        # inputs=inputs.split("\n")[0]+" "+inputs.split("\n")[1]

        a=1
    inputs = inputs.split("\n")[0] #temporary
    inputs = inputs.replace("\n"," ")
    inputs = inputs.replace("'","")
    inputs = inputs.replace(",","")
    print(f"gen by: {inputs}")
    full_abc=""
    if synth:
        full_abc=f"% {inputs}\n"
    options="\n"+music_options
    for i in range(1,track_count+1):
        # if i==3:
        #     abc=gen_abc(inputs=inputs,use_cache=True)
        # else:
        abc=gen_abc(inputs=inputs+options,api_token=Config['API_TOKEN'])
        full_abc+=f"\nX:{i}\n"+abc
        print(abc)

    __dir=os.path.dirname(os.path.realpath(__file__)) 
    timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())  
    abc_fname=__dir+'/../output_tunes/'+timestamp
    
    if user_id==-1:
        full_abc =  full_abc.replace('L:1/4','L:1/2')
        full_abc =  full_abc.replace('L:1/8','L:1/2')
        full_abc =  full_abc.replace('M:4/4','M:2/2')
        full_abc =  full_abc.replace('M:3/4','M:2/2')

    with open(abc_fname+'.abc', 'w') as f:
        f.write(full_abc)

    # abc_fname='/home/m_vs_m/whatsaidreaming/scripts/../output_tunes/2023-01-26_15_43_03'
    if not synth:
        return full_abc
    if user_id!=-1:
        result = subprocess.call([f"{__dir}/mp3_from_abc_users.sh", abc_fname,user_id,inputs],cwd=__dir)
        return full_abc
    else:
        result = subprocess.call([f"{__dir}/mp3_from_abc.sh", abc_fname,inputs],cwd=__dir)
        return result
    
def renum_tunes(full_abc):
    res_abc=""
    tunes_count=0
    for line in full_abc.strip().split("\n"):
        f_ind=line.find("X:")
        if f_ind>=0:
            tunes_count+=1
            line = f"X:{tunes_count}"
        res_abc+=line+"\n"
    return (tunes_count,res_abc)
    

def synth_from_abc(full_abc,user_id=-1,synth_options=""):
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    abc_fname = f"{__dir}/../synth/tmp/{user_id}"
    # abc_fname= f"{__dir}/../synth/tmp/1679640467456"
    progs = synth_options.split(",")
    progs=[p.strip() for p in progs]
    full_abc=renum_tunes(full_abc)
    with open(abc_fname+'.abc', 'w') as f:
        f.write(full_abc[1])
    with open(abc_fname+'.prog.txt', 'w') as f:
        ind=0
        for prog in progs:
            f.write(f"prog {ind} {prog}\n")
            ind+=1
    result = subprocess.call(["pkill", "lame"],cwd=__dir)
    print(f"({result}) pkill lame")
    result = subprocess.call(["abc2midi", f"{abc_fname}.abc"],cwd=f"{__dir}/../synth/tmp/")
    print(f"({result}) abc2midi {abc_fname}.abc ")
    midisox_py_args=["python3", "../../miditools/midisox_py","-M"]
    for ind in range(1,full_abc[0]+1):
        midisox_py_args.append(f"{abc_fname}{ind}.mid")
    midisox_py_args.append(f"{abc_fname}full.mid")
    result = subprocess.call(midisox_py_args,cwd=f"{__dir}/../synth/tmp/")
    # result = subprocess.call(["python3", "../../miditools/midisox_py","-M",abc_fname+"1.mid",abc_fname+"2.mid",abc_fname+"full.mid"],cwd=f"{__dir}/../synth/tmp/")
    # fluidsynth_cmd = f"fluidsynth -l -T raw --audio-file-endian little --audio-file-format=s16 --sample-rate 44100 -F - {__dir}/../synth/guinmoon.sf2 {abc_fname}full.mid -f {abc_fname}.prog.txt -g 0.5 | lame -f -b 128 -r - {abc_fname}.mp3"
    fluidsynth_cmd = f"fluidsynth -l -T raw -F - {__dir}/../synth/guinmoon.sf2 {abc_fname}full.mid -f {abc_fname}.prog.txt -g 0.5 | ffmpeg -y -f s32le -i - -b:a 128k {abc_fname}.mp3"
    print(f"{fluidsynth_cmd}")
    fluidsynth_ps = subprocess.Popen(fluidsynth_cmd,shell=True,cwd=f"{__dir}/../synth/tmp/")
    fluidsynth_ps.wait()
    return f"synth/tmp/{user_id}.mp3"

if __name__ == '__main__':    
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    
    
    if len(sys.argv)>2:
        track_count=int(sys.argv[2])
    if len(sys.argv)>1:
        inputs=sys.argv[1]
    else:
        inputs="""
        Verse 1:
I couldn't just sit and wait,
I needed to create,
Something new, something great,
I couldn't let my dreams just wait.

Chorus:
Doing something new, something different,
Pushing my boundaries, my limits,
This is the key to creativity,
To do something that has never been.

Verse 2:
I picked up the brush and paint,
Started to create without restraint,
Colors and shapes in my mind,
Now on the canvas they combine.

Chorus:
Doing something new, something different,
Pushing my boundaries, my limits,
This is the key to creativity,
To do something that has never been.

Verse 3:
The satisfaction that I feel,
As my creation becomes real,
I now understand the appeal,
Of doing new things, it's the real deal.

Chorus:
Doing something new, something different,
Pushing my boundaries, my limits,
This is the key to creativity,
To do something that has never been.

Bridge:
Let go of your worries,
Try something new that's not been done,
Now's the time, don't you worry,
Your creativity has just begun.

Chorus:
Doing something new, something different,
Pushing my boundaries, my limits,
This is the key to creativity,
To do something that has never been.
        """    
    user_id=-1
    track_count=3
    if len(sys.argv)>4:
        track_count=1
        user_id=sys.argv[4]
    gen_music(inputs,track_count=track_count,user_id=user_id)