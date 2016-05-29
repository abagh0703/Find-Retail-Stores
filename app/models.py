from app import db

class Store(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bossName = db.Column(db.String(64))
	bossEmail = db.Column(db.String(120))
	url = db.Column(db.String(120))
	address = db.Column(db.String(120))
	name = db.Column(db.String(64))
	items = db.relationship('Item', backref='owner', lazy = 'dynamic')
	
	def __repr__(self):
		return '<STORE NAME: %r>' % (self.name)
        
class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	price = db.Column(db.Float)
	storeID = db.Column(db.Integer, db.ForeignKey('store.id'))
	
	def __repr__(self):
		return '<NAME: %r>' % (self.name)