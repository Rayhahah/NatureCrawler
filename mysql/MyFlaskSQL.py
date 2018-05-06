import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 适配PyMySQL
import pymysql

pymysql.install_as_MySQLdb()

USER_NAME = 'rayhahah'
PASSWORD = '19940531'
IP_ADDRESS = 'localhost:3306'
SQL_CONFIG = 'mysql://{0}:{1}@{2}/easy_web?charset=utf8'.format(USER_NAME, PASSWORD, IP_ADDRESS)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True

db = SQLAlchemy(app)

# 一般以这样的方式来配置
# class Config:
#     SECRET_KEY = os.urandom (24)
#     SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost:3306/flaskrbac?charset=utf8'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_COMMIT_TEARDOWN = True
#
#
#
#     @staticmethod
#     def init_app(app):
#         pass
#
# app.config.from_object(Config)  # 这里在初始化db之前需要先加载配置文件，问题解决
# Config.init_app(app)
# db.init_app(app)


# 表定义
class Teacher(db.Model):
    """
    table for users
    """
    __tablename__ = "teacher"
    # 定义表结构，包括id，phone，password，createTime
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(50), nullable=False, index=True)
    password = db.Column(db.String(50), nullable=True)
    createTime = db.Column(db.DateTime, nullable=True)
    updateTime = db.Column(db.DateTime, nullable=True)

    def __init__(self, phone, password, createTime, updateTime):
        self.phone = phone
        self.password = password
        self.createTime = createTime
        self.updateTime = updateTime

    def add_teacher(self, phone, password):
        # 用户不存在，数据库表中插入用户信息
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_user = Teacher(phone, password, create_time, create_time)
        db.session.add(add_user)
        db.session.commit()

    def query_teacher(self, phone):
        ex_user = Teacher.query.filter_by(phone=phone).first()
        return ex_user

    def update_teacher(self, id, phone):
        user = Teacher.query.get(id)
        user.phone = phone
        db.add(user)
        db.commit()

    def delete_teacher(self, id):
        user = Teacher.query.get(id)
        db.session.delete(user)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()

    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_user = Teacher('2000', 'bojur', create_time, create_time)
    db.session.add(add_user)
    db.session.commit()
