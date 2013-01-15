# encoding: utf-8

"""
Xero
"""

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, Response, request, g, jsonify, redirect, url_for, flash, render_template
from .extensions import db, mail, cache, login
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.admin  import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from .Models import *
from .Views import *
from os import path as op
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.assets import Environment, Bundle
from flask_mail import Mail
from flask_principal import Principal, Permission, RoleNeed
from flask.ext.login import AnonymousUser
from flask.ext.xmlrpc import XMLRPCHandler, Fault

__all__ = ["create_app"]

DEFAULT_APP_NAME = 'maiden'

DEFAULT_MODULES = ((index_view,fga_view,sale_view,login_view,sale_view_sale,sale_product,sale_partner))

path = op.join(op.dirname(__file__), 'static')

def create_app(config=None, app_name=None, modules=None):
    
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES
    
    app = Flask(app_name,static_path=None, static_url_path=None,
                static_folder='static', template_folder='templates',
                instance_path=None, instance_relative_config=False)
    
    handler = XMLRPCHandler('sale')
    handler.connect(app, '/sale')
    
    @handler.register
    def hello(name="world"):
        if not name:
            raise Fault("unknown_recipient", "I need someone to greet!")
        return "Hello, %s!" % name
    
    app.config.from_pyfile('config.cfg',silent=True)
    app.debug = True
    app.config['SECRET_KEY'] = "zuSAyu3XRqGRvAg0HxsKX12Nrvf6Hk3AgZCWg1S1j9Y="
    for module in modules:
        app.register_blueprint(module)
    def url():
        pass
    app.add_url_rule('/url','url',url)
    
    def before():
        print 'Before-first-request'
    #app.before_first_request_funcs = [before]
    @app.errorhandler(414)
    def page_not_found(error):
        return 'This page does not exist', 414
    app.error_handler_spec[None][414] = page_not_found

    admin = Admin(app,name='Maiden',index_view=MyHomeView())
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
    admin.add_view(UserAdmin(db.session))
    admin.add_view(ProductsAdmin(db.session))
    
    #DebugToolbarExtension(app)
    login.login_view = "login_view.fun_login"
    class Anonymous(AnonymousUser):
        name = u"Anonymous"
    login.anonymous_user = Anonymous
    login.login_message = u"请登录."
    login.refresh_view = "users.reauth"
    login.setup_app(app)
    
    configure_logging(app)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_template_filters(app)
    

    
    assets = Environment()
    assets.ASSETS_DEBUG = True
    assets.init_app(app)
    mail = Mail(app)
    principals = Principal(app)
    
    return app

def configure_template_filters(app):
    @app.template_filter()
    def timesince(value):
        return helpers.timesince(value)

def configure_extensions(app):
    mail.init_app(app)
    db.init_app(app)
    cache.init_app(app)

def configure_errorhandlers(app):
    
    if app.testing:
        return
    
    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/sinuous.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        return render_template("errors/sinuous.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/sinuous.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))

def configure_logging(app):
    if app.debug or app.testing:
        return

    mail_handler = \
        SMTPHandler(app.config['MAIL_SERVER'],
                    'error@newsmeme.com',
                    app.config['ADMINS'], 
                    'application error',
                    (
                        app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'],
                    ))

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path, 
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, 
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)


