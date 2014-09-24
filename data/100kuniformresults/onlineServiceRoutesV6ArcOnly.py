# Title: onlineServiceRoutesV6.py
# Description: Find O-D distances and travel times using ArcGIS Online, Google Maps and OpenStreet Maps(MapQuest algorithm)
# Inputs: Lat-long text file as a single list of origins and destinations
# Outputs: .txt file
# Author(s): Derek Marsh
# Edit Date: May 30, 2014
# Version: 6.0
# Compatibility/Requirements: Python 2.7
# Reference: Google Maps limited to 2,500 routes a day
#            ArcGIS Online and MapQuest algorithm require token/key
#            https://developers.arcgis.com/en/
#            https://www.arcgis.com/sharing/oauth2/token?client_id=<your client ID>&grant_type=client_credentials&client_secret=<your client secret>&f=pjson
#            http://developer.mapquest.com/web/products/open/directions-service
#
#            Run script within same file as input file; output file will be written within same file
# ##########################################################################################################################################
import urllib2, simplejson, datetime, os, time
from urllib2 import urlopen

now=datetime.datetime.now()
print ("beginning time: {0}").format(now)

# #################################################################################################
# Variables

# Specify which lines of the OD Matrix to run for this iteration (should total 2,500)
beginLine = 70186
endLine = 79999

# File names and sleep time should not need to be changed; out file name will update based on begin line and end line values
inTextFileName = "100kuniform.txt"
outFileName = "100kuniformresultsarconly" + str(beginLine) + "-" + str(endLine) + ".txt"

sleepTime = .3 # in seconds

# ################################################################################################
# API functions

def arcOutput(originLat, originLng, destinationLat, destinationLng, token):
    arcApi = "http://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?token="
    stopsFormat = "&stops="
    outputFormat = "&f=json"
    arcOrigin = "%s,%s" % (originLng, originLat)
    arcDestination = "%s,%s" % (destinationLng, destinationLat)
    arcParts = arcApi+token+stopsFormat+arcOrigin+';'+arcDestination+outputFormat
    arcRequest = urlopen(arcParts)
    arcResults = simplejson.load(arcRequest)
    for routes in arcResults['routes']['features']:
        for attributes, values in routes['attributes'].iteritems():
            if attributes == 'Total_Miles':
                distAttributes = attributes
                distValues = values
            if attributes == 'Total_TravelTime':
                return "%s\t%s" % (distValues, values)

####def googleOutput(originLat, originLng, destinationLat, destinationLng):
####    googleapi = 'http://maps.googleapis.com/maps/api/directions/json'
####    sensor = 'sensor=false'
####    mode = 'mode=driving'
####    googleOrigin = "origin=%s,%s" % (originLat, originLng)
####    googleDestination = "destination=%s,%s" % (destinationLat, destinationLng)
####    parts_driving = [googleOrigin,googleDestination,sensor,mode]
####    driving_query = '&'.join(parts_driving)
####    url_driving = '%s?%s' % (googleapi, driving_query)
####    request_driving = urlopen(url_driving)
####    results_driving = simplejson.load(request_driving)
####    for route in results_driving['routes']:
####        for leg in route['legs']:
####            try:
####                distance_driving = leg['distance']['text']
####                duration_driving = leg['duration']['text']
####                return "%s\t%s" % (distance_driving,duration_driving)
####            except KeyError:
####                return "Error\tError"
####
####def mapquestOutput(originLat, originLng, destinationLat, destinationLng, mapquestKey):
####    mapquestParts = "http://open.mapquestapi.com/directions/v2/route?key=%s&outFormat=json&unit=m&from=%s,%s&to=%s,%s" %(mapquestKey, originLat, originLng, destinationLat, destinationLng)
####    mapquestRequest = urlopen(mapquestParts)
####    mapquestResults = simplejson.load(mapquestRequest)
####    for key, number in mapquestResults['route'].iteritems():
####        if key == 'distance':
####            distKey = key
####            distNumber = number
####        if key == 'time':
####            return "%s\t%s" % (distNumber, float(float(number)/60))
####
##### ################################################################################################
##### Authentication
####
####mapquestKey = "Fmjtd%7Cluur210r2h%2Cr5%3Do5-90yxq0"

clientId = "3iJDwTlM2RdCzrsx"
clientSecret = "8a1d9a923b474e80bf52bb80cb73528b"

arcAuth = "https://www.arcgis.com/sharing/oauth2/token?client_id=%s&grant_type=client_credentials&client_secret=%s&f=pjson" % (clientId, clientSecret)
arcAuthRequest = urlopen(arcAuth)
arcAuthResults = simplejson.load(arcAuthRequest)

for key, value in arcAuthResults.iteritems():
    if key == 'access_token':
	    token = value

# ################################################################################################
# Open output file and write header
# Open and read text files to list, Run O-D for each pair, output to file

cwd = os.getcwd()
outTextFile = "\\".join([str(cwd), outFileName])
outFile = open(outTextFile, 'w')
outFile.write("ODIndex\toriginLat\toriginLng\tdestinationLat\tdestinationLng\tArcGISMile\tArcGISMin\n") ##
    
inTextFile = "\\".join([str(cwd), inTextFileName])

pointList = []
pointFile = open(inTextFile, "r")
pointData = pointFile.readlines()
pointFile.close()
for point in pointData[beginLine:endLine+1]:
    pointData2 = point.strip("\n").split("\t")
    pointList.append(pointData2)

print("OD count: {0}\n").format(len(pointList))

runOD = 0
while runOD in range(len(pointList)):
    ODIndex = pointList[runOD][0]
    originLat = pointList[runOD][2] 
    originLng = pointList[runOD][1]
    destinationLat = pointList[runOD][4]
    destinationLng = pointList[runOD][3]
##    googleRoute = googleOutput(originLat, originLng, destinationLat, destinationLng)
    arcRoute = arcOutput(originLat, originLng, destinationLat, destinationLng, token)
##    mapquestRoute = mapquestOutput(originLat, originLng, destinationLat, destinationLng, mapquestKey)
    output = [ODIndex, originLat, originLng, destinationLat, destinationLng, arcRoute] ##
    outputFormat = '\t'.join(output)
    outputFormat = outputFormat + "\n"
    outFile.write(outputFormat)
    print("O-D completed: {0}").format(runOD+1)
    runOD += 1
    time.sleep(sleepTime)

outFile.close()
now1=datetime.datetime.now()
print("ending time: {0}").format(now1)
timeCost=now1-now
print("total run time: {0}").format(timeCost)

print('done')
