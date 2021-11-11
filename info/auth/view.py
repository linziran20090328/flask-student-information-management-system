from extensions import *
from info.auth import auth_bp
from flask import Flask, render_template, request, redirect, jsonify, Blueprint
from common.model import *

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = Personal_Information()
        pwd = request.form.get('password')
        user = request.form.get('title')
        if user_db.search(user, pwd):
            session['name'] = user
            session['password'] = pwd
            for i in db.all():
                # print('i', i)
                if i['username'] == user:
                    # print(i)
                    session['city'] = i['city']
                    session['hobby'] = i['hobby']
                    session['sex'] = i['sex']
                    session['text'] = i['text']
            # print(session)
            db.save()
            return redirect('/admin')
        else:
            db.save()
            return render_template('登录-弹窗.html')

    return render_template('登录.html')


@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        db = Personal_Information()
        password = request.form.get('password')
        username = request.form.get('username')
        city = request.form.get('city')
        hobby = request.form.getlist('hobby')
        sex = request.form.get('sex')
        text = request.form.get('text')
        # print(type(username))
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
        return redirect(f'/auth/login')
    return render_template('注册.html')

