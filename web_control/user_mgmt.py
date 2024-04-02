from flask_login import UserMixin
from db_model.mysql import conn_mysqldb

class User(UserMixin):
    def __init__(self, user_id, user_email, password):
        self.id = user_id
        self.user_email=user_email
        self.password = password

    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + str(user_id) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            db_cursor.close()
            return None
        print(user)
        user = User(user_id=user[0], user_email=user[1] password=user[2])
        db_cursor.close()
        return user
    
    @staticmethod
    def find(user_email, password):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_EMAIL = '" + str(user_email) + "AND PASSWORD = " + password
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            db_cursor.close()
            return None
        
        user = User(user_id=user[0], user_email=user[1] password=user[2])
        db_cursor.close()
        return user


    @staticmethod
    def create(user_email, password):
        user=User.find(user_email, password)
        if user == None:
            mysql_db=conn_mysqldb()
            db_cursor=mysql_db.cursor()
            sql = "INSERT INTO user_info (USER_EMAIL, PASSWORD) VALUES ('%s', '%s')" % (str(user_email), password)
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_email, password)
        else:
            return user

