from flask import Flask, jsonify, render_template, make_response, session, request
from flask_cors import CORS
from flask_login import LoginManager, login_user
from web_view import view
from web_control.user_mgmt import User
import os, requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #https만을 지원하는 설정을 http에서 테스트할때 필요한설정

app = Flask(__name__, static_url_path='/static')
CORS(app) #Cross Origin Resource Sharing 을 위한 코드()
app.secret_key = 'chris_server'
app.register_blueprint(view.routing_object, url_prefix='/routing') #url_prefix = 기본경로명

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(index_num):
    return User.get(index_num)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

@app.route("/")
def index():
    datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
    datas = datas.json()
    champion_name=[]
    for data in datas["data"]:
        champion_name.append(data)
    Fighter =[]
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
                                                                                                         #리스트가 빈 리스트로 초기화되었을 경우, 리스트의 인덱스에
                                                                                                        #직접값을 할당할수없다. 대신 append()메서드를 이용!

    return render_template('main.html', Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support)

@app.before_request
def app_before_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) #http request의 IP정보를 session객체에 추가해준다.

if __name__ == '__main__': #서버 띄우는건 맨 마지막줄에서 해야한다.
    app.run(host='127.0.0.1', port='5000')
