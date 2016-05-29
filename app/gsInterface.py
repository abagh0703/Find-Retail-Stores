import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import db
from .models import Item
from config import basedir

scope = ["https://spreadsheets.google.com/feeds"]
credentials = None

credentials = ServiceAccountCredentials.from_json_keyfile_name(basedir+"/RetailTrail-168c25034f99.json", scope)
gc = gspread.authorize(credentials)


wks = gc.open_by_url(url).sheet1
items = wks.col_values(1)
prices = wks.col_values(2)
result = []
for i in xrange(len(items)):
	result.append(Item(name=items[i], price=prices[i], owner=store))
for item in result:
	db.session.add(item)

