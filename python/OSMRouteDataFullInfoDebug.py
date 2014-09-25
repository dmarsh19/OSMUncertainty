# Title: OSMRouteDataFullInfoDebug.py
# Description: Use lat, long to identify road segments on the OSM network and retrieve their update history (MapQuest routing algorithm)
# Inputs: 
# Outputs: 
# Author(s): Derek Marsh
# Edit Date: September 4, 2014
# Version: 2.0 (v1.0 OSMRouteIdsWorking.py)
# Compatibility/Requirements: Python 2.7
# Reference: 
# ##########################################################################################################################################
import xml.etree.ElementTree as ET, datetime
# XML pretty printing
import xml.dom.minidom as MD
# Function Module - Hopefully in the same directory
import OSMRouteModule

mapquestKey = "Fmjtd%7Cluur210r2h%2Cr5%3Do5-90yxq0"

dataKeyList = ['version', 'timestamp', 'user']

# Test values
originX = "35.2585196067"
originY = "-80.8063941666"
destX = "35.3081159759"
destY = "-80.8701984774"

# Debug: Print statements for all steps ################################################################################

# (1)
# MapQuest Route XML pretty printing(using miniDOM)
mapquestXMLRoute = OSMRouteModule.mapquestXML(originX, originY, destX, destY, mapquestKey)
trunk = MD.parseString(mapquestXMLRoute)
prettyTrunk = trunk.toprettyxml()
print prettyTrunk
##### (2)
##### MapQuest way XML info pretty printing
####root = ET.fromstring(mapquestXMLRoute)
####legCoord = findRouteInfo(root)
####for leg in legCoord:
####    wayId = latLngToId(leg[0], leg[1])
####    base = MD.parseString(wayId)
####    prettyBase = base.toprettyxml()
####    print prettyBase
##### (3)
##### Mapquest way history XML info
####    top = ET.fromstring(wayId)
####    osmRouteIds = findOsmId(top)
####    for osmId in osmRouteIds:
####        OSMWayResults = OSMWayData(osmId)
####        print OSMWayResults
####        print osmId
##### (4)
##### Parse way history for select info
####        stalk = ET.fromstring(OSMWayResults)
