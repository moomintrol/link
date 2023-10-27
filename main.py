from flask import Flask, render_template, request, redirect, jsonify, session
from db import *
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import uuid, hashlib, random, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
app.secret_key = os.urandom(30).hex()
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

if len(seacrAccesses()) == 0:
    i = 0
    accesses = [["public","публичный"],["private","приватный"],["general","общий"]]
    while i < len(accesses):
        addAccesses(accesses[i][0],accesses[i][1])
        i = i + 1

@app.route('/', methods=['post', 'get'])
def index():
    long_link = request.form.get('long_link')
    accesses = request.form.get('accesses')
    massage = ''
    if long_link != None:
        if 'user' in session:
            user_short_link = ""
            user_short_link = hashlib.md5(long_link.encode()).hexdigest()[:random.randint(8, 12)]
            addLink(long_link,user_short_link,accesses,session['user'])
        else:
            massage = 'Войдите чтобы сокращать ссылки'
    return render_template("index.html", massage=massage)

@app.route('/auth', methods=['post', 'get'])
def auth():
    massage = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = searchUser(login)
        if login != "" and password != "":
            if len(user) != 0:
                if check_password_hash(user[0], password) == True:
                    massage = 'Вы вошли'
                    auth_user = searchUserId(login)[0]
                    session['user'] = auth_user
                    access_token = create_access_token(identity=login)
                    # get_jwt_identity()
                    # jwt_required()
                    return redirect('/profile')
                else:
                    massage = 'Неверный пароль'
            else:
                massage = 'Такой пользователя нет'
        else:
            massage = 'Неверный логин или пароль'

    return render_template("auth.html", massage=massage)

@app.route('/reg', methods=['post', 'get'])
def reg():
    massage = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm_password')
        user = searchUser(login)
        if login != "" and password != "":
            if user == None:
                if confirmPassword == password:
                    hash_password = generate_password_hash(password)
                    registration(login, hash_password)
                else:
                    massage = 'Пароли не совпадают'
            else:
                massage = 'Такой пользователь уже зарегестрирован'
        else:
            massage = 'Неверный логин или пароль'

    return render_template("reg.html", massage=massage)

@app.route('/profile', methods=['post', 'get'])
def profile():
    return render_template("/profile.html")

if __name__ == '__main__':
    app.run()