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

def sort_by_str_date(val):
    return val['created']

def run(outf,only_today=False,verbose=False,clnup=False):        
    images=glob.glob(target_dir+"/*.jpg")
    galery={}
    galery["images"]=[]
    for image in images:
        img_base_name=os.path.basename(image)
        c_date=datetime.fromtimestamp(os.path.getmtime(image))
        diff_dates = (datetime.today() - c_date)
        diff_dates_hours = (diff_dates.days*24 * 60 * 60+diff_dates.seconds)/3600
        if only_today:
            # if c_date.date() != datetime.today().date():
            if diff_dates_hours>=24.0:
                continue
        tmp_img_info = {"f_name":img_base_name,"prompt":img_base_name,"created":str(c_date)}
        if os.path.exists(image+".txt"):
            with open(image+".txt","r") as f:
                tmp_prompt = f.read()
                if tmp_prompt!="":
                    tmp_img_info["prompt"]= tmp_prompt
                else:
                    continue
        else:
            continue
        galery["images"].append(tmp_img_info)
    if clnup:
        cleanup(galery)
    galery["images"].sort(key=sort_by_str_date,reverse=True)
    gelery_json = json.dumps(galery,indent=4)
    with open(os.path.join(target_dir,outf),'w') as f:
        f.write(gelery_json)
    if verbose:
        print(gelery_json)


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__),'config_galery.json')
    with open(config_path) as json_file:
        Config = json.load(json_file)
    target_dir = Config['target_dir']


    # parser = argparse.ArgumentParser(
    #                     prog = 'wombo create',
    #                     description = 'get image from wombo',
    #                     epilog = 'Enjoy.')
    # parser.add_argument('-k','--key')
    # parser.add_argument('-u','--update',action='store_true')          
    # parser.add_argument('-i','--iterations',action='store_true')
    # parser.add_argument('-o','--one',action='store_true')
    # parser.add_argument('-c','--crop',action='store_true')
    # parser.add_argument('-d','--download',action='store_true')          
    # parser.add_argument('-r','--rename',action='store_true')
    # parser.add_argument('-b','--blacklist',action='store_true')
    # parser.add_argument('-s', '--style')      
    # parser.add_argument('-t', '--translate',action='store_true')
    # parser.add_argument('-p', '--prompt')      
    # args = parser.parse_args()

    # if args.update:
    #     update_styles("styles")

    run(res_json_fname,clnup=True)
    run("today.json",only_today=True,verbose=True)