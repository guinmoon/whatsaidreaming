import os,subprocess
from ai_news import *


if __name__=='__main__':
    __dir=os.path.dirname(os.path.realpath(__file__))    
    news_prompt = get_prompt_from_news("https://news.1777.ru/rss/yandex",only_check=True)
    if news_prompt is not None:
        result = subprocess.run(["python3.9",f"{__dir}/think_about_something.py", "-n"],cwd=__dir)