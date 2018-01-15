from flask import flash, redirect, render_template, request, url_for, session, abort  
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.validators import Required, Email
from . import main
from Stepanych.auth.form import LoginForm, RegistrationForm
from Stepanych import db
from ..email import send_email
#from flask import current_app as app
from flask import current_app
from Stepanych.auth.form import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from Stepanych.decorators import admin_required, permission_required
from Stepanych.models.post import Post
from Stepanych.models.users import Roles
from Stepanych.models.competition import Competition, CompetitionArchive
from Stepanych.models.site import Contacts, Logo
from Stepanych import doc, images 
import os, random, bleach
from werkzeug import secure_filename, FileStorage
from transliterate import translit, get_available_language_codes


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'] 

def name_rus(filename):
	return '.' not in filename

#===============INDEX===============

@main.route('/main')
@main.route('/index')
@main.route('/')
def index():
	if Logo.query.filter_by(status='active').first() is None:
		blank = True
		logo =''
	else:
		logo = Logo.query.filter_by(status='active').first()
		blank = False

	competition= Competition.query.first()
	registrationStatus = competition.registrationStatus

	page = request.args.get('page',1,type=int)
	registrationForm = RegistrationForm()
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items
	roles = Roles.query.order_by(Roles.permissions).all()

	return render_template('index.html', 
		displayLoginForm=request.args.get('displayLoginForm'), 
		displayRegistrationForm=request.args.get('displayRegistrationForm'),
		posts=posts, pagination=pagination, 
		registrationForm=registrationForm, 
		roles=roles,
		registrationStatus=registrationStatus, blank=blank, logo=logo)





#===============CONTACTS===============

@main.route('/contacts')
def contacts():
	contacts = Contacts.query.all();
	return render_template('contacts.html', displayLoginForm=request.args.get('displayLoginForm'), contacts=contacts)


@main.route('/contacts/add', methods=['POST'])
@admin_required
def add_contact():
	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(url_for('main.contacts', displayNewContact='block'))
		else:
			try:
				for file in request.files.getlist('docs'):
					if file and allowed_file(file.filename):
						if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
							raise TypeError("storage must be a werkzeug.FileStorage")
							flash('Левый файл')
							return redirect(url_for('main.contacts', displayNewContact='block'))
	
						file.filename = translit(file.filename,'ru', reversed=True)
						if len(file.filename)>64:
							file.filename = file.filename[0:20]+ os.path.splitext(file.filename)[1]
						filename = images.save(file)
						url = images.url(filename)

						contact = Contacts(fileName = filename, 
							url = url, 
							fullName = bleach.clean(request.form['fullName']), 
							jobDescription = bleach.clean(request.form['jobDescription']),
							email= bleach.clean(request.form['email']),
							vkURL=bleach.clean(request.form['vkURL']),
							fbURL=bleach.clean(request.form['fbURL'])
							)
						db.session.add(contact)
				
				db.session.commit()
				flash('%s добавлен в контакты' % (bleach.clean(request.form['fullName'])))
				return redirect(url_for('main.contacts'))
			except:
				flash('Некорректный файл')
				return redirect(url_for('main.contacts', displayNewContact='block'))

	return redirect(url_for('main.contacts'))

@main.route('/contacts/delete', methods=['POST'])
@admin_required
def delete_contact():
	fullName = request.form['fullName']
	contact = Contacts.query.filter_by(fullName=fullName).first()
	try:
		os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], contact.fileName))
	except:
		Contacts.query.filter_by(fullName=fullName).delete()
		flash('Контакт удален')
		return redirect(url_for('main.contacts'))
	
	Contacts.query.filter_by(fullName=fullName).delete()
	flash('%s удален' % fullName)
	return redirect(url_for('main.contacts'))





