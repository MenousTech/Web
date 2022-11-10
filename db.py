import json
import os
from pathlib import Path

path = os.path.join(Path(__file__).parent, 'data') + '/'

def init():
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path+'data.json'):
        with open(path+'data.json', 'w') as file:
            json.dump([], file)

def readDb():
    with open(path + 'data.json', 'r') as file:
        return json.load(file)

def readUserDb(user):
    data = readDb()
    if user.lower() in data.keys():
        return data[user.lower()]
    else:
        return 'User does not exist'

def writeDb(data):
    with open(path + 'data.json', 'w') as file:
        json.dump(data, file, indent=True)
    
def addUser(user):
    data = readDb()
    data[user] = []
    writeDb(data)

def addPost(user, title:str, date:str, body:list):
    data = readDb()
    Dict = {
        'title': title,
        'date': date,
        'body':body,
        'author':user
    }
    if not user.lower() in data.keys():
        addUser(user)
        data[user.lower()].append(Dict)
    else:
        data[user.lower()].append(Dict)
    writeDb(data)
    
