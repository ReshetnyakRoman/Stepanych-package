from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField, SelectField, HiddenField, ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from Stepanych.models.users import mainTable, Roles
from Stepanych.models.competition import Competition
from Stepanych.models.routes import setDescriptions
from Stepanych import db
from wtforms_sqlalchemy.fields import QuerySelectField

def set_query(): #factory function для подтягивания описания сетов в форму регистрации
	return setDescriptions.query.all()

class LoginForm(FlaskForm):
	teamName = StringField('Название команды', validators = [Required("введите название команды"), Length(1,128)], render_kw={"placeholder": "Пьяные инженеришки"})
	password = PasswordField('password', validators = [Required("введите пароль")], render_kw={"placeholder": "хитрый пароль"})		
	remember_me = BooleanField('Запомнить меня', render_kw={"checked": "checked"})
	submit1 = SubmitField('Войти')

class pswEmailForm(FlaskForm):
	teamName = StringField('Название команды', validators = [Required("введите название команды"), Length(1,128)], render_kw={"placeholder": "Пьяные инженеришки"})
	email = StringField('Ваш Email', validators = [Required("введите email команды"), Email("неправильное написание"), Length(1,128)], render_kw={"placeholder": "alpinist@krutoy.ya"})
	submit = SubmitField('Отправить')

class newEmailForm(FlaskForm):
	email = StringField('Ваш Email', validators = [Required("введите новый email"), Email("неправильное написание"), Length(1,128)], render_kw={"placeholder": "alpinist@krutoy.ya"})
	submit = SubmitField('Сохранить')

class passwordForm(FlaskForm):
	password = PasswordField('Пароль', validators = [Required("введите новый пароль"), Length(1,128)], render_kw={"placeholder": "хитрый пароль"})
	submit = SubmitField('Сохранить пароль')		
						
class RegistrationForm(FlaskForm):
	"""teams RegistrationForm"""
	alpSkill = [('', "разряд по альпизнизму"),('б/р','б/р'),('3й','3й'),('2й','2й'),('1й','1й'),('кмс','кмс'),('мс','мс'),('мсмк','мсмк')]
	climbSkill = [('', "разряд по скалолазанию"),('б/р','б/р'),('3й','3й'),('2й','2й'),('1й','1й'),('кмс','кмс'),('мс','мс'),('мсмк','мсмк')]

	competition = StringField('Название соревнований', validators = [
		Required("введите название команды"),
		Length(1,128),
		Regexp('^[A-Za-zА-Яа-яёЁ0-9][A-Za-zА-Яа-яёЁ0-9_ ]*$',0,'Допускаются только буквы, цыфры и нижнее подчеркивание и пробелы')],
		render_kw={"placeholder": "название соревнований: admin или guest", "id":"competition"})
	
	teamName = StringField('Название команды', validators = [
		Required("введите название команды"),
		Length(1,128),
		Regexp('^[A-Za-zА-Яа-яёЁЙ0-9()& +-][A-Za-zА-Яа-яёЁЙ0-9_ ()&+-]*$',0,'Допускаются только буквы, цыфры и нижнее подчеркивание и пробелы')],
		render_kw={"placeholder": "название команды"})
	
	email = StringField('Email', validators = [Required("введите email"), Email("неправильное написание"), Length(1,64)], render_kw = {"placeholder": "email*"})
	password = PasswordField('Пароль', validators = [Required("введите пароль")], render_kw = {"placeholder": "Хитрый пароль"})

	setNumber = QuerySelectField(query_factory=set_query, allow_blank=False, get_label='description')
	
	role = SelectField(default=('user', 'user'),
		#choices = [
		#('user','user'),
		#('guest','guest'),
		#('admin','admin')],
		validators = [Required("выбериъ роль")], id='role')

	name1 = StringField('Имя 1го участника', 
		validators =[
		Required("Введите имя 1го участника"), 
		Length(1,64), 
		Regexp('^[A-Za-zА-Яа-я0-9ёЁ][A-Za-zА-ЯЁёа-я0-9_ ]*$',0,'Допускаются только буквы, цыфры и нижнее подчеркивание и пробелы')],
		render_kw={"placeholder": "Имя участника"})

	sname1 = StringField('Фамилия 1го участника', 
		validators =[
		Required("Введите фамилию 1го участника"), 
		Length(1,64), 
		Regexp('^[A-Za-zА-ЯЁёа-я0-9][A-Za-zА-ЯЁёа-я0-9_ ]*$',0,'Допускаются только буквы, цыфры и нижнее подчеркивание и пробелы')],
		render_kw={"placeholder": "Файмилия участника"})
	
	club1 = StringField('Клуб', 
		validators =[
		Required("Введите клуб 1го участника"), 
		Length(1,128)],
		render_kw={"placeholder": "Клуб"})
	
	year1 = StringField('Год рождения', 
		validators =[
		Required("Введите год рождения 1го участника"), 
		Length(1,4), 
		Regexp('^[0-9]*$',0,'Допускаются цыфры')],
		render_kw={"placeholder": "год рождения", "maxlength":"4"})

	alpSkill1 = SelectField(default=('', "разряд по альпизнизму"), choices = alpSkill,
		validators = [Required("выберите разряд по альпизнизму")], id='alpSkill1')

	climbSkill1 = SelectField(default=('', "разряд по скалолазанию"), choices = climbSkill, validators = [Required("выберите разряд по скалолазанию")], id='climbSkill1')

	male1 = SelectField(default=('', "пол"), choices = [('','пол'),('М','М'),('Ж','Ж')], validators = [Required("укажите пол участника")], id='male1')			

	name2 = StringField('Имя 2го участника', 
		validators =[
		Required("Введите имя 2го участника"), 
		Length(1,64), 
		Regexp('^[A-Za-zА-ЯЁёа-я0-9][A-Za-zА-ЯЁёа-я0-9_ ]*$',0,'Допускаются только буквы, цыфры и нижнее подчеркивание и пробелы')],
		render_kw={"placeholder": "Имя участника"})

	sname2 = StringField('Фамилия 2го участника', 
		validators =[
		Required("Введите фамилию 2го участника"), 
		Length(1,64), 
		Regexp('^[A-Za-zА-ЯЁёа-я0-9][A-Za-zА-ЯЁёа-я0-9_ ]*$',0,'Допускаются только буквы, цыфры и нижнее подчеркивание и пробелы')],
		render_kw={"placeholder": "Файмилия участника"})

	club2 = StringField('Клуб', 
		validators =[
		Required("Введите клуб 1го участника"), 
		Length(1,80)],
		render_kw={"placeholder": "Клуб"})
	
	year2 = StringField('Год рождения', 
		validators =[
		Required("Введите год рождения 2го участника"), 
		Length(1,4), 
		Regexp('^[0-9]*$',0,'Допускаются цыфры')],
		render_kw={"placeholder": "год рождения", "maxlength":"4"})

	alpSkill2 = SelectField(default=('', "разряд по альпизнизму"), choices = alpSkill,
		validators = [Required("выберите разряд по альпизнизму")], id='alpSkill2')

	climbSkill2 = SelectField(default=('', "разряд по скалолазанию"), choices = climbSkill,
		validators = [Required("выберите разряд по скалолазанию")], id='climbSkill2')

	male2 = SelectField(default=('', "пол"), choices = [('','пол'),('М','М'),('Ж','Ж')],
		validators = [Required("укажите пол участника")], id='male2')

	submit1 = SubmitField('Зарегестрировать')

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		roles = Roles.query.order_by(Roles.permissions).all()
		self.role.choices = [(i.role, i.role) for i in roles]
	
	def validate_teamName(self, field):
		competition1 = Competition.query.first()
		if mainTable.query.filter_by(keyTeamCompetition=str(field.data)+str(competition1.competitionName)).first():
			raise ValidationError('Команда с таким названием уже зарегестрирована в этих соревнованиях')
		