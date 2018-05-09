from flask import Flask, render_template

app = Flask(__name__)

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


@app.route('/')
def index():
    """
    首页
    """
    teacher_list = Teacher.query.all()
    return render_template('index.html', teacher_list=teacher_list)


@app.route('/hello/<word>/')
def hello(word=None):
    return render_template('hello.html', word=word)


@app.route('/detail/<int:id>/')
def detail(id):
    return render_template('detail.html', id=id)


if __name__ == '__main__':
    app.run(debug=True)
