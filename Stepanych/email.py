from threading import Thread
from flask_mail import Mail, Message
#from flask import current_app as app
from manage import app
from flask import flash, redirect, render_template, request, url_for, session, abort  
from . import mail

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)


def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['MY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MY_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)
	thr = Thread(target = send_async_email, args=[app, msg])
	thr.start()
	return thr