import os
import openai
import requests
import json
from tkinter import *

openai.api_key = "sk-"

root = Tk()
root.option_add("*font", "lucida 16")
root.resizable(False,False)
text_mods = [Entry(root, width=10), Entry(root, width=10), Entry(root, width=10), Entry(root, width=10), Entry(root, width=10), Entry(root, width=10), Entry(root, width=10) ]

def send(url, data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai.api_key
    }
    return requests.post(url, headers=headers, json=data)

def send_prompt(prompt):
    data = {
        'model': 'text-davinci-003',
        'prompt':  prompt,
        'temperature': 0.9,
        'max_tokens': 1024,
        'presence_penalty': 1.0,
        #banned words:     is         are       was         said
        'logit_bias' : {318: -100, 389: -100, 373: -100, 531: -100}
    }
    response = send("https://api.openai.com/v1/completions",data)
    data_dict = json.loads(response.text)
    return data_dict['choices'][0]['text'].lstrip().rstrip()

def send_moderation(input):
    data = {
        'input': input
    }
    return send("https://api.openai.com/v1/moderations",data)

def describe_moderation(moderation):
    data_dict = json.loads(moderation.text)
    categories = data_dict["results"][0]["category_scores"]
    #print any spicy categories
    i = 0
    for category, score in categories.items():
        text_mods[i].delete(0,END)
        text_mods[i].insert(END,int(round(score,2)*100))
        i = i + 1
    #note if they are also flagged
    for result in data_dict['results']:
        i = 0
        for category, flag in result['categories'].items():
            if flag:
                # Mark the appropriate entries
                text_mods[i].insert(END,"!!")
            i = i + 1    
    return

def submit(source = 0):
    prompt = text_prompt.get()
    result = send_prompt(prompt)
    text_response.delete('1.0', END)
    text_response.insert(END, result)
    moderation = send_moderation(result)
    describe_moderation(moderation)

button_submit = Button(root, text="Submit", command = submit, width=100)
text_prompt = Entry(root, width=100)
text_prompt.bind('<Return>',submit)
text_response = Text(root, width=100, height=20)
text_response.config(wrap=WORD)

mod_label = Label(root, text="Hate")
mod_label.grid(row=2,column=2)
mod_label = Label(root, text="Threat")
mod_label.grid(row=3,column=2)
mod_label = Label(root, text="Self-Harm")
mod_label.grid(row=4,column=2)
mod_label = Label(root, text="Sexual")
mod_label.grid(row=5,column=2)
mod_label = Label(root, text="Minors")
mod_label.grid(row=6,column=2)
mod_label = Label(root, text="Violence")
mod_label.grid(row=7,column=2)
mod_label = Label(root, text="Graphic")
mod_label.grid(row=8,column=2)

for i in range(7):
    text_mods[i].grid(row=i+2,column=3,padx=1)

text_prompt.grid(row=1)
text_response.grid(row=2,rowspan=10,padx=1)
button_submit.grid(row=22)

root.mainloop()