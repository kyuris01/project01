from flask import Flask, jsonify, render_template, make_response, session, request
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user
from web_view import view
from web_control.user_mgmt import User
import os, requests, json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #https만을 지원하는 설정을 http에서 테스트할때 필요한설정

app = Flask(__name__, static_url_path='/static')
CORS(app) #Cross Origin Resource Sharing 을 위한 코드()
app.secret_key = 'chris_server'
app.register_blueprint(view.routing_object, url_prefix='/routing') #url_prefix = 기본경로명

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

@app.route("/")
def index():
    response = requests.get("https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/champion.json")
    champion_data = response.json()

    with open('champion_data.json', 'w') as json_file: #API호출의 제약이 있을수있으므로 서버내에 캐싱해둔다.
        json.dump(champion_data, json_file)
    
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
                                                                                                         #리스트가 빈 리스트로 초기화되었을 경우, 리스트의 인덱스에
                                                                                                        #직접값을 할당할수없다. 대신 append()메서드를 이용!

    return render_template('main.html', Fighter=Fighter, Tank=Tank, Mage=Mage, Assassin=Assassin, Marksman=Marksman, Support=Support)

@app.before_request
def app_before_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) #http request의 IP정보를 session객체에 추가해준다.

if __name__ == '__main__': #서버 띄우는건 맨 마지막줄에서 해야한다.
    app.run(host='127.0.0.1', port='5000')
