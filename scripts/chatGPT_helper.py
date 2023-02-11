
import os, json
import openai

def davincii003_query(prompt):
    openai_conf=None
    with open(os.path.join(os.path.dirname(__file__),'config_openai.json')) as json_file:
        openai_conf = json.load(json_file)
    openai.api_key = openai_conf['api_key']
    model_engine = "text-davinci-003"
    max_tokens = 128
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return(completion.choices[0].text)

if __name__=="__main__":
    prompt="Придумай ТЗ для модуля взаимодействия с перефирийными устройствами."
    print(prompt)
    print(davincii003_query(prompt))