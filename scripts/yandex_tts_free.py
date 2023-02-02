import http.client
import json
import sys

Cookie="yandexuid=1607909291673207985; _yasc=ShiyKBuLqsP6q9eEy5YRzdJBV+l8vQLBUQ2mF/AIEcMaVjsd5mlHhhjIDmRxhsKesOg=; is_gdpr=0; is_gdpr_b=CJaLGxDenwE=; i=Ddwf3WkHBw9odVOiiIj95KfAxGTMxm7S6jRmDFOyF6jHzcWyJRd6LPy3NwGibN+O3IBtOGgdIP0l3B7WXyprrlI8Mqo=; spravka=dD0xNjc1MDcwMjg5O2k9MTg1LjIyOC4yMzMuMTI5O0Q9MTYxRjFBQThDRUREMkZBRDNGRTJDODIyOTlFQjFGQ0Q1OUNEMUY1ODUxMzBGM0YzOTAwMjkwOTM0MzI1NDUwNUZCQzVENTZGNzExNEU0NzE3M0E1NUQ3NDZEQTM5OTt1PTE2NzUwNzAyODk4MTY1NjU0MTU7aD1jZmNkZTI0NWQ2N2RlZmQ2ZjU2YTI4OTA4NWU3MjEzZQ==; yashr=1176431671…IykI=1; session-geo-data=eyJyZWdpb25OYW1lIjoi0KHRgtCw0LLRgNC%2B0L%2FQvtC70YwiLCJjb3VudHJ5TmFtZSI6ItCg0L7RgdGB0LjRjyIsInRpbWV6b25lIjoiRXVyb3BlL01vc2NvdyIsImxvY2FsZSI6eyJjb2RlIjoicnUtUlUiLCJuYW1lIjoi0KDQvtGB0YHQuNGPICjQoNGD0YHRgdC60LjQuSkiLCJsYW5nIjoicnUiLCJsYW5nTmFtZSI6ItCg0YPRgdGB0LrQuNC5IiwicmVnaW9uIjoicnUiLCJyZWdpb25OYW1lIjoi0KDQvtGB0YHQuNGPIiwiY3VycmVuY3kiOiJSVUIiLCJ0bGQiOiJydSIsIm9yZGVyIjoxLCJkZWZhdWx0Ijp0cnVlLCJsb2NhbCI6dHJ1ZX19; XSRF-TOKEN=a58cf0b5c0dc6480b0469a9252dd08d03cf0963f%3A1675322770; gdpr=0"

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
  'x-csrf-token': '584bd50e0210a13d90bbe0881fbe6f037ed8bed2:1675322764'
}
conn.request("POST", "/api/speechkit/tts", payload, headers)
res = conn.getresponse()
data = res.read()
# fname=sys.argv[1]
fname ="out.ogg"
with open(fname,'wb') as f:
  f.write(data)
print(data)