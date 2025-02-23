import requests
import json
from data import API_KEY


def GenerateResponse(message):
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages" : [{"role": "user", "content": message_to_ask}],
        "temperature": 0.7
    }

    resp = requests.post(url=url, json = data, headers=headers)

    if resp.status_code == 200:
        print("Success!")
        resp_data = resp.json()

        with open('chat_response.json', 'w') as f:
            json.dump(resp_data, f, indent=4)
    else:
        print("Communication error")





message_to_ask = "Hey there chatGPT! I'm talking to you through openAPI. Did you get the message?"

#GenerateResponse(message_to_ask)

with open("chat_response.json", 'r') as f:
    resp_data = json.load(f)

print("ChatGPT says:")
print(resp_data['choices'][0]['message']['content'])