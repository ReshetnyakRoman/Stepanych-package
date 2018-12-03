from flask import render_template, redirect, request, url_for, flash, session
from . import auth
from flask_login import login_user, logout_user, login_required, current_user
from Stepanych.models.users import mainTable, Members
from Stepanych.models.competition import Competition
from .form import LoginForm, RegistrationForm, pswEmailForm, passwordForm, newEmailForm
from Stepanych import db
from ..email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from Stepanych import csrf
    

@auth.before_app_request
def before_request():
	if request.args.get('next') is not None: #если реквест содержит аргумент next url то мы записываем его в сессию, что бы дальше на него редиректнуть
		session['nextURL'] = request.args.get('next')
		if request.args.get('currentURL') is not None:
			session['currentURL'] = request.args.get('currentURL')
		else:
			session['currentURL'] = '/'			
	else:
		if request.args.get('currentURL') is not None: #иначе мы записываем в сессию текущий урл что бы остаться на той же странице от  куда производился вход
			session['currentURL'] = request.args.get('currentURL')
		else:
			pass
	try: request.endpoint[5:12] == 'confirm' #проверяем есть ли в урле слово confirm, тогда мы записываем в сессию token-ссылку для процедуры подтверждения email и завершения регистрации
	except:
		pass
		#return redirect(url_for('main.index'))
	else:
		if request.endpoint[5:12] == None and request.endpoint[5:12] == 'confirm':
			token = request.path[14:]
			session['confirmURL'] = url_for('auth.confirm', token=token)
		else:
			session['confirmURL'] = ''
			pass

	if current_user.is_authenticated and current_user.confirmed == 'False' and request.endpoint[:5] != 'auth.':
		return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET','POST'])
def login(currentURL=''):
	#session['nextURL'] = request.args.get('next')
	loginForm = LoginForm()
	competition1 = Competition.query.first().competitionName
	confirmationURL = session['confirmURL']
	if loginForm.validate_on_submit():
		team = mainTable.query.filter_by(teamName=loginForm.teamName.data).filter_by(competition=competition1).first()
		if team is not None and team.verify_password(loginForm.password.data): #сравниваем введеный хэш введенного пароля с хэшем в БД
			login_user(team, loginForm.remember_me.data) #создаем сессию текущего пользователя к которой можно обращатся через current_user
			session['teamName'] = loginForm.teamName.data #прописываем в сессию имя команды
			
			if mainTable.query.filter_by(teamName=loginForm.teamName.data).filter_by(competition=competition1).first() is None: #проверяем что вошедший НЕ зарегестрирован в текущих сорвенованиях, если это так то проверяем его роль ВНЕ этих соревнований
				session['role'] = mainTable.query.filter_by(teamName=loginForm.teamName.data).first().role #записываем его роль в сессию (скорее всего admin or guest)
				if confirmationURL != '': #проверяем что пользователь не переходит по ссылке завершающей регистрацию.
					#flash('1')
					return redirect(confirmationURL) #перенаправляем по ссылке для завершения регистрации   
				else: 
					#flash('2')
					try:
						return redirect(session['nextURL'])#перенаправляем по запрошенному урлу(?next=..) если такой был либо кабинет.
					except:
						return redirect(session['currentURL'] or url_for('main.index'))
			else: #если вошедший зарегестрирован в рамках этих соревнований
				session['role'] = mainTable.query.filter_by(teamName=loginForm.teamName.data).filter_by(competition=competition1).first().role #записываем в сессию его роль (скорее всего user)
				if confirmationURL != '': #проверяем что пользователь не переходит по ссылке завершающей регистрацию.
					#flash('3')
					return redirect(confirmationURL)  #перенаправляем по ссылке для завершения регистрации 
				else: 
					#flash('4')
					try:
						return redirect(session['nextURL'])#перенаправляем по запрошенному урлу(?next=..) если такой был либо кабинет.
					except:
						return redirect(session['currentURL'] or url_for('main.index'))
		flash('Неправильное название команды или пароль')	# в случае ошибки ввода выводим надпись и перенаправляем на главную спросьбой поторить
	
	return redirect(session['currentURL']+'?displayLoginForm=block' or url_for('main.index', displayLoginForm='block', loginForm=loginForm))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	session['email'] =''
	session['teamName'] = ''
	session['role'] = ''
	session['nextURL'] = ''
	flash('Вы вышли из профиля команды')
	return redirect(url_for('main.index'))


@auth.route('/teamoffice')
@login_required
def teamoffice():	
	competition1 = Competition.query.first().competitionName
	if session['role'] == 'admin' or session['role'] == 'guest':
		competition1 = mainTable.query.filter_by(teamName=session['teamName']).first().competition
		teamName = mainTable.query.filter_by(teamName=session['teamName']).first().teamName
		teamChange = mainTable.query.filter_by(teamName=session['teamName']).first().teamChange
		email = mainTable.query.filter_by(teamName=session['teamName']).first().email
		
		name1 = mainTable.query.filter_by(teamName=session['teamName']).first().name1
		sname1 = mainTable.query.filter_by(teamName=session['teamName']).first().sname1
		male1 = mainTable.query.filter_by(teamName=session['teamName']).first().male1
		year1 = mainTable.query.filter_by(teamName=session['teamName']).first().year1
		club1 = mainTable.query.filter_by(teamName=session['teamName']).first().club1
		alpSkill1 = mainTable.query.filter_by(teamName=session['teamName']).first().alpSkill1
		climbSkill1 = mainTable.query.filter_by(teamName=session['teamName']).first().climbSkill1

		name2 = mainTable.query.filter_by(teamName=session['teamName']).first().name2
		sname2 = mainTable.query.filter_by(teamName=session['teamName']).first().sname2
		male2 = mainTable.query.filter_by(teamName=session['teamName']).first().male2
		year2 = mainTable.query.filter_by(teamName=session['teamName']).first().year2
		club2 = mainTable.query.filter_by(teamName=session['teamName']).first().club2
		alpSkill2 = mainTable.query.filter_by(teamName=session['teamName']).first().alpSkill2
		climbSkill2 = mainTable.query.filter_by(teamName=session['teamName']).first().climbSkill2
		return render_template('auth/teamoffice.html',  

		competition=competition1, 
		teamName=teamName, 
		teamChange= teamChange,
		email=email,

		name1=name1,
		sname1 = sname1,
		male1 = male1,
		year1 = year1,
		club1 = club1,
		alpSkill1 = alpSkill1,
		climbSkill1 = climbSkill1,

		name2=name2,
		sname2 = sname2,
		male2=male2,
		year2 = year2,
		club2 = club2,
		alpSkill2 = alpSkill2,
		climbSkill2 = climbSkill2
		)
	else:
		if mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first() == None:
			flash('Такая команда не зарегистрирована в этих соревнованиях')	
			logout_user()
			session['email'] =''
			session['teamName'] = ''
			session['role'] = ''
			return redirect(url_for('auth.login'))
		else:	
			teamName = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().teamName
			email = mainTable.query.filter_by(teamName=session['teamName']).first().email
			teamChange = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().teamChange

			name1 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().name1
			sname1 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().sname1
			male1 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().male1
			year1 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().year1
			club1 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().club1
			alpSkill1 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().alpSkill1
			climbSkill1 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().climbSkill1

			name2 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().name2
			sname2 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().sname2
			male2 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().male2
			year2 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().year2
			club2 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().club2
			alpSkill2 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().alpSkill2
			climbSkill2 = mainTable.query.filter_by(teamName=session['teamName']).filter_by(competition=competition1).first().climbSkill2
			return render_template('auth/teamoffice.html', 
			competition = competition1, 
			teamName = teamName, 
			teamChange = teamChange,
			email=email,

			name1=name1,
			sname1 = sname1,
			male1 = male1,
			year1 = year1,
			club1 = club1,
			alpSkill1 = alpSkill1,
			climbSkill1 = climbSkill1,

			name2=name2,
			sname2 = sname2,
			male2 = male2,
			year2 = year2,
			club2 = club2,
			alpSkill2 = alpSkill2,
			climbSkill2 = climbSkill2
			)

@auth.route('/registration', methods=['GET', 'POST'])
def registration():
	registrationForm = RegistrationForm()	
	competition1 = Competition.query.first().competitionName
	if registrationForm.validate_on_submit():
		team = mainTable(
			keyTeamCompetition = registrationForm.teamName.data+competition1,
			competition = competition1,
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
			teamChange = 'no',
			teamStatus = 'ok',
			waitingListYes = registrationForm.setNumber.data,
			keyName1Sname1Year1 = registrationForm.name1.data+registrationForm.sname1.data+registrationForm.year1.data,
			keyName2Sname2Year2 = registrationForm.name2.data+registrationForm.sname2.data+registrationForm.year2.data
		 )
		if current_user.role != 'admin':
			team.role = 'user'

		db.session.add(team)
		
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
		
		db.session.commit()
		token = team.generate_confirmation_token()
		send_email(team.email, ': Подтвердите ваш аккаунт для Степаныча', 'auth/email/confirm', team=team, token=token)
		flash('Для завершения регистрации пройдите по ссылке, отправленной вам на Email ')
		return redirect(url_for('auth.registrationNextStep'))
	flash('Вы заполнили не все данные или ввели недопустимый символ! Разрешены только буквы, цифры и пробелы')
	return redirect(url_for('main.index', displayRegistrationForm='block'))


@auth.route('/nextstep')
def registrationNextStep():
	return render_template('auth/nextstep.html')

#-------------блоки подтверждения регистрации и запрета передвижения в случае не подтвержденного акаунта------------------
@auth.route('/confirm/<token>')
#@login_required
def confirm(token):
	s = Serializer(current_app.config['SECRET_KEY']) #создаем объект дешифратора с ключем для дешифровки из КОНФИГА приложения (config.py)
	data = s.loads(token).get('confirm') # Дешифруе запись и записываем ее в data
	try:
		mainTable.query.filter_by(keyTeamCompetition = data).first().confirmed #проверяем что зашифрованной команде соответствует запись в базе данных
	except:
		flash('Неправильная ссылка для подтверждения или закончился срок ее действия') #если не не существует отправляем лесом
		return render_template('auth/nextstep.html')
	else: #если существет создаем объект teamRegistration для этой команды.
		teamRegistration = mainTable.query.filter_by(keyTeamCompetition = data).first()
		if teamRegistration.confirmed == 'True':  #если по ссылке уже переходили и команда подтверждена, то переходим в кабинет.
			return redirect(url_for('auth.teamoffice'))
		else:  #если по ссылке не преходили и регистрация еще не подтверждена, то подтвердаем ее соответсвующей записью в БД.
			teamRegistration.confirmed = 'True'
			db.session.add(teamRegistration)
			db.session.commit()
			flash('Поздравляем, регистрация успешно завершена!')
			flash('Теперь вы можете продолжить работу, например:')
			flash('- заменить одного из участников команды в Личном кабинете (при необходимости)')
			flash('- регистрировать результаты вашей команды во время соревнований (меню: соревнования -> трассы)')
			flash('- изменить email вашей команды')
			return redirect(url_for('auth.registrationNextStep'))		

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, ': Подтвердите ваш аккаунт для Степаныча', 'auth/email/confirm', team=current_user, token=token)
	flash('Вам отправлено новое письмо с ссылкой для завершения регистрации')
	return redirect(url_for('auth.registrationNextStep'))


@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed == 'True':
		return redirect('main.index')
	return render_template('auth/unconfirmed.html')		

#---------------------два блока для восстановления пароля-------------------------
#1й блок отправляет письмо с шифрованной ссылкой на поле для задание нового пароля
@auth.route('/pswresend',  methods=['GET', 'POST'])
def password_resend():
	form = pswEmailForm()
	competition1 = Competition.query.first().competitionName
	if form.validate_on_submit():
		if mainTable.query.filter_by(teamName= form.teamName.data).filter_by(email=form.email.data).first() is not None:
			if mainTable.query.filter_by(teamName= form.teamName.data).filter_by(email=form.email.data).first().role == 'admin':
				team = mainTable.query.filter_by(teamName= form.teamName.data).filter_by(email=form.email.data).first()
			else:
				team = mainTable.query.filter_by(teamName = form.teamName.data).filter_by(competition=competition1).filter_by(email=form.email.data).first()
			if team is not None:
				token = team.generate_confirmation_token()
				send_email(form.email.data, ': Восстановление пароля для степаныча', 'auth/email/pswresendemail', team=team.teamName, token=token)
				flash('Вам отправлено новое письмо с ссылкой для восстановления пароля')
				return redirect(url_for('auth.registrationNextStep'))
			else:
				flash('Такая команда или Email не зарегистрированы в текущих соревнованиях')
				return render_template('/auth/pswresend.html', emailForm=form)
		else:
			flash('Такая команда не зарегистрирована')
	return render_template('/auth/pswresend.html', emailForm=form)

#2й блок берет новый пароль, записывает его хэш в БД, и отправляет письмо пользователю с новым паролем!
@auth.route('/newpassword/<token>', methods=['GET', 'POST'])	
def newpassword(token):
	s = Serializer(current_app.config['SECRET_KEY']) #создаем объект дешифратора с ключем для дешифровки из КОНФИГА приложения (config.py)
	data = s.loads(token).get('confirm') # Дешифруем токен из ссылки пользователя и записываем ее в data
	form = passwordForm()
	team = mainTable.query.filter_by(keyTeamCompetition = data).first()
	if team is not None: #проверяем что зашифрованной команде соответствует запись в базе данных
		if form.validate_on_submit():
			team.password = form.password.data
			send_email(team.email, ': Ваш новый пароль на сайте Степаныча', 'auth/email/newpassword', team=team.teamName, password = form.password.data)
			db.session.add(team)
			db.session.commit()
			flash('Ваш пароль изменен')
			flash('Письмо с новым паролем отправлено вам на почту')
			return redirect(url_for('auth.registrationNextStep'))
		else: 
			return render_template('/auth/newpassword.html', passwordForm = form, token1=token)	
	else: #если существет создаем объект teamRegistration для этой команды.
		flash('Неправильная ссылка для подтверждения или закончился срок ее действия') #если не не существует отправляем лесом
		flash(team)
		return redirect(url_for('auth.password_resend'))

#---------------------два блока для восстановления пароля-------------------------
#1й блок отправляет письмо с шифрованной ссылкой на поле для задание нового пароля

@auth.route('/newemailform', methods=['GET', 'POST'])
@login_required
def new_email():
	form = newEmailForm()
	if form.validate_on_submit():
		current_user.pendingEmail = form.email.data
		token = current_user.generate_confirmation_token()
		send_email(form.email.data, ': Подтвердите ваш новый email', 'auth/email/newemail', team = current_user.teamName, token=token)
		flash('На новый email вам отправлено письмо с секретной ссылкой, перейдите по ней для завершения изменений')
		return redirect(url_for('auth.registrationNextStep'))
	else:
		return render_template('/auth/newemail.html', newEmailForm=form)

@auth.route('/newemail/<token>')
@login_required
def new_email_change(token):
	s = Serializer(current_app.config['SECRET_KEY']) #создаем объект дешифратора с ключем для дешифровки из КОНФИГА приложения (config.py)
	data = s.loads(token).get('confirm') # Дешифруем токен из ссылки пользователя и записываем ее в data	
	if current_user.keyTeamCompetition == data:
		current_user.email = current_user.pendingEmail
		db.session.add(current_user)
		db.session.commit()
		flash('Поздравляем, ваш Email изменен!')
		return redirect(url_for('auth.registrationNextStep'))
	else:
		flash('Неправильная ссылка или истек срок ее действия')
		return redirect(url_for('auth.registrationNextStep'))

@auth.route('/memberchange', methods=['GET','POST'])
#@csrf.exempt
@login_required
def team_member_change():
	if request.method == 'POST':
		current_user.name1 = request.form['name1']
		current_user.sname1 = request.form['sname1']
		current_user.year1 = request.form['year1']
		current_user.club1 = request.form['club1']
		current_user.male1 = request.form['male1']
		current_user.alpSkill1 = request.form['alpSkill1']
		current_user.climbSkill1 = request.form['climbSkill1']

		current_user.name2 = request.form['name2']
		current_user.sname2 = request.form['sname2']
		current_user.year2 = request.form['year2']
		current_user.male2 = request.form['male2']
		current_user.club2 = request.form['club2']
		current_user.alpSkill2 = request.form['alpSkill2']
		current_user.climbSkill2 = request.form['climbSkill2']

		current_user.teamChange = 'Yes'
		
		db.session.add(current_user)
		
		member1 = Members.query.filter_by(name=request.form['name1']).filter_by(sname=request.form['sname1']).filter_by(year=request.form['year1']).first()
		if member1 is not None:
			member1.club = request.form['club1']
			member1.alpSkill = request.form['alpSkill1']
			member1.climbSkill = request.form['climbSkill1']
			member1.male = request.form['male1']	
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
				male = request.form['male1'])
			db.session.add(newMemeber1)
			

		member2 = Members.query.filter_by(name=request.form['name2']).filter_by(sname=request.form['sname2']).filter_by(year=request.form['year2']).first()
		if member2 is not None:
			member2.club = request.form['club2']
			member2.alpSkill = request.form['alpSkill2']
			member2.climbSkill = request.form['climbSkill2']
			member2.male = request.form['male2']

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
				male = request.form['male2'])
			db.session.add(newMemeber2)		
		
		db.session.commit()
		flash ('Участник изменен')
		return redirect(url_for('auth.teamoffice'))
	return redirect(url_for('auth.teamoffice'))



