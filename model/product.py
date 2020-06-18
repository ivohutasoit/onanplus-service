from application import database

class Product(database.Model):
    __tablename__  = 'PDCT01'

    id = database.Column('PDID00', database.Integer, primary_key=True, nullable=False)
    barcode = database.Column('PDBRCD', database.String(100), nullable=False)
    name = database.Column('PDNAME', database.String(256), nullable=False)
    company = database.Column('PDCMPY', database.String(100))
    detail = database.Column('PDDTIL', database.String(256))
    prices = {}

    def __init__(self, barcode, name, company, detail):
        self.barcode = barcode
        self.name = name
        self.company = company
        self.detail = detail

    def __repr__(self):
        return '<Product {}>'.format(self.barcode)

    def serialize(self):
        return {
            'id': self.id, 
            'barcode': self.barcode,
            'name': self.name,
            'company': self.company,
            'detail': self.detail
        }

    def set_prices(self, prices):
        self.prices = prices