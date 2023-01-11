read -r -d '' TEXT << EOM
> Я Яндекс Спичк+ит.
> Я могу превратить любой текст в речь.
> Теперь и в+ы — можете!
EOM
export FOLDER_ID=b1g8qqrgrlfsd2su0q6s
export IAM_TOKEN=t1.9euelZqQipWXk8abnJDOlMaXm86dke3rnpWajs-ZiorKlp6Kl5qWlMmPx8fl9PcvNgli-e8IRAi33fT3b2QGYvnvCEQItw.4ZbuO6537qiMF5SRVNKNdT2X8r7CGBDARV4TEHlvHaSHP9N5CWF4gW6P5B15KkGDTy1QpLLeRKIYCNRELhrLDg
curl -X POST \
   -H "Authorization: Bearer ${IAM_TOKEN}" \
   --data-urlencode "text=${TEXT}" \
   -d "lang=ru-RU&voice=filipp&folderId=${FOLDER_ID}" \
   "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize" > speech.ogg
