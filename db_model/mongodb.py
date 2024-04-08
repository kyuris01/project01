import pymongo

MONGO_HOST = 'localhost'
MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST))

def conn_mongodb():
    try:
        MONGO_CONN.admin.command('ismaster')
        lollipop_coll = MONGO_CONN.lollipop_session_db.lollipop_coll
    except:
        MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST))
        lollipop_coll = MONGO_CONN.lollipop_session_db.lollipop_coll
    return lollipop_coll