from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_login import login_user, current_user, logout_user
from web_control.user_mgmt import User
from web_control.session_mgmt import PageSession
import datetime, requests, json


routing_object = Blueprint('route', __name__) #블루프린트객체이름 = Blueprint(블루프린트이름, __name__)


@routing_object.route('/main') #메인페이지로 돌려보내는 로직
def main():
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
            Fighter.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png"])
        if "Tank" in champion_data["data"][champion_name[i]]["tags"]:
            Tank.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png"])
        if "Mage" in champion_data["data"][champion_name[i]]["tags"]:
            Mage.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png"])
        if "Assassin" in champion_data["data"][champion_name[i]]["tags"]:
            Assassin.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png"])
        if "Marksman" in champion_data["data"][champion_name[i]]["tags"]:
            Marksman.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png"])
        if "Support" in champion_data["data"][champion_name[i]]["tags"]:
            Support.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png"])
    #server.py를 import해서 이미지리스트 변수 사용하는것의 문제점 --> blueprint경로들이 꼬임                                                                                                     
    if current_user.is_authenticated:
        PageSession.save_session_info(session['client_id'], current_user.user_email)
        return render_template('main.html', nickname=current_user.nickname, Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support) #단순히 main.html을 render하면 server.py에서 들여왔던 이미지들은 로딩이 안되게됨.
    else:
        PageSession.save_session_info(session['client_id'], 'anonymous')
        return render_template('main.html', Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support)
    

@routing_object.route('/register_page') #회원가입 페이지 접근 로직
def register_page():
    return render_template('register.html')


@routing_object.route('/login_page') #로그인 페이지 접근 로직
def login_page():
    return render_template('login.html')


@routing_object.route('/register_function', methods=['GET','POST'])
def register_function():
    #print("point")
    if request.method == 'POST':
        print(request.form['nickname'], request.form['user_email'], request.form['password']) #success
        user = User.create(request.form['nickname'], request.form['user_email'], request.form['password']) #request.form : HTML POST 폼의 body 안의 키/값 쌍. 또는 JSON 인코딩이 아닌 자바스크립트 요청
        if user == 'already exist':
            return render_template('register.html', info1='exist', info2=request.form['user_email'])
        else:
            print("hihi")
            return render_template("register.html", info1='new', info2=request.form['user_email'])
   
    
@routing_object.route('/member_check', methods=['GET', 'POST']) #로그인 로직
def member_check():
    user = User.find(request.form['user_email'], request.form['password'])
    if user == None: #회원이 아닌 사용자의 로그인
        return render_template('login.html', validation=False)
    else:
        login_user(user, remember=True, duration=datetime.timedelta(days=365))
        print("-----------"+user.nickname+"-------")
        return redirect(url_for('route.main', nickname=user.nickname))
    
    
@routing_object.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('route.main')) #redirect(url_for('함수이름'))

@routing_object.route('/withdraw')
def withdraw():
    User.delete(current_user.user_id) #current_user객체를 이용해 현재 사용자의 정보에 접근가능
    flash("회원탈퇴 완료!")
    return redirect(url_for('route.main'))



@routing_object.route('/champion/<string:champ_name>')
def product_detail(champ_name):
    #champ_name변수 이용해 해당 챔피언의 모든 데이터값 여기서 파싱한다. 파싱한값은 render_template으로 champ.html로 보내준다.
    with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
    
    
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
    #챔피언 i의 모든 데이터를 변수에 할당하고, 이를 rendeR_template의 인자로 넣어서 리턴

    return render_template('champ.html', champ_name=champ_name, attack=attack, defense=defense, magic=magic, difficulty=difficulty, hp=hp,
                            hpperlevel=hpperlevel, mp=mp, mpperlevel=mpperlevel, movespeed=movespeed, armor=armor, armorperlevel=armorperlevel,
                            spellblock=spellblock, spellblockperlevel=spellblockperlevel, attackrange=attackrange, hpregen=hpregen,
                            hpregenperlevel=hpregenperlevel,mpregen=mpregen, mpregenperlevel=mpregenperlevel, crit=crit, critperlevel=critperlevel, 
                            attackdamage=attackdamage, attackdamageperlevel=attackdamageperlevel, attackspeedperlevel=attackspeedperlevel, 
                            attackspeed=attackspeed, champ_img=champ_img)
       
