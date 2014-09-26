"""
This module contains functions for OSMRouteDatav2.0.py,
including API calls and some logic processing
"""

from urllib2 import urlopen


def mapquest_xml(originX, originY, destX, destY, mapquestKey):
    """Calculate a network route from two points."""
    mapquestParts = ((r"http://open.mapquestapi.com/directions/v2/route"
                      "?key=%s&outFormat=xml&unit=m&from=%s,%s&to=%s,"
                      "%s&maxLinkId=15") % (mapquestKey, originX,
                                            originY, destX, destY))
    mapquestXMLRequest = urlopen(mapquestParts).read()
    return mapquestXMLRequest


def find_route_info(root):
    """Read route data and store a list of specified information."""
    routeInfo = []
    for maneuver in root.findall('./route/legs/leg/maneuvers/maneuver'):
        for sub in maneuver:
            if sub.tag == 'index':
                index = sub.text
            if sub.tag == 'startPoint':
                for child in sub:
                    if child.tag == 'lng':
                        lng = child.text
                    elif child.tag == 'lat':
                        lat = child.text
                latLng = (lat, lng)   
            elif sub.tag == 'distance':
                dist = sub.text
            elif sub.tag == 'directionName':
                direction = sub.text
            elif sub.tag == 'streets':
                streets = []
                for branch in sub:
                    streets.append(branch.text)
                streetTuple = tuple(streets)
        singleRouteInfo = [index, latLng, dist, direction, streetTuple]
        routeInfo.append(singleRouteInfo)
    return routeInfo


def lat_lng_to_id(lat, lng):
    """Obtain OSM way XML data from road segment coordinates."""
    latLngToIdParts = (r"http://open.mapquestapi.com/nominatim/v1/"
                        "reverse?lat=%s&lon=%s") % (lat, lng)
    latLngToIdRequest = urlopen(latLngToIdParts).read()
    return latLngToIdRequest


def find_osm_id(top):
    """Read OSM way XML data and append way id in route list.."""
    for osmId in top.findall('./result'):
        for key, value in osmId.attrib.iteritems():
            if key == 'osm_type' and value != 'way':
                return 'node'
            else:
                if key == 'osm_id':
                    return value


def osm_way_data(wayID):
    """Obtain OSM way history XML data."""
    OSMUrlStart = 'http://api.openstreetmap.org/api/0.6/way/'
    OSMUrlFinish = '/history'
    OSMUrlFull = r"%s%s%s" % (OSMUrlStart, wayID, OSMUrlFinish)
    OSMRequest = urlopen(OSMUrlFull).read()
    return OSMRequest


def get_data(stalk):
    """Read OSM way history XML data and store the specified value."""
    OSMdataKeyList = ['version', 'timestamp', 'user']
    for OSMdataKey in OSMdataKeyList:

        # Read the last 'child (or changeset)' in XML and return
        # the version value.
        if OSMdataKey == 'version':
            # len()-1, because python numbering starts with 0
            versionCount = stalk[(len(stalk)-1)].attrib[OSMdataKey]

        # Read the last changeset and return the timestamp.
        elif OSMdataKey == 'timestamp':
            timestamp = stalk[(len(stalk)-1)].attrib[OSMdataKey]
        
        # Appends all users to a list and count the users through the
        # unique_users function.
        elif OSMdataKey == 'user':
            stalkCount = 0
            userList = []
            while stalkCount < len(stalk):
                userList.append(stalk[stalkCount].attrib[OSMdataKey])
                stalkCount += 1
            findUniqueUsers = unique_users(userList)
            uniqueUserCount = findUniqueUsers
    getDataList = [versionCount, timestamp, uniqueUserCount]
    return getDataList

def unique_users(userList):
    """Determine a count of unique users from a total list."""
    uniqueUserList = []
    uniqueValues = set(userList)
    uniqueCount = len(uniqueValues)
    return uniqueCount
