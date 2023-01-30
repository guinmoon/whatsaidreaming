from datetime import datetime
import time
import threading
import random
import json
import os
import glob
import subprocess

target_dir =""
arch_dir = ""
__dir=os.path.dirname(__file__)

Config=None



def sort_by_str_date(val):
    return val['created']

def move_to_arch(track):    
    result = subprocess.call(["mv",track,arch_dir],cwd=__dir)

def run(outf,verbose=False):        
    tracks=glob.glob(target_dir+"/*.mp3")
    playlist={}
    playlist["tracks"]=[]
    for track in tracks:
        track_base_name=os.path.basename(track)
        c_date=datetime.fromtimestamp(os.path.getmtime(track))
        diff_dates = (datetime.today() - c_date)
        diff_dates_hours = (diff_dates.days*24 * 60 * 60+diff_dates.seconds)/3600
        if diff_dates_hours>=24.0:
            move_to_arch(track)
            continue
        tmp_track_info = {"f_name":track_base_name,"prompt":track_base_name,"created":str(c_date)}
        if os.path.exists(track+".txt"):
            with open(track+".txt","r") as f:
                tmp_prompt = f.read()
                if tmp_prompt!="":
                    tmp_track_info["prompt"]= tmp_prompt


        playlist["tracks"].append(tmp_track_info)
    playlist["tracks"].sort(key=sort_by_str_date,reverse=True)
    playlist_json = json.dumps(playlist,indent=4)
    with open(os.path.join(target_dir,outf),'w') as f:
        f.write(playlist_json)
    if verbose:
        print(playlist_json)


if __name__ == '__main__':
    config_path = os.path.join(__dir,'config_playlist.json')
    with open(config_path) as json_file:
        Config = json.load(json_file)
    target_dir = Config['target_dir']
    arch_dir = Config['arch_dir']


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
    
    run(target_dir+"/today.json",verbose=True)