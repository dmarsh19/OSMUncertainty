OSM Routing
=============
Using origin and destination points in latitude and longitude format, a
route is calculated using the MapQuest Open service. Each road segment
used for the route is identified based on coordinates. Additional
routing data, including distance, direction, and street name, is
stored. The coordinates are used to identify the corresponding ID in the
OpenStreetMap database. The OSM ID is then used to retrieve update
history data, including number of updates, number of contributors, and
the data of most recent update.

From coordinates to a network route including update frequency.