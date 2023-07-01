# Author : Snehashish Laskar
# Date of Start: 10-5-2022
# Latest date: 22-10-2022

# Importing all the modules needed 
from flask import *
from flask_session import Session
from flask_mail import Mail, Message
import requests
from pathlib import Path
import passwords
import auth
import blogs

# Initializing flask app called app
app = Flask(__name__)
# Getting the full path to the file
path = str(Path(__file__).parent) + '/'

# Setting up flask sessions to store cookies
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configuration of Flask Mail to send confirmation email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'admin@menoustech.com'
app.config['MAIL_PASSWORD'] = 'snehashish08036#@#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Setting the api url
apiurl = 'http://snehashishlaskar090.pythonanywhere.com/'
usrName = None
psword = None


def convertUserDataToJson(username):
    data = requests.get('{}sites?username={}'.format(apiurl, username)).json()
    return data


@app.route('/auth', methods=['GET', 'POST'])
def Login():
    return auth.login()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return auth.logout()


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    return render_template('delete_account.html', sess=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return auth.signup(mail, Message)


@app.route('/cookies', methods=['GET', 'POST'])
def cook():
    return jsonify(session['username'])


@app.route('/deleteusersure', methods=["GET", "POST"])
def deleteUser():
    return auth.deleteUser()


@app.route('/passwords/home', methods=["GET", "POST"])
def passwordHome():
    return redirect('/passwords/')


@app.route('/confirm/', methods=['GET', 'POST'])
def confirm():
    return auth.confirm()


@app.route('/passwords/', methods=['GET', 'POST'])
def pw():
    return passwords.home()


@app.route('/blogs/', methods=['GET', 'POST'])
def blog():
    return blogs.blog()


@app.route('/blogs/<username>', methods=['GET', 'POST'])
def userBlog(username):
    return blogs.blogUser(username)


@app.route('/blogs/newpost', methods=['POST', 'GET'])
def newpost():
    return blogs.newPost()


@app.route('/<page>', methods=['GET'])
def unknown(page):
    return render_template('error.html')


@app.route('/', methods=['GET', 'POST'])
def main():
    user = None
    pw = None

    try:
        user = session['username']
    except:
        pass

    if user != None:
        return render_template('index.html', sess=True)
    else:
        return render_template('index.html', sess=False)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
