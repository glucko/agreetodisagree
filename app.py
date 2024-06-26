from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from flask_assets import Environment, Bundle
from werkzeug.exceptions import abort
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
assets = Environment(app)

#TODO: fix site, add new pages, add interests, add login
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createuser', methods=['POST', 'GET'])
def createuser():
    if request.method == 'GET':
        return render_template('createuser.html')
    conn = connectDB()
    name = request.form['name']
    email = request.form['email']
    interests = request.form['interests']
    conn.execute("INSERT INTO USERS (EMAIL,NAME, INTERESTS) VALUES (?,?, ?)",(email, name, interests));
    conn.commit()
    conn.close()
    return redirect(url_for('displayusers'))

@app.route('/displayusers')
def displayusers():
    conn = connectDB()
    users = conn.execute('SELECT * FROM users').fetchall()
    userid = conn.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1").fetchone()[0]
    conn.close()
    return render_template('displayusers.html', users=users, id=userid)

@app.route('/getUser/', methods=['GET'])
def getUser():
    requestData = request.args
    id = requestData['id']
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT * from USERS WHERE id = ?", id)
    user = {
      'id': "",
      'name': "",
      'email': "",
      'interests': ""
    }
    for row in cursor:
      user['id'] = row[0]
      user['email'] = row[1]
      user['name'] = row[2]
      user['interests'] = row[3]
    conn.close()
    response = jsonify(user)
    
    return response, 200

@app.route('/chat/<int:id>/<int:userid>')
def chat(id, userid):
    currentuser = connectDB().execute("SELECT * FROM USERS WHERE id = ?", (userid,)).fetchone()
    otheruser = connectDB().execute("SELECT * FROM USERS WHERE id = ?", (id,)).fetchone()
    return render_template('chat.html', other=otheruser, currentuser=currentuser)

def connectDB():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return conn;
