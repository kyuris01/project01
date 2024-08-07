from flask import Flask, jsonify, render_template, make_response, session, request, flash, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user
from web_view import view
from web_control.user_mgmt import User
from web_control.session_mgmt import PageSession
import os, requests, json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #https만을 지원하는 설정을 http에서 테스트할때 필요한설정

app = Flask(__name__, static_url_path='/static')
CORS(app) #Cross Origin Resource Sharing 을 위한 코드()
app.secret_key = 'chris_server2'
app.register_blueprint(view.routing_object, url_prefix='/routing') #url_prefix = 기본경로명

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    message = "로그인 후 사용가능합니다!"
    return redirect(url_for("route.main", errmsg=message))   #redirect(url_for('route.login_page'))    #make_response(jsonify(success=False), 401)

@app.route("/")
def index():
    response = requests.get("https://ddragon.leagueoflegends.com/cdn/14.9.1/data/ko_KR/champion.json")
    champion_data = response.json()

    with open('champion_data.json', 'w') as json_file: #API호출의 제약이 있을수있으므로 서버내에 캐싱해둔다.
        json.dump(champion_data, json_file)
    
    with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
    
    champion_name =[]
    champ_name_kor_list =[]
    
    for i in champion_data["data"]:
        champion_name.append(i)
    
    for i in champion_data["data"]:
        champ_name_kor_list.append(champion_data['data'][i]['name'])
    
    Fighter = []
    Tank =[]
    Mage=[]
    Assassin=[]
    Marksman=[]
    Support=[]
    for i in range(len(champion_data["data"])): #[["aatrox", ".....png"],[],...]
        if "Fighter" in champion_data["data"][champion_name[i]]["tags"]:
            Fighter.append([champion_name[i], "../static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Tank" in champion_data["data"][champion_name[i]]["tags"]:
            Tank.append([champion_name[i], "../static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Mage" in champion_data["data"][champion_name[i]]["tags"]:
            Mage.append([champion_name[i], "../static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Assassin" in champion_data["data"][champion_name[i]]["tags"]:
            Assassin.append([champion_name[i], "../static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Marksman" in champion_data["data"][champion_name[i]]["tags"]:
            Marksman.append([champion_name[i], "../static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
        if "Support" in champion_data["data"][champion_name[i]]["tags"]:
            Support.append([champion_name[i], "../static/img/champ_img/" + champion_name[i] + ".png", champ_name_kor_list[i]])
                                                                                                         #리스트가 빈 리스트로 초기화되었을 경우, 리스트의 인덱스에
                                                                                                        #직접값을 할당할수없다. 대신 append()메서드를 이용!
# Support.append([champion_name[i], "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/" + champion_name[i] + ".png"])
    
    if current_user.is_authenticated:
        PageSession.save_session_info(session['client_id'], current_user.user_email)
        return render_template('main.html', nickname=current_user.nickname, Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support, errmsg="normal"
                               , champion_name = champion_name, champ_name_kor_list=champ_name_kor_list) #단순히 main.html을 render하면 server.py에서 들여왔던 이미지들은 로딩이 안되게됨.
    else:
        PageSession.save_session_info(session['client_id'], 'anonymous')
        return render_template('main.html', Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support, errmsg="normal",
                               champion_name=champion_name, champ_name_kor_list=champ_name_kor_list)

@app.before_request
def app_before_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) #http request의 IP정보를 session객체에 추가해준다.

if __name__ == '__main__': #서버 띄우는건 맨 마지막줄에서 해야한다.
    app.run(debug=True, host='127.0.0.1', port='5000')
