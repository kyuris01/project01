from db_model.mongodb import conn_mongodb
from datetime import datetime

class PageSession():
    
    @staticmethod
    def save_session_info(session_ip, user_email):
        now = datetime.now()
        now_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        mongo_db = conn_mongodb()
        mongo_db.insert_one({
            'session_ip':session_ip,
            'user_email':user_email,
            'access_time':now_time
        })