from flask import render_template, request, Blueprint, abort, url_for, session, redirect, flash
from main_app.user.forms import LoginForm, RegistrationForm
from flask_login import login_required, current_user, login_user, logout_user
from main_app import db
from main_app.models import User


user = Blueprint('user', __name__)

@user.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_anonymous:
        form = RegistrationForm()
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.email.data).first():
                flash("The username or the email has already been registered")
            else:
                user = User(username=form.username.data.strip(),email=form.email.data.strip(), password=form.password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('core.index'))#to be changed to the main chatting page when created
        errors = []
        [errors.append(x) for x in form.username.errors+form.email.errors+form.password.errors+form.pass_confirm.errors]
        return render_template('signup.html', form=form, errors=errors)
    else:abort(404)

@user.route('/signin',methods=['GET','POST'])
def signin():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data.strip()).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('core.index'))
                else:
                    flash('the entered password is incorrect')
            else:
                flash('You are not registered. Please signup to continue')
        errors = []
        [errors.append(x) for x in form.username.errors+form.email.errors+form.password.errors]
        return render_template('signin.html', form=form, errors=errors)
    else: abort(404)

@user.route('/signout')
@login_required
def signout():
    logout_user()
    flash('You are now signed out')
    return redirect(url_for('core.index'))



