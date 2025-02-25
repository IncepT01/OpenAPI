import requests
import json
from data import API_KEY, SF_DOMAIN, SF_AT
from jinja2 import Environment, FileSystemLoader
import random
import re
import base64

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
        "temperature": 0
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

def GenerateInterests(my_dict, names):
    interests = ['cycling', 'soccer', 'reading', 'games', 'jogging', 'hiking', 'cooking',
                  'chess', 'driving', 'eatin g', 'camping', 'painting', 'gardening', 'dancing']
    
    for c in names:
        for i in range(3):
            idx = random.randint(0, len(interests))
            my_dict[c].append(interests[i])

def SalesforceGET():
    url = SF_DOMAIN + "/services/data/v60.0/sobjects/Contact/"

    #Header with the API auth and to specify the json format
    headers = {
        "Authorization": "Bearer " + SF_AT,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    #GET request
    resp = requests.get(url=url, headers=headers)

    # Error handling and response file generation
    if resp.status_code == 200:
        print("Success!")
        resp_data = resp.json()

        with open('SF_response.json', 'w') as f:
            json.dump(resp_data, f, indent=4)
    else:
        print("Communication error! Code:", resp.status_code, "Response:", resp.text)

#Base64 filter for Jinja2
def base64_decode(value):
    decoded_bytes = base64.b64decode(value)
    return decoded_bytes.decode("utf-8")

customers = []

#Get the customers from salesforce commerce cloud
SalesforceGET()

#Load the response json
with open("SF_response.json", 'r') as f:
    resp_data = json.load(f)

#put their encoded names into an array
for i in resp_data["recentItems"]:
    print(i['Name'])
    customers.append(base64.b64encode((i['Name'].encode("utf-8"))))

customer_interests = {}

#Item the shop sells
stock = {'chessboard', 'card', 'board game', 'flower pot', 'Pride and Prejudice',
         'mobile phone', 'sport shoes', 'elegant shoes', 'sports shoes', 'sports shorts',
         'football shoes', 'laptop', 'watering can', 'watering hose', 'canvas', 'paint brush'}

#initialize their interest arrays
for i in customers:
    customer_interests[i] = []


GenerateInterests(customer_interests, customers)


### CHAT GPT PART

#message to prompt
message_to_ask = '''
I have a python dictionary wth customer names as keys,
 and their interests as values. I also have a list of items my webshop is selling.
 Basedd on their interests, can you give me one item for each person, that they would be intersted in?
 Also give me an estimate, how likely they would be intersted in, in percentage(don't put the percentage sign at the end).
 Please leave at least one customer from the given customers without recommendation. Only work with customers who are given as keys.
 Do not add new customers to the list and
 Do not change their names at all, even if is is encoded!
 
 can you list your answer similar to to this format:
        <n>name</n>,<i>item</i>,<p>percentage</p>

Customer and interests dictionary: {0}
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

#Regex
pattern = r"<n>(.*?)</n>,<i>(.*?)</i>"

#find matches
matches = re.findall(pattern, resp_msg)

#convert to dictionary
customer_items = {name: item for name, item in matches}



###Jinja2 templating part
file_loader = FileSystemLoader('templates') 
env = Environment(loader=file_loader)

#set the filter
env.filters['b64decode'] = base64_decode

template = env.get_template('email.txt')

output = template.render(recommendations=customer_items, signature="Gergo Tisza")
print(output)
with open('output.txt', 'w') as f:
    f.write(output)