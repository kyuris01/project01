from flask import Flask, render_template
from flask_cors import CORS
from web_view import view
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #https만을 지원하는 설정을 http에서 테스트할때 필요한설정

app = Flask(__name__, static_url_path='/static')
CORS(app) #Cross Orgiin Resource Sharing 을 위한 코드()
app.secret_key = 'chris_server'
app.register_blueprint(view.routing_object, url_prefix='/routing')

@app.route("/hello")
def hello():
    return render_template('main.html')

if __name__ == '__main__': #서버 띄우는건 맨 마지막줄에서 해야한다.
    app.run(host='127.0.0.1', port='5000')
