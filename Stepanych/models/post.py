from .. import db
from .. import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime
from markdown import markdown
import bleach, re, string

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	header = db.Column(db.String(1000))
	body = db.Column(db.Text)
	bodyHTML = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	keyTeamCompetition = db.Column(db.String(128), db.ForeignKey('main.keyTeamCompetition'))
	comments =  db.relationship('Comment', backref='post', lazy='dynamic')
	gallery = db.relationship('PostGallery', backref='post', lazy='dynamic')

	def snippet(self):
		split = str.split(self.bodyHTML, '\n')
		snippet =''
		nuber_of_lines = 6
		if split is not None:
			for i in range(len(split)):
				snippet=snippet+split[i]
				if i > nuber_of_lines: 
					break
		return snippet			


	@staticmethod
	def generate_fake(count=10):
		from random import seed, randint
		import forgery_py

		seed()
		team_count = mainTable.query.count()
		for i in range(count):
			t = mainTable.query.offset(randint(0, team_count-1)).first()
			p = Post(
				body=forgery_py.lorem_ipsum.sentences(randint(1,4)), 
				header=forgery_py.lorem_ipsum.sentences(1),
				timestamp=forgery_py.date.date(True), 
				author=t)
			db.session.add(p)
			db.session.commit()

	@staticmethod
	def on_change_body(target, value, oldvalue, initiator):
		
		allowed_tags = ['a', 'abbr', 'b', 'blockquote', 
		'code', 'em', 'i', 'li', 
		'ol', 'pre', 'strong', 'ul', 
		'h1', 'h2', 'h3', 'p', 
		'img', 'br', 'div', 'em', 
		'span', 'hr','iframe', 'mark', 
		'picture', 'small', 'del', 'strong', 
		'sub','sup','style', 'table', 
		'tr', 'td', 'th','strike',
		'u','font','br', 'pre']

		allowed_attr={'*':['class'],
		'img': ['src', 'alt', 'width', 'height', 'data-non-image'],
		'a': ['href', 'target'], 
		'*': ['color'], 
		"span": ['font-size'],
		'*':['style'],
		'iframe':['width','height','src', 'frameborder', 'gesture', 'allow', 'allowfullscreen'],
		"p": ['margin-left', 'text-align'],
		"h1": ['margin-left', 'text-align'],
		"h2": ['margin-left', 'text-align'],
		"h3": ['margin-left', 'text-align'],
		"h4": ['margin-left', 'text-align'],
		"h5": ['margin-left', 'text-align'],
		"h6": ['margin-left', 'text-align'],}
		allowed_styles=['color','font-size','margin-left','text-align','*']

		target.bodyHTML = bleach.linkify(bleach.clean(markdown(value, outpit_format='html'),
			tags=allowed_tags, strip=True,
			attributes=allowed_attr,
			styles=allowed_styles))

db.event.listen(Post.body, 'set', Post.on_change_body)


class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	bodyHTML = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	disabled = db.Column(db.Boolean)
	author_id = db.Column(db.String(256), db.ForeignKey('main.keyTeamCompetition'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

	@staticmethod
	def on_change_body(target, value, oldvalue, initiator):
		
		allowed_tags = [
		'a', 'abbr', 'b', 'blockquote', 
		'code', 'i',
		'pre', 'strong', 'p', 
		'img', 'br', 'em', 
		'span', 'mark', 
		'picture', 'small', 'del', 'strong', 
		'sub','sup','style','strike','iframe',
		'u','font','br', 'pre']

		allowed_attr={'*':['class'],
		'img': ['src', 'alt', 'width', 'height', 'data-non-image'],
		'a': ['href', 'target'], 
		'*': ['color'], 
		"span": ['font-size'],
		'*':['style'],
		'iframe':['width','height','src', 'frameborder', 'gesture', 'allow', 'allowfullscreen'],
		"p": ['margin-left', 'text-align']}
		allowed_styles=['color','font-size','margin-left','text-align','*']

		target.bodyHTML = bleach.linkify(bleach.clean(markdown(value, outpit_format='html'), 
			tags=allowed_tags, 
			strip=True, 
			attributes=allowed_attr, 
			styles=allowed_styles))

db.event.listen(Comment.body, 'set', Comment.on_change_body)

class PostGallery(db.Model):
	__tablename__='PostGallery'
	id=db.Column(db.Integer, primary_key=True)
	imgName = db.Column(db.String(128)) 
	imgURL = db.Column(db.String(128)) 
	postID =  db.Column(db.Integer, db.ForeignKey('posts.id'))

	def __repr__(self):
		return '<name %s gallery %s >' % (self.imgName, self.galleryName)