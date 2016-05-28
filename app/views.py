from app import app
from flask import render_template



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addStore', methods=['GET','POST'])
def addStore():
	#form = AddStoreForm()
	#if form.validate_on_submit()
	return render_template('addStore.html')
	
@app.route('/results')
def results():
	return render_template('results.html')