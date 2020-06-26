from application import database

class Price(database.Model):
    __tablename__ = 'SPPC01'

    id = database.Column('P0ID00', database.Integer, primary_key=True, nullable=False)
    sku = database.Column('P0SKU0', database.String(100))
    product_id = database.Column('PCPDID', database.Integer, database.ForeignKey('PDCT01.PDID00'))
    store_id = database.Column('PCSTID', database.Integer, database.ForeignKey('STOR01.STID00'))
    seller = database.Column('PCSELL', database.String(100))
    promotion = database.Column('PCPRMO', database.Boolean, default=False)
    unit = database.Column('PCUNIT', database.String(50), default='PC')
    currency = database.Column('PCCURR', database.String(50))
    amount = database.Column('PCAMNT', database.Float, default=0)
    start_date = database.Column('PCSADT', database.Date)
    end_date = database.Column('PCENDT', database.Date)
    active = database.Column('PCACTV', database.Boolean, default=True)
    product = database.relationship('Product', lazy=True)
    store = database.relationship('Store', lazy=True)

    def __init__(self, 
        sku, product_id, store_id, 
        seller, promotion, unit, currency, 
        amount):
        self.sku = sku
        self.product_id = product_id
        self.store_id = store_id
        self.seller = seller
        self.promotion = promotion
        self.unit = unit
        self.currency = currency
        self.amount = amount

    def __repr__(self):
        return '<Product Price {}>'.format(self.product)

    # def __cmp__(self, other):
    #     if hasattr(other, 'getKey'):
    #         return self.getKey().__cmp__(other.getKey())

    def serialize(self, refer=''):
        if refer == 'product':
            return {
                'id': self.id, 
                'sku': self.sku,
                'store': self.store.serialize(),
                'seller': self.seller,
                'promotion': self.promotion,
                'unit': self.unit,
                'currency': self.currency,
                'amount': self.amount,
                'start_date': self.start_date,
                'end_date': self.end_date
            }
        if refer == 'store':
            return {
                'id': self.id, 
                'sku': self.sku,
                'product': self.product.serialize(),
                'seller': self.seller,
                'promotion': self.promotion,
                'unit': self.unit,
                'currency': self.currency,
                'amount': self.amount,
                'start_date': self.start_date,
                'end_date': self.end_date
            }
        return {
            'id': self.id, 
            'sku': self.sku,
            'product': self.product.serialize(),
            'store': self.store.serialize(),
            'seller': self.seller,
            'promotion': self.promotion,
            'unit': self.unit,
            'currency': self.currency,
            'amount': self.amount,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

    def getKey(self):
        return self.amount