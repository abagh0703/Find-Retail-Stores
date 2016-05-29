from flask.ext.wtf import Form
from wtforms import StringField, SelectField, IntegerField, HiddenField, BooleanField, FileField
from wtforms.validators import InputRequired, URL, Email, Required

stateList = [("AK", "Alaska"), 
                ("AL", "Alabama"), 
                ("AR", "Arkansas"), 
                ("AS", "American Samoa"), 
                ("AZ", "Arizona"), 
                ("CA", "California"), 
                ("CO", "Colorado"), 
                ("CT", "Connecticut"), 
                ("DC", "District of Columbia"), 
                ("DE", "Delaware"), 
                ("FL", "Florida"), 
                ("GA", "Georgia"), 
                ("GU", "Guam"), 
                ("HI", "Hawaii"), 
                ("IA", "Iowa"), 
                ("ID", "Idaho"), 
                ("IL", "Illinois"), 
                ("IN", "Indiana"), 
                ("KS", "Kansas"), 
                ("KY", "Kentucky"), 
                ("LA", "Louisiana"), 
                ("MA", "Massachusetts"), 
                ("MD", "Maryland"), 
                ("ME", "Maine"), 
                ("MI", "Michigan"), 
                ("MN", "Minnesota"), 
                ("MO", "Missouri"), 
                ("MS", "Mississippi"), 
                ("MT", "Montana"), 
                ("NC", "North Carolina"), 
                ("ND", "North Dakota"), 
                ("NE", "Nebraska"), 
                ("NH", "New Hampshire"), 
                ("NJ", "New Jersey"), 
                ("NM", "New Mexico"), 
                ("NV", "Nevada"), 
                ("NY", "New York"), 
                ("OH", "Ohio"), 
                ("OK", "Oklahoma"), 
                ("OR", "Oregon"), 
                ("PA", "Pennsylvania"), 
                ("PR", "Puerto Rico"), 
                ("RI", "Rhode Island"), 
                ("SC", "South Carolina"), 
                ("SD", "South Dakota"), 
                ("TN", "Tennessee"), 
                ("TX", "Texas"), 
                ("UT", "Utah"), 
                ("VA", "Virginia"), 
                ("VI", "Virgin Islands"), 
                ("VT", "Vermont"), 
                ("WA", "Washington"), 
                ("WI", "Wisconsin"), 
                ("WV", "West Virginia"), 
                ("WY", "Wyoming") ]
                
class AddStoreForm(Form):
	bossName = StringField('boss name', validators = [InputRequired()])
	bossEmail = StringField('boss email', validators = [InputRequired()])
	name = StringField('store name', validators = [InputRequired()])
	streetAddress = StringField('street address', validators=[InputRequired()])
	city = StringField('city', validators=[InputRequired()])
	state = SelectField('state', choices=stateList)
	zipCode = IntegerField('zip code', validators=[InputRequired()]) 
	isHeading = BooleanField('sheet heading')
	#processed using ajax: inventoryURL = HiddenField('inventory URL')
	#csvFile = FileField('upload file')
	

	
class SearchForm(Form):
	searchBox = StringField('search')
	