#!/Users/macbookpro15/Documents/programming/Stepanych/venv-pyth36/bin/python
# -*- coding: utf-8 -*-
import os
from Stepanych import create_app, db
from Stepanych.models.users import mainTable, Members, Permission, anonymousTeam, Roles
from Stepanych.models.competition import Competition
from Stepanych.models.post import Post
from Stepanych.models.site import Page
from Stepanych.models.routes import setDescriptions
from flask_script import Manager, Shell
from flask import session

if os.path.exists('.env'):
	print('Importing environment from .env...') 
	for line in open('.env'):
		var = line.strip().split('=') 
		if len(var) == 2:
			os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
	return dict(app=app, db=db, mainTable=mainTable, competition=Competition, members=Members, Permission=Permission, Post=Post)

@manager.command
def test():
	"""Run the unit tests"""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ =='__main__':
	manager.run()

from Stepanych.auth.form import LoginForm, RegistrationForm
from Stepanych.models.users import Permission
@app.context_processor
def template_variables():
	infos = Page.query.filter_by(section='info').all()
	medias = Page.query.filter_by(section='media').all()
	competitions = Page.query.filter_by(section='competition').all()

	loginForm = LoginForm()
	registrationForm = RegistrationForm()
	displayRegistrationForm='none'
	displayLoginForm = 'none'

	return dict(loginForm=loginForm, 
		registrationForm=registrationForm, 
		displayRegistrationForm=displayRegistrationForm, 
		displayLoginForm=displayLoginForm, 
		Permission=Permission,
		infos=infos,
		medias=medias,
		competitions=competitions)

@app.before_first_request
def next_url():
	session['nextURL']='/'
	session['currentURL'] ='/'