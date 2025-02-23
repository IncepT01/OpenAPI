import requests
import json
from data import API_KEY

url = 'https://api.openai.com/v1/chat/completions'

message_to_ask = "I am testing the openAPI using python. If you received this message. Say something to welcome the audience"

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
    resp_data = resp.json()

    with open('chat_response.json', 'w') as f:
        json.dump(resp_data, f, indent=4)

    messsage = resp_data['choices'][0]['content']
    print(messsage)
else:
    print("Communication error")