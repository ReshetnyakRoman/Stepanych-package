from .. import db
from markdown import markdown
import bleach, re, string

class Docs(db.Model):
	__tablename__='docs'
	id=db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	url = db.Column(db.String(512))


	def to_json(self):
		json_doc ={

			"id":self.id,
			"url":self.url,
			"name":self.name
		}
		return json_doc

	def __repr__(self):
		return '<name %s url %s >' % (self.name,self.url)	

class Logo(db.Model):
	__tablename__='logo'
	id=db.Column(db.Integer, primary_key=True)
	imgName = db.Column(db.String(128)) 
	imgURL = db.Column(db.String(128)) 
	status = db.Column(db.String(32)) 
	
	def __repr__(self):
		return '<name %s gallery %s >' % (self.imgName, self.imgURL)

class Rules(db.Model):
	__tablename__='rules'
	id=db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128)) #имя документа на документа на диске
	nameRus = db.Column(db.String(128)) #название на карточке
	url = db.Column(db.String(512)) #ссылка на документы
	color = db.Column(db.Integer) # для разных цветов карточки


	def to_json(self):
		json_doc ={

			"id":self.id,
			"url":self.url,
			"name":self.name,
			"nameRus":self.nameRus

		}
		return json_doc

	def __repr__(self):
		return '<name %s url %s >' % (self.name,self.url)

class Contacts(db.Model):
	__tablename__='contacts'
	id=db.Column(db.Integer, primary_key=True)
	fileName = db.Column(db.String(128))
	fullName = db.Column(db.String(128))
	url = db.Column(db.String(128))
	jobDescription = db.Column(db.String(128))
	vkURL = db.Column(db.String(128))
	fbURL = db.Column(db.String(128))
	email = db.Column(db.String(128))


	def __repr__(self):
		return '<name %s role %s >' % (self.fullName,self.jobDescription)

class Press(db.Model):
	__tablename__='press'
	id=db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(128))
	url = db.Column(db.String(128))
	domain = db.Column(db.String(128))

	def __repr__(self):
		return '<description %s url %s >' % (self.description,self.url)

class Video(db.Model):
	__tablename__='video'
	id=db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(128))
	youtubeURL = db.Column(db.String(128))
	vimeoURL = db.Column(db.String(128))

	def __repr__(self):
		return '<description %s url %s >' % (self.description,self.url)

class Sponsors(db.Model):
	__tablename__='sponsors'
	id=db.Column(db.Integer, primary_key=True)
	imgName = db.Column(db.String(128)) 
	linkToSponsor = db.Column(db.String(128)) 
	imgURL = db.Column(db.String(128)) 
	sponsorName = db.Column(db.String(128)) #alt name for pic
	sponsorType = db.Column(db.String(128)) #general/partners/others
	
	def __repr__(self):
		return '<name %s url %s >' % (self.sponsorName, self.linkToSponsor)

class Photo(db.Model):
	__tablename__='gallery'
	id=db.Column(db.Integer, primary_key=True)
	imgName = db.Column(db.String(128)) 
	imgURL = db.Column(db.String(128))
	galleryURL = db.Column(db.String(512), default = 'None') 
	galleryName = db.Column(db.String(128))
	galleryID =  db.Column(db.Integer)
	authorName = db.Column(db.String(128))
	def __repr__(self):
		return '<name %s gallery %s >' % (self.imgName, self.galleryName)

class Page(db.Model):
	__tablename__ = 'pages'
	id = db.Column(db.Integer, primary_key=True)
	header = db.Column(db.String(1000))
	body = db.Column(db.Text)
	bodyHTML = db.Column(db.Text)
	icon = db.Column(db.String(32))
	iconDescription = db.Column(db.String(64), unique = True)
	iconDescriptionEng = db.Column(db.String(64), unique = True)
	section = db.Column(db.String(32))

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

db.event.listen(Page.body, 'set', Page.on_change_body)

