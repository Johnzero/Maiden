# encoding: utf-8

"""
Created by Xero 2012-12-08.
"""

from flask import Blueprint, url_for, redirect, g, flash, request, current_app, render_template, send_from_directory 
from ..Models import *
from flask.ext.login import login_required, fresh_login_required, current_user,login_user


fga_view = Blueprint('fga', __name__, url_prefix='/fga')

@fga_view.route("/")
@login_required
def fgaindex():
    products = Products.query.order_by(Products.id).limit(9)
    discounts = Discounts.query.all()
    purchase = Purchase.query.all()
    return render_template('fga.html',products = products,discounts = discounts,purchase = purchase)




    
