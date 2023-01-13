import http.client
import json
import sys

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
  'Cookie': 'yandexuid=4820047601666964160; yuidss=4820047601666964160; ymex=1982324160.yrts.1666964160#1982324160.yrtsi.1666964160; is_gdpr=0; gdpr=0; _ym_uid=1667193561507886098; _ym_d=1667193562; skid=3386796601667368099; _ga=GA1.2.1686453913.1668401924; my=YwA=; is_gdpr_b=CIy8DhCAlwEoAg==; yandex_login=andreas.svetlakov; font_loaded=YSv1; L=fCBoYlJHaFtIS2BnaXFVbAsLVWtBRll0LzcqEVcPGHg1BAhGNjAgKkI=.1669185429.15170.330354.51502f329c779b9bee36ebdd88a8dd19; ys=udn.cDphbmRyZWFzLnN2ZXRsYWtvdg%3D%3D#wprid.1671607457205048-15615117192998857305-sas3-0704-ded-sas-l7-balancer-8080-BAL-3748#c_chck.4076025427; yp=1684949848.szm.1:1920x1080:1920x969#1984545429.udn.cDphbmRyZWFzLnN2ZXRsYWtvdg%3D%3D#1986967458.pcs.1#1703143458.pgp.1_27860124#1672212253.mcv.0#1672212253.mcl.16d6fxq; yabs-frequency=/5/0000000000000000/swvnE0daUaO4IaSoR8W5ORFCL0HA9u6f6ZyhvZvR14eWlmdSQgKlb5G4IY3c_4pUHqc_KWHAG000/; i=lmSR0Tlgg6lS4aN5G+I09djP1Ae9QaJysnnfmDkGMjUzLxEl61ju77DFwevfvSm1QTCtLJJg81IPCbG15N+uWor2B3I=; _ym_isad=2; session-geo-data=eyJyZWdpb25OYW1lIjoi0KHRgtCw0LLRgNC%2B0L%2FQvtC70YwiLCJjb3VudHJ5TmFtZSI6ItCg0L7RgdGB0LjRjyIsInRpbWV6b25lIjoiRXVyb3BlL01vc2NvdyIsImxvY2FsZSI6eyJjb2RlIjoicnUtUlUiLCJuYW1lIjoi0KDQvtGB0YHQuNGPICjQoNGD0YHRgdC60LjQuSkiLCJsYW5nIjoicnUiLCJsYW5nTmFtZSI6ItCg0YPRgdGB0LrQuNC5IiwicmVnaW9uIjoicnUiLCJyZWdpb25OYW1lIjoi0KDQvtGB0YHQuNGPIiwiY3VycmVuY3kiOiJSVUIiLCJ0bGQiOiJydSIsIm9yZGVyIjoxLCJkZWZhdWx0Ijp0cnVlLCJsb2NhbCI6dHJ1ZX19; Session_id=3:1673597871.5.0.1669185265851:wpEAwg:35.1.2:1|1717287608.164.2.2:164|3:10264027.613980.8FeYrKM0730Wsfu8DcyGWJMU_u0; sessionid2=3:1673597871.5.0.1669185265851:wpEAwg:35.1.2:1|1717287608.164.2.2:164|3:10264027.613980.fakesign0000000000000000000; _ym_visorc=b; XSRF-TOKEN=81a944d5ac4de2213cd04cbe434bfb5f059c8a89%3A1673597891; _yasc=POihGQb455hEQU2FF0jqOqS2XcPVjhleRISSoHSLd6B4WS14eMkyPNavMbP+lXZ+Jw==',
  'Origin': 'https://cloud.yandex.ru',
  'Referer': 'https://cloud.yandex.ru/services/speechkit',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'x-csrf-token': '3d88b169fdd6b9214ae686f50c3e770ce731a0bd:1673597878'
}
conn.request("POST", "/api/speechkit/tts", payload, headers)
res = conn.getresponse()
data = res.read()
with open(sys.argv[1],'wb') as f:
  f.write(data)
print(data)