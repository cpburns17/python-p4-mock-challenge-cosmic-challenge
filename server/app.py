#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return 'home'

@app.get('/scientists')
def get_scientists():
    scientists = Scientist.query.all()
    scientist_list = []
    for s in scientists:
        scientist_list.append(s.to_dict(rules = ['-missions']))
    return scientist_list

@app.get('/scientists/<int:id>')
def get_scientist_by_id(id):
    scientist = db.session.get(Scientist, id)
    if not scientist:
        {'error': 'Scientist not found'}
    return scientist.to_dict()

@app.post('/scientists')
def add_scientist():
    try:
        data = request.json
        scientist = Scientist(name = data.get('name'), field_of_study = data.get('field_of_study'))
        db.session.add(scientist)
        db.session.commit()
        return scientist.to_dict()
    
    except Exception as e:
        return {'errors': ['validation errors']}, 400
    
@app.delete('/scientists/<int:id>')
def delete_scientist(id):
    scientist = db.session.get(Scientist, id)
    if not scientist:
        return {'error': 'Scientist not found'}, 404
    
    db.session.delete(scientist)
    db.session.commit()
    return {}, 204

@app.patch('/scientists/<int:id>')
def update_scientist(id):
    try:
        data = request.json
        scientist = db.session.get(Scientist, id)
        if not scientist:
            return {'error': 'Scientist not dound'}, 404
        for key in data:
            setattr(scientist, key, data[key])
            db.session.add(scientist)
            db.session.commit()
        return scientist.to_dict(), 202
    
    except Exception as e:
        return {'errors': ['validation errors']}, 400

@app.get('/planets')
def get_planets():
    planets = Planet.query.all()
    planet_list = []
    for p in planets:
        planet_list.append(p.to_dict(rules = ['-missions']))
    
    return planet_list, 200

# @app.post('/planets')
# def add_planets():
#     try:
#         data = request.json
#         planet = Planet(name = data.get('name'), distance_from_earth = data.get('distance_from_earth'), nearest_star = data.get('nearest_star'))
#         db.session.add(planet)
#         db.session.commit()
#         return planet.to_dict(), 200
    
#     except Exception as e:
#         return {'error': 'no planets exist'}

@app.post('/missions')
def add_mission():
    try:
        data = request.json
        mission = Mission(name = data.get('name'), planet_id = data.get('planet_id'), scientist_id = data.get('scientist_id'))
        db.session.add(mission)
        db.session.commit()
        return mission.to_dict(), 201
    
    except Exception as e:
        return {'errors': ['validation errors']}, 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
