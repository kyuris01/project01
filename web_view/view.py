from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_login import login_user, current_user, logout_user
from web_control.user_mgmt import User
from web_control.session_mgmt import PageSession
import datetime, requests


routing_object = Blueprint('route', __name__) #블루프린트객체이름 = Blueprint(블루프린트이름, __name__)


@routing_object.route('/main') #메인페이지로 돌려보내는 로직
def main():
    datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
    datas = datas.json()
    champion_name=[]
    for data in datas["data"]:
        champion_name.append(data)
    Fighter = []
    Tank =[]
    Mage=[]
    Assassin=[]
    Marksman=[]
    Support=[]
    for i in range(len(datas["data"])):
        if "Fighter" in datas["data"][champion_name[i]]["tags"]:
            Fighter.append("http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png")
        if "Tank" in datas["data"][champion_name[i]]["tags"]:
            Tank.append("http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png")
        if "Mage" in datas["data"][champion_name[i]]["tags"]:
            Mage.append("http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png")
        if "Assassin" in datas["data"][champion_name[i]]["tags"]:
            Assassin.append("http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png")    
        if "Marksman" in datas["data"][champion_name[i]]["tags"]:
            Marksman.append("http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png")
        if "Support" in datas["data"][champion_name[i]]["tags"]:
            Support.append("http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champion_name[i] + ".png")
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
    return redirect(url_for('route.main'))
        