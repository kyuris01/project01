from flask import Flask, render_template
from flask_cors import CORS
from web_view import view
import os, requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #https만을 지원하는 설정을 http에서 테스트할때 필요한설정

app = Flask(__name__, static_url_path='/static')
CORS(app) #Cross Origin Resource Sharing 을 위한 코드()
app.secret_key = 'chris_server'
app.register_blueprint(view.routing_object, url_prefix='/routing')

@app.route("/")
def index():
    champion = []
    datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
    datas = datas.json()
    for data in datas["data"]:
        champion.append(data) #champion = ["Aatrox", "Ahri",...]   
    image_url = []
    for champ in champion:
        image_url.append("http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champ + ".png") #리스트가 빈 리스트로 초기화되었을 경우, 리스트의 인덱스에
                                                                                                            #직접값을 할당할수없다. 대신 append()메서드를 이용!

    return render_template('main.html', image_url=image_url)
#다음할것:챔피언 역할별로 이미지분류해서 html로 보내기
@app.route("/hello")
def hello():
    return render_template('main.html')

if __name__ == '__main__': #서버 띄우는건 맨 마지막줄에서 해야한다.
    app.run(host='127.0.0.1', port='5000')
