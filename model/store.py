from application import database

# class StoreGroup(Type):
#     __mapper_args__ = {
#         'polymorphic_identity': 'STOREGROUP'
#     }

class Store(database.Model):
    __tablename__ = 'STOR01'

    id = database.Column('STID00', database.Integer, primary_key=True, nullable=False)
    code = database.Column('STCODE', database.String(100))
    name = database.Column('STNAME', database.String(256), nullable=False)
    online = database.Column('STONLN', database.Boolean, default=False)
    website = database.Column('STWBST', database.String(256)) 
    latitude = database.Column('STLATD', database.Float)
    longitude = database.Column('STLONG', database.Float)
    source = database.Column('STSOUR', database.String(256))
    source_id = database.Column('STSRID', database.String(100))

    distance = None

    def __init__(self, name, online, website, longitude, latitude, 
        code=None, source=None, source_id=None):
        self.code = code
        self.name = name
        self.online = online
        self.website = website
        self.longitude = longitude
        self.latitude = latitude
        self.source = source
        self.source_id = source_id

    def __repr__(self):
        return '<Store {}>'.format(self.name)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'code': self.code,
            'online': self.online,
            'website': self.website,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'source': self.source,
            'source_id': self.source_id,
            'distance': self.distance
        }