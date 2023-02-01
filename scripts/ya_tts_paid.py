import os
import time
 
import requests
 
 
def synthesize(text,folder_id,token,voice='alena',emotion='neutral',lang='ru-RU',speed='1.0',format='mp3'):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {'Authorization': 'Bearer ' + token,}
 
    data = {
        'folderId': folder_id,
        'text': text,
        'lang': lang,
        'voice':voice, # oksana
        'emotion':emotion,
        'speed':speed,
        'format': format
        # 'sampleRateHertz': 48000,
    }
 
    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk
 
def tts_to_mp3(text,f_path,folder_id,token,voice='alena',emotion='neutral',lang='ru-RU',speed='1.0'):
    with open(f_path, "wb") as f:
        for audio_content in synthesize(text,folder_id,token,voice,emotion,lang,speed):
            f.write(audio_content)
    return f_path

def tts_to_lpcm(text,f_path,folder_id,token,voice='alena',emotion='neutral',lang='ru-RU',speed='1.0'):
    with open(f_path, "wb") as f:
        for audio_content in synthesize(text,folder_id,token,voice,emotion,lang,speed,format='lpcm'):
            f.write(audio_content)
    return f_path
 
if __name__=='__main__':
    root_path = os.path.dirname(__file__)
    target_path = root_path
    filename = str(int(time.time()))
    f_path=target_path + filename + ".mp3"
    tts_to_mp3("hello",f_path)