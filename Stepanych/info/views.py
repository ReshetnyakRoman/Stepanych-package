from flask import flash, redirect, render_template, request, url_for, session, abort  
from . import info
from Stepanych import db
from flask import current_app
from flask_login import login_user, logout_user, login_required, current_user
from Stepanych.decorators import admin_required, permission_required
from Stepanych.models.site import Press, Video, Rules, Sponsors
import os, bleach, random
from Stepanych import doc, images
from urllib.parse import urlparse
from werkzeug import secure_filename, FileStorage
from transliterate import translit, get_available_language_codes
from Stepanych.models.competition import Competition, CompetitionArchive


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'] 

def name_rus(filename):
	return '.' not in filename




#===============RULES===============

@info.route('/rules')
def rules():
	colors = ['w3-black','w3-blue','w3-lime','w3-light-green', 'w3-indigo','w3-lime','w3-orange','w3-deep-orange','w3-purple','w3-teal']
	competitionArchive = CompetitionArchive.query.order_by(CompetitionArchive.competitionName.desc()).all()
	docList = Rules.query.all()

	return render_template('info/rules.html', 
		displayLoginForm=request.args.get('displayLoginForm'),
		competitionArchive=competitionArchive,
		docList=docList,
		colors=colors)



@info.route('/rules/add', methods=['POST'])
@admin_required
def add_rules():

	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(url_for('info.rules', displayNewRule='block'))
		else:
			try:
				for file in request.files.getlist('docs'):
					if file and allowed_file(file.filename):
						if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
							raise TypeError("storage must be a werkzeug.FileStorage")
							flash('Левый файл')
							return redirect(url_for('info.rules', displayNewRule='block'))
	
						file.filename = translit(file.filename,'ru', reversed=True)
						filename = doc.save(file)
						url = doc.url(filename)
						doc1 = Rules(name = filename, url = url, nameRus = request.form['nameRus'], color = random.randint(-1,10))
						db.session.add(doc1)
				db.session.commit()
				flash('Документ %s добавлен' % (filename))
				return redirect(url_for('info.rules'))
			except:
				flash('Некорректный файл')
				return redirect(url_for('info.rules', displayNewRule='block'))
	flash('Упс, что-то не сработало :(')
	return redirect(url_for('info.rules'))



@info.route('/rules/delete', methods=['POST'])
@admin_required
def delete_rules():
	nameRus = request.form['nameRus']
	doc = Rules.query.filter_by(nameRus=nameRus).first()
	try:
		os.remove(os.path.join(current_app.config['UPLOADED_DOCUMENTS_DEST'], doc.name))
	except:
		Rules.query.filter_by(nameRus=nameRus).delete()
		flash('Такого документа уже нет на сервере!')
		return redirect(url_for('info.rules'))
	
	Rules.query.filter_by(nameRus=nameRus).delete()
	flash('Документ удален')
	return redirect(url_for('info.rules'))




#===============SPONSORS===============

@info.route('/sponsors')
def sponsors():

	generalSponsors = Sponsors.query.filter_by(sponsorType='генеральный').order_by(Sponsors.sponsorName).all()
	partners = Sponsors.query.filter_by(sponsorType='партнер').order_by(Sponsors.sponsorName).all()
	otherSponsors = Sponsors.query.filter_by(sponsorType='остальные').order_by(Sponsors.sponsorName).all()

	return render_template('info/sponsors.html', 
		displayLoginForm=request.args.get('displayLoginForm'),
		generalSponsors=generalSponsors,
		partners=partners,
		otherSponsors=otherSponsors)




@info.route('/sponsors/add', methods=['POST'])
@admin_required
def add_sponsor():
	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(url_for('info.sponsors', displayNewSponsor='block'))
		else:
			try:
				for file in request.files.getlist('docs'):
					if file and allowed_file(file.filename):
						if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
							raise TypeError("storage must be a werkzeug.FileStorage")
							flash('Левый файл')
							return redirect(url_for('info.sponsors', displayNewSponsor='block'))
	
						file.filename = translit(file.filename,'ru', reversed=True)
						if len(file.filename)>21:
							file.filename = file.filename[0:20]+ os.path.splitext(file.filename)[1]
						imgName = images.save(file)
						imgURL = images.url(imgName)
						sponsor = Sponsors(
							imgName = imgName, 
							imgURL = imgURL, 
							linkToSponsor = bleach.clean(request.form['linkToSponsor'])	, 
							sponsorName = bleach.clean(request.form['sponsorName']), 
							sponsorType = bleach.clean(request.form['sponsorType']))
						db.session.add(sponsor)
				db.session.commit()
				flash('%s добавлен в %s' % (request.form['sponsorName'],request.form['sponsorType']))
				return redirect(url_for('info.sponsors'))
			except:
				flash('Некорректный файл')
				return redirect(url_for('info.sponsors', displayNewSponsor='block'))
	flash('Упс, что-то не сработало :(')
	return redirect(url_for('info.sponsors'))




@info.route('/sponsors/delete', methods=['POST'])
@admin_required
def delete_sponsor():
	sponsorName = request.form['sponsorName']
	sponsor = Sponsors.query.filter_by(sponsorName=sponsorName).first()
	try:
		os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], sponsor.imgName))
	except:
		Sponsors.query.filter_by(sponsorName=sponsorName).delete()
		flash('Такого документа уже нет на сервере!')
		return redirect(url_for('info.sponsors'))
	
	Sponsors.query.filter_by(sponsorName=sponsorName).delete()
	flash('Этот жид удален!')
	return redirect(url_for('info.sponsors'))