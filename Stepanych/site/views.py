from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from Stepanych import db, doc, images
from flask import current_app
from Stepanych.decorators import admin_required, permission_required
from Stepanych.models.site import Docs, Logo, Page
from Stepanych.models.users import Permission
from . import site
import os
from werkzeug import secure_filename, FileStorage
from transliterate import translit, get_available_language_codes
from flask import jsonify, json, Response
from Stepanych.news.form import PostForm

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'] 

def name_rus(filename):
	return '.' not in filename    

#==========Docs upload/delete==========#

@site.route('/docs')
@login_required
@permission_required(Permission.ADMINVIEW)
def docs():
	docList = Docs.query.all()
	return render_template('site/docs.html', docList=docList, displayLoginForm=request.args.get('displayLoginForm'))

@site.route('/docs/upload', methods=['POST', 'GET'])
@login_required
@admin_required
def file_upload():
	if request.args.get('prevURL') is not None:
		session['prevURL'] = request.args.get('prevURL')

	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(session['prevURL']+'?displayFileUpload=block' or url_for('main.index', displayFileUpload='block'))
		else:
			try:
				for file in request.files.getlist('docs'):
					if file and allowed_file(file.filename):
						if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
							raise TypeError("storage must be a werkzeug.FileStorage")
							flash('Левый файл')
							return redirect(url_for('site.docs', displayFileUpload='block'))
	
						file.filename = translit(file.filename,'ru', reversed=True)
						if len(file.filename)>64:
							file.filename = file.filename[0:20]+ os.path.splitext(file.filename)[1]
						filename = doc.save(file)
						url = doc.url(filename)
						doc1 = Docs(name = filename, url = url)
						db.session.add(doc1)
				db.session.commit()
				flash('Документ %s добавлен' % (filename))
				return redirect(url_for('site.docs'))
			except:
				flash('Некорректный файл')
				return redirect(session['prevURL']+'?displayFileUpload=block' or url_for('main.index', displayFileUpload='block'))

	
	flash('Ошибка при заполнении ')
	return redirect(url_for('competition.routes', displayFileUpload='block'))

@site.route('/docs/delete', methods=['POST'])
@admin_required
def doc_delete():
	docName = request.form['name']
	doc = Docs.query.filter_by(name=docName).first()
	try:
		os.remove(os.path.join(current_app.config['UPLOADED_DOCUMENTS_DEST'], doc.name))
	except:
		Docs.query.filter_by(name=docName).delete()
		flash('Такого документа уже нет на сервере')
		return redirect(url_for('site.docs'))
	Docs.query.filter_by(name=docName).delete()
	flash('Документ удален')
	return redirect(url_for('site.docs'))


#==========Site structure administration==========#

@site.route('/admin')
@login_required
@permission_required(Permission.ADMINVIEW)
def administration():
	logos = Logo.query.all()
	infos = Page.query.filter_by(section='info').all()
	medias = Page.query.filter_by(section='media').all()
	competitions = Page.query.filter_by(section='competition').all()
	
	if Logo.query.filter_by(status='active').first() is None:
		blank = True
	else:
		blank = False
	return render_template('site/admin.html', logos=logos, blank=blank, infos=infos, medias=medias, competitions=competitions)

	#==========Main Logo Section==========#

@site.route('/admin/add_logo', methods=['POST'])
@admin_required
def add_logo():
	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(url_for('site.administration', displayNewPhoto='block'))
		else:
			try:
				for file in request.files.getlist('docs'):
					if file and allowed_file(file.filename):
						if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
							raise TypeError("storage must be a werkzeug.FileStorage")
							flash('Левый файл')
							return redirect(url_for('site.administration', displayNewPhoto='block'))

						file.filename = translit(file.filename,'ru', reversed=True)
						if len(file.filename)>34:
							file.filename = file.filename[0:20]+ os.path.splitext(file.filename)[1]
						imgName = images.save(file)
						imgURL = images.url(imgName)
						
						photo = Logo(
							imgName = imgName, 
							imgURL = imgURL, 
							status = '')
						db.session.add(photo)
				db.session.commit()
				flash('Логотип добавлен')
				return redirect(url_for('site.administration'))
			except:
				flash('Какой-то некорректный файл :(')
				return redirect(url_for('site.administration', displayNewPhoto='block'))
	flash('Упс, что-то не сработало :(')
	return redirect(url_for('site.administration'))	

@site.route('/admin/delete_logo', methods=['POST'])
@admin_required
def delete_logo():
	logoID = request.form['logoID']
	logo = Logo.query.filter_by(id=logoID).first()
	
	try:
		os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], logo.imgName))
	except:
		pass
	
	Logo.query.filter_by(id=logoID).delete()
	flash('Логотип удален')	
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@site.route('/admin/make_logo_active', methods=['POST'])
@admin_required
def make_logo_active():

	if Logo.query.filter_by(status='active').first() is not None:
		Logo.query.filter_by(status='active').first().status = ''
	
	if request.form['logoID'] != '0':
		Logo.query.filter_by(id=request.form['logoID']).first().status = 'active'	
	
	db.session.commit()

	flash('Изменения сохранены')	
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}	





	#==========Site structure administration==========#

@site.route('/admin/create_page', methods=['POST'])
@admin_required
def create_page():
	if request.method == 'POST':

		if Page.query.filter_by(iconDescription=request.form['description']).first() is None:
			iconDescriptionEng = translit(request.form['description'],'ru', reversed=True)
			iconDescriptionEng = iconDescriptionEng.replace(' ','_')
			page = Page(
				icon=request.form['icon'], 
				iconDescription = request.form['description'],
				iconDescriptionEng = iconDescriptionEng, 
				section=request.form['section'],
				header='', body='')
			db.session.add(page)
			db.session.commit()

			return redirect(url_for('site.administration'))
		else:
			flash('Такое описание уже существует!')
			return	redirect(url_for('site.administration', displayNewPage='block'))
	flash('Возникла ошибка')
	return redirect(url_for('site.administration'))



@site.route('/edit_page/<iconDescriptionEng>', methods=['GET','POST'])
@login_required
def edit_page(iconDescriptionEng):
	
	page = Page.query.filter_by(iconDescriptionEng=iconDescriptionEng).first()
	form = PostForm()
	if page is None:
		return render_template('site/page.html', page={"header":"Такой страницы не существует :(", "body":"", "bodyHTML":""})
	
	if form.validate_on_submit():
		if current_user.role != 'admin': 
			abort(403)

		page.body = form.body.data
		page.header = form.header.data
		db.session.add(page)
		flash('Страничка обновлена')

		form.header.data = page.header
		form.body.data = page.body
		
		return redirect(url_for('site.page', iconDescriptionEng=iconDescriptionEng))
	
	form.header.data = page.header
	form.body.data = page.body
	return render_template('/site/editpage.html', form=form, page=page, iconDescriptionEng=iconDescriptionEng)



@site.route('/page/<iconDescriptionEng>')
def page(iconDescriptionEng):
	page = Page.query.filter_by(iconDescriptionEng=iconDescriptionEng).first()
	if page is not None:
		return render_template('site/page.html', page=page)
	else: 
		return render_template('site/page.html', page={"header":"Такой страницы не существует :(", "body":"", "bodyHTML":""})


@site.route('/admin/delete_page', methods=['POST'])
@admin_required
def delete_page():
	pageID = request.form['pageID']
	page = Page.query.filter_by(id=pageID).delete()
	
	flash('Страница удалена')	
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
