from flask import *
import requests
import db

def blog():
    if 'username' in session:
        if session['username'] == '':
            return redirect('/auth/')
        else:
            data = db.readUserDb(session['username'])
            data.reverse()
            return render_template('blogs.html', data=data, sess = True)
    else:
        return redirect('/auth')


def blogUser(username):
    data = db.readUserDb(username)
    data.reverse()
    if session['username'] == None:
        return render_template('blogs.html', data=data, sess = False)
    return render_template('blogs.html', data=data, sess = True)

def newPost():

    if request.method == 'GET':
        return render_template('add-post.html')
    else:
        if session ['username'] == None:
            return redirect('/auth')

        title = request.form['title']
        date = request.form['date']
        txt = request.form['txt']
        body = txt.split('\r\n')

        db.addPost(session['username'], title, date, body)
        return redirect('/blogs/')