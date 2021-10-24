import pymysql


class DB:
    def __init__(self):
        self.c = pymysql.connect(host='39.104.80.98',
                                 port=3306,
                                 password='123456',
                                 user='windows')
        self.cc = self.c.cursor()
        self.cc.execute('use student;')
        self.student = []
        self.load()
        self.student.sort(key=lambda item: str(int(item['math']) + int(item['chinese']) + int(item['english']) / 3),reverse=True)

    def all(self):
        print(self.student)
        print(self.student)
        return self.student

    def insert(self, student):
        self.student.append(student)
        self.student.sort(key=lambda item: str(int(item['math']) + int(item['chinese']) + int(item['english']) / 3),reverse=True)

    def save(self):
        self.cc.execute('truncate table student_xlsx;')
        for i in self.student:
            insert = 'insert into student_xlsx(name,math,chinese,english)values(%s, %s, %s, %s)'
            self.cc.execute(insert, (i['name'], i['math'], i['chinese'], i['english']))
        self.c.commit()
        self.cc.close()
        self.c.close()

    def load(self):
        self.cc.execute('use student;')
        self.cc.execute('select * from student_xlsx;')
        # print(self.cc.fetchall())
        for i in self.cc.fetchall():
            # print(i)
            self.student.append({
                'name': i[0],
                'chinese': i[2],
                'math': i[1],
                'english': i[3],
            })

    def delete(self, student):
        """删除学员信息"""
        self.student.remove(student)
        self.student.sort(key=lambda item: str(int(item['math']) + int(item['chinese']) + int(item['english']) / 3),reverse=True)


class Personal_Information:
    def __init__(self):
        self.c = pymysql.connect(host='39.104.80.98', port=3306, password='123456', user='windows')
        self.cc = self.c.cursor()
        self.cc.execute('use student_user;')
        self.data = []
        self.load()

    def load(self):
        self.cc.execute('use student_user;')
        self.cc.execute('select * from student_user_xlsx;')
        table = self.cc.fetchall()
        # print(table)
        for i in table:
            # print(i)
            self.data.append({
                'username': i[0+1],
                'password': i[1+1],
                'city': i[2+1],
                'hobby': i[3+1],
                'sex': i[4+1],
                'text': i[5+1],
            })
        print(self.data)

    def delete(self, student):
        """删除学员信息"""
        self.data.remove(student)

    def all(self):
        return self.data

    def insert(self, student):
        self.data.append(student)

    def save(self):
        """

    username,    password ,  city ,hobby ,  sex ,text ,
        :return:
        """
        self.cc.execute('truncate table student_user_xlsx;')
        for i in self.data:
            insert = 'insert into student_user_xlsx(username,password,city,hobby,sex,text)values(%s, %s, %s, %s, %s, %s)'
            self.cc.execute(insert, (i['username'], i['password'], i['city'], i['hobby'], i['sex'], i['text']))
        self.c.commit()
        self.cc.close()
        self.c.close()
if __name__ == '__main__':
    db = Personal_Information()
    db.save()