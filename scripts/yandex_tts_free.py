import http.client
import json
import sys

Cookie=None

conn = http.client.HTTPSConnection("cloud.yandex.ru")
payload = json.dumps({
  "message": "Привет!\nЯ Яндекс Спичк+ит.\nЯ могу превратить любой текст в речь.",
  "language": "ru-ru",
  "speed": 1,
  "voice": "alena",
  "emotion": "good",
  "format": "oggopus"
})
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json',
  'Cookie': Cookie,
  'Origin': 'https://cloud.yandex.ru',
  'Referer': 'https://cloud.yandex.ru/services/speechkit',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'x-csrf-token': '---'
}
conn.request("POST", "/api/speechkit/tts", payload, headers)
res = conn.getresponse()
data = res.read()
with open(sys.argv[1],'wb') as f:
  f.write(data)
print(data)