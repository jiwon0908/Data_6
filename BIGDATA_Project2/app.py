# 설치해야 할 외부 라이브러리
from flask import Flask, render_template, url_for
from flask_mail import Mail
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 프로그램 내의 파이썬 파일
from config import Config
from database import *

app = Flask(__name__)

admin = Admin(app, name='microblog', template_mode='bootstrap4')
# Add administrative views here

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # 캐시 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '빅데이터고려대학교6조'
app.config.from_object(Config)
mail = Mail(app)


class User(db.Model):
    __tablename__ = "user_data"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.Text(10), unique=False, nullable=False)
    culture_view = db.Column(db.Float(20), unique=False, nullable=False)
    culture_parti = db.Column(db.Float(20), unique=False, nullable=False)
    sport_view = db.Column(db.Float(20), unique=False, nullable=False)
    sport_parti = db.Column(db.Float(20), unique=False, nullable=False)
    sightsee = db.Column(db.Float(20), unique=False, nullable=False)
    entertain = db.Column(db.Float(20), unique=False, nullable=False)
    rest = db.Column(db.Float(20), unique=False, nullable=False)
    social_act = db.Column(db.Float(20), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

#me = User()
#db.session.add(me)
#db.session.commit()

@app.route('/')
def show_home():
    return render_template('coming_soon.html')

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/<path>')
def show_path(path):
    return render_template('%s.html' % path)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True)