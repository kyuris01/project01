from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_paginate import Pagination, get_page_args
from web_control.user_mgmt import User
from web_control.session_mgmt import PageSession
from db_model.mysql import conn_mysqldb
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import datetime, requests, json
import re

load_dotenv(find_dotenv())

routing_object = Blueprint('route', __name__) #블루프린트객체이름 = Blueprint(블루프린트이름, __name__)
glb_champ_name = ''
posts = []
click_num = {} #챔프별 클릭수 저장
sorted_champ = [] #[('Aatrox',13),('Camille',10),...]

def regex_pw (pw):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
    if re.match(pattern, pw):
        return True
    else:
        return False
    
@routing_object.route('/main/<errmsg>') #메인페이지로 돌려보내는 로직
def main(errmsg):
    with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
        
    champion_name = []
    champ_name_kor_list = []
    for data in champion_data["data"]:
        champion_name.append(data)
    
    for i in champion_data["data"]:
        champ_name_kor_list.append(champion_data["data"][i]['name'])
    Fighter = []
    Tank =[]
    Mage=[]
    Assassin=[]
    Marksman=[]
    Support=[]
    Hottest = []
    for i in range(len(champion_data["data"])):
        if "Fighter" in champion_data["data"][champion_name[i]]["tags"]:
            Fighter.append([champion_name[i], "/static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Tank" in champion_data["data"][champion_name[i]]["tags"]:
            Tank.append([champion_name[i], "/static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Mage" in champion_data["data"][champion_name[i]]["tags"]:
            Mage.append([champion_name[i], "/static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Assassin" in champion_data["data"][champion_name[i]]["tags"]:
            Assassin.append([champion_name[i], "/static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Marksman" in champion_data["data"][champion_name[i]]["tags"]:
            Marksman.append([champion_name[i], "/static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Support" in champion_data["data"][champion_name[i]]["tags"]:
            Support.append([champion_name[i], "/static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
    #server.py를 import해서 이미지리스트 변수 사용하는것의 문제점 --> blueprint경로들이 꼬임
    
    for i in range(len(sorted_champ)):
        #print("sortedchamp :", sorted_champ)
        Hottest.append([sorted_champ[i][0],"/static/img/champ_img/" + sorted_champ[i][0] + ".png", champion_data["data"][sorted_champ[i][0]]['name']])
    
                                                                                                         
    if current_user.is_authenticated:
        PageSession.save_session_info(session['client_id'], current_user.user_email)
        return render_template('main.html', nickname=current_user.nickname, Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support, Hottest=Hottest, 
                               errmsg=errmsg, champion_name=champion_name, champ_name_kor_list=champ_name_kor_list) #단순히 main.html을 render하면 server.py에서 들여왔던 이미지들은 로딩이 안되게됨.
    else:
        PageSession.save_session_info(session['client_id'], 'anonymous')
        return render_template('main.html', Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support, Hottest=Hottest, errmsg=errmsg
                               , champion_name=champion_name, champ_name_kor_list=champ_name_kor_list)
    

@routing_object.route('/register_page') #회원가입 페이지 접근 로직
def register_page():
    return render_template('register.html')


@routing_object.route('/login_page') #로그인 페이지 접근 로직
def login_page():
    return render_template('login.html')

@routing_object.route('return_address')
def return_address():
    return jsonify({"result" : "localhost:5000/routing/login_page"})

@routing_object.route('/register_function', methods=['GET','POST'])
def register_function():
    if request.method == 'POST':
        if not regex_pw(request.form['password']):
            return render_template('register.html', error=True)
        else:
            user = User.create(request.form['nickname'], request.form['user_email'], request.form['password']) #request.form : HTML POST 폼의 body 안의 키/값 쌍. 또는 JSON 인코딩이 아닌 자바스크립트 요청
            if user == 'already exist':
                return render_template('register.html', info1='exist', info2=request.form['user_email'])
            else:
                return render_template("register.html", info1='new', info2=request.form['user_email'])
   
    
@routing_object.route('/member_check', methods=['GET', 'POST']) #로그인 로직
def member_check():
    user = User.find(request.form['user_email'], request.form['password'])
    if user == None: #회원이 아닌 사용자의 로그인
        return render_template('login.html', validation=False)
    else:
        login_user(user, remember=True, duration=datetime.timedelta(days=365)) #사용자 세션 생성
        return redirect(url_for('route.main', errmsg="normal")) #redirect(url_for('route.main', nickname=user.nickname))
    
    
@routing_object.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('route.main', errmsg="normal")) #redirect(url_for('함수이름'))

@routing_object.route('/withdraw')
def withdraw():
    User.delete(current_user.user_id) #current_user객체를 이용해 현재 사용자의 정보에 접근가능
    flash("회원탈퇴 완료!")
    return redirect(url_for('route.main', errmsg="normal"))

@routing_object.route('/delete_post/<int:writer_id>/<int:post_num>', methods=['POST'])
def delete_post(writer_id, post_num):
    if writer_id == current_user.user_id:
        mysql_db=conn_mysqldb()
        db_cursor=mysql_db.cursor()
        sql = "DELETE FROM user_post WHERE post_num = %s"
        db_cursor.execute(sql, (post_num))                                
        mysql_db.commit()
        flash("삭제 완료!")
        db_cursor.close()
    else:
        flash("자신이 작성한 글만 지울수 있습니다!")
    return redirect(url_for('route.product_detail', champ_name = glb_champ_name))


@routing_object.route('/champion/<string:champ_name>')
@login_required
def product_detail(champ_name):
    #champ_name변수 이용해 해당 챔피언의 모든 데이터값 여기서 파싱한다. 파싱한값은 render_template으로 champ.html로 보내준다.
    #if current_user.is_authenticated:
    with open('champion_data.json', 'r') as json_file:
        champion_raw_data = json.load(json_file)
    global glb_champ_name #python에서 전역변수를 사용하기 위해서는 다음과같이 global키워드와 함께 재선언을 해줘야한다
    glb_champ_name = champ_name
    global click_num
    global sorted_champ
    
    #챔피언 이미지와 이름 데이터 파싱
    champ_name_list=[]
    champ_data = []
    for data in champion_raw_data["data"]:
        champ_name_list.append(data)
    champ_name_kor_list = []
    for i in champion_raw_data["data"]:
        champ_name_kor_list.append(champion_raw_data["data"][i]['name'])    
    
    for i in range(len(champion_raw_data["data"])):
       champ_data.append([champ_name_kor_list[i], "/static/img/champ_img/" + champ_name_list[i] + ".png"])
    champ_name_kor = champion_raw_data['data'][champ_name]['name']
    champ_title = champion_raw_data['data'][champ_name]['title']
    champ_blurb = champion_raw_data['data'][champ_name]['blurb']
    champ_tags = champion_raw_data['data'][champ_name]['blurb']
    
    #챔프별 클릭수 계산 후 sorting
    if champ_name in click_num:
        click_num[champ_name] = click_num[champ_name] + 1
    else:
        click_num[champ_name] = 1
    #print(click_num[champ_name])
    sorted_champ = sorted(click_num.items(), key = lambda x : x[1], reverse=True)
    
    attack = champion_raw_data['data'][champ_name]['info']['attack']
    defense = champion_raw_data['data'][champ_name]['info']['defense']
    magic = champion_raw_data['data'][champ_name]['info']['magic']
    difficulty = champion_raw_data['data'][champ_name]['info']['difficulty']
    
    champ_img = champion_raw_data['data'][champ_name]['image']['full']
    champ_tags = champion_raw_data['data'][champ_name]['tags']
    #챔피언 i의 모든 데이터를 변수에 할당하고, 이를 render_template의 인자로 넣어서 리턴
    
    
    #처음 챔피언 상세페이지에 접속했을때 포스트 출력을 위한 로직
    mysql_db=conn_mysqldb()
    db_cursor=mysql_db.cursor()
    global posts
    sql = "SELECT post_num, content, user_id, writer, wr_date FROM user_post WHERE champ = %s ORDER BY wr_date DESC"
    db_cursor.execute(sql, (glb_champ_name))
    posts = db_cursor.fetchall()
    db_cursor.close()
    #페이지네이션을 위한 코드
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(posts) + per_page - 1) // per_page
    
    items_on_page = posts[start:end]
    
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    return render_template('champ.html', items_on_page=items_on_page, total_pages=total_pages, page=page, champ_name=champ_name, 
                           attack=attack, defense=defense, magic=magic, difficulty=difficulty,
                             champ_img=champ_img, openai_api_key= openai_api_key, champ_data=champ_data, 
                             champ_name_kor_list=champ_name_kor_list, champ_name_kor = champ_name_kor, 
                             champ_title=champ_title, champ_blurb=champ_blurb, champ_tags=champ_tags
                             , YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY"))

    

@routing_object.route('/post', methods=['GET','POST']) #챔프상세페이지에서 코멘트 작성하는 로직
def post():
    mysql_db=conn_mysqldb()
    db_cursor=mysql_db.cursor()
    global posts
    if request.method == 'POST':
        nickname = current_user.nickname
        user_id = current_user.user_id
        content = request.form['content']
        sql = "INSERT INTO user_post (content, user_id, writer, champ) VALUES (%s, %s, %s, %s)" 
        db_cursor.execute(sql, (content, user_id, nickname, glb_champ_name))                                
        mysql_db.commit()
        sql = "SELECT post_num, content, user_id, writer, wr_date FROM user_post WHERE champ = %s ORDER BY wr_date DESC"
        db_cursor.execute(sql, (glb_champ_name))
        posts = db_cursor.fetchall() 
        #fetchall()은 SELECT 쿼리 이후에 결과 집합을 가져올 때 사용되며, INSERT 쿼리 후에는 사용할 수 없다.
        #내가 자꾸 insert하고나서 fetch하려고해서 빈 객체가 db로부터 오는것이었다...

    else:
        sql = "SELECT post_num, content, writer, wr_date FROM user_post WHERE champ = %s ORDER BY wr_date DESC"
        db_cursor.execute(sql, (glb_champ_name))
        posts = db_cursor.fetchall() #cursor.fetchall()은 2차원 배열형태로 저장하므로 각 행별결과를 보려면 인덱스로 접근
    
    
    #print('glb_champ_name: ', glb_champ_name)   
    db_cursor.close()
    return redirect(url_for('route.product_detail', champ_name = glb_champ_name))

@routing_object.route('/env', methods=["POST"])
def env():
    return jsonify({"key" : os.getenv("OPENAI_API_KEY")})

@routing_object.route('/translate', methods=['GET'])
def translate():
    with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
        
    champion_name = []
    champ_name_kor_list = []
    for data in champion_data["data"]:
        champion_name.append(data)
    
    for i in champion_data["data"]:
        champ_name_kor_list.append(champion_data["data"][i]['name'])
    
    
    name_dict = {}
    for i in range(len(champion_name)):
        name_dict[champ_name_kor_list[i]] = champion_name[i]
    #print(name_dict)    
    return jsonify(name_dict)

# @routing_object.route('/opponent')
# def opponent():
    