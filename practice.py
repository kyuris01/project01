'''
import pymysql

MYSQL_HOST = 'localhost'
MYSQL_CONN = pymysql.connect (
    host=MYSQL_HOST,
    port=3306,
    user='chris',
    passwd='1013',
    db='lollipop',
    charset='utf8'
)

def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN

mysql_db = conn_mysqldb()
db_cursor = mysql_db.cursor()
#sql = "INSERT INTO user_info (NICKNAME, USER_EMAIL, PASSWORD) VALUES ('%s','%s', '%s')" % ('koko','koko@naver.com', '1212')
sql = "SELECT * FROM user_info WHERE user_email = 'koko@naver.com' AND password = '1212'"
db_cursor.execute(sql)
user = db_cursor.fetchone()
print(user[0], user[1], user[2], user[3])
'''