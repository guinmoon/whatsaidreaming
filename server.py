from flask import Response
from flask import Flask
from flask import render_template
from flask import request, send_from_directory

import threading, os, sys
import subprocess
import queue
from datetime import datetime
from time import sleep
from scripts.chatGPT_helper import *
from scripts.abc_ttm_hufa_api import *


PRODUCTION=False

song_text_sample="""
(Verse 1)
Artemka's the winner,
Our champion of the day,
He's got the skills and the fire,
To light up the way.

(Chorus)
Oh, Artemka, Artemka,
Rising to the top,
You've got the heart, the strength, the soul,
To never, ever stop.

(Verse 2)
With every move he makes,
He brings the crowd to their feet,
They know that he's the one,
The one who can't be beat.

(Chorus)
Oh, Artemka, Artemka,
Rising to the top,
You've got the heart, the strength, the soul,
To never, ever stop.

(Bridge)
He's put in the work,
Day after day,
And now he's reaping the rewards,
In every single way.

(Chorus)
Oh, Artemka, Artemka,
Rising to the top,
You've got the heart, the strength, the soul,
To never, ever stop.

(Outro)
Artemka's the winner,
Our champion of the day,
And we know he'll keep on winning,
In every single way.
"""

abc_text_sample="""
X:1
L:1/2
Q:1/2=90
M:2/2min
K:F
 F2 F2 | A2 A2 | G2 G2 | F4 | F2 c2 | c2 c3/2 B/ | A3 G | F3 z | c4 | B4 | A4 | G4 | D4 | E4 |
 F4- | !fermata!F2 z2!D.C.! |]
"""

mp3_link_sample = "synth/tmp/1679640467456.mp3"

class generate_song_item:
    def __init__(self,song_text_query,i_was_here):
        self.i_was_here=i_was_here
        self.created = datetime.now()
        self.song_text_query = song_text_query
        self.status="generating..."
    
    def _gen_thread(self):
        song_query=f"write short song about: {self.song_text_query}"
        print(song_query)
        generated = False
        while not generated:
            self.status="generating..."
            if PRODUCTION:
                song_text = gpt35_query([song_query],[])
            else:
                song_text = song_text_sample
            sleep(0.2)
            generated=True
        print(song_text)
        self.song_text=song_text
        self.status ="done"
        pass

    def generate(self):
        self.gen_thread = threading.Thread(target=self._gen_thread)
        self.gen_thread.start()
        pass



class generate_music_item:
    def __init__(self,song_text,music_options,i_was_here):
        self.i_was_here=i_was_here
        self.created = datetime.now()
        self.song_text = song_text
        self.music_options = music_options
        self.abc_text = ""
        self.status="generation..."
    
    def _gen_thread(self):
        print(self.song_text)
        generated = False
        while not generated:
            self.status="generating..."
            if PRODUCTION:
                self.abc_text = gen_music(self.song_text,music_options=self.music_options,track_count=1,user_id=self.i_was_here,synth=False)
            else:
                self.abc_text = abc_text_sample
            sleep(0.2)
            generated=True
        print(self.abc_text)
        self.status ="done"
        pass

    def generate(self):
        self.gen_thread = threading.Thread(target=self._gen_thread)
        self.gen_thread.start()
        pass


class synth_music_item:
    def __init__(self,abc_text,synth_options,i_was_here):
        self.i_was_here=i_was_here
        self.created = datetime.now()
        self.abc_text = abc_text
        self.synth_options = synth_options
        self.mp3_link = ""
        self.status="synth..."
    
    def _synth_thread(self):
        print(self.synth_options)
        synthed = False
        while not synthed:
            self.status="synth..."
            if PRODUCTION:
                self.mp3_link = synth_from_abc(self.abc_text,synth_options=self.synth_options,user_id=self.i_was_here)
            else:
                self.mp3_link = synth_from_abc(self.abc_text,synth_options=self.synth_options,user_id=self.i_was_here)
                # self.mp3_link = mp3_link_sample
            sleep(0.2)
            synthed=True
        print(self.mp3_link)
        self.status ="done"
        pass

    def synth(self):
        self.synth_thread = threading.Thread(target=self._synth_thread)
        self.synth_thread.start()
        pass



__dir=os.path.dirname(os.path.realpath(__file__))  
web_server_config= None
template_dir = os.path.abspath('./')
web_server = Flask(__name__,template_folder=template_dir)

Synth_Music_Queue={}
Create_Music_Queue={}
Generate_Song_Queue={}

@web_server.route("/")
def index():
	return render_template("./index_new.html")

def _generate_song_text(song_text_query,i_was_here):
    status = "..."
    song_text=""
    if i_was_here in Generate_Song_Queue:
        status = Generate_Song_Queue[i_was_here].status
        if status=="done":
            song_text=Generate_Song_Queue[i_was_here].song_text
            del Generate_Song_Queue[i_was_here]
            if len(Generate_Song_Queue)>0:
                min_date = datetime.now()
                i_was_here_min_date=0
                for song_query_item in Generate_Song_Queue.values():
                    if song_query_item.created<min_date:
                        min_date=song_query_item.created
                        i_was_here_min_date=song_query_item.i_was_here
                Generate_Song_Queue[i_was_here_min_date].generate()
    else:
        if song_text_query is None:
            return ("","")
        Generate_Song_Queue[i_was_here]=generate_song_item(song_text_query,i_was_here)
        if (len(Generate_Song_Queue)==1):
            Generate_Song_Queue[i_was_here].generate()
        else:
            status= f"{len(Generate_Song_Queue)} in queue"
            Generate_Song_Queue[i_was_here].status=f"in queue..."
    return (status,song_text)



def _generate_music(song_text,music_options,i_was_here):
    status = "..."
    abc_text= ""
    if i_was_here in Create_Music_Queue:
        status = Create_Music_Queue[i_was_here].status
        if status=="done":
            abc_text=Create_Music_Queue[i_was_here].abc_text
            # output_tunes/1679485295975.svg
            del Create_Music_Queue[i_was_here]
            if len(Create_Music_Queue)>0:
                min_date = datetime.now()
                i_was_here_min_date=0
                for song_query_item in Create_Music_Queue.values():
                    if song_query_item.created<min_date:
                        min_date=song_query_item.created
                        i_was_here_min_date=song_query_item.i_was_here
                Create_Music_Queue[i_was_here_min_date].generate()
    else:
        if song_text is None:
            return ("","")
        Create_Music_Queue[i_was_here]=generate_music_item(song_text,music_options,i_was_here)
        if (len(Create_Music_Queue)==1):
            Create_Music_Queue[i_was_here].generate()
        else:
            status= f"{len(Create_Music_Queue)} in queue"
            Create_Music_Queue[i_was_here].status=f"in queue..."
    return (status,abc_text)

def _synth_music(abc_text,synth_options,i_was_here):
    status = "..."
    mp3_link= ""
    if i_was_here in Synth_Music_Queue:
        status = Synth_Music_Queue[i_was_here].status
        if status=="done":
            mp3_link=Synth_Music_Queue[i_was_here].mp3_link
            # output_tunes/1679485295975.svg
            del Synth_Music_Queue[i_was_here]
            if len(Synth_Music_Queue)>0:
                min_date = datetime.now()
                i_was_here_min_date=0
                for song_query_item in Synth_Music_Queue.values():
                    if song_query_item.created<min_date:
                        min_date=song_query_item.created
                        i_was_here_min_date=song_query_item.i_was_here
                Synth_Music_Queue[i_was_here_min_date].synth()
    else:
        if abc_text is None:
            return ("","")
        Synth_Music_Queue[i_was_here]=synth_music_item(abc_text,synth_options,i_was_here)
        if (len(Synth_Music_Queue)==1):
            Synth_Music_Queue[i_was_here].synth()
        else:
            status= f"{len(Synth_Music_Queue)} in queue"
            Synth_Music_Queue[i_was_here].status=f"in queue..."
    return (status,mp3_link)



@web_server.route('/generate_song_text', methods = ['POST'])
def generate_song_text():
    song_text_query = request.form['song_text_query']
    i_was_here = request.form['i_was_here']
    result=_generate_song_text(song_text_query,i_was_here)
    return json.dumps(result,ensure_ascii=False)


@web_server.route('/check_song_generating', methods = ['POST'])
def check_song_generating():
    i_was_here = request.form['i_was_here']
    result=_generate_song_text(None,i_was_here)
    return json.dumps(result,ensure_ascii=False)

@web_server.route('/generate_music', methods = ['POST'])
def generate_music():
    song_text = request.form['song_text']
    i_was_here = request.form['i_was_here']
    music_options = request.form['music_options']
    result=_generate_music(song_text,music_options,i_was_here)
    return json.dumps(result,ensure_ascii=False)

@web_server.route('/check_music_generating', methods = ['POST'])
def check_create_music():
    i_was_here = request.form['i_was_here']
    result=_generate_music(None,None,i_was_here)
    return json.dumps(result,ensure_ascii=False)
###
@web_server.route('/synth_music', methods = ['POST'])
def synth_music():
    abc_text = request.form['abc_text']
    i_was_here = request.form['i_was_here']
    synth_options = request.form['synth_options']
    result=_synth_music(abc_text,synth_options,i_was_here)
    return json.dumps(result,ensure_ascii=False)

@web_server.route('/check_music_synth', methods = ['POST'])
def check_music_synth():
    i_was_here = request.form['i_was_here']
    result=_synth_music(None,None,i_was_here)
    return json.dumps(result,ensure_ascii=False)
####
@web_server.route('/<path:path>')
def send_dist_files(path):
    return send_from_directory('./', path)

# @web_server.route("/video_feed")
# def video_feed():	
# 	return Response(generate_response(),
# 		mimetype = "multipart/x-mixed-replace; boundary=frame")



def run_server():
    if PRODUCTION:
        web_server.run(host="0.0.0.0", port="36000", debug=True,threaded=True, use_reloader=False)
    else:
        web_server.run(host="0.0.0.0", port="4444", debug=True,threaded=True, use_reloader=False)



if __name__ == '__main__':  
    # with open('web_server_config.json') as json_file:
    #     web_server_config = json.load(json_file)  
    if len(sys.argv)>1:
        if sys.argv[1]=="prod":
            PRODUCTION=True
    with open(os.path.join(os.path.dirname(__file__),'scripts/config_hufa.json')) as json_file:
        Config_hufa = json.load(json_file)
    with open(os.path.join(os.path.dirname(__file__),'scripts/config_openai.json')) as json_file:
        Config_openai = json.load(json_file)
    openai.api_key = Config_openai['api_key']
    web_server_thread = threading.Thread(target = run_server)    
    web_server_thread.start() 
    input("Press any key to exit...")



# https://github.com/spv420/chatgpt-clone
