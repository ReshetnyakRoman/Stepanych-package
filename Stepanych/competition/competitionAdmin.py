from flask import flash, redirect, render_template, request, url_for, session, abort  
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from Stepanych import db
from . import competition
from Stepanych.models.users import mainTable, Permission
from Stepanych.models.routes import setDescriptions, Routes
from Stepanych.models.competition import Competition, CompetitionArchive
from Stepanych.decorators import admin_required, permission_required
from flask_login import login_user, logout_user, login_required, current_user
from flask import jsonify
from Stepanych.auth.form import RegistrationForm

@competition.route('/admin')
@login_required
@permission_required(Permission.ADMINVIEW)
def admin():
	registrationForm = RegistrationForm()
	teamList = mainTable.query.all()
	competitionArchive = CompetitionArchive.query.order_by(CompetitionArchive.competitionName.desc()).all()
	competition = Competition.query.first()
	sets = setDescriptions.query.all()

	return render_template('competition/competitionAdmin.html',
	 displayLoginForm=request.args.get('displayLoginForm'),
	 competitionArchive=competitionArchive,
	 competitionStatus=competition.competitionStatus,
	 registrationStatus=competition.registrationStatus,
	 sets=sets, setStatus=int(competition.routesStatus))

@competition.route('/admin/delete-archive', methods=['POST'])
@admin_required
def delete_archive():
	if request.method == 'POST':
		competitionName = request.form['competitionName']
		CompetitionArchive.query.filter_by(competitionName=competitionName).delete()
		db.session.commit()
		flash('Архив соревнований "%s" удален' % (competitionName))
		return redirect(url_for('competition.admin'))
	flash('Что-то пошло не так...')	
	return redirect(url_for('competition.admin'))


@competition.route('/admin/open-competition', methods=['POST'])
@admin_required
def open_competition():
	if request.method == 'POST':
		competitionName = request.form['competitionName']
		numberOfSets = int(request.form['numberOfSets'])+1
		newDescriptions = [
			request.form['set1'],
			request.form['set2'],
			request.form['set3'],
			request.form['set4'],
			request.form['set5'],
			request.form['set6'],
			request.form['set7'],
			request.form['set8'],
			request.form['set9'],
			request.form['set10']]

		competition = Competition.query.first()
		competition.competitionName = competitionName
		competition.numberOfSets = numberOfSets
		competition.competitionStatus = 'open'
		competition.participantsListStatus = 'closed'
		competition.finalResultsStatus = 'closed'
		competition.routesStatus = 0
		competition.numberOfRoutes = 0
		competition.highlightFinals = 'yes'
		competition.resultsHeader = ''
		competition.resultsBody = ''
		competition.registrationStatus = 'open'

		#Routes.query.delete()
		setDescriptions.query.filter(setDescriptions.setNuber != 0).delete()
		
		db.session.add(competition)
		
		x=1
		while x <= numberOfSets:
			description = setDescriptions(setNuber=x, description=newDescriptions[x-1])
			db.session.add(description)
			x=x+1

		db.session.commit()

		flash('Соревнования октрыты, добавлено %s сета' % (numberOfSets))
		return redirect(url_for('competition.admin'))

	flash('Что-то пошло не так...')	
	return redirect(url_for('competition.admin'))

@competition.route('/admin/close-competition', methods=['POST'])
@admin_required
def close_competition():
	if request.method == 'POST':

		competition = Competition.query.first()
		competition.competitionStatus = 'closed'
		competition.registrationStatus = 'closed'
		competition.routesStatus = 0

		if CompetitionArchive.query.filter_by(competitionName=competition.competitionName).first() is None:
			newArchive = CompetitionArchive(competitionName=competition.competitionName)
			db.session.add(newArchive)

		db.session.add(competition)
		db.session.commit()

		flash('Соревнования закрыты и добавлены в архив')
		return redirect(url_for('competition.admin'))

	flash('Что-то пошло не так... Не получилось закрыть соревнования :(')	
	return redirect(url_for('competition.admin'))


@competition.route('/admin/open-registration', methods=['POST'])
@admin_required
def open_registration():
	if request.method == 'POST':

		competition = Competition.query.first()
		competition.registrationStatus = 'open'

		db.session.add(competition)
		db.session.commit()

		flash('Регистрация открыта!')
		return redirect(url_for('competition.admin'))

	flash('Что-то пошло не так... Не получилось открыть регистрацию :(')	
	return redirect(url_for('competition.admin'))



@competition.route('/admin/close-registration', methods=['POST'])
@admin_required
def close_registration():
	if request.method == 'POST':

		competition = Competition.query.first()
		competition.registrationStatus = 'closed'

		db.session.add(competition)
		db.session.commit()

		flash('Регистрация закрыта!')
		return redirect(url_for('competition.admin'))

	flash('Что-то пошло не так... Не получилось закрыть регистрацию :(')	
	return redirect(url_for('competition.admin'))

@competition.route('/admin/open-set', methods=['POST'])
@admin_required
def open_set():
	if request.method == 'POST':

		competition = Competition.query.first()
		competition.routesStatus = int(competition.routesStatus) | 2**(int(request.form['setNuber'])-1)

		db.session.add(competition)
		db.session.commit()

		flash('Трассы %sго сета открыты!' %(request.form['setNuber']))
		return redirect(url_for('competition.admin'))

	flash('Что-то пошло не так... Не получилось отрыть трассы :(')	
	return redirect(url_for('competition.admin'))


@competition.route('/admin/close-set', methods=['POST'])
@admin_required
def close_set():
	if request.method == 'POST':

		competition = Competition.query.first()
		competition.routesStatus = int(competition.routesStatus) ^ 2**(int(request.form['setNuber'])-1)

		db.session.add(competition)
		db.session.commit()

		flash('Трассы %sго сета закрыты!' %(request.form['setNuber']))
		return redirect(url_for('competition.admin'))

	flash('Что-то пошло не так... Не получилось отрыть трассы :(')	
	return redirect(url_for('competition.admin'))


