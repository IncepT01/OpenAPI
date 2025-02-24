import requests
import json
from data import API_KEY
from jinja2 import Environment, FileSystemLoader


def GenerateResponse(message, personality=""):
    url = 'https://api.openai.com/v1/chat/completions'

    #Header with the API auth and to specify the json format
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    #Payload we send
    data = {
        "model": "gpt-3.5-turbo",
        "messages" : [{"role": "system", "content": personality},{"role": "user", "content": message_to_ask}],
        "temperature": 0.7
    }

    #Post request
    resp = requests.post(url=url, json = data, headers=headers)

    #Error handling and response file generation
    if resp.status_code == 200:
        print("Success!")
        resp_data = resp.json()

        with open('chat_response.json', 'w') as f:
            json.dump(resp_data, f, indent=4)
    else:
        print("Communication error! Code:",resp.status_code)




#message to prompt
message_to_ask = "I'm trying out the new openAPI. If you get this message, please welcome the audience"

#Personality for chatGPT
personality = '''You are a sports commentator who is currently going through a divorce.
                Everything around you reminds you of your ex-wife, and you occasionally bring up memoried
                "f her while commenting on sports events. Despite this, you try to keep your commentary focused
                "n the game, but emotions sometimes creep in.'''

#Send the API post request and create a json file fromm the response
#GenerateResponse(message_to_ask, personality)

#Load the response json
with open("chat_response.json", 'r') as f:
    resp_data = json.load(f)

#print the response
print("ChatGPT says:")
print(resp_data['choices'][0]['message']['content'])


#Jinja2 templating
file_loader = FileSystemLoader('templates') 
env = Environment(loader=file_loader)

template = env.get_template('email.txt')

output = template.render()
print(output)