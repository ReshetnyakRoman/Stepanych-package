from flask import flash, redirect, render_template, request, url_for, session, abort  
from flask_wtf.csrf import CSRFProtect
from Stepanych import db
from . import competition
from Stepanych.models.users import mainTable, Permission, Members
from Stepanych.models.competition import Competition
from Stepanych.decorators import admin_required, permission_required
from flask_login import login_user, logout_user, login_required, current_user
from flask import jsonify, json, Response

@competition.route('/registredteams')
def registred_teams():
	competition = Competition.query.first()
	numberOfSets = competition.numberOfSets
	registredTeams = {}
	registredTeamsUpdated = {} #список команд с обновленным после лотереи номером сета который записан в колонке waitingListYes
	waitingList = mainTable.query.filter_by(waitingListYes=0).all()
	for i in range (1,numberOfSets+1):
		registredTeams[i]= mainTable.query.filter_by(competition=competition.competitionName).filter_by(setNumber=i).all()
	for i in range (1,numberOfSets+1):
		registredTeamsUpdated[i]= mainTable.query.filter_by(competition=competition.competitionName).filter_by(waitingListYes=i).all()

	return render_template('competition/registredTeams.html', 
		registredTeams=registredTeams,
		registredTeamsUpdated=registredTeamsUpdated,
		numberOfSets = numberOfSets,
		displayLoginForm=request.args.get('displayLoginForm'),
		competition=competition.competitionName,
		waitingList=waitingList,
		participantsListStatus = competition.participantsListStatus
		)	

@competition.route('/registredteams/update', methods=['POST'])
@admin_required
def registred_teams_update():
	competition = Competition.query.first()
	jsonTeamList = request.get_json(silent=True)
	if request.is_json and len(jsonTeamList['teamName'])>0:
		
		for i in range(len(jsonTeamList['teamName'])):
			changeSet = mainTable.query.filter_by(competition=competition.competitionName).filter_by(teamName=jsonTeamList['teamName'][i]).first()
			changeSet.waitingListYes = jsonTeamList['set'][i]
			db.session.add(changeSet)

		competition.participantsListStatus = "published"
		db.session.add(competition)
		changeStatusTeams = mainTable.query.filter_by(competition=competition.competitionName).filter_by(waitingListYes=0).all()
		for team in changeStatusTeams:
			team.teamStatus = 'ожид'
		db.session.commit()		
		flash('Изменения сохранены, списки участников опубликованы')
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	else: 
		competition.participantsListStatus = "published"
		db.session.add(competition)
		db.session.commit()
		flash('Списки участников опубликованы без изменений')
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@competition.route('/registredteams/save_update', methods=['POST'])
@admin_required
def registred_teams_update_save():
	competition = Competition.query.first()
	jsonTeamList = request.get_json(silent=True)
	if request.is_json and len(jsonTeamList['teamName'])>0:
		
		for i in range(len(jsonTeamList['teamName'])):
			changeSet = mainTable.query.filter_by(competition=competition.competitionName).filter_by(teamName=jsonTeamList['teamName'][i]).first()
			changeSet.waitingListYes = jsonTeamList['set'][i]
			db.session.add(changeSet)

		changeStatusTeams = mainTable.query.filter_by(competition=competition.competitionName).filter_by(waitingListYes=0).all()
		for team in changeStatusTeams:
			team.teamStatus = 'ожид'
		db.session.commit()		
		flash('Изменения сохранены')
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	else: 
		competition.participantsListStatus = "published"
		db.session.add(competition)
		db.session.commit()
		flash('Списки участников опубликованы без изменений')
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}		


@competition.route('/registredteams/unpublish', methods=['POST'])
@admin_required
def registred_teams_unpublish():
	participantsListStatus = request.form['status']
	competition = Competition.query.first()
	competition.participantsListStatus = participantsListStatus
	db.session.add(competition)
	db.session.commit()
	flash('Списки участников сняты с публикации')
	return Response({'success':True}, 200)

