from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField, ValidationError, TextAreaField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from Stepanych.models.users import mainTable, Roles
from Stepanych.models.competition import Competition
from Stepanych.models.post import Post
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
	header = StringField('Заголовок новости', 
		validators = [Required("Введите заголовок поста")], 
		render_kw={"placeholder": "Заголовок для новости"})
	body = TextAreaField("Какие новости сегодня?", 
		validators = [Required("Вы забыли написать новость!")], 
		render_kw={"placeholder": "Текст новости, например: В горах отличная погода!","data-autosave":"editor-content"})
	submit1 = SubmitField("Запостить")

class CommentForm(FlaskForm):
	body = TextAreaField('Заголовок новости', 
		validators = [Required("Введите комментарий")], 
		render_kw={"placeholder": "Оставьте комментарий"})
	submit1 = SubmitField("Отправить")