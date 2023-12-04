from flask import render_template, request, url_for, redirect, session, make_response, Blueprint
import json
from .utils import load_user_data

sessionBp = Blueprint('session', __name__, template_folder="templates/session")

@sessionBp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = load_user_data()

        if username in user_data and user_data[username] == password:
            session['username'] = username
            return redirect(url_for("session.info"))

    return render_template('login.html')

@sessionBp.route('/info', methods=['GET', 'POST'])
def info():
    if 'username' in session:
        username = session['username']
        cookies = request.cookies

        user_data = load_user_data()

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
        return redirect("session.login")

@sessionBp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("session.login")