from flask import Blueprint, render_template

portfolio = Blueprint('portfolio', __name__, template_folder="templates/portfolio", static_folder="static")

@portfolio.route("/")
def portfolioRoute():
    return render_template('home.html')

@portfolio.route('/contact')
def contact():
    return render_template('contact.html')

my_skills = ["HTML", "CSS", "JavaScript", "Python"]

@portfolio.route('/skills')
@portfolio.route('/skills/<int:id>')
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