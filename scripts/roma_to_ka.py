habr_song="""
Got something to share, gotta get it out
Habr blog's where it's at, no doubt
Tech and coding, all in one place
Follow along, keep up with the pace

Habr blog, Habr blog
Where tech geniuses come to log
Code and innovation, all in one spot
Habr blog, Habr blog, never stop

From AI to cybersecurity
Habr blog's got it covered, oh my
Learn from the best, no need to pay
Habr blog's free, just come and play

Habr blog, Habr blog
Where tech geniuses come to log
Code and innovation, all in one spot
Habr blog, Habr blog, never stop

Stay connected, never miss a beat
Join the Habr community and take a seat
Comment, share, and contribute too
Habr blog, there's always something new

Habr blog, Habr blog
Where tech geniuses come to log
Code and innovation, all in one spot
Habr blog, Habr blog, never stop

Habr blog, Habr blog, never stop
Keep on coding, keep on sharing, until the last drop.
"""


# https://krakozyabr.ru/2011/12/transliteraciya/
# https://lingust.ru/japanese/japanese-lessons/lesson3
# https://ru.wikipedia.org/wiki/%D0%A4%D1%83%D1%80%D0%B8%D0%B3%D0%B0%D0%BD%D0%B0

# https://github.com/actlaboratory/englishToKanaConverter
# https://github.com/Pugnator/kananization

# https://github.com/enzo1982/superfast#superfast-codecs
# https://lame.sourceforge.io/links.php

# https://ru.wikipedia.org/wiki/Utau
# https://piaprostudio.com/?lang=en

# !!!!# https://vocalsynth.fandom.com/wiki/Synthesizer_V

# !!! http://www.sinsy.jp/

# !!!!! https://github.com/r9y9/pysinsy/blob/master/docs/notebooks/Demo.ipynb

# https://gitlab.schukai.com/oss/minerva/grapesjs-blocks-bootstrap

# https://runwayml.com/#generate-videos

# https://github.com/rustformers/llama-rs

# https://shuffle.dev/


from englishToKanaConverter.englishToKanaConverter import EnglishToKanaConverter

converter = EnglishToKanaConverter(True)
# res=romkan.to_katakana(habr_song)
res=converter.process(habr_song)
print(res)