#!/usr/bin/env python

"""
Usage: ./OSMRouteDatav2.0

Using origin and destination points in latitude and longitude format, a
route is calculated using the MapQuest Open service. Each road segment
used for the route is identified based on coordinates and routing data,
including the coordinates, distance, direction, and street name, is
stored. The coordinates are used to identify the corresponding ID in the
OpenStreetMap database. The OSM ID is then used to retrieve update data,
including number of updates, number of contributors, and the data of
most recent update.
"""
 
__author__ = "Derek Marsh"
__email__ = "dmarsh19@uncc.edu"

import datetime
import xml.etree.ElementTree as ET

import osmroutes2


##beginTime=datetime.datetime.now()
##print("begin time: {0}").format(beginTime)

mapquestKey = 'Fmjtd%7Cluur210r2h%2Cr5%3Do5-90yxq0'

OSMdataKeyList = ['version', 'timestamp', 'user']
mapquestDataKeys = ['latlng', 'distance', 'direction', 'street']

# Test values
originX = '35.2565196067'
originY = '-80.8063941666'
destX = '35.3081159759'
destY = '-80.8701984774'

###############################################################################################################################
def main():
# Request MapQuest route XML based on lat, lng
    mapquestXMLRoute = OSMRouteModule.mapquest_xml(originX, originY, destX, destY, mapquestKey)
# Assign route API results to XML tree 'root'
    root = ET.fromstring(mapquestXMLRoute)
# Search MapQuest route for each road leg coordinates, store as tuple
    legCoord = OSMRouteModule.findRouteInfo(root)
# Convert maneuver coordinates to IDs
    for leg in legCoord:
        wayId = OSMRouteModule.latLngToId(leg[0], leg[1])
        top = ET.fromstring(wayId)
        osmRouteIds = OSMRouteModule.findOsmId(top)
        for osmId in osmRouteIds:
# Using osm_ids, find the update history
            OSMWayResults = OSMRouteModule.OSMWayData(osmId)
            stalk = ET.fromstring(OSMWayResults)
# Within way history, find number of version updates
            for OSMdataKey in OSMdataKeyList:
                wayVersionCount = OSMRouteModule.getData(stalk, OSMdataKey)
                print(osmId + ': ' + OSMdataKey + ': ' + str(wayVersionCount))

if __name__ == '__main__':
    main()

##endTime=datetime.datetime.now()
##print("end time: {0}").format(endTime)
##runTime=endTime-beginTime
##print("run time: {0}").format(runTime)
##
##print('done')
