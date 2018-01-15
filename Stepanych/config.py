#Этот конфигурационный файл для сайта Stepanich.ru должен храниться на уровень ввыше каталога Stepanych в том же каталоче что и manage.py 
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	WTF_CSRF_ENABLED = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'stepanych is the best ever competitions since 2001'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	MY_MAIL_SUBJECT_PREFIX = '[От_Степаныча]'
	MY_MAIL_SENDER = 'Степаныч <registration@stepanich.ru>'
	ADMIN_EMAIL = 'registration@stepanich.ru'
	POSTS_PER_PAGE = 6
	COMMENTS_PER_PAGE = 10
	ALLOWED_PIC_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
	ALLOWED_DOC_EXTENSIONS = set(['doc', 'docx', 'xls', 'xlsx', 'pdf', 'txt'])
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','doc', 'docx', 'xls', 'xlsx', 'pdf', 'txt','rtf','ico','svg','ppt','pptx','csv'])
	#ммаксимальный размер загружаемого файла
	MAX_CONTENT_LENGTH = 1024*1204*6 
	UPLOADED_IMAGES_DEST = '/home/flask/Stepanych/img'
	UPLOADED_IMAGES_URL = '/img/'
	UPLOADED_DOCUMENTS_DEST = '/home/flask/Stepanych/doc'
	UPLOADED_DOCUMENTS_URL = '/doc/'
	UPLOADED_DATA_DEST = '/home/flask/Stepanych/data'
	UPLOADED_DATA_URL = '/data/'
	UPLOADS_DEFAULT_DEST = '/home/flask/Stepanych/'
	UPLOADS_DEFAULT_URL = '/'


	@staticmethod
	def init_app(Stepanych): 
		pass

class DevelopmentConfig(Config): 
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://stepanich:Stepanich_competition2001@localhost/stepanich?charset=utf8'
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'sql_repository')
	MAIL_SERVER = '104.238.111.93'
	MAIL_USE_TLS = True
	MAIL_PORT = 25
	MAIL_USERNAME = 'registration' # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = 'Registration_2001' # os.environ.get('MAIL_PASSWORD')
	
class TestingConfig(Config): 
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'mysql://stepanych:Stepanich_competition2001@localhost/mytestdb?charset=utf8'	

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://stepanich:Stepanich_competition2001@localhost/stepanich?charset=utf8'
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'sql_repository')
	MAIL_SERVER = '104.238.111.93'
	MAIL_USE_TLS = True
	MAIL_PORT = 25
	MAIL_USERNAME = 'registration' # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = 'Registration_2001' # os.environ.get('MAIL_PASSWORD')

class UnixConfig(ProductionConfig):
	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)
		# log to syslog
		import logging
		from logging.handlers import SysLogHandler
		syslog_handler = SysLogHandler()
		syslog_handler.setLevel(logging.WARNING)
		app.logger.addHandler(syslog_handler)
		#логи пишуться в /var/log/messages

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'poduction_logging':UnixConfig,
    'default': UnixConfig
}  

	        
