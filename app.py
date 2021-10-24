from flask import Flask, render_template, request, redirect, jsonify, Blueprint
from model import *
from db import StudentDB

admin_bp = Blueprint('auth', __name__, url_prefix='/admin')
user_db = StudentDB()
session: dict = {}
name = ''
app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = Personal_Information()
        pwd = request.form.get('password')
        user = request.form.get('title')
        if user_db.search(user, pwd):
            session['name'] = user
            session['password'] = pwd
            for i in db.all():
                print('i', i)
                if i['username'] == user:
                    # print(i)
                    session['city'] = i['city']
                    session['hobby'] = i['hobby']
                    session['sex'] = i['sex']
                    session['text'] = i['text']
            print(session)
            db.save()
            return redirect('/admin')
        else:
            db.save()
            return render_template('登录-弹窗.html')

    return render_template('登录.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        db = Personal_Information()
        password = request.form.get('password')
        username = request.form.get('username')
        city = request.form.get('city')
        hobby = request.form.getlist('hobby')
        sex = request.form.get('sex')
        text = request.form.get('text')
        print(type(username))
        db.insert({
            'username': username,
            'password': password,
            'city': city,
            'hobby': ','.join(hobby),
            'sex': sex,
            'text': text
        })

        data = {
            'name': username,
            'pwd': password
        }
        if user_db.search(username, password):
            return render_template('注册-弹窗.html')
        else:
            user_db.add(data['name'], data['pwd'])
        db.save()
        return redirect(f'/login')
    return render_template('注册.html')


@app.route('/students')
def students():
    db = DB()
    student = db.all()
    student.sort(key=lambda item: item['math'],reverse=True)
    ret = {"code": 0, "message": "", "count": len(student), "data": student, 'success': True}
    db.save()
    return jsonify(ret)


@app.route('/admin')
def admin():
    name = session.get('name')
    password = session.get('password')
    if name and password:
        db = DB()
        db.save()
        return render_template('主页面.html', user=name)
    else:
        return redirect('/login')


@app.route('/change', methods=['GET', 'POST'])
def change():
    if request.method == 'POST':
        db = Personal_Information()
        password = session.get('password')
        name = request.form.get('username')
        pwd_new = request.form.get('new_password')
        pwd_old = request.form.get('old_password')
        if password != pwd_old:
            return render_template('修改密码-错误弹窗.html', user=session.get('name'))
        changes = user_db.change(session.get('name'), name, pwd_old, pwd_new)
        if changes:
            for i in db.all():
                if i['username'] == session['name']:
                    print(i)
                    session['city'] = i[0]['city']
                    session['hobby'] = i[0]['hobby']
                    session['sex'] = i[0]['sex']
                    session['text'] = i[0]['text']
            session['name'] = name
            session['password'] = pwd_new
            db.save()
            return render_template('修改密码-正确弹窗.html', user=session.get('name'))
    return render_template('修改密码.html', user=session.get('name'))


@app.route('/admin_personal')
def admin_personal():
    db = Personal_Information()
    return render_template('个人信息.html', user=session.get('name'), student_user=session)


@app.route('/admin_information', methods=['GET', 'POST'])
def admin_information():
    """
    username,    password ,  city ,hobby ,  sex ,text ,
    :return:
    """
    db = Personal_Information()
    if request.method == 'POST':
        for i in db.all():
            if i['username'] == session['name']:
                username = request.form.get('username')
                password = request.form.get('password')
                city = request.form.get('city')
                hobby = request.form.get('hobby')
                sex = request.form.get('sex')
                text = request.form.get('text')
                student_user = {
                    'username': username,
                    'password': password,
                    'city': city,
                    'hobby': hobby,
                    'sex': sex,
                    'text': text
                }
                # print(student_user)
                # print(i)
                db.delete(i)
                # print(db.all())
                db.insert(student_user)
                db.save()
                return redirect('/admin')
    return render_template('设置个人信息.html', student_user=session, user=session.get('name'))


@app.route('/exit_user')
def exit_user():
    global session
    session = {}
    return redirect('/login')


@app.route('/exit_register')
def exit_register():
    global session
    session = {}
    return redirect('/register')


@app.route('/add', methods=['GET', 'POST'])
def add():
    db = DB()
    if request.method == 'POST':
        db.insert({
            'name': request.form.get('name'),
            'chinese': request.form.get('chinese'),
            'math': request.form.get('math'),
            'english': request.form.get('english')
        })
        db.save()
        return redirect('/admin')
    return render_template('录入.html', user=session.get('name'))


@app.route('/delete')
def delete():
    db = DB()
    name = request.args.get('name')
    for stu in db.all():
        if stu['name'] == name:
            db.delete(stu)
            db.save()
    return redirect('/admin')


@app.route('/change_table', methods=['GET', 'POST'])
def change_table():
    db = DB()
    username = request.args.get('name')
    for stu in db.all():
        if stu['name'] == username:
            if request.method == 'POST':
                stu['name'] = request.form.get('name')
                stu['chinese'] = request.form.get('chinese')
                stu['math'] = request.form.get('math')
                stu['english'] = request.form.get('english')
                db.delete(stu)
                db.insert(stu)
                db.save()
                # return redirect('/admin')
            return render_template('修改(1).html', name=username, students=stu)


@app.route('/user')
def user():
    # 分页信息获取
    db = DB()
    print(db.all())
    for student in db.all():
        print(student)
        if student['name'] == request.args.get('name'):
            ret = {"message": "获取数据成功", "user_info": student, 'success': True}
            db.save()
            return jsonify(ret)
    db.save()
    return jsonify({"message": "获取数据失败", "user_info": "", 'success': True})


@app.route('/')
def main():
    return redirect('/login')


@app.route('/test')
def test():
    return render_template('text-layui.html')


if __name__ == '__main__':
    app.run()
