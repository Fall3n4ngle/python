from flask import Blueprint, flash
from flask import redirect, url_for, render_template
from .forms import FeedbackForm
from .models import Feedback
from extensions import db

feedback = Blueprint('feedback', __name__, template_folder="templates/feedback")

@feedback.route("/", methods=['GET', 'POST'])
def feedbackRoute():
    form = FeedbackForm()
    feedback_list = db.session.query(Feedback).all()

    if form.validate_on_submit():
        name = form.name.data
        message = form.message.data
        feedback = Feedback(name=name, message=message)
        db.session.add(feedback)
        db.session.commit()
        flash("Added your feedback!")
        return redirect(url_for("feedback.feedbackRoute"))
    
    return render_template('feedback.html', feedback_list=feedback_list, form=form)