from flask import *
from DB import *
import blogdb as blog
api = Flask(__name__)

@api.route('/', methods=['GET'])
def data():
    try:
        if request.args == {}:
            return jsonify(listAllAuthData())

        elif 'username' in request.args:

            return jsonify(selectiveUsername(request.args['username']))
    except Exception as err:
        return str(err)

@api.route('/createuser', methods=['POST'])
def addUsers():
    try:
        if request.method == 'POST':

            username = request.args['username']
            password = request.args['password']

            try:
                return jsonify(addUser(username, password))

            except:
                abort (404)

        else:
            return 'sorry'
    except Exception as err:
        return str(err)


@api.route('/addsite', methods=['POST'])
def addsite():
    try:
        username = request.args['username']
        sitename = request.args['sitename']
        email = request.args['email']
        password = request.args['password']
        siteusername = request.args['siteusrname']

        try:
            addSite(username, sitename, email, password, siteusername)
            return jsonify(fetchAllUserdata(username))
        except Exception as excep:
            return str(excep)
    except Exception as er:
        return str(er)
    
@api.route('/sites', methods=['GET'])
def sites():
    try:
        if request.args == {}:
            return 'not enough arguments'
        else:
            return jsonify(convertUserDataToJson(request.args['username'])) 

    except Exception as er:
        return str(er)


@api.route('/delsite', methods=['DELETE'])
def delsite():
    try:
        if request.method == 'DELETE':
            try:
                username = request.args['username']
                site = request.args['site']

                deletesite(username, site)
                return jsonify(convertUserDataToJson(request.args['username'])) 
            except Exception as ex:
                return str(ex)
    except Exception as ex:
        return str(ex)


@api.route('/delete', methods=['DELETE'])
def deleteuser():
    try:
        if request.method == 'DELETE':
            try:
                username = request.args['username']
                deleteUser(username)
                
                return jsonify(convertUserDataToJson(request.args['username'])) 
            except Exception as ex:
                return str(ex)
    except Exception as ex:
        return str(ex)

@api.route('/blogs/', methods = ['GET', 'POST'])
def blogs():
    try:
        if request.method == 'GET':
            if 'user' in request.headers:
                return jsonify(blog.readUserDb(request.headers['user']))
            else:
                return jsonify(blog.readDb())
                
        elif request.method == 'POST':
            user = request.json['user']
            title = request.json['title']
            date = request.json['date']
            body = request.json['body']

            blog.addPost(
                user,title, date, body
            )
            return jsonify({
                'response':200,
                'operation':'success',
                'body':blog.readDb()
            })
    except Exception as ex:
        return str(ex)
        
if __name__ == '__main__':
    api.run(debug=True, host = '0.0.0.0', port=8000)