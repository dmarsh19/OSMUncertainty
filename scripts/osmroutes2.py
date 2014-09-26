"""
This module contains functions for OSMRouteDatav2.0.py,
including API calls and some logic processing
"""

from urllib2 import urlopen


def mapquest_xml(originX, originY, destX, destY, mapquestKey):
    """Calculate a network route from two points."""
    mapquestParts = ((r"http://open.mapquestapi.com/directions/v2/route"
                      "?key=%s&outFormat=xml&unit=m&from=%s,%s&to=%s,"
                      "%s&maxLinkId=15") %
                      (mapquestKey, originX, originY, destX, destY))
    mapquestXMLRequest = urlopen(mapquestParts).read()
    return mapquestXMLRequest

# Working ##############################################################

def find_route_info(root):
    """Read route data and store a list of specified information."""
    for maneuver in root.findall('./route/legs/leg/maneuvers/maneuver'):
        for mapquestDataKey in mapquestDataKeys:

            if mapquestDataKey == 'latlng':
                legCoord = []
                for latlng in root.findall('./route/legs/leg/maneuvers/'
                                           'maneuver/startPoint'):
                    if 
                    for child in latlng:
                        if child.tag == 'lng':
                            lng = child.text
                        elif child.tag == 'lat':
                            lat = child.text
                    latLng = (lat, lng)
                    legCoord.append(latLng)
                return legCoord
    
            elif mapquestDataKey == 'distance':
                for latlng in root.findall('./route/legs/leg/maneuvers/maneuver/distance'):
                    
            elif OSMdataKey == 'user':
                
        # return list of all datakey info at this tab
# End Working ##########################################################


def lat_lng_to_id(lat, lng):
    """Convert road segment coordinates into OpenStreetMap way id."""
    latLngToIdParts = (r"http://open.mapquestapi.com/nominatim/v1/"
                        "reverse?lat=%s&lon=%s") % (lat, lng)
    latLngToIdRequest = urlopen(latLngToIdParts).read()
    return latLngToIdRequest


def find_osm_id(top):
    """Read OSM way data and store way id."""
    osmWayIds = []
    for osmId in top.findall('./result'):
        for key, value in osmId.attrib.iteritems():
            if key == 'osm_type' and value != 'way':
                break  # breaks smallest for loop, moves to next osm_id
            else:
                if key == 'osm_id':
                    osmWayIds.append(value)
    return osmWayIds


def osm_way_data(wayID):
    """Obtain OSM way history XML data."""
    OSMUrlStart = 'http://api.openstreetmap.org/api/0.6/way/'
    OSMUrlFinish = '/history'
    OSMUrlFull = r"%s%s%s" % (OSMUrlStart, wayID, OSMUrlFinish)
    OSMRequest = urlopen(OSMUrlFull).read()
    return OSMRequest


##def osm_changeset_data(changesetID):
##    """Obtain OSM way changeset XML data."""
##    OSMUrl = 'http://api.openstreetmap.org/api/0.6/changeset/'
##    OSMUrlFull = r"%s%s" % (OSMUrl, changesetID)
##    OSMRequest = urlopen(OSMUrlFull).read()
##    return OSMchangesetRequest


def get_data(stalk, OSMdataKey):
    """Read OSM way history XML data and store the indicated value"""
        # Read the last 'child (or changeset)' in XML and return
        # version value
    if OSMdataKey == 'version':
        # len()-1, because python numbering starts with 0
##        versionCount = stalk[(len(stalk)-1)].get(OSMdataKey)
        versionCount = stalk[(len(stalk)-1)].attrib[OSMdataKey]
        return versionCount

    # Read the last changeset and return timestamp
    elif OSMdataKey == 'timestamp':
        return stalk[(len(stalk)-1)].attrib[OSMdataKey]
    
    # Appends all users to a list, count the users through
    # unique_users function
    elif OSMdataKey == 'user':
        stalkCount = 0
        userList = []
        while stalkCount < len(stalk):
            userList.append(stalk[stalkCount].attrib[OSMdataKey])
            stalkCount += 1
        findUniqueUsers = unique_users(userList)
        return findUniqueUsers
    
    # If a new data key is added without specifying customized commands,
    # data will be stored anyway
    else:
        stalkCount = 0
        dataList = []
        while stalkCount < len(stalk):
            dataList.append(stalk[stalkCount].attrib[OSMdataKey])
            stalkCount += 1
        return dataList

def unique_users(userList):
    """Determine a count of unique users from a total list"""
    uniqueUserList = []
    uniqueValues = set(userList)
    uniqueCount = len(uniqueValues)
    for oneValue in uniqueValues:
         uniqueUserList.append([oneValue, userList.count(oneValue)])
    # If needed, the list of unique users and their contribution count
    # can be stored in Python shell for reference
    return uniqueCount  #, uniqueUserList
