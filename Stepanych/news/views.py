from flask import render_template, redirect, request, url_for, flash, session
from . import news
from flask_login import login_user, logout_user, login_required, current_user
from Stepanych.models.users import mainTable, Permission
from Stepanych.models.competition import Competition
from Stepanych.models.post import Post, Comment, PostGallery
from Stepanych.models.routes import setDescriptions
from .form import PostForm, CommentForm
from flask import current_app
from Stepanych.decorators import admin_required, permission_required
import os, bleach
from werkzeug import secure_filename, FileStorage
from transliterate import translit, get_available_language_codes
from Stepanych import db, images


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'] 

def name_rus(filename):
	return '.' not in filename


@news.route('/', methods=['GET','POST'])
@permission_required(Permission.ADMINVIEW)
def new_post():
	postForm = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and postForm.validate_on_submit():
		post = Post(body = postForm.body.data, header=postForm.header.data, author = current_user._get_current_object())
		db.session.add(post)
		db.session.commit()
		postID = Post.query.order_by(Post.id.desc()).first().id

		if request.method == 'POST' and request.files.getlist('docs'):
			
			if request.files['docs'].filename == '':
				return redirect(url_for('main.index'))
			else:
				try:
					for file in request.files.getlist('docs'):
						if file and allowed_file(file.filename):
							if not isinstance(file, FileStorage): # Validate that what we have been supplied with is infact a file
								raise TypeError("storage must be a werkzeug.FileStorage")
								flash('Левый файл')
								return render_template('/news/newpost.html', NewsForm=postForm)

							file.filename = translit(file.filename,'ru', reversed=True)
							if len(file.filename)>34:
								file.filename = file.filename[0:20]+ os.path.splitext(file.filename)[1]
							imgName = images.save(file)
							imgURL = images.url(imgName)
							

							gallery = PostGallery(
								imgName = imgName, 
								imgURL = imgURL, 
								postID = postID,
								)
							db.session.add(gallery)
					db.session.commit()
					return redirect(url_for('main.index'))
				
				except:
					flash('Некорректный файл')
					return render_template('/news/newpost.html', NewsForm=postForm)
	
		return redirect(url_for('main.index'))
		
	return render_template('/news/newpost.html', NewsForm=postForm)

@news.route('/post/<int:id>', methods=['POST','GET'])
def post(id):
	form=CommentForm()
	if request.args.get('prevURL') is not None:
		session['prevURL'] = request.args.get('prevURL')
	prevURL=str(request.args.get('prevURL'))[2:]
	post = Post.query.get_or_404(id)
	if form.validate_on_submit():
		comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
		db.session.add(comment)
		flash('Ваш комментарий добавлен!')
		return redirect(url_for('news.post', id=id))
	comments = post.comments.order_by(Comment.timestamp.desc())
	gallery = post.gallery
	return render_template('/news/post.html', posts=post, prevURL=session['prevURL'][2:], form = form, comments = comments,gallery=gallery)

@news.route('/delete/<int:id>')
@admin_required
def delete(id):
	
	gallery = PostGallery.query.filter_by(postID=id).all()

	if gallery is not None:
		for pic in gallery:
			try:
				os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], pic.imgName ))
			except:
				pass
	PostGallery.query.filter_by(postID=id).delete()
	Post.query.filter_by(id=id).delete()
	return redirect(url_for('main.index'))

@news.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
	Comment.query.filter_by(id=id).delete()
	flash('Комментарий удален!')
	return redirect(session['currentURL'])


@news.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
	if request.args.get('prevURL') is not None:
		session['prevURL'] = request.args.get('prevURL')
	post = Post.query.get_or_404(id)
	gallery = post.gallery
	if current_user != post.author and not current_user.can(Permission.ADMIN):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		post.header = form.header.data
		db.session.add(post)
		flash('Пост успешно обновлен!')
		form.header.data = post.header
		form.body.data = post.body
		return render_template('/news/editpost.html', form=form, prevURL=session['prevURL'], gallery=gallery, post=post)
	form.header.data = post.header
	form.body.data = post.body
	return render_template('/news/editpost.html', form=form, prevURL=session['prevURL'], gallery=gallery, post=post)

@news.route('/edit/add_post_photo', methods=['POST'])
@login_required
def add_post_photo():
	postID = request.form['postID']
	if request.method == 'POST' and request.files.getlist('docs'):
		if request.files['docs'].filename == '':
			flash('Файл не приложен')
			return redirect(url_for('news.edit_post', id=postID, displayNewPhoto='block'))
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
						
						gallery = PostGallery(
							imgName = imgName, 
							imgURL = imgURL, 
							postID = bleach.clean(postID))
						db.session.add(gallery)
				db.session.commit()
				flash('Фото добавлены!')
				return redirect(url_for('news.edit_post', id=postID))
			except:
				flash('Некорректный файл')
				return redirect(url_for('news.edit_post', id=postID, displayNewPhoto='block'))
	flash('Упс, что-то не сработало :(')
	return redirect(url_for('news.edit_post', id=postID, displayNewPhoto='block'))


@news.route('/edit/delete_post_photo', methods=['POST'])
@login_required
def delete_post_photo():
	photoID = request.form['photoID']
	photo = PostGallery.query.filter_by(id=photoID).first()
	
	try:
		os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], photo.imgName))
	except:
		pass
	
	PostGallery.query.filter_by(id=photoID).delete()
	return redirect(url_for('main.index'))	