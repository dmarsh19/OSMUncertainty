# Title: OSMRouteData.py
# Description: Use lat, long to identify road segments on the OSM network and retrieve their update history (MapQuest routing algorithm)
# Inputs: 
# Outputs: 
# Author(s): Derek Marsh
# Edit Date: September 4, 2014
# Version: 1.0
# Compatibility/Requirements: Python 2.7
# Reference: 
# ##########################################################################################################################################
import xml.etree.ElementTree as ET, datetime
# Function Module - Hopefully in the same directory
import OSMRouteModule

beginTime=datetime.datetime.now()
print("begin time: {0}").format(beginTime)

mapquestKey = "Fmjtd%7Cluur210r2h%2Cr5%3Do5-90yxq0"

OSMdataKeyList = ['version', 'timestamp', 'user']

# Test values
originX = "35.2565196067"
originY = "-80.8063941666"
destX = "35.3081159759"
destY = "-80.8701984774"

###############################################################################################################################
# Request MapQuest route XML based on lat, lng
mapquestXMLRoute = OSMRouteModule.mapquestXML(originX, originY, destX, destY, mapquestKey)
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

endTime=datetime.datetime.now()
print("end time: {0}").format(endTime)
runTime=endTime-beginTime
print("run time: {0}").format(runTime)

print('done')
