#!/Users/macbookpro15/Documents/programming/Stepanych/venv-pyth36/bin/python
from migrate.versioning import api 
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO
from config import DevelopmentConfig, config
from Stepanych import create_app
from flask_sqlalchemy import SQLAlchemy
import os.path
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
db = SQLAlchemy(app)
SQLALCHEMY_DATABASE_URI = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = DevelopmentConfig.SQLALCHEMY_MIGRATE_REPO
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
	api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))	