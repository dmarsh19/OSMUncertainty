"""
Using origin and destination coordinates (manually identified as
beginning and ending nodes of an OSM segment), travel distance along the
segment is calculated across the OSM (MapQuest) and Google Maps dataset
"""

__author__ = "Derek Marsh"
__email__ = "dmarsh19@uncc.edu"

import os
import datetime
import time
import urllib2
from urllib2 import urlopen

import simplejson

mapquestKey = 'Fmjtd%7Cluur210r2h%2Cr5%3Do5-90yxq0'
sleepTime = 3 # in seconds
pointList = [['-80.5624187', '35.5029057', '-80.6020244', '35.4481171'],
             ['-80.841945', '35.227995', '-80.833915', '35.221155']]


def googleOutput(originLat, originLng, destinationLat, destinationLng):
    """Google Directions API using origin and destination coordinates"""
    googleapi = 'http://maps.googleapis.com/maps/api/directions/json'
    sensor = 'sensor=false'
    mode = 'mode=driving'
    googleOrigin = 'origin=%s,%s' % (originLat, originLng)
    googleDestination = "destination=%s,%s" % (destinationLat,
                                               destinationLng)
    parts_driving = [googleOrigin, googleDestination, sensor, mode]
    driving_query = '&'.join(parts_driving)
    url_driving = '%s?%s' % (googleapi, driving_query)
    request_driving = urlopen(url_driving)
    results_driving = simplejson.load(request_driving)
    for route in results_driving['routes']:
        for leg in route['legs']:
            try:
                distance_driving = leg['distance']['text']
                return str(distance_driving)
            except KeyError:
                return "Error"

def mapquestOutput(originLat, originLng, destinationLat, destinationLng,
                   mapquestKey):
    """MapQuest Open API using origin and destination coordinates"""
    mapquestParts = (('http://open.mapquestapi.com/directions/v2/route?'
                     'key=%s&outFormat=json&unit=m&from=%s,%s&to=%s,%s')
                     %(mapquestKey, originLat, originLng,
                       destinationLat, destinationLng))
    mapquestRequest = urlopen(mapquestParts)
    mapquestResults = simplejson.load(mapquestRequest)
    for key, number in mapquestResults['route'].iteritems():
        if key == 'distance':
            distNumber = number
            return str(distNumber)

def main():
    runOD = 0
    while runOD in range(len(pointList)):
        originLat = pointList[runOD][1] 
        originLng = pointList[runOD][0]
        destinationLat = pointList[runOD][3]
        destinationLng = pointList[runOD][2]
        googleRoute = googleOutput(originLat, originLng, destinationLat,
                                   destinationLng)
        mapquestRoute = mapquestOutput(originLat, originLng, destinationLat,
                                       destinationLng, mapquestKey)
        output = [originLat, originLng, destinationLat, destinationLng,
                  googleRoute, mapquestRoute]
        outputFormat = '\t'.join(output)
        outputFormat = outputFormat + '\n'
        print(outputFormat)
        runOD += 1
        time.sleep(sleepTime)
    print('done')

if __name__ == '__main__':
    main()
