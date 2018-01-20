from flask import flash, redirect, render_template, request, url_for, session, abort  
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from Stepanych import db
from . import competition
from Stepanych.models.users import mainTable
from Stepanych.models.competition import Competition
from Stepanych.models.routes import Routes
from Stepanych.decorators import admin_required, permission_required
from flask import jsonify, json, Response

@competition.route('/results')
def results():
	competition =  Competition.query.first()
	mainTable.update_scores(competition.competitionName)
	mainTable.update_positions(competition.competitionName)
	
	teams = mainTable.query.filter_by(competition=competition.competitionName).filter_by(teamStatus='ok').order_by(mainTable.routeScoreTotal.desc()).order_by(mainTable.routeTimeSecTotal).all()
	badTeams = mainTable.query.filter_by(competition=competition.competitionName).filter(mainTable.teamStatus != 'ok').order_by(mainTable.routeScoreTotal.desc()).all()
	routesInfo = Routes.query.filter_by(competition=competition.competitionName).all()
	return render_template('competition/results.html', 
		displayLoginForm=request.args.get('displayLoginForm'),
		routesInfo=routesInfo,
		teams=teams,
		badTeams=badTeams,
		competition =competition.competitionName,
		finalResultsStatus=competition.finalResultsStatus,
		highlightFinals=competition.highlightFinals,
		resultsHeader=competition.resultsHeader,
		resultsBodyHTML=competition.resultsBodyHTML)	

@competition.route('/results/update', methods=['POST'])
@admin_required
def results_update():
	jsonResultsUpdate = request.get_json(silent=True)
	
	if request.is_json:
		team = mainTable.query.filter_by(competition=jsonResultsUpdate['competition']).filter_by(teamName=jsonResultsUpdate['teamName']).first()
		if team is not None:
			competition=jsonResultsUpdate['competition']
			team.routeScoreFinal = jsonResultsUpdate['routeScoreFinal']
			team.teamStatus = jsonResultsUpdate['teamStatus']
			if jsonResultsUpdate['teamStatus'] == 'ok':
				team.waitingListYes = team.setNumber

			del jsonResultsUpdate['competition']
			del jsonResultsUpdate['teamName']		
			del jsonResultsUpdate['routeScoreFinal']
			del jsonResultsUpdate['teamStatus']
			
			for key, value  in jsonResultsUpdate.items():
				route = Routes.query.filter_by(routeNuber=key[12:]).filter_by(competition=competition).first()
				if route is not None:
					if value !=0 and getattr(team, key) == 0:
							route.teamsPassTrough = route.teamsPassTrough + 1
							setattr(team, key, value)
					else:
						if value !=0 and getattr(team, key) != 0:
							route.teamsPassTrough = route.teamsPassTrough
							setattr(team, key, value)
						else:
							if value == 0 and getattr(team, key) != 0:
								route.teamsPassTrough = route.teamsPassTrough - 1
								setattr(team, key, value)	
				

			db.session.add(route)
			db.session.add(team)
			db.session.commit()

			mainTable.update_scores(competition)

			flash('Изменения сохранены')
			return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	flash('Изменения не сохранены, возможно вы ввели некорректные данные или изменили данные стрзу нескольких команд')	
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@competition.route('/results/publish', methods=['POST'])
@admin_required
def results_publish():
	competition =  Competition.query.first()
	if request.method == 'POST':
		resultsHeader = request.form['resultsHeader']
		resultsBody = request.form['resultsBody']
		competition.resultsHeader = resultsHeader
		competition.resultsBody = resultsBody
		if competition.finalResultsStatus == 'closed':
			competition.finalResultsStatus = 'published'
			flash('Результаты опубликованы')
		else:
			competition.finalResultsStatus = 'closed'
			flash('Результаты сняты с публикации')
		
		db.session.add(competition)
		db.session.commit()
		return redirect(url_for('competition.results'))
	flash('Ошибочный запрос')	
	return redirect(url_for('competition.results'))


@competition.route('/results/highlight', methods=['POST'])
@admin_required
def highlightFinals():
	jsonHighlightFinals = request.get_json(silent=True)
	competition =  Competition.query.first()
	
	if request.is_json:
		competition.highlightFinals = jsonHighlightFinals['highlight']
		db.session.add(competition)
		db.session.commit()
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	
	flash('Выделить финалистов не удалось :(')
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@competition.route('/archive/<competitionName>')
def archive(competitionName):
	mainTable.update_scores(competitionName)
	mainTable.update_positions(competitionName)
	if request.args.get('prevURL') is not None:
		session['prevURL'] = request.args.get('prevURL')

	teams = mainTable.query.filter_by(competition=competitionName).filter_by(teamStatus='ok').order_by(mainTable.routeScoreTotal.desc()).order_by(mainTable.routeTimeSecTotal).all()
	badTeams = mainTable.query.filter_by(competition=competitionName).filter(mainTable.teamStatus != 'ok').order_by(mainTable.routeScoreTotal.desc()).all()
	routesInfo = Routes.query.filter_by(competition=competitionName).all()
	return render_template('competition/archive.html', 
		displayLoginForm=request.args.get('displayLoginForm'),
		routesInfo=routesInfo,
		teams=teams,
		badTeams=badTeams,
		competition =competitionName,
		highlightFinals='yes',
		prevURL=session['prevURL'])
