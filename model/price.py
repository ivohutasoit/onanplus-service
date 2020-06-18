from application import database

class Price(database.Model):
    __tablename__ = 'SPPC01'

    id = database.Column('P0ID00', database.Integer, primary_key=True, nullable=False)
    sku = database.Column('P0SKU0', database.String(100))
    product_id = database.Column('PCPDID',database.Integer, database.ForeignKey('PDCT01.PDID00'))
    store_id = database.Column('PCSTID',database.Integer, database.ForeignKey('STOR01.STID00'))
    seller = database.Column('PCSELL', database.String(100))
    currency = database.Column('PCCURR', database.String(50))
    normal = database.Column('PCNRML', database.Float, default=0)
    promo = database.Column('PCPRMO', database.Float)
    promo_start = database.Column('PCPOST', database.Date)
    promo_end = database.Column('PCPOEN', database.Date)
    date = database.Column('PCDATE', database.Date)
    product = database.relationship('Product', lazy=True)
    store = database.relationship('Store', lazy=True)

    def __init__(self, sku, product, store, seller, currency, normal, promo, promo_start, promo_end, date):
        self.sku = sku
        self.product_id = product
        self.store_id = store
        self.seller = seller
        self.currency = currency
        self.normal = normal
        self.promo = promo
        self.promo_start = promo_start
        self.promo_end = promo_end
        self.date = date

    def __repr__(self):
        return '<Product Price {}>'.format(self.product)

    def serialize(self):
        return {
            'id': self.id, 
            'sku': self.sku,
            'product': self.product.serialize(),
            'store': self.store.serialize(),
            'seller': self.seller,
            'currency': self.currency,
            'normal': self.normal,
            'promo': self.promo,
            'promo_start': self.promo_start,
            'promo_end': self.promo_end,
            'date': self.date
        }