import requests
import json
from data import API_KEY


def GenerateResponse(message, personality=""):
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages" : [{"role": "system", "content": personality},{"role": "user", "content": message_to_ask}],
        "temperature": 0.7
    }

    resp = requests.post(url=url, json = data, headers=headers)

    if resp.status_code == 200:
        print("Success!")
        resp_data = resp.json()

        with open('chat_response.json', 'w') as f:
            json.dump(resp_data, f, indent=4)
    else:
        print("Communication error! Code:",resp.status_code)





message_to_ask = "I'm trying out the new openAPI. If you get this message, please welcome the audience"

personality = '''You are a sports commentator who is currently going through a divorce.
                Everything around you reminds you of your ex-wife, and you occasionally bring up memoried
                "f her while commenting on sports events. Despite this, you try to keep your commentary focused
                "n the game, but emotions sometimes creep in.'''

GenerateResponse(message_to_ask, personality)

with open("chat_response.json", 'r') as f:
    resp_data = json.load(f)

print("ChatGPT says:")
print(resp_data['choices'][0]['message']['content'])