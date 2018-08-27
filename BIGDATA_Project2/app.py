# coding: utf-8

import sys
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, url_for,redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired,InputRequired, Email,Length
from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from flask_mail import Mail

import pandas as pd
import json

import json

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
    survey_choices=[(0, '예'), (1, '아니오')]
    email= StringField('이메일',validators=[InputRequired(),Email(message='이메일 형식으로 써주세요')])
    username = StringField('이름', validators=[InputRequired()])
    password = PasswordField('비밀번호', validators=[InputRequired()])
    address= SelectField("거주 지역",choices=add_choices, validators=[InputRequired()], coerce= str)
    health= RadioField('1. 귀하는 건강을 위한 여가활동을 원하십니까?', validators=[InputRequired()], choices=survey_choices)
    group = RadioField("2. 귀하는 단체활동을 선호하십니까?", validators=[InputRequired()], choices=survey_choices)
    self_develop= RadioField("3. 귀하는 자기 개발 프로그램을 원하십니까?", validators=[InputRequired()], choices=survey_choices)
    IT= RadioField("4. 귀하는 스마트폰, 컴퓨터에 관심이 많으십니까?", validators=[InputRequired()], choices=survey_choices)
    sports = RadioField("5. 귀하는 운동을 좋아하십니까?", validators=[InputRequired()], choices=survey_choices)
    music = RadioField("6. 귀하는 음악을 좋아하십니까?", validators=[InputRequired()], choices=survey_choices)
    history = RadioField("7. 귀하는 역사 관심이 많으십니까?", validators=[InputRequired()], choices=survey_choices)
    study = RadioField("8. 귀하는 새로운 지식 관심이 많으십니까?", validators=[InputRequired()], choices=survey_choices)
    walk = RadioField("9. 귀하는 산책을 좋아하십니까?", validators=[InputRequired()], choices=survey_choices)
    art = RadioField("10. 귀하는 문화, 예술에 관심이 많으십니까?", validators=[InputRequired()], choices=survey_choices)
    handicap = RadioField("11. 귀하는 현재 몸에 불편한 곳이 있습니까?", validators=[InputRequired()], choices=survey_choices)
    indoor= RadioField("12. 귀하는 실내 활동을 좋아합니까?", validators=[InputRequired()], choices=survey_choices)

class User(UserMixin, db.Model ):
    id= db.Column(db.Integer, primary_key=True, nullable=False)
    username= db.Column(db.String(), nullable=False)
    email= db.Column(db.String(), unique=True, nullable=False)
    password= db.Column(db.String(), nullable=False)
    address= db.Column(db.String(), nullable=False)
    health= db.Column(db.Integer(), nullable=True)
    group= db.Column(db.Integer(),nullable=True)
    self_develop= db.Column(db.Integer(),nullable=True)
    IT= db.Column(db.Integer(),nullable=True)
    sports= db.Column(db.Integer(),nullable=True)
    music= db.Column(db.Integer(),nullable=True)
    history= db.Column(db.Integer(),nullable=True)
    walk= db.Column(db.Integer(),nullable=True)
    art = db.Column(db.Integer(),nullable=True)
    handicap = db.Column(db.Integer(),nullable=True)
    indoor = db.Column(db.Integer(),nullable=True)
    culture_view= db.Column(db.REAL(),nullable=True)
    culture_parti = db.Column(db.REAL(),nullable=True)
    sport_view= db.Column(db.REAL(),nullable=True)
    sport_parti = db.Column(db.REAL(),nullable=True)
    sightsee = db.Column(db.REAL(),nullable=True)
    entertain = db.Column(db.REAL(),nullable=True)
    rest = db.Column(db.REAL(),nullable=True)
    social_act = db.Column(db.REAL(),nullable=True)

class Survey(FlaskForm):
    user=StringField()

@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password= generate_password_hash(form.password.data, method='sha256')
        new_user= User(username=form.username.data, email=form.email.data, password=hashed_password, address= form.address.data)
        db.session.add(new_user)
        db.session.commit()
        form.email.default = form.email.data
        form.username.default = form.username.data
        print("!!!!!")
        return render_template('survey.html', form=form)
    return render_template('register.html', form=form)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method=='POST':
        form = RegisterForm()
        form.email.default= form.email.data
        form.username.default= form.username.data
    return render_template('survey.html', form= form)


@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method== 'POST':
        form= RegisterForm()
        user= User.query.filter_by(email= form.email.data).first()
        if user:
            user.health= form.health.data
            user.group= form.group.data
            user.self_develop= form.self_develop.data
            user.IT= form.IT.data
            user.sports= form.sports.data
            user.music= form.music.data
            user.history= form.history.data
            user.walk= form.walk.data
            user.art= form.art.data
            user.handicap= form.handicap.data
            user.indoor= form.indoor.data

            sql= sql = "select culture_view, culture_parti, sport_view, sport_parti , sightsee, entertain, rest , social_act from question_score"
            result = engine.execute(sql)
            question_scores = pd.DataFrame(result.fetchall(),
                                           columns=(
                                           '문화예술관람활동', '문화예술참여활동', '스포츠관람활동', '스포츠참여활동', '관광활동', '취미오락활동', '휴식활동',
                                           '사회활동'))

            select_list= [form.health.data, form.group.data, form.self_develop.data, form.IT.data, form.sports.data, form.music.data, form.history.data, form.walk.data, form.art.data, form.handicap.data, form.indoor.data]
            user_scores = pd.DataFrame(columns=(question_scores.columns))

            for index, data in enumerate(select_list):
                user_scores = user_scores.append(question_scores.iloc[2 * index + int(data)], ignore_index=True)
            user_scores = user_scores.sum(axis=0)

            user.culture_view= user_scores['문화예술관람활동']
            user.culture_parti = user_scores['문화예술참여활동']
            user.sport_view = user_scores['스포츠관람활동']
            user.sport_parti = user_scores['스포츠참여활동']
            user.sightsee = user_scores['관광활동']
            user.entertain = user_scores['취미오락활동']
            user.rest = user_scores['휴식활동']
            user.social_act = user_scores['사회활동']
            db.session.commit()
            new_form= LoginForm()
    return render_template('index.html', form= new_form)

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

@app.route('/activities', methods=['get'])
def activity():
    email = request.args.get('email')
    act_list = fetch_activity(email)
    random_listing = define_listing()
    return render_template('activities.html', data=act_list, random_listing=random_listing, email=email)

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

@app.route('/mypage_reviews', methods=['get'])
def my_review():
    email = request.args.get("email")
    order = request.args.get("orderby", "Latest")
    order = True if order == "Latest" else False

    review_info = get_review(email, order)
    return render_template('mypage_reviews.html' , data=review_info)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/register_wish', methods=['post'])
def reg_wish_ajax():
    info = request.form['info'][1:].split(' ')
    email = info[0]
    lecture = info[1]
    center = info[2]
    category = info[3]

    flag = request.form['class']
    if flag == "wish_bt liked":
        flag = True
    else:
        flag = False
    register_wish(email, center, lecture,category, flag)
    return json.dumps({'status': 'OK'})

@app.route('/remove_wish', methods=['post'])
def remove_wish_ajax():
    info = request.form['info'][1:].split(' ')
    email = info[0]
    lecture = info[1]
    center = info[2]

    remove_wish(email, lecture, center)
    return json.dumps({'status': 'OK'})


@app.route('/faq')
def faq():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('show_home'))
    else:
        flash('잘못된 이메일/비밀번호 입니다')
    return render_template('faq.html', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/<path>')
def path(path):
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
