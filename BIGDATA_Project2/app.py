# coding: utf-8

# 파이썬 2.7버전의 경우
# import sys
# if sys.version_info.major < 3:
#     reload(sys)
#sys.setdefaultencoding('utf8')

from flask import Flask, render_template, url_for,redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired,InputRequired, Email,Length
from flask import render_template, flash, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from flask_mail import Mail
import json



# 프로그램 내의 파이썬 파일
from database import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # 캐시 설정
app.config['SECRET_KEY'] = '빅데이터고려대학교6조'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///userdata.db'

db = SQLAlchemy(app)
mail = Mail(app)
Bootstrap(app)
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'

class LoginForm(FlaskForm):
    username = StringField("이메일", validators=[InputRequired()])
    password = PasswordField('비밀번호', validators=[InputRequired()])
    remember_me = BooleanField('로그인 유지')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    add_choices=[('강남구', '강남구'), ('강동구', '강동구'), ('강북구', '강북구'), ('강서구', '강서구'),('관악구', '관악구'),('광진구', '광진구'),('구로구', '구로구'),('금천구', '금천구'),('노원구', '노원구'),('도봉구', '도봉구'),('동대문구', '동대문구'),('동작구', '동작구'),('마포구', '마포구'),('서대문구', '서대문구'),('서초구', '서초구'),('성동구', '성동구'),('성북구', '성북구'),('송파구', '송파구'),('양천구', '양천구'),('영등포구', '영등포구'),('용산구', '용산구'),('은평구', '은평구'),('종로구', '종로구'),('중랑구', '중랑구'),('중구','중구')]
    email= StringField('이메일',validators=[InputRequired(),Email(message='이메일 형식으로 써주세요')])
    username = StringField('이름', validators=[InputRequired()])
    password = PasswordField('비밀번호', validators=[InputRequired()])
    address= SelectField("거주 지역",choices=add_choices, validators=[InputRequired()], coerce= str)

class User(UserMixin, db.Model ):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String())
    email= db.Column(db.String(), unique=True)
    password= db.Column(db.String())
    address= db.Column(db.String())

@app.route('/register',  methods=['GET', 'POST'])
def register():
    form= RegisterForm()
    if form.validate_on_submit():
        hashed_password= generate_password_hash(form.password.data, method='sha256')
        new_user= User(username=form.username.data, email=form.email.data, password=hashed_password, address= form.address.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>'+form.username.data+'</h1>'
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email= form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember= form.remember_me.data)
                return redirect(url_for('show_home'))
    else:
        flash('잘못된 이메일/비밀번호 입니다')
    return render_template('login.html', title='login', form=form)

@app.route('/program', methods=['get'])
def program():
    email = request.args.get('email')
    _, program_list = fetch_welfare_center_program(email)
    random_listing = define_listing()
    return render_template('program.html', data=program_list, random_listing=random_listing, email=email)

@app.route('/mypage', methods=['get'])
@login_required
def mypage():
    email = request.args.get("email")
    data = get_my_page(email)

    return render_template('mypage.html', name= current_user.username, data=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_home'))

@app.route('/')
def home():
    return render_template('coming_soon.html')
  
@app.route('/index')
def show_home():
    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username= form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember= form.remember_me.data)
                return redirect(url_for('show_home'))
    else:
        flash('잘못된 이메일/비밀번호 입니다')
    return render_template('index.html', form=form)

# @app.route('/faq')
# def faq():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password, form.password.data):
#                 login_user(user, remember=form.remember_me.data)
#                 return redirect(url_for('show_home'))
#     else:
#         flash('잘못된 이메일/비밀번호 입니다')
#     return render_template("faq.html", form=form)


@app.route('/center-detail', methods=['get'])
def center_detail_get():
    center = request.args.get("welfare")
    center_data = get_welfare_center(center)
    return render_template('center-detail.html', data= center_data)

@app.route('/center-detail', methods=['post'])
def center_review_register():

    name = request.form['name_review']
    email = request.form['email_review']
    rating = request.form['rating_review']
    content = request.form['review_text']
    location = request.form['location']

    insert_welfare_review(email, content, rating, name, location)
    center_data = get_welfare_center(location)

    return render_template('center-detail.html', data= center_data)


#
# @app.route('/mypage_bookmarks', methods=['get'])
# def my_wish():
#     email = request.args.get("email")
#
#
#     return render_template('center-detail.html', data= center_data)

@app.route('/mypage_reviews', methods=['get'])
def my_review():
    email = request.args.get("email")
    order = request.args.get("orderby", "Latest")
    order = True if order == "Latest" else False

    review_info = get_review(email, order)
    return render_template('mypage_reviews.html' , data=review_info)



@app.route('/register_wish', methods=['post'])
def reg_wish_ajax():
    info = request.form['info'][1:].split(' ')
    email = info[0]
    lecture = info[1]
    center = info[2]

    flag = request.form['class']
    if flag == "wish_bt liked":
        flag = True
    else:
        flag = False
    register_wish(email, center, lecture, flag)
    return json.dumps({'status': 'OK'})


@app.route('/<path>')
def faq(path):
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('show_home'))
    else:
        flash('잘못된 이메일/비밀번호 입니다')
    return render_template('%s.html' % path, form=form)

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
