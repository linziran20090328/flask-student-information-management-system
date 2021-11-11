from extensions import *
from info.index import index_bp
from flask import Flask, render_template, request, redirect, jsonify, Blueprint
from common.model import *

@index_bp.route('/students')
def students():
    db = DB()
    student = db.all()
    # 分页信息获取
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=10)
    start = (page - 1) * limit
    data = student[start:start + limit]
    # print(students)
    ret = {"code": 0, "message": "", "count": len(student), "data": data, 'success': True}
    return jsonify(ret)
@index_bp.route('/change', methods=['GET', 'POST'])
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
                    # print(i)
                    session['city'] = i[0]['city']
                    session['hobby'] = i[0]['hobby']
                    session['sex'] = i[0]['sex']
                    session['text'] = i[0]['text']
            session['name'] = name
            session['password'] = pwd_new
            db.save()
            return render_template('修改密码-正确弹窗.html', user=session.get('name'))
    return render_template('修改密码.html', user=session.get('name'))
@index_bp.route('/exit_user')
def exit_user():
    global session
    session = {}
    return redirect('/auth/login')


@index_bp.route('/exit_register')
def exit_register():
    global session
    session = {}
    return redirect('/auth/register')


@index_bp.route('/add', methods=['GET', 'POST'])
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


@index_bp.route('/delete')
def delete():
    db = DB()
    name = request.args.get('name')
    for stu in db.all():
        if stu['name'] == name:
            db.delete(stu)
            db.save()
    return redirect('/admin')


@index_bp.route('/change_table', methods=['GET', 'POST'])
def change_table():
    db = DB()
    for stu in db.all():
        username = request.args.get('name')
        if stu['name'] == username:
            if request.method == 'POST':
                print(stu)

                print(stu['name'])
                # print('1',db.all())
                stu['name'] = request.form.get('name')
                stu['chinese'] = request.form.get('chinese')
                stu['math'] = request.form.get('math')
                stu['english'] = request.form.get('english')
                db.delete(stu)
                db.insert(stu)
                db.save()
            return render_template('修改(1).html', name=username, students=stu)
@index_bp.route('/')
def main():
    return redirect('/auth/login')
@index_bp.route('/user')
def user():
    # 分页信息获取
    db = DB()
    # print(db.all())
    for student in db.all():
        # print(student)
        if student['name'] == request.args.get('name'):
            ret = {"message": "获取数据成功", "user_info": student, 'success': True}
            db.save()
            return jsonify(ret)
    db.save()
    return jsonify({"message": "获取数据失败", "user_info": "", 'success': True})
@index_bp.route('/admin')
def admin():
    name = session.get('name')
    password = session.get('password')
    if name and password:
        return render_template('主页面.html', user=name)
    else:
        return redirect('/auth/login')



@index_bp.route('/admin_personal')
def admin_personal():
    db = Personal_Information()
    return render_template('个人信息.html', user=session.get('name'), student_user=session)


@index_bp.route('/admin_information', methods=['GET', 'POST'])
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
