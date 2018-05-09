# 适配PyMySQL
import pymysql

pymysql.install_as_MySQLdb()

# 连接数据库
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

USER_NAME = 'rayhahah'
PASSWORD = '19940531'
IP_ADDRESS = 'localhost:3306'
SQL_CONFIG = 'mysql://{0}:{1}@{2}/easy_web?charset=utf8'.format(USER_NAME, PASSWORD, IP_ADDRESS)
engine = create_engine(SQL_CONFIG, encoding="utf8", echo=False)
BaseDB = declarative_base()

# 创建orm操作对象
from sqlalchemy.orm import scoped_session, sessionmaker

# 创建表

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)


# 表定义
class Users(BaseDB):
    """
    table for users
    """
    __tablename__ = "users"
    # 定义表结构，包括id，phone，password，createTime
    id = Column(Integer, primary_key=True)
    phone = Column(String(50), nullable=False, index=True)
    password = Column(String(50), nullable=True)
    createTime = Column(DateTime, nullable=True)
    updateTime = Column(DateTime, nullable=True)

    def __init__(self, phone, password, createTime, updateTime):
        self.phone = phone
        self.password = password
        self.createTime = createTime
        self.updateTime = updateTime


# 真正执行ORM操作
# 日期
from datetime import datetime


class OrmTest():

    def __init__(self):
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False,
                                              autoflush=True,
                                              expire_on_commit=False))

    def add_user(self, phone, password):
        # 用户不存在，数据库表中插入用户信息
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_user = Users(phone, password, create_time, create_time)
        self.db.add(add_user)
        self.db.commit()
        self.db.close()

    def query_user(self, phone):
        ex_user = self.db.query(Users).filter_by(phone=phone).first()
        self.db.close()

        return ex_user

    def update_user(self, id, phone):
        user = self.db.query(Users).get(id)
        user.phone = phone
        self.db.add(user)
        self.db.commit()
        self.db.close()

    def delete_user(self, id):
        user = self.db.query(Users).get(id)
        self.db.delete(user)
        self.db.commit()


if __name__ == '__main__':
    o = OrmTest()
    # o.add_user('103', 'hello')
    # o.update_user(6,'200')
    #
    o.delete_user(7)
