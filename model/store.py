from application import database

class Store(database.Model):
    __tablename__ = 'STOR01'

    id = database.Column('STID00', database.Integer, primary_key=True, nullable=False)
    code = database.Column('STCODE', database.String(100))
    name = database.Column('STNAME', database.String(256), nullable=False)
    online = database.Column('STONLN', database.Boolean, default=False)
    website = database.Column('STWBST', database.String(256)) 
    longitude = database.Column('STLONG', database.Float)
    latitude = database.Column('STLATD', database.Float)

    def __init__(self, code, name, online, website, longitude, latitude):
        self.code = code
        self.name = name
        self.online = online
        self.website = website
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<Store {}>'.format(self.code)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'code': self.code,
            'online': self.online,
            'website': self.website,
            'longitude': self.longitude,
            'latitude': self.latitude
        }