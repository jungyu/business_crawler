import sqlalchemy
import sqlalchemy.ext.automap
import sqlalchemy.orm
import sqlalchemy.schema

import configparser

config = configparser.ConfigParser()
config.read('scrapy.cfg') # Assuming it is at the same location
host = config['mysql']['Host']
port = int(config['mysql']['Port'])
username = config['mysql']['User']
password = config['mysql']['Password']
database = config['mysql']['Database']

# 建立連線引擎 
connect_string = connect_string = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(username, password, host, port, database)
connect_args = {'connect_timeout': 10}
engine = sqlalchemy.create_engine(connect_string, connect_args=connect_args, echo=False)

#取得資料庫元資料
metadata = sqlalchemy.schema.MetaData(engine)
#產生自動對應參照
automap = sqlalchemy.ext.automap.automap_base()
automap.prepare(engine, reflect=True)

#準備ORM連線
session = sqlalchemy.orm.Session(engine)