from .. import db
from markdown import markdown
import bleach, re, string

class Competition(db.Model):
	__tablename__='competition'
	id=db.Column(db.Integer, primary_key=True)
	competitionName = db.Column(db.String(64)) # название соревнований
	numberOfSets = db.Column(db.Integer, default = 0) # количество сетов в соревновании 
	participantsListStatus = db.Column(db.String(64)) #статус финальных списков (опубликован или нет) default = closed
	finalResultsStatus = db.Column(db.String(64)) #статус результатов соревнований (опубликованы или нет) default = closed
	competitionStatus = db.Column(db.String(64)) #статус самих соревнований (открыты или нет) default = closed
	routesStatus = db.Column(db.String(64), default = '0') #статус трасс, открыты или нет (default =  0 == all sets closed ), может прнимать значения 1-512 в зависимости от того какой сет сейчас открыт
	numberOfRoutes = db.Column(db.Integer) #количество трасс по default = 0
	highlightFinals = db.Column(db.String(32)) #нужно ли выделять финалистов или нет default = 'yes'
	resultsHeader = db.Column(db.String(1000)) #заголовок для финальных результатов
	resultsBody = db.Column(db.Text) #текст для финальных результатов
	resultsBodyHTML = db.Column(db.Text) #html-текст для финальных результатов
	registrationStatus = db.Column(db.String(64)) #Статус регстрации - открыта/закрыта defaulte = 'closed'

	def __repr__(self):
		return '<competition %s nuber of sets %s >' % (self.competitionName, self.numberOfSets)	
		
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

		target.resultsBodyHTML = bleach.linkify(bleach.clean(markdown(value, outpit_format='html'),
			tags=allowed_tags, strip=True,
			attributes=allowed_attr,
			styles=allowed_styles))

db.event.listen(Competition.resultsBody, 'set', Competition.on_change_body)

class CompetitionArchive(db.Model):
	__tablename__='competitionArchive'
	id=db.Column(db.Integer, primary_key=True)
	competitionName = db.Column(db.String(64))
	

	def __repr__(self):
		return '<competition %s >' % (self.competitionName)	
