# encoding: utf-8

"""
Created by Xero 2012-12-08.
"""

from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, HiddenField, SubmitField, SelectField

from ..Models.user import User

class LoginForm(Form):
    username = TextField(u'用户名')
    password = PasswordField(u'密码')
    remember = BooleanField(u'记住登录')
    next = HiddenField()
    submit = SubmitField(u'登录')

class UserForm(Form):
    username = TextField(u'用户名')
    password = TextField(u'密码')
    email = TextField(u'Email')
    role = SelectField(u'角色', choices=[(User.ADMIN, u'管理员'), (User.EDITOR, u'编辑'), (User.RESELLER, u'经销商')],
                       coerce=int)
    active = BooleanField('active')