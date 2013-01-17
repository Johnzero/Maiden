# encoding: utf-8

"""
Created by Xero 2012-12-08.
"""

from flask.ext.wtf import Form, TextField, Required, TextAreaField, SubmitField


class PageForm(Form):
    keyword = TextField('关键字', validators=[Required()])
    content = TextAreaField('页面内容', validators=[Required()])
    submit = SubmitField("保存")