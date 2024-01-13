import datetime
from flask import Blueprint, request
from .model import Entrances
from pystreamapi import Stream

blueprint = Blueprint('statistics', __name__, url_prefix='/statistics')

def valueOf(value):
    return {
        "value" : value
     }

@blueprint.route('/entrances/')
def entrances():
    return Stream.of(list(Entrances.select()))\
        .map(lambda e: e.to_json()).\
        to_list()

@blueprint.route('/entrances/', methods=['POST'])
def create_entrance():
    entrance = Entrances.create(timestamp=datetime.datetime.now(),
                                genre=request.json['genre'],
                                age_interval=request.json['age_interval'],
                                image=request.json['image'])
    return entrance.to_json()
    
@blueprint.route('/entrances/<int:entrance_id>/')
def entrance(entrance_id):
    return Stream.of(list(Entrances.select().where(Entrances.id == entrance_id)))\
        .map(lambda e: e.to_json()).\
        to_list()
    
@blueprint.route('/visitors/today/')
def visitors_today():
    now = datetime.datetime.now()
    return valueOf(Stream.of(list(Entrances.select().where(
        Entrances.timestamp.day == now.day,
        Entrances.timestamp.month == now.month,
        Entrances.timestamp.year == now.year)))
    \
    .count())

@blueprint.route('/visitors/week/')
def visitors_week():
    now = datetime.datetime.now()
    return valueOf(Stream.of(list(Entrances.select()\
                          .where(
                                Entrances.timestamp.day >= now.day - 7,
                                Entrances.timestamp.month == now.month,
                                Entrances.timestamp.year == now.year)))\
            .count())

@blueprint.route('/visitors/per_month/')
def visitors_grouped():
    return Stream.of(range(1, 13))\
        .map(lambda m: Stream.of(list(Entrances.select()\
                          .where(
                                Entrances.timestamp.month == m,
                                Entrances.timestamp.year == datetime.datetime.now().year)))\
            .count())\
        .to_list()
        
        
@blueprint.route('/visitors/current/')
def visitors_current():
    return valueOf(0)