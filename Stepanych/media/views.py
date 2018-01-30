from flask import flash, redirect, render_template, request, url_for, session, abort  
from . import media
from Stepanych import db, images
from flask import current_app
from flask_login import login_user, logout_user, login_required, current_user
from Stepanych.decorators import admin_required, permission_required
from Stepanych.models.site import Press, Video, Photo
import os, bleach
from urllib.parse import urlparse
from werkzeug import secure_filename, FileStorage
from transliterate import translit, get_available_language_codes

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'] 

def name_rus(filename):
	return '.' not in filename

#===============PRESS===============

@media.route('/press')
def press():
	press = Press.query.all();
	return render_template('media/press.html', displayLoginForm=request.args.get('displayLoginForm'), press=press)

@media.route('/press/add', methods=['POST'])
@admin_required
def add_article():
	if request.method == 'POST':
		url = bleach.clean(request.form['url'])
		url_object = urlparse(url)
		article = Press(
			description = bleach.clean(request.form['description']),
			url = url,
			domain = url_object.netloc
			)
		db.session.add(article)
		db.session.commit()
		flash('Ссылка на %s добавлена!' % (url_object.netloc))	
		return redirect(url_for('media.press'))
	flash('Упс, возникла какая-то проблема :(')	
	return redirect(url_for('media.press', displayNewArticle='block'))

@media.route('/press/delete', methods=['POST'])
@admin_required
def delete_article():
	if request.method == 'POST':

		url = request.form['url']
		Press.query.filter_by(url=url).delete()
		db.session.commit()
		flash('Запись удалена')
		return redirect(url_for('media.press'))

	flash('Упс, что-то пошло не так...')
	return redirect(url_for('media.press'))

#===============VIDEO===============

@media.route('/video')
def video():
	videos = Video.query.order_by(Video.id.desc()).all()
	return render_template('media/video.html', displayLoginForm=request.args.get('displayLoginForm'), videos=videos)

@media.route('/video/add', methods=['POST'])
@admin_required
def add_video():
	if request.method == 'POST':
		if request.form['youtubeURL'] == '' and request.form['vimeoURL'] == '':
			flash('Вы не добавили ни одной ссылки')	
			return redirect(url_for('media.video', displayNewVideo='block'))
		else:	
			video = Video(
				description = bleach.clean(request.form['description']),
				youtubeURL = bleach.clean(request.form['youtubeURL']),
				vimeoURL = bleach.clean(request.form['vimeoURL']))

			db.session.add(video)
			db.session.commit()
			flash('Ссылка на %s добавлена!' % (request.form['description']))	
			return redirect(url_for('media.video'))
	flash('Упс, возникла какая-то проблема :(')	
	return redirect(url_for('media.video', displayNewVideo='block'))

@media.route('/video/delete', methods=['POST'])
@admin_required
def delete_video():
	if request.method == 'POST':

		description = request.form['description']
		Video.query.filter_by(description=description).delete()
		db.session.commit()
		flash('Видео удалено')
		return redirect(url_for('media.video'))

	flash('Упс, что-то пошло не так...')
	return redirect(url_for('media.video'))	

#===============PHOTO===============

@media.route('/photo')
def photo():
	galleries = []
	galleryIDs = db.session.query(Photo.galleryID).group_by(Photo.galleryID)
	for index, row in enumerate(galleryIDs):
		galleries.append({})
		imgage = Photo.query.filter_by(galleryID=row.galleryID).first()
		galleries[index]['imgURL'] = imgage.imgURL
		galleries[index]['imgName'] = imgage.imgName
		galleries[index]['galleryName'] = imgage.galleryName
		galleries[index]['galleryID'] = imgage.galleryID
		galleries[index]['authorName'] = imgage.authorName


	return render_template('media/galleries.html', 
		displayLoginForm=request.args.get('displayLoginForm'),
		galleries=galleries)


@media.route('/photo/add', methods=['POST'])
@login_required
def add_gallery():
	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(url_for('media.photo', displayNewGallery='block'))
		else:
			try:
				if Photo.query.order_by(Photo.galleryID.desc()).first() is None:
							galleryID = 1
				else: 
					galleryID = int( Photo.query.order_by(Photo.galleryID.desc()).first().galleryID ) + 1
				for file in request.files.getlist('docs'):
					if file and allowed_file(file.filename):
						if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
							raise TypeError("storage must be a werkzeug.FileStorage")
							flash('Левый файл')
							return redirect(url_for('media.photo', displayNewGallery='block'))

						file.filename = translit(file.filename,'ru', reversed=True)
						if len(file.filename)>34:
							file.filename = file.filename[0:20]+ os.path.splitext(file.filename)[1]
						imgName = images.save(file)
						imgURL = images.url(imgName)
						

						gallery = Photo(
							imgName = imgName, 
							imgURL = imgURL, 
							galleryURL = bleach.clean(request.form['galleryURL']),
							galleryName = bleach.clean(request.form['galleryName']),
							galleryID = galleryID,
							authorName=current_user.teamName)
						db.session.add(gallery)
				db.session.commit()
				flash('Альбом "%s" добавлен!' % (request.form['galleryName']) )
				return redirect(url_for('media.photo'))
			except:
				flash('Вы не залогинены или некорректный файл')
				return redirect(url_for('media.photo', displayNewGallery='block'))
	flash('Упс, что-то не сработало :(')
	return redirect(url_for('media.photo'))




@media.route('/photo/delete', methods=['POST'])
@login_required
def delete_gallery():
	galleryID = request.form['galleryID']
	gallery = Photo.query.filter_by(galleryID=galleryID).all()
	
	for photo in gallery:
		try:
			os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], photo.imgName))
		except:
			pass
	
	Photo.query.filter_by(galleryID=galleryID).delete()
	flash('Альбом удален')
	return redirect(url_for('media.photo'))





@media.route('/photo/<int:id>')
def photo_gallery(id):
	gallery =  Photo.query.filter_by(galleryID=id).all()
	galleryInfo = Photo.query.filter_by(galleryID=id).first()
	return render_template('media/photo-gallery.html', 
		displayLoginForm=request.args.get('displayLoginForm'),
		gallery=gallery,galleryInfo=galleryInfo)



@media.route('/photo/add_photo', methods=['POST'])
@login_required
def add_photo():
	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(url_for('media.photo_gallery', displayNewPhoto='block'))
		else:
			try:
				for file in request.files.getlist('docs'):
					if file and allowed_file(file.filename):
						if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
							raise TypeError("storage must be a werkzeug.FileStorage")
							flash('Левый файл')
							return redirect(url_for('media.photo_gallery', displayNewPhoto='block'))

						file.filename = translit(file.filename,'ru', reversed=True)
						if len(file.filename)>34:
							file.filename = file.filename[0:20]+ os.path.splitext(file.filename)[1]
						imgName = images.save(file)
						imgURL = images.url(imgName)
						
						gallery = Photo(
							imgName = imgName, 
							imgURL = imgURL, 
							galleryName = bleach.clean(request.form['galleryName']),
							galleryID = bleach.clean(request.form['galleryID']),
							authorName=current_user.teamName)
						db.session.add(gallery)
				db.session.commit()
				flash('Фото добавлены')
				return redirect(url_for('media.photo_gallery', id=request.form['galleryID']))
			except:
				flash('Вы не залогинены или некоректный файл')
				return redirect(url_for('media.photo_gallery', id=request.form['galleryID'], displayNewPhoto='block'))
	flash('Упс, что-то не сработало :(')
	return redirect(url_for('media.photo_gallery'))




@media.route('/photo/delete_photo', methods=['POST'])
@login_required
def delete_photo():
	photoID = request.form['photoID']
	photo = Photo.query.filter_by(id=photoID).first()
	
	try:
		os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], photo.imgName))
	except:
		pass
	
	Photo.query.filter_by(id=photoID).delete()
	flash('Альбом удален')
	return redirect(url_for('media.photo'))