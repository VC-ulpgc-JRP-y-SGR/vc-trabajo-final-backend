import datetime
from flask import Blueprint, request

from storage import counter
from .model import Counter, Entrances
from pystreamapi import Stream

blueprint = Blueprint('statistics', __name__, url_prefix='/statistics')

def valueOf(value):
    return {
        "value" : value
     }

@blueprint.route('/visitors/male_female_ratio/')
def male_female_ratio():
    male_count = Stream.of(list(Entrances.select().where(Entrances.genre == 'm'))).count()
    female_count = Stream.of(list(Entrances.select().where(Entrances.genre == 'f'))).count()
    return [{
        "name": "male",
        "value" : male_count
    },
    {
        "name": "female", 
        "value" : female_count
    }]

@blueprint.route('/visitors/age_interval_count/')
def age_interval():
    return Stream.of(list(Entrances.select()))\
        .map(lambda e: e.age_interval)\
        .group_by(lambda e: e)\
        .map(lambda e: {
            "name": e[0],
            "value": len(e[1])
        })\
        .to_list()

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
    return valueOf(sum(Stream.of(list(Counter.select())).map(lambda c: c.value).to_list()))
