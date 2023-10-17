from flask import Flask, render_template, request, url_for
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

my_skills = ["HTML", "CSS", "JavaScript", "Python"]

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

if __name__ == '__main__':
    app.run(debug=True)