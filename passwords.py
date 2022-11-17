from flask import *
apiurl = 'http://snehashishlaskar090.pythonanywhere.com/'
import requests

def convertUserDataToJson(username):
    data = requests.get('{}sites?username={}'.format(apiurl, username)).json()
    return data

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
            return redirect('/passwords/home')
        
        elif 'del' in request.form:
            name = request.form['name']

            query = requests.delete('{}delsite?username={}&site={}'.format(
                apiurl,
                session['username'],
                name
            ))

            return redirect('/passwords/home')
    elif request.method == 'GET':
        return render_template('home.html', sess = True, data = convertUserDataToJson(session['username']))