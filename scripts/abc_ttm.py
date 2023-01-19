import torch
from samplings import top_p_sampling, temperature_sampling
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained('sander-wood/text-to-music')
model = AutoModelForSeq2SeqLM.from_pretrained('sander-wood/text-to-music')
model = model

max_length = 1024
top_p = 0.9
temperature = 1.0

text = "This is a traditional Irish dance music."
input_ids = tokenizer(text, 
                      return_tensors='pt', 
                      truncation=True, 
                      max_length=max_length)['input_ids']

decoder_start_token_id = model.config.decoder_start_token_id
eos_token_id = model.config.eos_token_id

decoder_input_ids = torch.tensor([[decoder_start_token_id]])

for t_idx in range(max_length):
    outputs = model(input_ids=input_ids, 
    decoder_input_ids=decoder_input_ids)
    probs = outputs.logits[0][-1]
    probs = torch.nn.Softmax(dim=-1)(probs).detach().numpy()
    sampled_id = temperature_sampling(probs=top_p_sampling(probs, 
                                                           top_p=top_p, 
                                                           return_probs=True),
                                      temperature=temperature)
    decoder_input_ids = torch.cat((decoder_input_ids, torch.tensor([[sampled_id]])), 1)
    if sampled_id!=eos_token_id:
        continue
    else:
        tune = "X:1\n"
        tune += tokenizer.decode(decoder_input_ids[0], skip_special_tokens=True)
        print(tune)
        break