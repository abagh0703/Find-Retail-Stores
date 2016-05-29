from app import app, db, gc, lex, ALLOWED_EXTENSIONS
from flask import render_template, flash, redirect, request, url_for, session
from .forms import AddStoreForm, SearchForm
from .models import Store, Item
import gspread
#import gmInterface
import json
import config
#import csv
#from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
@app.route('/results/', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	if form.validate_on_submit():
		#do search stuff here
		flash("SEARCHING!!")
		#print "YOLO"
		searchText = form.searchBox.data
		return redirect('/results/%s'%searchText)
	else:
		print "Not valid"
	return render_template('index.html',
							form = form)

@app.route('/addStore', methods=['GET','POST'])
@app.route('/addStore.html', methods=['GET','POST'])
def addStore():
	searchForm = SearchForm()
	form = AddStoreForm()
	if searchForm.validate_on_submit() and searchForm.searchBox.data:
		#do search stuff here
		#flash("SEARCHING!!")
		print "YOLO"
		searchText = searchForm.searchBox.data
		return redirect('/results/%s'%searchText)
	
	elif form.validate_on_submit():
		#flash("Thank you, your data has been submitted")
		print "Thank you, your data has been submitted"
		
		session["store name"] =  form.name.data
		
		
		
		#if data is given in a .csv file, convert it to google sheet	
		#if form.csvFile.filename != "":
		#	session['sheetURL'] = config.csvDataURL	
		
		#create new database entry
		store = Store.query.filter_by(name=session["store name"]).first() 
		if store == None:
			store = Store(bossName=form.bossName.data,
							bossEmail=form.bossEmail.data,
							url=session['sheetURL'],
							address="%s, %s, %s %s" %(form.streetAddress.data, form.city.data, form.state.data, form.zipCode.data),
							name=session["store name"]
							)
			
			#check all other sheets to see if there are any changes
			#if there are they are updated
			#update_all_sheets()
			spreadSheet = gc.open_by_url(session["sheetURL"])
			wks = spreadSheet.get_worksheet(0)
			#if form.csvFile.filename != "":
			#	worksheet = spreadSheet.add_worksheet(title=session['store name'], rows = 500, cols = 2) #hopefully 500 is enough
				#load the csv files into the sheet
			#	with read(app.config[UPLOAD_FOLDER] + "/" + form.csvFile.filename, "r") as file:
			#		reader = csv.reader(file, delimier=',')
			#		i=1
			#		for row in reader:
			#			worksheet.update_cell(i, 1, row[0])
			#			worksheet.update_cell(i, 2, row[1])
			#	wks = spreadSheet.worksheet(session['store name'])
				
			items = wks.col_values(1)
			prices = wks.col_values(2)
			
			if form.isHeading.data: #There are headings on the spreadsheets
				items = items[1:]
				prices = prices[1:]
				print items
				
			if len(items) != len(prices):
				return render_template('addStore.html',
							form = form,
							errorMessage = "Make sure the item and price columns are the same length".toUpper())
			
			result = []
			for i, j in zip(items, prices):
				
				if i.strip() and j.strip():
					print i, "|", j
					if j.strip() == "":
						j = "-1"
						#set the default price at -1 for javascript processing
					result.append(Item(name=i.strip(), price=float(j.strip()), owner=store))
			for item in result:
				db.session.add(item)


			db.session.add(store)
		
			db.session.commit()
		#print session['sheetURL'] --- work around because hiddenfield wasn't working
		return redirect(url_for("thankyou"))
	#else:
		#flash("Error!")
		#print "This didn't work"
	return render_template('addStore.html',
							form = form,
							searchForm = searchForm,
							errorMessage = "")
	
@app.route('/results/<keyword>', methods=['GET', 'POST'])
@app.route('/results.html/<keyword>', methods=['GET', 'POST'])
def results(keyword):
	keyword = keyword.lower()
	#do search stuff here
	allItems = Item.query.all()
	results = []
	for item in allItems:
		itna = item.name.lower()
		if matches(itna, keyword):
			results.append([item.owner.name, item.owner.address, item.price])
	print results
	#if len(results) != 0:
	#	print results	
		#gmInterface.load_map(results)
	
	
	form = SearchForm()
	if form.validate_on_submit():
		
		#flash("SEARCHING!!")
		#print "YOLO"
		searchText = form.searchBox.data
		return redirect('/results/%s' %searchText)
	return render_template('results.html',
							form = form,
							mapLocs = results,
							search = keyword.upper()
							)

@app.route('/urlsent', methods=['GET','POST'])
def urlsent():
	#print request.get_json()
	session['sheetURL'] = request.get_json()['sheetURL']
	#print session['sheetURL']
	return redirect(url_for("addStore"))

@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou():
	form = SearchForm()
	if form.validate_on_submit():
		#flash("SEARCHING!!")
		#print "YOLO"
		searchText = form.searchBox.data
		return redirect('/results/%s' %searchText)
	return render_template('thankyou.html',
					form = form
					)
	
	
def update_all_sheets():
	stores = Store.query.all()
	for store in stores:
		wks = gc.open_by_url(store.url).sheet1
		items = wks.col_values(1)
		prices = wks.col_values(2)
		if len(items) != len(prices):
			print "Error updating: %s"%(store.name)
			continue
		
		store_items = Item.query.filter_by(storeID=store.id)
		for item in store_items:
			db.session.delete(item)
		
		result = []
		for i, j in zip(items, prices):
			
			if i.strip() and j.strip():
				print i, "|", j
				try:
					result.append(Item(name=i.strip(), price=float(j.strip()), owner=store))
				except Exception:
					continue
		for item in result:
			db.session.add(item)
		db.session.commit()

def matches(itemName, searchWord):
	
	#return itemName.find(searchWord) != -1 or searchWord.find(itemName) != -1
	combos = set()
	combos = combos | lex.substitutions(itemName)
	
	#combos = set()#lex.combos(itemName) #or itemName.find(searchWord) != -1 or searchWord.find(itemName) != -1
	#combos = combos | {lex.combos(itna) for itna in itemName.split()}
	#for itna in itemName.split(" "):
	#	combos = combos | lex.combos(itna)
	for c in combos:
		if c.find(searchWord) != -1 or searchWord.find(c) != -1:
			return True
	return False


def allowed_file(filename):
	return "." in filename and filename.split(".", 1)[1] in ALLOWED_EXTENSIONS