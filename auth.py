from flask import *
import requests
from pathlib import Path
import random as r
import os
path = str(Path(__file__).parent) + '/'
apiurl = 'http://snehashishlaskar090.pythonanywhere.com/'
import db

usrName = None
psword = None

def convertUserDataToJson(username):
    data = requests.get('{}sites?username={}'.format(apiurl, username)).json()
    return data

def login():

    if request.method == 'POST':

        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user == None and pw == None:

            usrname = request.form['username']
            psword = request.form['password']

            data = requests.get(apiurl).json()
            
            for i in data:
                print(usrname, psword)
                if i[0] == usrname and i[1] == psword:
                    session['username'] = usrname
                    return redirect('/passwords/home')
        
            return render_template('login.html', error=True)

        else:
            return redirect('/passwords/home')

    else:
        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user == None and pw == None:


            return render_template('login.html')

        else:
            return redirect('/passwords/home')

def logout():
    session['username'] = None
    print(session['username'])
    return redirect('/auth')

def delete():
    return render_template('delete_account.html', sess=True)
def signup(mail, Message):
    if request.method == 'POST':
        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user == None and pw == None:
        
            username = request.form['username']
            usrName = username
            password = request.form['password']
            psword = password

            email = request.form['email']
            try:
                convertUserDataToJson(username)
                return render_template('signup.html', msg = "User Already Exists!")
            except:
                if len(password) < 8:
                    return render_template('signup.html', msg = "Please select a password more than 8 digits!")
                else:
                    with open(path+'creds.json') as file:
                        data = json.load(file)
                    with open(path+'creds.json', 'w') as file:
                        data['username'] = username
                        data['password'] = password
                        json.dump(data, file)

                    token = str(r.randint(100000, 1000000))

                    if os.path.exists(path+'tokens.json'):
                        with open(path+'tokens.json', 'w') as file:
                            json.dump([], file)

                    with open(path+'tokens.json') as file:
                        data = json.load(file)

                    data.append(token)

                    with open(path+'tokens.json', 'w') as file:
                        json.dump(data, file)
                    db.addUser(username)
                    try:
                        msg = Message(
                            'Confirmation Email',
                            sender = "admin@menoustech.com",
                            recipients=[email]
                        ) 
                        msg.body = render_template('email.html', username = username, OTP = token)
                        msg.html = render_template('email.html', username = username, OTP = token)

                        mail.send(msg)
                        return redirect('/confirm')
                    except Exception as ex:
                        return str(ex)

        else:
            return redirect('/passwords/home')

    else:
        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user != None and pw != None:
            return redirect('/passwords/home')
        else:
            return render_template('signup.html', msg = "")

def deleteUser():

    requests.delete(f"{apiurl}delete?username={session['username']}")
    return redirect('/logout')  

def confirm():

    with open(path+'tokens.json') as file:
        data = json.load(file)

    with open(path+'creds.json') as file:
        data2 = json.load(file)

    if request.method == 'GET':
        return render_template('confirm.html')
    else:
        otp = str(request.form['otp'])
        if otp in data:
            print(otp)
            requests.post('{}createuser?username={}&password={}'.format(
                    apiurl,data2['username'], data2['password']
                ))
            session['username'] = data2['username']
            data2['username'] = ''
            data2['password'] = ''
            with open(path+'creds.json', 'w') as file:
                json.dump(data2, file)
            return redirect('/passwords/home')
        else:
            return render_template('confirm.html', incorrect=True)
