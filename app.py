from flask import Flask, flash, render_template, request, redirect, url_for, make_response, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.secret_key = 'hellosarpens'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Userlogpass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    if not request.cookies.get('dataxd'):
        return "<center><h1>Seems like you're not logged in...</h1></center>" + render_template('reg.html')
    else:
        return render_template('index.html')

@app.route("/regs")
def regs():
    return render_template('reg.html')

@app.route("/cookiedelete")
def cookiedelete():
    return render_template('cookie_delete.html')


@app.route("/login")
def log():
    return render_template('login.html')

@app.post("/regs")
def reg():
    iusr = request.form.get("iusr")
    ipass = request.form.get("ipass")
    if iusr and ipass == db.session.query(Userlogpass):
        login = Userlogpass(username=iusr, password=ipass)
        db.session.add(login)
        db.session.commit()
        return redirect( url_for('login') )
    else:
        return '<center><h5>account already exists, please log in</h5></center>' + render_template('login.html')
    #регистрация пользователя + занесение в DB

@app.route("/login", methods = ['POST', 'GET']) 
def login():
    usr = {"username": request.form.get("iusrku"), "password":request.form.get("ipassku")}
    exists = db.session.query(Userlogpass).filter_by(username=usr["username"], password=usr["password"]).first()
    if exists != None:
        resp = make_response(redirect( url_for('index') ))
        resp.set_cookie('dataxd', usr['username'], max_age=300000)
        return resp
    else :
        return '<center><h5>account not found, sign up instead</h5></center>' + render_template('reg.html')
    #логин пользователя + чек по DB

@app.route('/', methods=['GET', 'POST'])
def removecookie():
    res = make_response(redirect( url_for('cookiedelete') ))
    res.set_cookie('dataxd', max_age=0)
    return res
    #удаление cookie


if __name__ == '__main__':
    app.run()