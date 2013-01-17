# encoding: utf-8

"""
Created by J.W. on 2012-12-08.
Copyright (c) 2012 Maiden Industrial Co., Lmt.. All rights reserved.
"""

from flask import Flask,current_app
from maiden import create_app
from maiden.extensions import db
from flask.ext.script import Manager, prompt, prompt_pass, \
                                prompt_bool, prompt_choices, Command,Server
from maiden.Models import User

manager = Manager(create_app)
@manager.command
def createall():
    "Creates database tables"
    db.create_all()
    
@manager.command
def initdb():
    from maiden.createdb import init_products
    init_products(db)
    
@manager.option('-u', '--username', dest="username", required=False)
@manager.option('-p', '--password', dest="password", required=False)
@manager.option('-e', '--email', dest="email", required=False)
@manager.option('-r', '--role', dest="role", required=False)
def createuser(username=None, password=None, email=None, role=None):
    """
    Create a new user
    """
    if username is None:
        while True:
            username = prompt("Username")
            user = User.query.filter(User.username==username).first()
            if user is not None:
                print "Username %s is already taken" % username
            else:
                break

    if email is None:
        while True:
            email = prompt("Email address")
            user = User.query.filter(User.email==email).first()
            if user is not None:
                print "Email %s is already taken" % email
            else:
                break

    if password is None:
        password = prompt("Password")

        while True:
            password_again = prompt("Password again")
            if password != password_again:
                print "Passwords do not match"
            else:
                break
    
    roles = (
        (User.FUGUANG, "fuguang"),
        (User.FGA, "fga"),
        (User.ADMIN, "admin"),
    )

    if role is None:
        role = prompt_choices("Role", roles, resolve=int, default=User.FUGUANG)

    user = User(username=username,
                email=email,
                password=password,
                role=role)

    db.session.add(user)
    db.session.commit()

    print "User created with ID", user.id


@manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

manager.add_command("runserver", Server(
    host = '127.0.0.1',
    port = '1000'))

if __name__ == "__main__":
    manager.run()