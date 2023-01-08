
#!/usr/bin/python3

import http.client
import json
import time
import argparse
import random
import os
import pickle
import ssl

from wombo import *

DEBUG=False





identify_key = "AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw"

style = "r"
prompt = "r"
task_id = None
res_f_name = __dir=os.path.dirname(os.path.realpath(__file__))+'/res.jpg'

parser = argparse.ArgumentParser(
                    prog = 'wombo create',
                    description = 'get image from wombo',
                    epilog = 'Enjoy.')
parser.add_argument('-k','--key')
parser.add_argument('-u','--update',action='store_true')          
parser.add_argument('-i','--iterations',action='store_true')
parser.add_argument('-o','--one',action='store_true')
parser.add_argument('-c','--crop',action='store_true')
parser.add_argument('-d','--download',action='store_true')          
parser.add_argument('-r','--rename',action='store_true')
parser.add_argument('-b','--blacklist',action='store_true')
parser.add_argument('-s', '--style')      
parser.add_argument('-t', '--translate',action='store_true')
parser.add_argument('-p', '--prompt')      
args = parser.parse_args()




if __name__ == '__main__':
    
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    if args.update:
        update_styles("styles.txt")
        print("done")
        exit(0)

    # prompt = generate_prompt(__dir+"/words1.txt",__dir+"/words2.txt")
    # prompt_balaboba = sync_balaboba(prompt,11)
    # # prompt_balaboba = sync_balaboba(prompt,27)
    # with open('balaboba.dump', 'wb') as f:
    #     pickle.dump(prompt_balaboba, f)

    

    # if args.key is not None:
    #     identify_key =   args.key                        
    # if args.style is not None:    
    #     style = args.style
    # if args.prompt is not None:  
    #     prompt = args.prompt
    # if args.iterations:  
    #     task_id = args.iterations

    # if args.crop:
    #     from PIL import Image
    #     im = Image.open(res_f_name)
    #     width, height = im.size
    #     left = 62
    #     top = 215
    #     right = width-62
    #     bottom = height-154
        
    #     im = im.crop((left, top, right, bottom))
    #     if args.rename:
    #         from datetime import datetime
    #         now = datetime.now()            
    #         dt_string = now.strftime("%Y-%m-%d_%H_%M_%S")
    #         res_f_name = __dir=os.path.dirname(os.path.realpath(__file__))+f'/out/{dt_string}.jpg'
    #         with open('prompt.dump', 'r') as f:
    #             info_prompt = f.readlines()
    #             with open(res_f_name+'.txt', 'w') as f:
    #                 f.writelines(info_prompt)
    #     im.save(res_f_name)
    #     print("crop done")
    #     exit(0)

    

    # if prompt=="r":       
    #     prompt = generate_prompt(__dir+"/words1.txt",__dir+"/words2.txt")
    # if prompt=="b":
    #     prompt = generate_prompt(__dir+"/words1.txt",__dir+"/words2.txt")
    #     prompt=sync_balaboba(prompt,27)

    # if args.translate:    
    #     prompt = prompt.replace('\n','')
    #     prompt = prompt.replace('+','')
    #     prompt=translate(prompt, 'en')

    # if style=="r":        
    #     if args.blacklist:
    #         style = get_random_style(__dir+"/styles.txt",__dir+"/styles_blist.txt")    
    #     else:
    #         style = get_random_style(__dir+"/styles.txt")    


    # prompt = escape_prompt(prompt)

    # if  not args.download:
    #     res = identify(identify_key=identify_key)
    #     img_uri = create(res["id_token"], prompt, style,task_id,args.one)
    #     with open('url.dump', 'w') as f:
    #         f.write(img_uri)    
    #     print("get url done")   
    # else:
    #     with open('url.dump', 'r') as f:
    #         import urllib.request        
    #         img_uri=f.readline()
    #         ssl._create_default_https_context = ssl._create_unverified_context                
    #         urllib.request.urlretrieve(img_uri, res_f_name)
    #     print("download img done")   

    # print(img_uri)

    # python3 wombo_create.py -p b && python3 wombo_create.py -i && python3 wombo_create.py -d && python3 wombo_create.py -c