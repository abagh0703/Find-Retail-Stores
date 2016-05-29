from app import app, db, gc
from flask import render_template, flash, redirect, request, url_for, session
from .forms import AddStoreForm, SearchForm
from .models import Store, Item
import gspread

#import gmInterface
import json
import config

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
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
	form = AddStoreForm()
	if form.validate_on_submit():
		#flash("Thank you, your data has been submitted")
		print "Thank you, your data has been submitted"
		
		session["store name"] =  form.name.data
		
		
		
			#There are headings on the spreadsheets
			
		
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
			update_all_sheets()
			wks = gc.open_by_url(session["sheetURL"]).sheet1
			
			items = wks.col_values(1)
			prices = wks.col_values(2)
			
			if form.isHeading.data:
				items = items[1:]
				prices = prices[1:]
				
			if len(items) != len(prices):
				return render_template('addStore.html',
							form = form,
							errorMessage = "Make sure the item and price columns are the same length".toUpper())
			
			result = []
			for i, j in zip(items, prices):
				
				if i.strip() and j.strip():
					print i, "|", j
					result.append(Item(name=i.strip(), price=float(j.strip()), owner=store))
			for item in result:
				db.session.add(item)


			db.session.add(store)
		
			db.session.commit()
		#print session['sheetURL'] --- work around because hiddenfield wasn't working
		return redirect("/index")
	else:
		#flash("Error!")
		print "This didn't work"
	return render_template('addStore.html',
							form = form,
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
		if itna.find(keyword) != -1 or keyword.find(itna) != -1:
			results.append([item.owner.name, item.owner.address, item.price])
	print results
	#if len(results) != 0:
	#	print results	
		#gmInterface.load_map(results)
	
	
	form = SearchForm()
	if form.validate_on_submit():
		
		flash("SEARCHING!!")
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
				result.append(Item(name=i.strip(), price=float(j.strip()), owner=store))
		for item in result:
			db.session.add(item)
		db.session.commit()

	