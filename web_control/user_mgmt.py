from flask_login import UserMixin
from db_model.mysql import conn_mysqldb

class User(UserMixin):
    def __init__(self, user_id, nickname, user_email, password):
        self.id = user_id
        self.nickname = nickname
        self.user_email=user_email
        self.password = password

    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE user_id = '" + str(user_id) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            db_cursor.close()
            return None
        print(user)
        user = User(user_id=user[0], user_email=user[1], password=user[2])
        db_cursor.close()
        return user
    
    @staticmethod
    def find(user_email, password):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE user_email = '" + str(user_email) + "' AND password = '" + str(password) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        
        user = User(user_id=user[0], nickname=user[1], user_email=user[2], password=user[3])
        
        return user


    @staticmethod
    def create(nickname, user_email, password): #회원가입 로직
        user=User.find(user_email, password)
        if user == None:
            mysql_db=conn_mysqldb()
            db_cursor=mysql_db.cursor()
            sql = "INSERT INTO user_info (nickname, user_email, password) VALUES (%s, %s, %s)" % (str(nickname), str(user_email), str(password))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_email, password)
        else:
            return 'already exist'
        
    @staticmethod
    def delete(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM user_info WHERE user_id = %d" % (user_id) 
        deleted = db_cursor.execute(sql) #deleted가 1이면 삭제된것. 0이면 삭제할 데이터가 없는것.
        mysql_db.commit()
        return deleted 

