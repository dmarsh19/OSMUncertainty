#!/usr/bin/env python

"""
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

import argparse
import xml.etree.ElementTree as ET

import osmroutes2

mapquestKey = 'Fmjtd%7Cluur210r2h%2Cr5%3Do5-90yxq0'


def main(input_file, begin_index, end_index):
    """All logic is within this function to provide command-line use."""
    # Opens the input_file and saves indicated data to a list.
    routeCoords = osmroutes2.read_coord_file(input_file, begin_index,
                                             end_index)
    for routeCoord in routeCoords:
        originLng = routeCoord[1]
        originLat = routeCoord[2]
        destLng = routeCoord[3]
        destLat = routeCoord[4]
        # Calculate a network route from two points.
        mapquestXMLRoute = osmroutes2.mapquest_xml(originLat, originLng,
                                                       destLat, destLng,
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


if __name__ == '__main__':
    # Command-line descriptors
    parser = argparse.ArgumentParser(epilog = "'input_file' type must "
                                     "be '*.txt' in the following "
                                     "format:\n------------------------"
                                     "---------------------------------"
                                     "---------------\n<header: index\t"
                                     "OriginLong\tOriginLat\tDestLong\t"
                                     "DestLat>\n1<tab>-80.804455<tab>"
                                     "35.245815<tab>-80.944335<tab>"
                                     "35.226081\n2\t-80.822452\t"
                                     "35.078326\t-80.894568\t35.075842"
                                     "\n...\n\nPath defaults to script "
                                     "directory, but absolute paths can"
                                     " be used to \noverride the "
                                     "default.",
                                     description = __doc__,
                                     formatter_class = argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument("input_file", help = "The filename that "
                        "contains origin and destination coordinates "
                        "used to create routes. See help epilog (below)"
                        " for 'input_file' format and usage.")
    parser.add_argument("begin_index", help = "The index of the "
                        "'input_file' that corresponds to the first "
                        "origin and destination coordinates used for "
                        "route calculation.", type = int)
    parser.add_argument("end_index", help = "The index of the "
                        "'input_file' that corresponds to the last "
                        "origin and destination coordinates used for "
                        "route calculation.", type = int)
    args = parser.parse_args()
    main(args.input_file, args.begin_index, args.end_index)
