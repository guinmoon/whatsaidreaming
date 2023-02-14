
import os, json, time
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
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    prompt = ""
    context = ""
    timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())  
    history_log = f"{__dir}/gpt_history/{timestamp}.log"
    file = open(history_log, "w")

    while True:
        print(">>")
        prompt = input()
        if prompt == 'exit':
            break
        if prompt == 'new':
            context = ""
            continue
        file.write(prompt)
        response = davincii003_query(prompt="context:" + context + "\n\n" + "prompt:" + prompt)
        file.write(response+ "\n")
        print("\n Re:"+response + "\n")
        context += "\n".join([context, prompt, response])
        file.flush()

    file.close()