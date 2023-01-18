import os
import time
from creds import token, folder_id
 
import requests
 
root_path = os.path.dirname(__file__)
target_path = root_path
 
"""
Протухает через 12 часов не использования
yc iam create-token >> /home/web/token.txt
 
Кусок текста меньше 5000 симв
 
 
https://cloud.yandex.ru/docs/speechkit/tts/request#wav
https://cloud.yandex.ru/docs/speechkit/tts/request
https://cloud.yandex.ru/docs/speechkit/api-ref/grpc/tts_service
"""
 
def synthesize(text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {'Authorization': 'Bearer ' + token,}
 
    data = {
        'folderId': folder_id,
        'text': text,
        'lang': 'en-EN',
        # 'voice':'alena', # премиум - жрет в 10 раз больше денег
        'voice':'alena', # oksana
        'emotion':'good',
        'speed':'1.0',
        # по умолчанию конвертит в oggopus, кот никто не понимает, зато занимат мало места
        'format': 'mp3'
        # 'sampleRateHertz': 48000,
    }
 
    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
 
        for chunk in resp.iter_content(chunk_size=None):
            yield chunk
 
def write_file(text):
    """
    Пишет чанки в вайл
    :param text:
    :return:
    """
    filename = str(int(time.time()))
    with open(target_path + filename + ".mp3", "wb") as f:
        for audio_content in synthesize(text):
            f.write(audio_content)
 
    time.sleep(2)
 
    return filename
 

write_file("hello")