# encoding: utf-8

"""
Created by Xero 2012-12-08.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory
from flask.ext.login import login_required, fresh_login_required, current_user,login_user
from ..extensions import db, mail, cache, login
from ..Forms.user import LoginForm
from ..Models.user import User
from ..Models.fga import Products
from flask.ext.admin.base import expose,AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext import wtf
from flask_principal import Principal, identity_changed, Identity, AnonymousIdentity, identity_loaded, UserNeed, RoleNeed

index_view = Blueprint('index_view',__name__,static_folder=None,
                    static_url_path=None, template_folder=None,
                    url_prefix='/', subdomain=None, url_defaults=None)


@index_view.route('/',methods=["GET", "POST"])
def indexhtml():
    
    return render_template('index.html')


class MyHomeView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return render_template('admin.html',admin_view=self)
  
class UserAdmin(ModelView):
    # Disable model creation
    can_create = True
    excluded_list_columns = ['_password','_openid']
    # Override displayed fields

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserAdmin, self).__init__(User, session, **kwargs)
    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password = wtf.TextField('Password')
        form_class.openid = wtf.TextField('Openid')
        return form_class
    
class ProductsAdmin(ModelView):
    # Disable model creation
    can_create = True
    excluded_list_columns = []
    # Override displayed fields
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ProductsAdmin, self).__init__(Products, session, **kwargs)
    def scaffold_form(self):
        form_class = super(ProductsAdmin, self).scaffold_form()
        return form_class