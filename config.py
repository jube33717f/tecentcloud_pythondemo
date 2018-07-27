

import os

SECRET_KEY=os.urandom(24)

DIALECT ='mysql'
DRIVER ='pymysql'
USERNAME ='root'
PASSWORD ='czy2018'
HOST ='127.0.0.1'
PORT ='3306'
DATABASE ='registe_demo'
# 这个连接字符串变量名是固定的具体 参考 flask_sqlalchemy  文档 sqlalchemy会自动找到flask配置中的 这个变量
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS=False