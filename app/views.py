from app import app
from flask import render_template
from .forms import AddStoreForm


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/addStore', methods=['GET','POST'])
@app.route('/addStore.html', methods=['GET','POST'])
def addStore():
	#form = AddStoreForm()
	#if form.validate_on_submit()
	return render_template('addStore.html')
	
@app.route('/results')
@app.route('/results.html')
def results():
	return render_template('results.html')