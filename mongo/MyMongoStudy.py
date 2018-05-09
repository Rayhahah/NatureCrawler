# MongoDB原生操作
from pymongo import MongoClient

from bson.objectid import ObjectId


class NatureMongo():

    def __init__(self):
        # 建立数据库链接
        self.client = MongoClient('localhost', 27017)

        # 切换到数据库
        self.db = self.client['students']

    def add_student(self, name, age, sex):
        stu = {
            'name': name,
            'age': age,
            'sex': sex
        }
        return self.db.students.insert_one(stu)

    def get_student(self, id):
        """
        根据id查询学生
        """

        return self.db.students.find({'_id': ObjectId(id)})

    def update_student(self):
        """
        更新数据
        """

        return self.db.students.update_one({'name': 'hello'}, {'name': 'john'})
        # return self.db.students.update_many({'name': 'mike'}, {'name': 'john'})

    def delete_student(self):
        """
        删除数据
        @:return 删除成功返回 1，删除失败返回 0
        """

        return self.db.students.delete_one({'name': 'hello'})
        # return self.db.students.delete_many({'name': 'mike'})


from mongoengine import (
    connect,
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    BooleanField,
    EmbeddedDocumentField,
    FloatField, ListField)

# 固定选择
SEX_CHOICES = (
    ('male', '男'),
    ('female', '女生')
)


class Grade(EmbeddedDocument):
    name = StringField(required=True)
    score = FloatField(required=True)


class Child(Document):
    """
    Child模型
    对应文档如下：
    {
        ”name“:"tom",
        "age":18,
        "sex":"male"
        "grades":[
            {
            "name":"math"
            "score":97.5
            },
            {
            "name":"chinese"
            "score":92.5
            },
        ]
    }
    """

    name = StringField(max_length=32, required=True)
    sex = StringField(choices=SEX_CHOICES, required=True)
    age = IntField(required=True)
    # 有许多的科目成绩，文档的嵌套使用类型
    grades = ListField(EmbeddedDocumentField(Grade))

    meta = {
        # 指定排序规则，年龄倒序
        "ordering": ["-age"]

    }


class MongoEngineFacade:

    def __init__(self):
        connect('Child', host='localhost', port=27017)

    def add_child(self, name, age, sex,
                  chinese=Grade(name="chinese", score=87.5),
                  math=Grade(name="math", score=95.5)):
        new_child = Child(
            name=name,
            age=age,
            sex=sex,
            grades=[chinese, math]
        )

        return new_child.save()

    def query_child(self):
        """
        查询全部
        """

        return Child.objects.all()

    def query_child_byid(self, oid):
        oc = Child.objects.filter(id=oid)
        return oc.first()

    def update_child(self):
        # 修改一条数据
        # return Child.objects.filter(sex='male').update_one(set__age=1)
        return Child.objects.filter(sex='male').update(set__age=1)

    def delete_child(self):
        # 匹配的全部删除
        # return Child.objects.filter(sex='male').delete()

        # 只删除一条
        return Child.objects.filter(sex='male').first().delete()


if __name__ == '__main__':
    # nm = NatureMongo()
    # objectStudent = nm.add_student('nihao', 60, 'female')
    # print(nm.get_student(objectStudent.inserted_id)[0]['name'])
    # nm.delete_student()

    mef = MongoEngineFacade()
    # mef.add_child('lisi', 25, SEX_CHOICES[0][0])
    oid = mef.query_child()[0].id
    print(str(oid))
    print(mef.query_child_byid(oid).grades[0].name)

