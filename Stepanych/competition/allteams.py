from flask import flash, redirect, render_template, request, url_for, session, abort  
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from Stepanych import db
from . import competition
from Stepanych.models.users import mainTable, Permission, Members, Volunteers
from Stepanych.models.competition import Competition
from Stepanych.decorators import admin_required, permission_required
from flask_login import login_user, logout_user, login_required, current_user
from flask import jsonify
from Stepanych.auth.form import RegistrationForm

#================Teams================

@competition.route('/allteams')
@login_required
@permission_required(Permission.ADMINVIEW)
def allteams():
	registrationForm = RegistrationForm()
	teamList = mainTable.query.all()
	jsonTeamList = { 'team' : [ team.to_json() for team in teamList] }
	return render_template('competition/allteams.html', jsonTeamList=jsonTeamList, teamList=teamList,
		displayLoginForm=request.args.get('displayLoginForm'), registrationForm =  registrationForm
		)

@competition.route('/allteams/delete/<TeamCompetition>')
@login_required
@admin_required
def delete_team(TeamCompetition):
	mainTable.query.filter_by(keyTeamCompetition=TeamCompetition).delete()
	db.session.commit()
	return redirect(url_for('competition.allteams'))

@competition.route('/allteams/change', methods=['POST'])
@login_required
@admin_required
def change():
	if request.method == 'POST':
		TeamCompetition = request.form['keyTeamCompetition']
		team = mainTable.query.filter_by(keyTeamCompetition=TeamCompetition).first()
		if team is not None:
			team.name1 = request.form['name1']
			team.sname1 = request.form['sname1']
			team.year1 = request.form['year1']
			team.club1 = request.form['club1']
			team.phone1 = request.form['phone1']
			team.male1 = request.form['male1']
			team.alpSkill1 = request.form['alpSkill1']
			team.climbSkill1 = request.form['climbSkill1']

			team.name2 = request.form['name2']
			team.sname2 = request.form['sname2']
			team.year2 = request.form['year2']
			team.club2 = request.form['club2']
			team.phone2 = request.form['phone2']
			team.male2 = request.form['male2']
			team.alpSkill2 = request.form['alpSkill2']
			team.climbSkill2 = request.form['climbSkill2']

			db.session.add(team)

		member1 = Members.query.filter_by(name=request.form['name1']).filter_by(sname=request.form['sname1']).filter_by(year=request.form['year1']).first()
		if member1 is not None:
			member1.club = request.form['club1']
			member1.male = request.form['male1']
			member1.alpSkill = request.form['alpSkill1']
			member1.climbSkill = request.form['climbSkill1']
			member1.phone = request.form['phone1']
			db.session.add(member1)

		else:
			newMemeber1 = Members(
				name = request.form['name1'],
				sname = request.form['sname1'],
				year = request.form['year1'],
				keyNameSnameYear = request.form['name1']+request.form['sname1']+request.form['year1'],
				club = request.form['club1'],
				alpSkill = request.form['alpSkill1'],
				climbSkill = request.form['climbSkill1'],
				male = request.form['male1'],
				phone = request.form['phone1'])
			db.session.add(newMemeber1)
			

		member2 = Members.query.filter_by(name=request.form['name2']).filter_by(sname=request.form['sname2']).filter_by(year=request.form['year2']).first()
		if member2 is not None:
			member2.club = request.form['club2']
			member2.male = request.form['male2']
			member2.alpSkill = request.form['alpSkill2']
			member2.climbSkill = request.form['climbSkill2']
			member2.phone = request.form['phone2']
			db.session.add(member2)
			
		else:
			newMemeber2 = Members(
				name = request.form['name2'],
				sname = request.form['sname2'],
				year = request.form['year2'],
				keyNameSnameYear = request.form['name2']+request.form['sname2']+request.form['year2'],
				club = request.form['club2'],
				alpSkill = request.form['alpSkill2'],
				climbSkill = request.form['climbSkill2'],
				male = request.form['male2'],
				phone = request.form['phone2'])
			db.session.add(newMemeber2)
			
				
		db.session.commit()
		flash('Данные успешно сохранены')
		return redirect(url_for('competition.allteams'))
	flash('Данные НЕ сохранены')
	return redirect(url_for('competition.allteams'))	

@competition.route('/allteams/registration', methods=['GET', 'POST'])
@login_required
@admin_required
def registration():
	registrationForm = RegistrationForm()
	if registrationForm.validate_on_submit():
		if Members.query.filter_by(keyNameSnameYear=registrationForm.name1.data+registrationForm.sname1.data+registrationForm.year1.data).first() is None:
			memeber1 = Members(
				name = registrationForm.name1.data,
				sname = registrationForm.sname1.data,
				year = registrationForm.year1.data,
				keyNameSnameYear = registrationForm.name1.data+registrationForm.sname1.data+registrationForm.year1.data,
				club = registrationForm.club1.data,
				alpSkill = registrationForm.alpSkill1.data,
				climbSkill = registrationForm.climbSkill1.data,
				male = registrationForm.male1.data,
				tshirtSize = registrationForm.tshirtSize1.data,
				country = (registrationForm.country1.data).upper(),
				city = registrationForm.city1.data,
				phone = registrationForm.phone1.data
				)
			db.session.add(memeber1)
		else: 
			memeber1 = Members.query.filter_by(keyNameSnameYear=registrationForm.name1.data+registrationForm.sname1.data+registrationForm.year1.data).first()
			memeber1.club = registrationForm.club1.data  
			memeber1.alpSkill = registrationForm.alpSkill1.data
			memeber1.climbSkill = registrationForm.climbSkill1.data
			memeber1.tshirtSize = registrationForm.tshirtSize1.data
			memeber1.country = (registrationForm.country1.data).upper()
			memeber1.city = registrationForm.city1.data
			memeber1.phone = registrationForm.phone1.data
			db.session.add(memeber1)	

		if Members.query.filter_by(keyNameSnameYear=registrationForm.name2.data+registrationForm.sname2.data+registrationForm.year2.data).first() is None:
			memeber2 = Members(
				name = registrationForm.name2.data,
				sname = registrationForm.sname2.data,
				year = registrationForm.year2.data,
				keyNameSnameYear = registrationForm.name2.data+registrationForm.sname2.data+registrationForm.year2.data,
				club = registrationForm.club2.data,
				alpSkill = registrationForm.alpSkill2.data,
				climbSkill = registrationForm.climbSkill2.data,
				male = registrationForm.male2.data,
				tshirtSize = registrationForm.tshirtSize2.data,
				country = (registrationForm.country2.data).upper(),
				city = registrationForm.city2.data,
				phone = registrationForm.phone2.data
				)
			db.session.add(memeber2)
		else: 
			memeber2 = Members.query.filter_by(keyNameSnameYear=registrationForm.name2.data+registrationForm.sname2.data+registrationForm.year2.data).first()
			memeber2.club = registrationForm.club2.data  
			memeber2.alpSkill = registrationForm.alpSkill2.data
			memeber2.climbSkill = registrationForm.climbSkill2.data
			memeber2.tshirtSize = registrationForm.tshirtSize2.data
			memeber2.country = (registrationForm.country2.data).upper()
			memeber2.city = registrationForm.city2.data
			memeber2.phone = registrationForm.phone2.data
			db.session.add(memeber2)

		if mainTable.query.filter_by(competition=registrationForm.competition.data).filter_by(teamName=registrationForm.teamName.data).first() is None:
			team = mainTable(
				keyTeamCompetition = registrationForm.teamName.data+registrationForm.competition.data,
				competition = registrationForm.competition.data,
				email = registrationForm.email.data,
				teamName = registrationForm.teamName.data,
				password = registrationForm.password.data,
				setNumber = registrationForm.setNumber.data,
				name1 = registrationForm.name1.data,
				sname1 = registrationForm.sname1.data,
				year1 = registrationForm.year1.data,
				male1 = registrationForm.male1.data,
				club1 = registrationForm.club1.data,
				alpSkill1 = registrationForm.alpSkill1.data,
				climbSkill1 = registrationForm.climbSkill1.data,
				tshirtSize1 = registrationForm.tshirtSize1.data,
				country1 = (registrationForm.country1.data).upper(),
				city1 = registrationForm.city1.data,
				phone1 = registrationForm.phone1.data,

				name2 = registrationForm.name2.data,
				sname2 = registrationForm.sname2.data,
				year2 = registrationForm.year2.data,
				male2 = registrationForm.male2.data,
				club2 = registrationForm.club2.data,
				alpSkill2 = registrationForm.alpSkill2.data,
				climbSkill2 = registrationForm.climbSkill2.data,
				tshirtSize2 = registrationForm.tshirtSize2.data,
				country2 = (registrationForm.country2.data).upper(),
				city2 = registrationForm.city2.data,
				phone2 = registrationForm.phone2.data,

				role = registrationForm.role.data,
				teamStatus = 'ok',
				teamChange = 'no',
				waitingListYes = registrationForm.setNumber.data,
				keyName1Sname1Year1 = registrationForm.name1.data+registrationForm.sname1.data+registrationForm.year1.data,
				keyName2Sname2Year2 = registrationForm.name2.data+registrationForm.sname2.data+registrationForm.year2.data,
				confirmed ='True'
			 )
			db.session.add(team)
			db.session.commit()
			flash('Команда "%s" добавлена' % (registrationForm.teamName.data))
			return redirect(url_for('competition.allteams'))
		else:
			db.session.commit()
			flash('Такая команда уже существует в этих соревнованиях')
			return redirect(url_for('competition.allteams', displayRegistrationForm='block'))
	flash('Вы заполнили не все поля или допустили ошибку')
	return redirect(url_for('competition.allteams', displayRegistrationForm='block'))

#================Memebers================

@competition.route('/allmembers')
def allmembers():
	memberList = Members.query.all()
	return render_template('competition/allmembers.html', memberList=memberList, displayLoginForm=request.args.get('displayLoginForm'))

@competition.route('/allmembers/delete', methods=['POST'])
@login_required
@admin_required
def delete_member():
	keyNameSnameYear = request.form['keyNameSnameYear']
	Members.query.filter_by(keyNameSnameYear=keyNameSnameYear).delete()
	db.session.commit()
	flash('Участник удален')
	return redirect(url_for('competition.allmembers'))

@competition.route('/profile')
def profile():
	name = request.args.get('name')
	sname = request.args.get('sname')
	year = request.args.get('year')
	member1 = mainTable.query.filter_by(name1=name).filter_by(sname1=sname).filter_by(year1=year).all()
	member2 = mainTable.query.filter_by(name2=name).filter_by(sname2=sname).filter_by(year2=year).all()
	member = Members.query.filter_by(name=name).filter_by(sname=sname).filter_by(year=year).first()
	return render_template('competition/profile.html', member=member, member1=member1, member2=member2, displayLoginForm=request.args.get('displayLoginForm'))

#================Volunteers================

@competition.route('/volunteers', methods=['GET','POST'])
def volunteers():
	competition= Competition.query.first()
	if request.method == 'POST':
		volunteer = Volunteers(
			competition =  competition.competitionName,
			name=request.form['name'],
			sname=request.form['sname'],
			tshirtSize=request.form['tshirtSize'],
			role=request.form['role'],
			phone=request.form['phone']
			)
		db.session.add(volunteer)
		db.session.commit()
		return redirect(url_for('competition.volunteers'))
	else:	
		status = competition.volunteersStatus
		volunteerList = Volunteers.query.filter_by(competition=competition.competitionName).order_by(Volunteers.role).all()
		return render_template('competition/volunteers.html', volunteerList=volunteerList, status=status, displayLoginForm=request.args.get('displayLoginForm'))

@competition.route('/volunteers/delete', methods=['POST'])
@login_required
@admin_required
def delete_volunteer():
	name = request.form['name']
	sname = request.form['sname']
	competition= Competition.query.first().competitionName
	Volunteers.query.filter_by(name=name).filter_by(sname=sname).filter_by(competition=competition).delete()
	db.session.commit()
	flash('Участник удален')
	return redirect(url_for('competition.volunteers'))

#================Tshirts================	
@competition.route('/tshirts')
def tshirts():
	competition = Competition.query.first().competitionName
	xsParticipants = mainTable.query.filter_by(competition=competition).filter_by(tshirtSize1='XS').count()+mainTable.query.filter_by(competition=competition).filter_by(tshirtSize2='XS').count()
	xsVolunteers = Volunteers.query.filter_by(competition=competition).filter_by(tshirtSize='XS').count()

	sParticipants = mainTable.query.filter_by(competition=competition).filter_by(tshirtSize1='S').count()+mainTable.query.filter_by(competition=competition).filter_by(tshirtSize2='S').count()
	sVolunteers = Volunteers.query.filter_by(competition=competition).filter_by(tshirtSize='S').count()

	mParticipants = mainTable.query.filter_by(competition=competition).filter_by(tshirtSize1='M').count()+mainTable.query.filter_by(competition=competition).filter_by(tshirtSize2='M').count()
	mVolunteers = Volunteers.query.filter_by(competition=competition).filter_by(tshirtSize='M').count()

	lParticipants = mainTable.query.filter_by(competition=competition).filter_by(tshirtSize1='L').count()+mainTable.query.filter_by(competition=competition).filter_by(tshirtSize2='L').count()
	lVolunteers = Volunteers.query.filter_by(competition=competition).filter_by(tshirtSize='L').count()

	xlParticipants = mainTable.query.filter_by(competition=competition).filter_by(tshirtSize1='XL').count()+mainTable.query.filter_by(competition=competition).filter_by(tshirtSize2='XL').count()
	xlVolunteers = Volunteers.query.filter_by(competition=competition).filter_by(tshirtSize='XL').count()
	return render_template('competition/tshirts.html', 
		competition=competition,
		xsParticipants=xsParticipants, xsVolunteers=xsVolunteers, 
		sParticipants=sParticipants, sVolunteers=sVolunteers,
		mParticipants=mParticipants, mVolunteers=mVolunteers,
		lParticipants=lParticipants, lVolunteers=lVolunteers,
		xlParticipants=xlParticipants, xlVolunteers=xlVolunteers,)