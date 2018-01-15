from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, validators, SelectField, ValidationError, IntegerField, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from Stepanych.models.users import mainTable, Roles
from Stepanych.models.competition import Competition
from Stepanych.models.routes import setDescriptions
from Stepanych import db, images
from wtforms_sqlalchemy.fields import QuerySelectField


class RoutesForm(FlaskForm):
	scores = [('0', "очки за трассу"),('10','10'),('20','20'),('30','30'),('40','40'),('50','50'),('60','60'),('70','70'),('80','80'),('90','90'),('100','100')]
	time = [('0', "контрольное время"),('3','3'),('5','5'),('7','7'),('10','10'),('12','12'),('15','15'),('20','20')]

	routeNuber = IntegerField('Номер трассы', 
		validators =[
		Required("Введите номер трассы"), 
		#Length(1,2), 
		#Regexp('^[0-9]*$',0,'Допускаются только цыфры')
		],
		render_kw={"placeholder": "номер трассы", "maxlength":"2", "min":1 , "style":"width:200px"})	

	routeName = StringField('Название трассы', 
			#validators = [
			#Length(1,128),
			#Regexp('^[A-Za-zА-Яа-яёЁ0-9][A-Za-zА-Яа-яёЁ0-9_. ]*$',0,'Допускаются только буквы, цыфры и нижнее подчеркивание и пробелы')],
			render_kw={"placeholder": "название трассы", "style":"width:200px"})
	
	routeScore = SelectField(default=('0', "баллы за трассу"), choices = scores, validators = [Required("установите очки за трассу")], 
		render_kw={"style":"width:200px"})

	routeTime = SelectField(default=('0', "контрольное время"), choices = time, validators = [Required("установите контрольное вермя")],
		render_kw={"style":"width:200px"})

	img = FileField('Схема', validators=[FileAllowed(images, 'Только картинки')],
		render_kw={"style":"width:200px", "size":50})

	submit = SubmitField('Создать трассу', id="pic-upload")