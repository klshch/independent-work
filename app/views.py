#!/usr/bin/python3

from flask import flash, redirect, render_template, url_for, make_response, request, session

from app import app, db
from app import Feedback

import os
from datetime import datetime

from data import skills
import json

from forms import LoginForm
from forms import ChangePassword
from forms import FeedbackForm

def get_system_info():
    os_info = os.uname()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return os_info, user_agent, current_time

json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'json', 'users.json')
with open(json_file_path, 'r') as users_file:
    users = json.load(users_file)


@app.route('/')
def home():
    os_info, user_agent, current_time = get_system_info()
    return render_template('home.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/page1')
def page1():
    os_info, user_agent, current_time = get_system_info()
    return render_template('page1.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/page2')
def page2():
    os_info, user_agent, current_time = get_system_info()
    return render_template('page2.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/page3')
@app.route('/page3/<int:idx>')
def page3(idx=None):
    os_info, user_agent, current_time = get_system_info()
    if idx is not None:
        if 0 <= idx < len(skills):
            skill = skills[idx]
            return render_template('page3.html', skill=skill, os_info=os_info, user_agent=user_agent, current_time=current_time)
        else:
            total_skills = len(skills)
            return render_template('page3.html', skills=skills, total_skills=total_skills, os_info=os_info, user_agent=user_agent, current_time=current_time)
    else:
        total_skills = len(skills)
        return render_template('page3.html', skills=skills, total_skills=total_skills, os_info=os_info, user_agent=user_agent, current_time=current_time)



#@app.route('/form', methods=["GET", "POST"])
#def form():
#    os_info, user_agent, current_time = get_system_info()
#
#    if request.method == "POST":
#        name = request.form.get("name")
#        password = request.form.get("password")
#
#        if name in users and users[name] == password:
#            session["username"] = name
#            return redirect(url_for("info"))
#        
#    return render_template('form.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


#lab5

@app.route('/form', methods=["GET", "POST"])
def form():
    
    form = LoginForm()  

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        if name in users and users[name] == password:
            if form.remember.data == True:
                flash("Вхід виконано. Інформація збережена.", category="success")
                session["username"] = name

                return redirect(url_for("info"))
                
            else:
                flash("Вхід виконано. Інформація не збережена", category="success")

                return redirect(url_for("home"))

        else:
            flash("Вхід не виконано", category="warning")
            return redirect(url_for("form"))

    return render_template('form.html', form=form)



@app.route('/info', methods=["GET", "POST"])
def info():

    form = ChangePassword()

    if session.get("username"):
        cookies = get_cookies_data()
        if request.method == "POST":
 
            cookie_key = request.form.get("cookie_key")
            cookie_value = request.form.get("cookie_value")
            cookie_expiry = request.form.get("cookie_expiry")
            delete_cookie_key = request.form.get("delete_cookie_key")

            if cookie_key and cookie_value and cookie_expiry:
                add_cookie(cookie_key, cookie_value, int(cookie_expiry))
            if delete_cookie_key:
                delete_cookie(delete_cookie_key)

            cookies = get_cookies_data()  
        return render_template('info.html', cookies=cookies, form=form)
    else:
        return redirect(url_for('form'))


def get_cookies_data():
    cookies = []
    for key, value in request.cookies.items():
        expiry = request.cookies.get(key + "_expires")
        created = request.cookies.get(key + "_created")

        cookies.append((key, value, expiry, created))
    return cookies

@app.route('/clearsession', methods=["GET"])
def clear_session():
    session.pop("username", None)
    return redirect(url_for("form"))

@app.route('/add_cookie', methods=["POST"])
def add_cookie():
    if session.get("username"):
        cookie_key = request.form.get("cookie_key")
        cookie_value = request.form.get("cookie_value")
        cookie_expiry = request.form.get("cookie_expiry")

        response = make_response(redirect(url_for("info")))
        response.set_cookie(cookie_key, cookie_value, max_age=int(cookie_expiry) * 3600) 
        flash("Куки додано.", category="success")
        return response
    else:
        return redirect(url_for('form'))

@app.route('/delete_cookie', methods=["POST"])
def delete_cookie():
    if session.get("username"):
        cookie_key_to_delete = request.form.get("cookie_key_to_delete")

        response = make_response(redirect(url_for("info")))
        response.delete_cookie(cookie_key_to_delete)
        flash("Куки видалено.", category="success")
        return response
    else:
        return redirect(url_for('form'))

@app.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():
    if session.get("username"):
        response = make_response(redirect(url_for("info")))
        for key in request.cookies:
            response.delete_cookie(key)
        return response
    else:
        return redirect(url_for('form'))

@app.route('/change_password', methods=["POST"])
def change_password():

    form = ChangePassword()

    if form.validate_on_submit():

        if session.get("username"):
            current_password = form.current_password.data
            new_password = form.new_password.data
            username = session["username"]

            json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'json', 'users.json')

            with open(json_file_path, 'r') as users_file:
                users = json.load(users_file)

            if users.get(username) == current_password:
                users[username] = new_password

                with open(json_file_path, 'w') as users_file:
                    json.dump(users, users_file)

                flash("Пароль змінено.", category="success")
                
                return redirect(url_for("info"))
            
            else:
                flash("Пароль не змінено.", category="warning")

                return redirect(url_for("info"))
        
        else:
            return redirect(url_for('form'))
        
    return render_template('info.html', form=form)


#самостійна робота

@app.route('/reviews', methods=["GET", "POST"])
def reviews():
    
    reviews = FeedbackForm()

    if request.method == 'POST' and reviews.validate_on_submit():
        name = reviews.name.data
        content = reviews.content.data
        feedback_entry = Feedback(name=name, content=content)
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Ваш відгук було успішно збережено', 'success')
        return redirect(url_for('reviews'))

    feedback_entries = Feedback.query.all() 

    return render_template('reviews.html', reviews=reviews, feedback_entries=feedback_entries)