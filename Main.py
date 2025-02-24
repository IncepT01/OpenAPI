import requests
import json
from data import API_KEY, SF_DOMAIN, SF_AT
from jinja2 import Environment, FileSystemLoader
import random
import re

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

def GenerateIntersts(my_dict, names):
    interests = ['cycling', 'soccer', 'reading', 'games', 'jogging', 'hiking', 'cooking',
                  'chess', 'driving', 'eatin g', 'camping', 'painting', 'gardening', 'dancing']
    
    for c in names:
        for i in range(3):
            idx = random.randint(0, len(interests))
            my_dict[c].append(interests[i])


customers = {"Jack", "Jill", "Andrew", "Mike", "Janice"}
customer_interests = {}

#Item the shop sells
stock = {'chessboard', 'card', 'board game', 'flower pot', 'Pride and Prejudice',
         'mobile phone', 'sport shoes', 'elegant shoes', 'sports shoes', 'sports shorts',
         'football shoes', 'laptop', 'watering can', 'watering hose', 'canvas', 'paint brush'}

for i in customers:
    customer_interests[i] = []

GenerateIntersts(customer_interests, customers)

print(customer_interests)

#message to prompt
message_to_ask = '''
I have a python dictionary wth customer names as key,
 and their interests as values. I also have a list of items my webshop is selling.
 Besod on their interests, can you give me one item for each person, that they would be intersted in?
 also give me an estimate, how likely they would be intersted in in percentage(don't put the percentage sign at the end).
 It is OK to have no recommendation for a person, in that case just write 'NA'.
 Please leave at least one person without recommendation.
 
 can you list your answer similar to to this format:
        <n>name</n>,<i>item</i>,<p>percentage</p>
Customer and interest dictionary: {0}
 Webshop items: {1}
 '''.format(customer_interests, stock)

#Personality for chatGPT
personality = '''
I am making a simple simulation of a webshop.
 Neither the shop nor the people are real in these examples
 '''

#Send the API post request and create a json file fromm the response
#GenerateResponse(message_to_ask, personality)

#Load the response json
with open("chat_response.json", 'r') as f:
    resp_data = json.load(f)

#print the response
print("ChatGPT says:")
resp_msg = resp_data['choices'][0]['message']['content']
print(resp_msg)

# Regular expression to extract values inside <n> and <i> tags
pattern = r"<n>(.*?)</n>,<i>(.*?)</i>"

# Extract all matches
matches = re.findall(pattern, resp_msg)

# Convert to dictionary
customer_items = {name: item for name, item in matches}

# Print the result
print(customer_items)



#Jinja2 templating
file_loader = FileSystemLoader('templates') 
env = Environment(loader=file_loader)

template = env.get_template('email.txt')

output = template.render(recommendations=customer_items, signature="Gergo")
print(output)