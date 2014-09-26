#!/usr/bin/env python

"""
Usage: ./OSMRouteDatav2.0

Using origin and destination points in latitude and longitude format, a
route is calculated using the MapQuest Open service. Each road segment
used for the route is identified based on coordinates and routing data,
including the coordinates, distance, direction, and street name, is
stored. The coordinates are used to identify the corresponding ID in the
OpenStreetMap database. The OSM ID is then used to retrieve update
history data, including number of updates, number of contributors, and
the data of most recent update.
"""
 
__author__ = "Derek Marsh"
__email__ = "dmarsh19@uncc.edu"

import xml.etree.ElementTree as ET

import osmroutes2


mapquestKey = 'Fmjtd%7Cluur210r2h%2Cr5%3Do5-90yxq0'
OSMdataKeyList = ['version', 'timestamp', 'user']

# Test values
originX = '35.2565196067'
originY = '-80.8063941666'
destX = '35.3081159759'
destY = '-80.8701984774'


mapquestXMLRoute = osmroutes2.mapquest_xml(originX, originY,
                                               destX, destY,
                                               mapquestKey)
# Assign route results as XML tree 'root'.
root = ET.fromstring(mapquestXMLRoute)
# Read route data and store a list of specified information.
routes = osmroutes2.find_route_info(root)
# Obtain OSM way XML data from road segment coordinates.
for route in routes:
    wayId = osmroutes2.lat_lng_to_id(route[1][0], route[1][1])
    top = ET.fromstring(wayId)
    # Read OSM way XML data and store way id in route list.
    osmId = osmroutes2.find_osm_id(top)
    route.append(osmId)
    # Obtain OSM way history XML data and append to route.
    if route[5] == 'node':
        continue
    else:
        OSMWayResults = osmroutes2.osm_way_data(route[5])
        stalk = ET.fromstring(OSMWayResults)
        # Read OSM way history XML data and store
        # the specified value.
        getDataList = osmroutes2.get_data(stalk)
        route = route + getDataList
        print route


##def main():
##    """All logic is within this function to provide command-line use."""
##    # Calculate a network route from two points.
##    mapquestXMLRoute = osmroutes2.mapquest_xml(originX, originY,
##                                                   destX, destY,
##                                                   mapquestKey)
##    # Assign route results as XML tree 'root'.
##    root = ET.fromstring(mapquestXMLRoute)
##    # Read route data and store a list of specified information.
##    routes = osmroutes2.find_route_info(root)
##    # Obtain OSM way XML data from road segment coordinates.
##    for route in routes:
##        wayId = osmroutes2.lat_lng_to_id(route[1][0], route[1][1])
##        top = ET.fromstring(wayId)
##        # Read OSM way XML data and store way id in route list.
##        for osmId in top.findall('./result'):
##            for key, value in osmId.attrib.iteritems():
##                if key == 'osm_type' and value != 'way':
##                    break  # breaks last for loop, moves to next osm_id
##                else:
##                    if key == 'osm_id':
##                        route.append(value)
##        # Obtain OSM way history XML data and append to route.
##        OSMWayResults = osmroutes2.osm_way_data(route[5])
##        stalk = ET.fromstring(OSMWayResults)
##        # Read OSM way history XML data and store
##        # the specified value.
##        for OSMdataKey in OSMdataKeyList:
##            wayVersionCount = osmroutes2.get_data(stalk, OSMdataKey)
##            print(osmId + ': ' + OSMdataKey + ': ' +
##                  str(wayVersionCount))
##
##if __name__ == '__main__':
##    main()
