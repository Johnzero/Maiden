# encoding: utf-8

"""
Created by Xero 2012-12-08.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory
from flask.ext.login import login_required, login_url,fresh_login_required, current_user,login_user,logout_user
from ..extensions import db, mail, cache, login
from ..Forms.user import LoginForm
from ..Models.user import User
from ..Models.fga import Products
from flask.ext.admin.base import expose,AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext import wtf
from flask_principal import Principal, identity_changed, Identity, AnonymousIdentity, identity_loaded, UserNeed, RoleNeed

login_view = Blueprint('login_view',__name__,url_prefix='/login')
REDERICT_URL = '/'

@login.user_loader
def load_user(userid):
    return User.query.get(userid)

@login_view.route('/',methods=["GET", "POST"])
def fun_login():
    global REDERICT_URL
    form = LoginForm()
    user, success = User.query.authenticate(form.username.data, form.password.data)
    if request.args.get('next'):REDERICT_URL = request.args.get('next')
    if form.validate_on_submit():
        user, success = User.query.authenticate(form.username.data, form.password.data)
        if success:
            flash("Welcome Back!")
            login_user(user)
            return redirect(REDERICT_URL)
        else:
            flash("Retry Please!")
    return render_template('login.html',form=form)

@login_view.route('/logout')
@login_required
def fun_logout():
    logout_user()
    return redirect(request.args.get('next') or '/')