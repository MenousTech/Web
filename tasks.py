import json
import os
from pathlib import Path
import secrets

path = os.path.join(Path(__file__).parent, "data") + "/"
file = path + 'tasks.json'

def startup():

    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)

def readDb():
    with open(file, 'r') as f:
        return json.load(f)

def writeDb(data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=True)

def addUser(username):

    data = readDb()
    data[username] = {
        "default":[]
    }
    writeDb(data)
    
def addTask(username, project, title, description, deadline, tag):
    data = readDb()
    id = secrets.token_hex(16)
    data[username][project].append({
        'id': id,
        'title': title,
        'description': description,
        'deadline': deadline,
        'tag': tag
    })
    writeDb(data)

def removeTask(username, project, id):
    data = readDb()
    for i in data[username][project]:
        if i['id'] == id:
            del data[username][project][i]

    writeDb(data)
addUser('snehashish2')

