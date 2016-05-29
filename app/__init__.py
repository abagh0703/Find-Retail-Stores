from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config
from oauth2client.service_account import ServiceAccountCredentials
import gspread

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

#google sheets api
scope = ["https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(config.json_keyfile, scope)
gc = gspread.authorize(credentials)

from app import views, models
