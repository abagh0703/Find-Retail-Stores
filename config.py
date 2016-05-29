import os
basedir = os.path.abspath(os.path.dirname(__file__))
json_keyfile = basedir+"/RetailTrail-168c25034f99.json"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
