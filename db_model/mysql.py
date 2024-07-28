import pymysql, os
from dotenv import load_dotenv, find_dotenv

MYSQL_HOST = 'mysqldb_container'
MYSQL_CONN = pymysql.connect (
    host=MYSQL_HOST,
    port=3306,
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DB"),
    charset='utf8'
)

def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN
