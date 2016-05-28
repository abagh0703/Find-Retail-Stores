from app import db

class URL(db.model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(120), index = True, unique = True)
	def __repr__(self):
        return '<URL %r>' % (self.url)
        
#class Inventory(