from flask import Blueprint, redirect, url_for, flash, session, render_template
from flask_login import login_user, current_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm
from .models import User
from extensions import bcrypt
from extensions import db
from .utils import save_uploaded_image

auth = Blueprint('auth', __name__, template_folder="templates/auth")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for("portfolio.portfolioRoute"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account was created for {form.username.data}!', category="success")
        return redirect(url_for("auth.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', category="danger")

    return render_template('register.html', form=form, title="Register")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("portfolio.portfolioRoute"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category="success")
            session['username'] = user.username  
            return redirect(url_for("portfolio.portfolioRoute"))
        else:
            flash('Login unsuccessful. Check your email and password!', category="danger")

    return render_template('login.html', form=form, title="Login")

@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("portfolio.portfolioRoute"))

@auth.route("/account")
@login_required
def account():
    form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()

    return render_template("account.html", title="Account", form=form, change_password_form=change_password_form)

@auth.route("/update_account", methods=['POST'])
@login_required
def update_account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if form.image_file.data:
            image_filename = save_uploaded_image(form.image_file.data)
            current_user.image_file = image_filename
            
        db.session.commit()
        flash('Account updated successfully', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('auth.account'))

@auth.route("/change_password", methods=['POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_password_form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(change_password_form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully', 'success')
        else:
            flash('Old password is incorrect', 'danger')
    else:
        for field, errors in change_password_form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(change_password_form, field).label.text}: {error}', 'danger')

    return redirect(url_for('auth.account'))