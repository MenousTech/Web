# Author : Snehashish Laskar
# Date of Start: 10-5-2022
# Latest date: 22-10-2022

# Importing all the modules needed 
from flask import *
from flask_session import Session
from flask_mail import Mail, Message
import requests
from secrets import token_urlsafe
import json 
from pathlib import Path
import os

# Initializing flask app called app
app = Flask(__name__)
# Getting the full path to the file
path = str(Path(__file__).parent) + '/'

# Setting up flask sessions to store cookies
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configuration of Flask Mail to send confirmation email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'admin@menoustech.com'
app.config['MAIL_PASSWORD'] = 'snehashish08036#@#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Setting the api url
apiurl = 'http://snehashishlaskar090.pythonanywhere.com'
usrName = None
psword = None


def convertUserDataToJson(username):
    data = requests.get('{}sites?username={}'.format(apiurl, username)).json()

    return data


# Login Page
@app.route('/auth', methods=['GET', 'POST'])
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
                    return redirect('/home')
        
            return render_template('login.html', error=True)

        else:
            return redirect('/home')

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
            return redirect('/home')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['username'] = None
    print(session['username'])
    return redirect('/auth')

@app.route('/delete', methods=['POST','GET'])
def delete():
    return render_template('delete_account.html', sess=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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

                    token = str(token_urlsafe(16))
                    if os.path.exists(path+'tokens.json'):
                        with open(path+'tokens.json', 'w') as file:
                            json.dump([], file)

                    with open(path+'tokens.json') as file:
                        data = json.load(file)

                    data.append(token)

                    with open(path+'tokens.json', 'w') as file:
                        json.dump(data, file)
                    
                    

                    try:
                        msg = Message(
                            'Confirmation Email',
                            sender='snehashish.laskar@gmail.com',
                            recipients=[email]
                        ) 
                        msg.body = render_template('email.html', username = username, link = f'http://www.manager.menoustech.com/confirm/{token}')
                        msg.html = render_template('email.html', username = username, link = f'http://www.manager.menoustech.com/confirm/{token}')
                        mail.send(msg)
                        return render_template('confirm.html')
                    except Exception as ex:
                        return str(ex)

        else:
            return redirect('/home')

    else:
        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user != None and pw != None:
            return redirect('/home')
        else:
            return render_template('signup.html', msg = "")       


# Snehashish Laskar
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form['addname']
            email = request.form['addemail']
            username =  request.form['addusername']
            password = request.form['addpass']

            query = requests.post('{}addsite?username={}&sitename={}&password={}&email={}&siteusrname={}'.format(
                apiurl,
                session['username'],
                name,
                password,
                email,
                username,
            ))
            return redirect('/home')
        
        elif 'del' in request.form:
            name = request.form['name']

            query = requests.delete('{}delsite?username={}&site={}'.format(
                apiurl,
                session['username'],
                name
            ))

            return redirect('/home')
    else:
        return render_template('home.html', sess = True, data = convertUserDataToJson(session['username']))


@app.route('/cookies', methods = ['GET', 'POST'])
def cook():
    return jsonify(session['username'])
    
@app.route('/', methods = ['GET', 'POST'])
def main():

    user = None
    pw = None

    try:
        user = session['username']
    except:
        pass

    if user != None:
        return render_template('index.html', sess = True)
    else:
        return render_template('index.html', sess = False)

@app.route('/deleteusersure', methods=["GET", "POST"])
def deleteUser():

    requests.delete(f"{apiurl}delete?username={session['username']}")
    return redirect('/logout')



@app.route('/confirm/<token>', methods=['GET'])
def confirm(token):

    with open(path+'tokens.json') as file:
        data = json.load(file)
    with open(path+'creds.json') as file:
        data2 = json.load(file)
    if token in data:
        query = requests.post('{}createuser?username={}&password={}'.format(
                apiurl,data2['username'], data2['password']
            ))
        session['username'] = data2['username']
        data2['username'] = ''
        data2['password'] = ''
        with open(path+'creds.json', 'w') as file:
            json.dump(data2, file)

        return redirect('/home')
    else:
        return redirect('/signup')



@app.route('/<page>', methods=['GET'])
def unknown(page):
    return render_template('error.html')

app.run(debug=True, host = '0.0.0.0', port =80)

