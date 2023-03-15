
import os, json, time
import openai

openai_conf=None

# def davincii003_query(prompt):
def davincii003_query(prompts,responses):
    # model_engine = "text-davinci-003"
    model_engine = "gpt-3.5-turbo"
    has_answer = False
    while not has_answer:
        prompt=""
        if len(prompts)>1:
            prompt="context: "
        for i in range(len(prompts)-1):
            prompt+=f"{prompts[i]}\n{responses[i]}\n"
        prompt+="prompt: "+prompts[-1]
        try:
            # completion = openai.Completion.create(
            #     engine=model_engine,
            #     prompt=prompt,
            #     max_tokens=1024,
            #     temperature=0.5,
            #     top_p=1,
            #     frequency_penalty=0,
            #     presence_penalty=0     
            # )
            completion=openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "user", "content": prompt}
                        # {"role": "assistant", "content": prompt}
                        # {"role": "system", "content": prompt}
                    ]
            )
            has_answer = True
        except Exception as eee:
            if str(eee).find("maximum context length")>=0:
                has_answer = False
                prompts.pop(0)
                responses.pop(0)
    # return(completion.choices[0].text)
    return(completion.choices[0].message.content)


if __name__=="__main__":
    __dir=os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(os.path.dirname(__file__),'config_openai.json')) as json_file:
        openai_conf = json.load(json_file)
    openai.api_key = openai_conf['api_key']
    prompt = ""
    context = ""
    timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())  
    history_log = f"{__dir}/gpt_history/{timestamp}.log"
    file = open(history_log, "w")
    prompts= []
    responses= []
    while True:
        prompt = input(">> ")
        if prompt == 'exit':
            break
        if prompt == 'new':
            context = ""
            prompts= []
            responses= []
            continue
        prompts.append(prompt)
        file.write(f">> {prompt}\n")
        # response = davincii003_query(prompt="context:" + context + "\n\n" + "prompt:" + prompt)
        response = davincii003_query(prompts,responses)
        response = response.lstrip()
        responses.append(response)
        print(f"<< {response}\n")
        file.write(f"<< {response}\n")
        # context += "\n".join([context, prompt, response])
        file.flush()

    file.close()