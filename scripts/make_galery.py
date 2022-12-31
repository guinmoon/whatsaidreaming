from datetime import datetime
import time
import threading
import random
import json
import os
import glob

target_dir =""
res_json_fname="galery.json"
Config=None

def cleanup(galery):
    txts=glob.glob(target_dir+"/*.txt")
    for txt in txts:
        txt_base_name=os.path.basename(txt)
        in_galery=False
        for image in galery["images"]:
            if image["f_name"]+".txt"==txt_base_name:
                in_galery = True
                break
        if not in_galery:
            os.remove(txt)

def run():
    with open('config.json') as json_file:
        Config = json.load(json_file)
    target_dir = Config['target_dir']
    images=glob.glob(target_dir+"/*.jpg")
    galery={}
    galery["images"]=[]
    for image in images:
        img_base_name=os.path.basename(image)
        tmp_img_info = {"f_name":img_base_name,"prompt":img_base_name,"created":str(datetime.fromtimestamp(os.path.getctime(image)))}
        if os.path.exists(image+".txt"):
            with open(image+".txt","r") as f:
                tmp_prompt = f.read()
                tmp_img_info["prompt"]= tmp_prompt
        galery["images"].append(tmp_img_info)
    cleanup(galery)
    gelery_json = json.dumps(galery,indent=4)
    with open(os.path.join(target_dir,res_json_fname),'w') as f:
        f.write(gelery_json)
    print(gelery_json)


if __name__ == '__main__':
    run()