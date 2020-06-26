import json
import requests;

from flask import Blueprint, jsonify, request
from geopy import distance

from application import database
from model import Store

store_controller = Blueprint('store_controller', __name__)

@store_controller.route('', methods=['GET'])
def index():
    try:
        stores = Store.query.order_by(Store.name).all()
        return jsonify({ 'status': 'OK', 'stores': [store.serialize() \
            for store in stores] }), 200
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@store_controller.route('', methods=['POST'])
def create():
    try:
        store=Store(
            code= request.json['code'] or None,
            name=request.json['name'], 
            online=request.json['online'] or False,
            website=request.json['website'] or None,
            longitude=request.json['longitude'] or None,
            latitude=request.json['latitude'] or None,
            source='OWN',
            source_id=request.json['source_id'] or None
        )
        database.session.add(store)
        database.session.commit()
        return jsonify({ 'status': 'OK', 'store': store.serialize() }), 201
    except Exception as e:
	    return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@store_controller.route('/<id>', methods=['GET'])
def detail(id):
    try:
        store=Store.query.filter_by(id=id).first()

        if store:
            return jsonify({ 'status': 'OK', 'store': store.serialize() }), 200

        return jsonify({ 'status': 'NOT FOUND'}), 404
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

# @store_controller.route('search/<query>', methods=['GET'])
# def search(query):
#     try:
#         store=Store.query.filter_by(code=query).first()
#         if not store:
#             store=Store.query.filter_by(name=query).first()

#         return jsonify({ 'status': 'OK', 'store': store.serialize() if store else '{}'}), 200
#     except Exception as e:
#         return jsonify({ 'status': 'ERROR', 'error': str(e) }), 404

#https://ourcodeworld.com/articles/read/1019/how-to-find-nearest-locations-from-a-collection-of-coordinates-latitude-and-longitude-with-php-mysql
@store_controller.route('/around', methods=['GET'])
def around():
    sql = """
    SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) ) 
    * cos( radians( lng ) - radians(-122) ) + sin( radians(37) ) * sin(radians(lat)) ) ) AS distance 
    FROM markers 
    HAVING distance < 25 
    ORDER BY distance 
    LIMIT 0 , 20;
    """

    latitude = 3.10568
    longitude = 101.64696
    radius = 1 # in KM

    query = """
    SELECT * FROM (SELECT *, 
        (((ACOS(
            sin((3.10568 * pi() / 180)) *
            sin(("STLATD" * pi() / 180)) + cos((3.10568 * pi() /180 )) *
            cos(("STLATD" * pi() / 180)) * cos(((101.64696 - "STLONG") * pi()/180)))
        ) * 180/pi() 
        ) * 60 * 1.1515 * 1.609344 
        ) "DISTANCE"
    FROM "STOR01") AS A
    WHERE A."DISTANCE" <= 1
    ORDER BY A."DISTANCE";
    """

    results = database.session.execute(query)
    stores = []
    for item in results:
        store = Store(
            code=item[1],
            name=item[2], 
            online=item[3],
            website=item[4],
            latitude=item[5], 
            longitude=item[6],
            source='OWN',
            source_id=item[8]
        ) 
        store.id = item[0]
        store.distance = item[9]
        stores.append(store)

    base_url = 'http://overpass-api.de/api/interpreter'
    # base_url = 'https://places.ls.hereapi.com/places/v1/discover/around'
    url_query = """
    [out:json];
    node(around.center:1000,3.10568,101.64696)[~"."~"."][shop];
    out meta;
    """

    response = requests.get(base_url, 
                        params={'data': url_query})
                        # params={
                        #     'at': '3.1059857049166495,101.64676227155495;r=50',
                        #     'cat': 'shopping',
                        #     'apiKey': '3pGS1RhTklIcwhc14IwoV9m7miWFNsvLVWsVmCwls6M'
                        # })
    elements = response.json()['elements']

    for item in elements:
        if 'name' not in item['tags']:
            continue

        store = Store(
            code=None,
            name=str(item['tags']['name']).upper(), 
            latitude=item['lat'], 
            longitude=item['lon'],
            online=False,
            website=None,
            source='OSM',
            source_id=str(item['id'])
        )
        exist = any(x for x in stores if ((x.latitude == store.latitude) & (x.longitude==store.longitude)))
        if not exist:
            store.distance = distance.distance((store.latitude, store.longitude), (latitude, longitude)).km
            stores.append(store)

    stores.sort(key=lambda x: x.distance, reverse=False)
                        
    return jsonify({ 'status': 'OK', 'stores': [store.serialize() \
            for store in stores]  }), 200
    # return jsonify({'status': 'OK', 'stores': elements}), 200