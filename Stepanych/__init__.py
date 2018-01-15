# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from flask_moment import Moment
from config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager 
from flask_pagedown import PageDown
from flask_uploads import UploadSet, IMAGES, DOCUMENTS, DATA, TEXT, configure_uploads, patch_request_class


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
moment = Moment()
csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()
images = UploadSet('images', IMAGES)
docs = UploadSet('docs', DOCUMENTS)
data = UploadSet('data', DATA)
doc = UploadSet('doc', extensions=('txt', 'rtf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'pdf', 'ppt', 'pptx'))

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	
	
	config[config_name].init_app(app)
	moment.init_app(app)
	db.init_app(app)
	csrf.init_app(app)
	mail.init_app(app)
	login_manager.init_app(app)
	pagedown.init_app(app)
	# Configure the image uploading via Flask-Uploads
	configure_uploads(app, (images, docs, data, doc))
	#configure_uploads(app, docs)
	#configure_uploads(app, data)
	patch_request_class(app, 8 * 1024 * 1024)
		
	from Stepanych.main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from Stepanych.auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from Stepanych.competition import competition as competition_blueprint
	app.register_blueprint(competition_blueprint, url_prefix='/competition')

	from Stepanych.news import news as news_blueprint
	app.register_blueprint(news_blueprint, url_prefix='/news')

	from Stepanych.site import site as site_blueprint
	app.register_blueprint(site_blueprint, url_prefix='/site')

	from Stepanych.media import media as media_blueprint
	app.register_blueprint(media_blueprint, url_prefix='/media')

	from Stepanych.info import info as info_blueprint
	app.register_blueprint(info_blueprint, url_prefix='/info')

	return app


