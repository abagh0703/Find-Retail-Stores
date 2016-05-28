from app import app
from flask import render_template, flash, redirect
from .forms import AddStoreForm, SearchForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	if form.validate_on_submit():
		#do search stuff here
		flash("SEARCHING!!")
		print "YOLO"
		return redirect('/results')
	else:
		print "Not valid"
	return render_template('index.html',
							form = form)

@app.route('/addStore', methods=['GET','POST'])
@app.route('/addStore.html', methods=['GET','POST'])
def addStore():
	form = AddStoreForm()
	if form.validate_on_submit():
		flash("Thank you, your data has been submitted")
		return redirect("/index")
	return render_template('addStore.html')
	
@app.route('/results')
@app.route('/results.html')
def results():
	return render_template('results.html')