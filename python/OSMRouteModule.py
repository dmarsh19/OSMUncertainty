# Title: OSMRouteModule.py
# Description: Module for OSMRouteData.py
# Inputs: 
# Outputs: 
# Author(s): Derek Marsh
# Edit Date: September 4, 2014
# Version: 1.0
# Compatibility/Requirements: Python 2.7
# Reference: 
# ##########################################################################################################################################
from urllib2 import urlopen

# O-D points to create route in OSM(MapQuest)
def mapquestXML(originX, originY, destX, destY, mapquestKey):
    mapquestParts = "http://open.mapquestapi.com/directions/v2/route?key=%s&outFormat=xml&unit=m&from=%s,%s&to=%s,%s&maxLinkId=15" % (mapquestKey, originX, originY, destX, destY)
    mapquestXMLRequest = urlopen(mapquestParts).read()
    return mapquestXMLRequest

# Parse route XML for coordinates of leg roads
def findLatLng(root):
    legCoord = []
    for latlng in root.findall('./route/legs/leg/maneuvers/maneuver/startPoint'):
        for child in latlng:
            if child.tag == 'lng':
                lng = child.text
            elif child.tag == 'lat':
                lat = child.text
        latLng = (lat, lng)
        legCoord.append(latLng)
    return legCoord

# Waypoint coordinates converted into OSM way IDs
def latLngToId(lat, lng):
    latLngToIdParts = 'http://open.mapquestapi.com/nominatim/v1/reverse?lat=%s&lon=%s' % (lat, lng)
    latLngToIdRequest = urlopen(latLngToIdParts).read()
    return latLngToIdRequest

# Parse way XML to pull out osm_id only
def findOsmId(top):
    osmWayIds = []
    for osmId in top.findall('./result'):
        for key, value in osmId.attrib.iteritems():
            if key == 'osm_type' and value != 'way':
                break # breaks the smallest 'for' loop, moves on to the next osm_id
            else:
                if key == 'osm_id':
                    osmWayIds.append(value)
    return osmWayIds

# Call OpenStreetMap API to obtain history data
def OSMWayData(wayID):
    OSMUrlStart = 'http://api.openstreetmap.org/api/0.6/way/'
    OSMUrlFinish = '/history'
    OSMUrlFull = '%s%s%s' % (OSMUrlStart, wayID, OSMUrlFinish)
    OSMRequest = urlopen(OSMUrlFull).read()
    return OSMRequest

# Call OpenStreetMap API to obtain changeset data
def OSMChangesetData(changesetID):
    OSMUrl = 'http://api.openstreetmap.org/api/0.6/changeset/'
    OSMUrlFull = '%s%s' % (OSMUrl, changesetID)
    OSMRequest = urlopen(OSMUrlFull).read()
    return OSMchangesetRequest

# Parse OSM way history data and return applicable information
def getData(stalk, OSMdataKey):
# Because python numbering starts with 0, go to the last 'child (or changeset)' in XML stalk and return version value
    if OSMdataKey == 'version':
        #versionCount = stalk[(len(stalk)-1)].get(OSMdataKey)
        versionCount = stalk[(len(stalk)-1)].attrib[OSMdataKey]
        return versionCount

    # Find the last changeset and return its timestamp
    elif OSMdataKey == 'timestamp':
        return stalk[(len(stalk)-1)].attrib[OSMdataKey]
    
    # Appends all users to a list, counts the users through unique users function
    elif OSMdataKey == 'user':
        stalkCount = 0
        userList = []
        while stalkCount < len(stalk):
            userList.append(stalk[stalkCount].attrib[OSMdataKey])
            stalkCount += 1
        findUniqueUsers = uniqueUsers(userList)
        return findUniqueUsers
    # If a new data key is added without specifying customized commands, data will be stored anyway
    else:
        stalkCount = 0
        dataList = []
        while stalkCount < len(stalk):
            dataList.append(stalk[stalkCount].attrib[OSMdataKey])
            stalkCount += 1
        return dataList

def uniqueUsers(userList):
    uniqueUserList = []
    uniqueValues = set(userList)
    uniqueCount = len(uniqueValues)
    for oneValue in uniqueValues:
         uniqueUserList.append([oneValue, userList.count(oneValue)])
    return uniqueCount#, uniqueUserList
