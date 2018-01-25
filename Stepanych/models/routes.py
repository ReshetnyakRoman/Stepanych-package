from .. import db
from Stepanych.models.competition import Competition

class Routes(db.Model):
	__tablename__='routes'
	id=db.Column(db.Integer, primary_key=True)
	routeNuber=db.Column(db.Integer)
	score = db.Column(db.Integer)
	controlTimeSec = db.Column(db.Integer)
	teamsPassTrough = db.Column(db.Integer)
	picName = db.Column(db.String(128))
	picURL = db.Column(db.String(512))
	name = db.Column(db.String(128))
	competition = db.Column(db.String(128))

	def to_json(self):
		json_route ={
			"routeNuber":self.routeNuber,
			"score":self.score,
			"controlTimeSec":self.controlTimeSec,
			"teamsPassTrough":self.teamsPassTrough,
			"picName":self.picName,
			"picURL":self.picURL,
			"name":self.name
		}
		return json_route

	#@property
	@staticmethod
	def routeList(competition):
		routes = Routes.query.filter_by(competition=competition).all()
		routeList = []
		for route in routes:
			routeList[loop.index]=route.routeNuber
		return routeList

	@property
	def weight(self):
		if self.teamsPassTrough == 0:
			weight = self.score
		else:
			weight = self.score / self.teamsPassTrough
		return weight



	def __repr__(self):
		return '<competition %s nuber of sets %s >' % (self.name, self.competition)	

class setDescriptions(db.Model):
	__tablename__='setDescriptions'
	id=db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(64))
	setNuber = db.Column(db.Integer)

	@property
	def bitwhiseStatus(self):
		competition = Competition.query.first()
		return int(competition.routesStatus) & int(2**(int(self.setNuber)-1)) 

	def __repr__(self):
		return '%s' % (self.setNuber)	
