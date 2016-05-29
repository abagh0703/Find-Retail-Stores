from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from Lexigraph import Lexigraph
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

#google sheets api
scope = ["https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(config.json_keyfile, scope)
gc = gspread.authorize(credentials)

UPLOAD_FOLDER = config.basedir + "/uploads"
ALLOWED_EXTENSIONS = set(['csv'])
#spell checker
lex = Lexigraph()
from app import views, models, config




app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
