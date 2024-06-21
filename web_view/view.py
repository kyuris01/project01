from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_paginate import Pagination, get_page_args
from web_control.user_mgmt import User
from web_control.session_mgmt import PageSession
from db_model.mysql import conn_mysqldb
import datetime, requests, json


routing_object = Blueprint('route', __name__) #블루프린트객체이름 = Blueprint(블루프린트이름, __name__)
glb_champ_name = ''
posts = []

@routing_object.route('/main/<errmsg>') #메인페이지로 돌려보내는 로직
def main(errmsg):
    with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
        
    champion_name=[]
    for data in champion_data["data"]:
        champion_name.append(data)
    Fighter = []
    Tank =[]
    Mage=[]
    Assassin=[]
    Marksman=[]
    Support=[]
    for i in range(len(champion_data["data"])):
        if "Fighter" in champion_data["data"][champion_name[i]]["tags"]:
            Fighter.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/" + champion_name[i] + ".png"])
        if "Tank" in champion_data["data"][champion_name[i]]["tags"]:
            Tank.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/" + champion_name[i] + ".png"])
        if "Mage" in champion_data["data"][champion_name[i]]["tags"]:
            Mage.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/" + champion_name[i] + ".png"])
        if "Assassin" in champion_data["data"][champion_name[i]]["tags"]:
            Assassin.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/" + champion_name[i] + ".png"])
        if "Marksman" in champion_data["data"][champion_name[i]]["tags"]:
            Marksman.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/" + champion_name[i] + ".png"])
        if "Support" in champion_data["data"][champion_name[i]]["tags"]:
            Support.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/" + champion_name[i] + ".png"])
    #server.py를 import해서 이미지리스트 변수 사용하는것의 문제점 --> blueprint경로들이 꼬임                                                                                                     
    if current_user.is_authenticated:
        PageSession.save_session_info(session['client_id'], current_user.user_email)
        return render_template('main.html', nickname=current_user.nickname, Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support, errmsg=errmsg) #단순히 main.html을 render하면 server.py에서 들여왔던 이미지들은 로딩이 안되게됨.
    else:
        PageSession.save_session_info(session['client_id'], 'anonymous')
        return render_template('main.html', Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support, errmsg=errmsg)
    

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
    #print("point")
    if request.method == 'POST':
        print(request.form['nickname'], request.form['user_email'], request.form['password']) #success
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
        #print("-----------"+user.nickname+"-------")
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



@routing_object.route('/champion/<string:champ_name>')
@login_required
def product_detail(champ_name):
    #champ_name변수 이용해 해당 챔피언의 모든 데이터값 여기서 파싱한다. 파싱한값은 render_template으로 champ.html로 보내준다.
    #if current_user.is_authenticated:
    with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
    global glb_champ_name #python에서 전역변수를 사용하기 위해서는 다음과같이 global키워드와 함께 재선언을 해줘야한다
    glb_champ_name = champ_name

    # print("attack :", attack)
    # print("defense :", defense)
    # print("magic :", magic)
    # print("difficulty :", difficulty)
    # print("hp :", hp)
    
    attack = champion_data['data'][champ_name]['info']['attack']
    defense = champion_data['data'][champ_name]['info']['defense']
    magic = champion_data['data'][champ_name]['info']['magic']
    difficulty = champion_data['data'][champ_name]['info']['difficulty']
    hp = champion_data['data'][champ_name]['stats']['hp']
    hpperlevel = champion_data['data'][champ_name]['stats']['hpperlevel']
    mp = champion_data['data'][champ_name]['stats']['mp']
    mpperlevel = champion_data['data'][champ_name]['stats']['mpperlevel']
    movespeed = champion_data['data'][champ_name]['stats']['movespeed'] 
    armor = champion_data['data'][champ_name]['stats']['armor']
    armorperlevel = champion_data['data'][champ_name]['stats']['armorperlevel']
    spellblock = champion_data['data'][champ_name]['stats']['spellblock']
    spellblockperlevel = champion_data['data'][champ_name]['stats']['spellblockperlevel']
    attackrange = champion_data['data'][champ_name]['stats']['attackrange']
    hpregen = champion_data['data'][champ_name]['stats']['hpregen']
    hpregenperlevel = champion_data['data'][champ_name]['stats']['hpregenperlevel']
    mpregen = champion_data['data'][champ_name]['stats']['mpregen']
    mpregenperlevel = champion_data['data'][champ_name]['stats']['mpregenperlevel']
    crit = champion_data['data'][champ_name]['stats']['crit']
    critperlevel = champion_data['data'][champ_name]['stats']['critperlevel']
    attackdamage = champion_data['data'][champ_name]['stats']['attackdamage']
    attackdamageperlevel = champion_data['data'][champ_name]['stats']['attackdamageperlevel']
    attackspeedperlevel = champion_data['data'][champ_name]['stats']['attackspeedperlevel']
    attackspeed = champion_data['data'][champ_name]['stats']['attackspeed']
    champ_img = champion_data['data'][champ_name]['image']['full']
    #챔피언 i의 모든 데이터를 변수에 할당하고, 이를 render_template의 인자로 넣어서 리턴
    
    #처음 챔피언 상세페이지에 접속했을때 포스트 출력을 위한 로직
    mysql_db=conn_mysqldb()
    db_cursor=mysql_db.cursor()
    global posts
    sql = "SELECT content, writer, wr_date FROM user_post WHERE champ = %s ORDER BY wr_date DESC"
    db_cursor.execute(sql, (glb_champ_name))
    posts = db_cursor.fetchall()
    
    #페이지네이션을 위한 코드
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(posts) + per_page - 1) // per_page
    
    items_on_page = posts[start:end]
    
    return render_template('champ.html', items_on_page=items_on_page, total_pages=total_pages, page=page, champ_name=champ_name, attack=attack, defense=defense, magic=magic, difficulty=difficulty, hp=hp,
                            hpperlevel=hpperlevel, mp=mp, mpperlevel=mpperlevel, movespeed=movespeed, armor=armor, armorperlevel=armorperlevel,
                            spellblock=spellblock, spellblockperlevel=spellblockperlevel, attackrange=attackrange, hpregen=hpregen,
                            hpregenperlevel=hpregenperlevel,mpregen=mpregen, mpregenperlevel=mpregenperlevel, crit=crit, critperlevel=critperlevel, 
                            attackdamage=attackdamage, attackdamageperlevel=attackdamageperlevel, attackspeedperlevel=attackspeedperlevel, 
                            attackspeed=attackspeed, champ_img=champ_img)
        
        
        

    # return render_template('champ.html', champ_name=champ_name, attack=attack, defense=defense, magic=magic, difficulty=difficulty, hp=hp,
    #                         hpperlevel=hpperlevel, mp=mp, mpperlevel=mpperlevel, movespeed=movespeed, armor=armor, armorperlevel=armorperlevel,
    #                         spellblock=spellblock, spellblockperlevel=spellblockperlevel, attackrange=attackrange, hpregen=hpregen,
    #                         hpregenperlevel=hpregenperlevel,mpregen=mpregen, mpregenperlevel=mpregenperlevel, crit=crit, critperlevel=critperlevel, 
    #                         attackdamage=attackdamage, attackdamageperlevel=attackdamageperlevel, attackspeedperlevel=attackspeedperlevel, 
    #                         attackspeed=attackspeed, champ_img=champ_img, posts=posts)
    
    #else:
        #flash("로그인 후 이용가능합니다!")
        #return redirect(url_for("route.main"))
    
    
    

@routing_object.route('/post', methods=['GET','POST'])
def post():
    mysql_db=conn_mysqldb()
    db_cursor=mysql_db.cursor()
    global posts
    
    if request.method == 'POST':
        #print("POST TEST")
        nickname = current_user.nickname
        #print(nickname)
        content = request.form['content']
        sql = "INSERT INTO user_post (content, writer, champ) VALUES (%s, %s, %s)" 
        db_cursor.execute(sql, (content, nickname, glb_champ_name))                                
        mysql_db.commit()
        sql = "SELECT content, writer, wr_date FROM user_post WHERE champ = %s ORDER BY wr_date DESC"
        db_cursor.execute(sql, (glb_champ_name))
        posts = db_cursor.fetchall() #fetchall()은 SELECT 쿼리 이후에 결과 집합을 가져올 때 사용되며, INSERT 쿼리 후에는 사용할 수 없다.
        #내가 자꾸 insert하고나서 fetch하려고해서 빈 객체가 db로부터 오는것이었다...

    else:
        sql = "SELECT content, writer, wr_date FROM user_post WHERE champ = %s ORDER BY wr_date DESC"
        db_cursor.execute(sql, (glb_champ_name))
        posts = db_cursor.fetchall() #cursor.fetchall()은 2차원 배열형태로 저장하므로 각 행별결과를 보려면 인덱스로 접근
    
    
    print('glb_champ_name: ', glb_champ_name)   
    db_cursor.close()
    return redirect(url_for('route.product_detail', champ_name = glb_champ_name))
