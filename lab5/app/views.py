from flask import render_template, request, url_for, redirect, session, make_response, flash
import json
import os
from datetime import datetime
from app import app
from .forms import LoginForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

my_skills = ["HTML", "CSS", "JavaScript", "Python"]

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/skills')
@app.route('/skills/<int:id>')
def skills(id=None):
    total_skills = len(my_skills)
    if id is not None:
        if 0 <= id < total_skills:
            skill = my_skills[id]
            return render_template('skill.html', skill=skill)
        else:
            return "Немає такої навички"
    else:
        return render_template('skills.html', my_skills=my_skills, total_skills=total_skills)
    
@app.context_processor
def inject_bootstrap():
    return dict(bootstrap_css_url=url_for('static', filename='css/bootstrap.min.css'))

@app.context_processor
def inject_system_info():
    os_name = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dict(os_name=os_name, user_agent=user_agent, current_time=current_time)

def load_user_data():
    try:
        with open('users.json', 'r') as file:
            user_data = json.load(file)
        return user_data
    except FileNotFoundError:
        return {}

user_data = load_user_data()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in user_data and user_data[username] == password:
            session['username'] = username
            if form.remember.data:
                flash('Login successful', 'success')
                return redirect('/info')

        flash('Invalid username or password', 'error')
        return redirect('/login')

    return render_template('login.html', form=form)

@app.route('/info', methods=['GET', 'POST'])
def info():
    if 'username' in session:
        username = session['username']
        cookies = request.cookies

        if request.method == 'POST':
            key = request.form.get('key')
            value = request.form.get('value')
            expiration = request.form.get('expiration')

            if request.form.get('change_password'):
                new_password = request.form.get('new_password')
                if new_password:
                    user_data[username] = new_password
                    with open('users.json', 'w') as file:
                        json.dump(user_data, file)

            if key and value:
                expiration = int(expiration) if expiration else None

                response = make_response(render_template('info.html', username=username, cookies=cookies))
                response.set_cookie(key, value, max_age=expiration)
                return response
            elif request.form.get('delete_all'):
                response = make_response(render_template('info.html', username=username))
                for key in cookies:
                    response.delete_cookie(key)
                return response
            elif request.form.get('delete_key'):
                key_to_delete = request.form.get('key_to_delete')
                if key_to_delete in cookies:
                    response = make_response(render_template('info.html', username=username, cookies=cookies))
                    response.delete_cookie(key_to_delete)
                    return response

        return render_template('info.html', username=username, cookies=cookies)

    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
