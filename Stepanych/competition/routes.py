from flask import flash, redirect, render_template, request, url_for, session, abort, jsonify
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from Stepanych import db
from . import competition
from flask import current_app
from Stepanych import images
from Stepanych.competition.form import RoutesForm
from Stepanych.models.routes import Routes
from Stepanych.models.users import mainTable
from Stepanych.models.competition import Competition
from Stepanych.decorators import admin_required, permission_required
from flask_login import login_user, logout_user, login_required, current_user
import os
from transliterate import translit, get_available_language_codes

@competition.route('/routes')
def routes():
	competition = Competition.query.first()
	routeForm = RoutesForm()
	routes = Routes.query.filter_by(competition=competition.competitionName).all()
	openSet = int(competition.routesStatus)
	
	if current_user.is_anonymous:
		userSetStatus = 0
	else:
		if current_user.waitingListYes != 0:
			userSet =  int(current_user.waitingListYes)
			userSetStatus = 2**(userSet-1)&openSet
		else:
			userSetStatus = 0

	if Routes.query.filter_by(competition=competition.competitionName).first() is None:
		noRotes = True
	else:
		noRotes = False
	return render_template('competition/routes.html', routeForm=routeForm, routes=routes, noRotes=noRotes, openSet = int(competition.routesStatus), userSetStatus=userSetStatus)


@competition.route('/routes/add', methods=['POST'])
@admin_required
def routes_add():
	routeForm = RoutesForm()
	competition = Competition.query.first()
	RouteCounter = Competition.query.first()
	if routeForm.validate_on_submit():
		if Routes.query.filter_by(routeNuber=routeForm.routeNuber.data).filter_by(competition=competition.competitionName).first() is None:
			if request.files['img'].filename == '':
				filename='logo_route.jpg'
				url = current_app.config['UPLOADED_IMAGES_URL'] + filename
			else:
				try:
					request.files['img'].filename = translit(request.files['img'].filename,'ru', reversed=True)
					if len(request.files['img'].filename)>64:
							request.files['img'].filename = request.files['img'].filename[0:20]+ os.path.splitext(request.files['img'].filename)[1]
					filename = images.save(request.files['img'])
					url = images.url(filename)
				except:
					flash('Некорректное имя файла')
					return redirect(url_for('competition.routes', displayAddNewRoute='block'))
			route = Routes(
				competition = competition.competitionName,
				routeNuber=routeForm.routeNuber.data,
				score = routeForm.routeScore.data,
				controlTimeSec = routeForm.routeTime.data,
				teamsPassTrough = 0,
				picName = filename,
				picURL = url,
				name = routeForm.routeName.data)
			
			RouteCounter.numberOfRoutes = RouteCounter.numberOfRoutes + 1
			db.session.add(route)
			db.session.add(RouteCounter)
			db.session.commit()
			flash('Трасса №%s добавлена' % (routeForm.routeNuber.data))
			return redirect(url_for('competition.routes'))
		else:
			flash('Трасса №%s уже существует' % (routeForm.routeNuber.data))
			return redirect(url_for('competition.routes', displayAddNewRoute='block'))
	
	flash('Ошибка при заполнении')
	return redirect(url_for('competition.routes', displayAddNewRoute='block'))


@competition.route('/routes/delete', methods=['POST'])
@admin_required
def route_delete():
	competition = Competition.query.first()
	routeNuber = request.form['routeNuber']
	route = Routes.query.filter_by(routeNuber=routeNuber).filter_by(competition=competition.competitionName).first()
	RouteCounter = Competition.query.first()
	if route.picName != 'logo_route.jpg':
		try:
			os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], route.picName))
			Routes.query.filter_by(routeNuber=routeNuber).filter_by(competition=competition.competitionName).delete()
			RouteCounter.numberOfRoutes = RouteCounter.numberOfRoutes - 1
			db.session.add(RouteCounter)
			db.session.commit()
			flash('Трасса удалена')
			return redirect(url_for('competition.routes'))
		except:
			Routes.query.filter_by(routeNuber=routeNuber).delete()
			flash('Трасса удалена')
			return redirect(url_for('competition.routes'))
	else:
		try:
			Routes.query.filter_by(routeNuber=routeNuber).filter_by(competition=competition.competitionName).delete()
			RouteCounter.numberOfRoutes = RouteCounter.numberOfRoutes - 1
			db.session.add(RouteCounter)
			db.session.commit()
			flash('Трасса удалена')
			return redirect(url_for('competition.routes'))
		except:
			Routes.query.filter_by(routeNuber=routeNuber).filter_by(competition=competition.competitionName).delete()
			flash('Трасса удалена')
			return redirect(url_for('competition.routes'))

@competition.route('/routes/info/<int:routeNuber>')
def route_info(routeNuber):
	competition = Competition.query.first()
	route = Routes.query.filter_by(routeNuber=routeNuber).filter_by(competition=competition.competitionName).first()
	return jsonify(route.to_json())

@competition.route('/routes/submit', methods=['POST'])
@login_required
def route_submit():
	competition = Competition.query.first()
	openSet = int(competition.routesStatus)
	userSet = int(current_user.waitingListYes) 
	if  2**int(userSet-1)&openSet !=0 and openSet != 0:
		if request.method == 'POST':
			routeNuberStr = request.form['routeNuber']
			teamRouteTimeSec = 'routeTimeSec'+routeNuberStr

			routeNuber = int(request.form['routeNuber'])
			routeMin = int(request.form['route_time_min'])
			routeSec = int(request.form['route_time_sec'])
			totalTimeSec = routeMin*60 + routeSec
			route = Routes.query.filter_by(routeNuber=routeNuber).filter_by(competition=competition.competitionName).first()

			if totalTimeSec>route.controlTimeSec*60:
				flash('Введеное время больше контрольного, трасса не засчитывается!')
				return redirect(url_for('competition.routes'))

			if getattr(current_user, teamRouteTimeSec,'x') == 0 and totalTimeSec > 0:
				route.teamsPassTrough = route.teamsPassTrough+1
			else:
				if getattr(current_user, teamRouteTimeSec,'x') != 0 and totalTimeSec == 0:
					route.teamsPassTrough = route.teamsPassTrough-1
				else: 
					route.teamsPassTrough = route.teamsPassTrough	

			setattr(current_user, teamRouteTimeSec, int(totalTimeSec))
			
			current_user.routeScoreTotal = 0
			current_user.routeTimeSecTotal = 0

			for i in range(1,36):
				timex = 'routeTimeSec' + str(i)
				current_user.routeTimeSecTotal= int(current_user.routeTimeSecTotal) + int(getattr(current_user, timex,0))+int(current_user.routeTimeSecFinal)

			
			db.session.add(current_user)
			db.session.add(route)
			mainTable.update_scores()
			db.session.commit()
			flash('Результат трассы №%s добавлен!' % (request.form['routeNuber']))
			return redirect(url_for('competition.routes'))
	flash('Ошибка, ваш сет закрыт или вы не авторизованы')
	return redirect(url_for('competition.routes'))
	