import yaml
import os
import requests
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import urllib.request
import json
import pandas as pd
import numpy as np

dirname = os.path.dirname(__file__)
base_url = "https://maps.googleapis.com/maps/api/directions/json?origin="


def get_credentials():
    credentials = os.path.join(dirname, 'credentials.yml')
    stream = open(credentials, 'r')
    parsed_yaml_file = yaml.load(stream, Loader=yaml.FullLoader)
    API_KEY = parsed_yaml_file["google_api"]['google_maps']
    return API_KEY


def get_emissions(mode):
    emissions = os.path.join(dirname, 'emissions.yml')
    stream = open(emissions, 'r')
    parsed_yaml_file = yaml.load(stream, Loader=yaml.FullLoader)
    factor = parsed_yaml_file["emissions"][str(mode)]
    return factor


def carbon_emissions(mode, distance):
    if mode == 'driving':
        return (get_emissions('driving') * distance) / 1000
    elif mode == 'walking':
        return 0
    elif mode == 'bicycling':
        return 0
    elif mode == 'transit&transit_mode=train':
        return (get_emissions('rail') * distance) / 1000
    elif mode == 'transit&transit_mode=subway':
        return (get_emissions('rail') * distance) / 1000
    elif mode == 'transit&transit_mode=bus':
        return (get_emissions('bus') * distance) / 1000
    elif mode == 'transit':
        return (get_emissions('rail') * distance) / 1000
    else:
        return 0


def get_distance(mode, origin, destination,dateDeparture, dateArrival):
    API_KEY = get_credentials()
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    navigate = 'origin={}&destination={}&mode={}&key={}'.format(origin, destination,mode,API_KEY)
    request = endpoint + navigate
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)

    results = {
        'distance': directions['routes'][0]['legs'][0]['distance']['value'],
        'time': directions['routes'][0]['legs'][0]['duration']['value'],
        'emissions': carbon_emissions(mode, directions['routes'][0]['legs'][0]['distance']['value'])

    }

    return results


def get_all_journeys(origin, destination,dateDeparture, dateArrival):
    driving = get_distance('driving', origin, destination,dateDeparture, dateArrival)
    walking = get_distance('walking', origin, destination,dateDeparture, dateArrival)
    cycling = get_distance('bicycling',origin, destination,dateDeparture, dateArrival)
    transit_train = get_distance('transit&transit_mode=train',origin, destination,dateDeparture, dateArrival)
    transit_subway = get_distance('transit&transit_mode=subway', origin, destination,dateDeparture, dateArrival)
    transit_bus = get_distance('transit&transit_mode=bus', origin, destination,dateDeparture, dateArrival)
    public_transport = get_distance('transit',origin, destination,dateDeparture, dateArrival)

    results = {
        'driving': driving,
        'walking': walking,
        'cycling': cycling,
        'transit_train': transit_train,
        'transit_subway': transit_subway,
        'transit_bus': transit_bus,
        'public_transport': public_transport
    }
    return results

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def mult_dictionary(a,b):
    for key in b:
        a[key] *= b[key]
    return a

def get_results(**kwargs):
    if kwargs['returnBool'] == False:
        if kwargs['clientTripBool'] == False:
            results = get_all_journeys(kwargs['origin'], kwargs['destination'],kwargs["dateDepartureOneWay"],kwargs["dateArrivalOneWay"])
            return results

        else:
            days = int(kwargs['clienttime'])
            trip1 = get_all_journeys(kwargs['origin'], kwargs['destination'],kwargs["dateDepartureOneWay"],kwargs["dateArrivalOneWay"])
            trip2 = get_all_journeys(kwargs['originClient'], kwargs['destinationClient'],kwargs["dateDepartureOneWay"],kwargs["dateArrivalOneWay"])
            results =  merge_dicts(trip1, trip2)
            return results

    elif kwargs['returnBool'] == True:
        if kwargs['clientTripBool'] == False:
            trip1 = get_all_journeys(kwargs['origin'], kwargs['destination'], kwargs["dateDepartureOneWay"],
                                       kwargs["dateArrivalOneWay"])
            trip2 = get_all_journeys(kwargs['destination'], kwargs['origin'], kwargs["dateDepartureReturn"],
                                       kwargs["dateArrivalReturn"])
            results = merge_dicts(trip1, trip2)
            return results

        else:
            trip1 = get_all_journeys(kwargs['origin'], kwargs['destination'], kwargs["dateDepartureOneWay"],
                                        kwargs["dateArrivalOneWay"])
            trip2 = get_all_journeys(kwargs['destination'], kwargs['origin'], kwargs["dateDepartureReturn"],
                                       kwargs["dateArrivalReturn"])
            trip3 = get_all_journeys(kwargs['originClient'], kwargs['destinationClient'], kwargs["dateDepartureOneWay"],
                                        kwargs["dateArrivalOneWay"])
            results = merge_dicts(trip1, trip2, trip3)
            return results




