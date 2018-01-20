from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from markdown import markdown
import bleach, re, string
from Stepanych.models.routes import Routes
from Stepanych.models.competition import Competition
from sqlalchemy import event
from sqlalchemy.orm import backref

class mainTable(db.Model, UserMixin):
	__tablename__='main'
	keyTeamCompetition = db.Column(db.String(256), primary_key=True, index=True, unique = True)
	competition = db.Column(db.String(64), index=True)
	email = db.Column(db.String(64), index=True)
	teamName = db.Column(db.String(128), index=True)
	passwordHash = db.Column(db.String(256))
	setNumber = db.Column(db.Integer, default = 1)
	name1 = db.Column(db.String(64))
	sname1 = db.Column(db.String(64))
	year1 = db.Column(db.Integer, default = 0)
	male1 = db.Column(db.String(64))
	club1 = db.Column(db.String(64))
	alpSkill1 = db.Column(db.String(64))
	climbSkill1 = db.Column(db.String(64))
	name2 = db.Column(db.String(64))
	sname2 = db.Column(db.String(64))
	year2 = db.Column(db.Integer, default = 0)
	male2 = db.Column(db.String(64))
	club2 = db.Column(db.String(64))
	alpSkill2 = db.Column(db.String(64))
	climbSkill2 = db.Column(db.String(64))	
	role = db.Column(db.String(64), db.ForeignKey('roles.role', ondelete='CASCADE'))
	teamChange = db.Column(db.String(64))
	waitingListYes = db.Column(db.Integer, default = 1)
	keyName1Sname1Year1 = db.Column(db.String(256))
	keyName2Sname2Year2 = db.Column(db.String(256))
	position = db.Column(db.Integer, default = 0)
	confirmed = db.Column(db.String(64), default = 'False')
	pendingEmail = db.Column(db.String(64))
	teamStatus = db.Column(db.String(64)) # discqualified/не явились/ок
	bestTeams = db.Column(db.String(64)) # best weemen team, best M+W

	routeTimeSec1 = db.Column(db.Integer, default = 0)
	routeTimeSec2 = db.Column(db.Integer, default = 0)
	routeTimeSec3 = db.Column(db.Integer, default = 0)
	routeTimeSec4 = db.Column(db.Integer, default = 0)
	routeTimeSec5 = db.Column(db.Integer, default = 0)
	routeTimeSec6 = db.Column(db.Integer, default = 0)
	routeTimeSec7 = db.Column(db.Integer, default = 0)
	routeTimeSec8 = db.Column(db.Integer, default = 0)
	routeTimeSec9 = db.Column(db.Integer, default = 0)
	routeTimeSec10 = db.Column(db.Integer, default = 0)
	routeTimeSec11 = db.Column(db.Integer, default = 0)
	routeTimeSec12 = db.Column(db.Integer, default = 0)
	routeTimeSec13 = db.Column(db.Integer, default = 0)
	routeTimeSec14 = db.Column(db.Integer, default = 0)
	routeTimeSec15 = db.Column(db.Integer, default = 0)
	routeTimeSec15 = db.Column(db.Integer, default = 0)
	routeTimeSec16 = db.Column(db.Integer, default = 0)
	routeTimeSec17 = db.Column(db.Integer, default = 0)
	routeTimeSec18 = db.Column(db.Integer, default = 0)
	routeTimeSec19 = db.Column(db.Integer, default = 0)
	routeTimeSec20 = db.Column(db.Integer, default = 0)
	routeTimeSec21 = db.Column(db.Integer, default = 0)
	routeTimeSec22 = db.Column(db.Integer, default = 0)
	routeTimeSec23 = db.Column(db.Integer, default = 0)
	routeTimeSec24 = db.Column(db.Integer, default = 0)
	routeTimeSec25 = db.Column(db.Integer, default = 0)
	routeTimeSec26 = db.Column(db.Integer, default = 0)
	routeTimeSec27 = db.Column(db.Integer, default = 0)
	routeTimeSec28 = db.Column(db.Integer, default = 0)
	routeTimeSec29 = db.Column(db.Integer, default = 0)
	routeTimeSec30 = db.Column(db.Integer, default = 0)
	routeTimeSec31 = db.Column(db.Integer, default = 0)
	routeTimeSec32 = db.Column(db.Integer, default = 0)
	routeTimeSec33 = db.Column(db.Integer, default = 0)
	routeTimeSec34 = db.Column(db.Integer, default = 0)
	routeTimeSec35 = db.Column(db.Integer, default = 0)

	routeScoreFinal = db.Column(db.Float, default = 0)
	routeTimeSecFinal = db.Column(db.Integer, default = 0)
	routeScoreTotal = db.Column(db.Float, default = 0)
	routeTimeSecTotal = db.Column(db.Integer, default = 0)
	
	posts = db.relationship('Post', backref=backref('author', passive_deletes=True), lazy='dynamic', primaryjoin='Post.keyTeamCompetition == mainTable.keyTeamCompetition', cascade='all, delete-orphan')
	comments =db.relationship('Comment', backref=backref('author', passive_deletes=True), lazy='dynamic', cascade='all, delete-orphan')

	def is_authenticated(self):
		return True

	def get_id(self):
		return self.keyTeamCompetition

	@login_manager.user_loader
	def load_user(user_id):
	    try:
	        return mainTable.query.get(user_id)
	    except:
	        return None
	
	def to_json(self):
		json_team = {
			'keyTeamCompetition':self.keyTeamCompetition,
			'competition':self.competition,
			'email':self.email,
			'teamName':self.teamName,
			'name1':self.name1,
			'sname1':self.sname1,
			'club1':self.club1,
			'year1':self.year1,
			'alpSkill1':self.alpSkill1,
			'climbSkill1':self.climbSkill1,
			'male1':self.male1,
			'name2':self.name2,
			'sname2':self.sname2,
			'club2':self.club2,
			'year2':self.year2,
			'alpSkill2':self.alpSkill2,
			'climbSkill2':self.climbSkill2,				
			'male2':self.male2
		}
		return json_team

	
	def results(self,routeNuber,competition):
		results = {
		'routeScoreTotal':self.routeScoreTotal,
		'routeScoreFinal':round(self.routeScoreFinal,0),
		'routeTimeSecTotal':self.routeTimeSecTotal,
		'routeTimeSecTotalMin': round((self.routeTimeSecTotal - self.routeTimeSecTotal%60)/60,0),
		'routeTimeSecTotalSec': self.routeTimeSecTotal%60
		}
		if routeNuber == 0:
			routesPassed = 0
			for route in Routes.query.filter_by(competition=competition).all():
				timex = 'routeTimeSec' + str(route.routeNuber)
				if getattr(self,timex) != 0 :
					routesPassed = routesPassed + 1
			results['routesPassed'] = routesPassed
		else:
			if routeNuber == 1000:
				pass
			else:	
				route = Routes.query.filter_by(competition=competition).filter_by(routeNuber=routeNuber).first()
				timex = 'routeTimeSec' + str(route.routeNuber)
				timeMin = timex + 'Min'
				timeSec = timex + 'Sec'
				results[timex] = getattr(self,timex,0)
				results[timeMin] = round((results[timex] - results[timex]%60)/60,0)
				results[timeSec] = results[timex]%60
		
		return results

	@staticmethod
	def update_scores(competition):
		teams = mainTable.query.filter_by(competition=competition).all()
		routes = Routes.query.filter_by(competition=competition).all()
		for team in teams:
			
			team.routeTimeSecTotal = 0
			for i in range(1,36):
				timex = 'routeTimeSec' + str(i)
				team.routeTimeSecTotal = int(team.routeTimeSecTotal) + int(getattr(team, timex,0))+int(team.routeTimeSecFinal)

			team.routeScoreTotal = 0
			for route in routes:
				routeAttrName = 'routeTimeSec'+str(route.routeNuber)
				if getattr(team,routeAttrName,0) != 0:
					team.routeScoreTotal = team.routeScoreTotal + route.weight
				else:
					team.routeScoreTotal = team.routeScoreTotal
			
			team.routeScoreTotal = team.routeScoreTotal + team.routeScoreFinal
					
			db.session.add(team)

		db.session.commit	

	@staticmethod
	def update_positions(competition):
		
		teams = mainTable.query.filter_by(competition=competition).filter_by(teamStatus='ok').order_by(mainTable.routeScoreTotal.desc()).order_by(mainTable.routeTimeSecTotal).all()
		for index, team in enumerate(teams, start=1):
			team.position = index
			team.bestTeams = 'none'
			db.session.add(team)

		badTeams = mainTable.query.filter_by(competition=competition).filter(mainTable.teamStatus != 'ok').all()
		for teamx in badTeams:
			teamx.position = 0
			teamx.bestTeams = 'none'
			db.session.add(teamx)

		bestWeemen = mainTable.query.filter_by(male1='Ж').filter_by(male2='Ж').filter_by(competition=competition).order_by(mainTable.routeScoreTotal.desc()).order_by(mainTable.routeTimeSecTotal).first()
		if bestWeemen is not None:
			bestWeemen.bestTeams = 'weemen'
			db.session.add(bestWeemen)
		bestMix1 = mainTable.query.filter_by(male1='М').filter_by(male2='Ж').filter_by(competition=competition).order_by(mainTable.routeScoreTotal.desc()).order_by(mainTable.routeTimeSecTotal).first()
		bestMix2 = mainTable.query.filter_by(male1='Ж').filter_by(male2='М').filter_by(competition=competition).order_by(mainTable.routeScoreTotal.desc()).order_by(mainTable.routeTimeSecTotal).first()
		
		if bestMix1 is None and bestMix2 is not None:
			if bestMix2.routeScoreTotal > 0:
				bestMix2.bestTeams = 'mix'
				db.session.add(bestMix2)

		if bestMix2 is None and bestMix1 is not None:
			if bestMix1.routeScoreTotal > 0:
				bestMix1.bestTeams = 'mix'
				db.session.add(bestMix1)
				
		if bestMix1 is None and bestMix2 is None:
			pass	
		else:
			if bestMix1 is not None and bestMix2 is not None:		
				if bestMix1.routeScoreTotal > bestMix2.routeScoreTotal:
					bestMix1.bestTeams = 'mix'
					db.session.add(bestMix1)
				else:
					bestMix2.bestTeams = 'mix'
					db.session.add(bestMix2)

		db.session.commit()


	@property
	def password(self):
		raise AttributeError('пароль запрещен к просмотру')

	@password.setter
	def password(self, password):
		self.passwordHash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.passwordHash, password)

	def __repr__(self):
		return '<Team %s email %s Competition %s Set %s>' % (self.teamName, self.email, self.competition, self.setNumber)
	
	# Функции отвечающие за подтверждение акаунта
	def generate_confirmation_token(self, expiration = 259200):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.keyTeamCompetition})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False	
		if data.get('confirm') != self.keyTeamCompetition:
			return False
		self.confirmed = 'True'
		db.session.add(self)
		return True

	#функции отвечающие за проверку прав пользователя
	def can(self, permissions1):
		return self.roleName is not None and (self.roleName.permissions & permissions1) == permissions1

	def is_administrator(self):
		return self.can(Permission.ADMIN)
	#функции для генерации фэйковых данных для девелопмента, не нужны в продакшене
	@staticmethod
	def generate_fake(count=10):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			teamName1 = forgery_py.internet.user_name(True)
			competition1 = 'Степаныч2017'
			t = mainTable(
				competition=competition1,
				email=forgery_py.internet.email_address(),
				teamName=teamName1,
				password=forgery_py.lorem_ipsum.word(),
				confirmed=True,
				name1=forgery_py.name.first_name(),
				sname1=forgery_py.name.last_name(),
				club1=forgery_py.internet.user_name(),
				year1=forgery_py.date.year(past=True, min_delta=18, max_delta=38),
				alpSkill1='1й',
				climbSkill1='2й',
				male1='М',
				name2=forgery_py.name.first_name(),
				sname2=forgery_py.name.last_name(),
				club2=forgery_py.internet.user_name(),
				year2=forgery_py.date.year(past=True, min_delta=18, max_delta=38),
				alpSkill2='1й',
				climbSkill2='2й',				
				keyTeamCompetition=teamName1+competition1,
				male2='Ж',
				role='user',
				teamChange='False'
				)
			db.session.add(t)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()


class anonymousTeam(AnonymousUserMixin):
	role = 'anonymous'
	teamName = 'anonymous'
	def can(self, permissions):
		return False
	def is_administrator(self):
		return False

login_manager.anonymous_user = anonymousTeam


class Members(db.Model):
	__tablename__='members'
	id=db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	sname = db.Column(db.String(64))
	year = db.Column(db.Integer)
	keyNameSnameYear = db.Column(db.String(128))
	club = db.Column(db.String(128))
	alpSkill = db.Column(db.String(32))
	climbSkill = db.Column(db.String(32))
	male = db.Column(db.String(32))


	def __repr__(self):
		return '<name %s second name %s birth year %s club %s alb %s climb %s >' % (self.name,self.sname, self.year, self.club, self.alpSkill, self.climbSkill)	



class Permission: 
	#bit based permissions, for example if we need to provide comment + write article permission it will be 0x01 + 0x02 = 0x03
	COMMENT = 0x01 #in HEX = 00000001 in duble
	WRITE_ARTICLES = 0x02 #in HEX = 00000010 in duble
	ADMINVIEW =0x04 #in HEX = 00000100 in duble
	MODERATE_COMMENTS = 0x08 #in HEX = 00001000 in duble
	ADMIN = 0x80 #in HEX = 10000000 in duble



class Roles(db.Model):
	__tablename__='roles'	
	role = db.Column(db.String(64), unique = True, primary_key=True)
	defaults = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	keyTeamCompetition = db.relationship('mainTable', backref=backref('roleName', passive_deletes=True), lazy='dynamic')

	@staticmethod
	def insert_roles():
		rolesDict ={
		'user':(Permission.COMMENT | Permission.WRITE_ARTICLES, True),
		'guest':(Permission.ADMINVIEW, False),
		'admin':(0xff, False)
		}
		for r in rolesDict:
			role = Roles.query.filter_by(role = r).first()
			if role is None:
				role = roles(role=r)
			role.permissions = rolesDict[r][0]
			role.defaults = rolesDict[r][1]
			db.session.add(rold)
		db.session.commit()	