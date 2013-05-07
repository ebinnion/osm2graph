"""
Name: Eric Binnion
Program 4
Description:
    Will parse an OSM file to files that can be used to make a graph.
Future Programming Ideas: 
        - I/O is slow. Let's throw all file output into buffers/lists.... then use threads to print. 
            Each print probably doesn't need to be read in order anyways!
            
        - Let's thread the node input, but read the ways without threading.
"""

import sys
import time
import math

startTime = time.time()

# Will get the slug from filename. Ex. - will be texas for texas.osm
fileSlug = sys.argv[1].split('.')[0]
edgesOut = open(fileSlug + '_edges.txt', 'w')
nodesOut = open(fileSlug + '_nodes.txt', 'w')
geomOut = open(fileSlug + '_geometry.txt', 'w')

# Initialize some variables for keep tracking of ways
ndRefList = []
wayFlag = 0
wayType = ''
wayId = ''
wayName = ''
wayType = ''
highwayFlag = 0

# Initialize a map for the nodes
nodes = {}

for line in open(sys.argv[1], "r"):
    # Remove '<', '/>', '>', and '"', strip spaces on each end of string then split on the spaces. Hell yea for python...
    line = line.replace('<', '').replace('/>', '').replace('>', '').replace('"', '').strip().split(' ')

    if line[0] == 'node':
        stringOut = ''

        for part in line:
            # Split each part of the line on the =
            part = part.split('=')

            # Iterate over the string and only pull out the values that are id, lat, or lon
            if part[0] == 'id':
                nodeId = part[1]
            elif part[0] == 'lat':
                lat = part[1]
            elif part[0] == 'lon':
                lon = part[1]
                
        # Let's build a map of nodes
        # Add a used flag and then wait to print until the end ;)
        stringOut = nodeId + ' ' +  lat + ' ' + lon + '\n'
        nodesOut.write(stringOut)

        nodes[nodeId] = (lat,lon)
        
    else:
        if line[0] == 'way':
            # Set a flag so that we know we're in the middle of processing a way
            wayFlag = 1
           
            for part in line:
                
                part = part.strip().split('=')
                if part[0] == 'id':
                    wayId = part[1]

            # Clears out the list
            ndRefList[:] = []

        elif line[0] == '/way':
            # This signals that we have reached the end of a way
            
            # If the way we were processing is of type highway, let's process
            if highwayFlag:
                length = 0
                latLonList = []

                # Build a list of lat lons, then run through and calculate the total distance
                for ref in ndRefList:
                    try:
                        lat,lon = nodes[ref]
                        latLonList.append( ( float(lat),float(lon) ) )
                    except:
                        continue

                i = 0
                while i < (len(latLonList) - 1):
                    lat1, lon1 = latLonList[i]
                    lat2, lon2 = latLonList[i+1]
                    radius = 6371 # km

                    dlat = math.radians(lat2-lat1)
                    dlon = math.radians(lon2-lon1)
                    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                    d = radius * c * 1000 # for meters

                    length = length + d

                    i = i + 1

                # http://wiki.openstreetmap.org/wiki/Key:highway
                if wayType == 'motorway':
                    # A restricted access major divided highway, normally with 2 or more running lanes plus emergency hard shoulder. Equivalent to the Freeway, Autobahn, etc..
                    cost = 0.1
                elif wayType == 'motorway_link':
                    # The link roads (sliproads/ramps) leading to/from a motorway from/to a motorway or lower class highway. Normally with the same motorway restrictions.
                    cost = 0.15
                elif wayType == 'trunk':
                    # Important roads that aren't motorways. Typically maintained by central, not local government. Need not necessarily be a divided highway. In the UK, all green signed A roads are, in OSM, classed as 'trunk'.
                    cost = 0.25
                elif wayType == 'trunk_link':
                    # The link roads (sliproads/ramps) leading to/from a trunk road from/to a trunk road or lower class highway.
                    cost = 0.35
                elif wayType == 'primary':
                    # Administrative classification in the UK, generally linking larger towns.
                    cost = 0.35
                elif wayType == 'primary_link':
                    # The link roads (sliproads/ramps) leading to/from a primary road from/to a primary road or lower class highway.
                    cost = 0.40
                elif wayType == 'secondary':
                    # Administrative classification in the UK, generally linking smaller towns and villages
                    cost = 0.40
                elif wayType == 'seconday_link':
                    # The link roads (sliproads/ramps) leading to/from a secondary road from/to a secondary road or lower class highway.
                    cost = 0.45
                elif wayType == 'tertiary':
                    # A "C" road in the UK. Generally for use on roads wider than 4 metres (13') in width, and for faster/wider minor roads that aren't A or B roads. In the UK, they tend to have dashed lines down the middle, whereas unclassified roads don't.
                    cost = 0.45
                elif wayType == 'tertiary_link':
                    # The link roads (sliproads/ramps) leading to/from a tertiary road from/to a tertiary road or lower class highway.
                    cost = 0.5
                elif wayType == 'living_street':
                    # For living streets, which are residential streets where pedestrians have legal priority over cars, speeds are kept very low and where children are allowed play on the street. Also known as Home Zones in the UK.
                    cost = 0.8
                elif wayType == 'residential':
                    # Roads which are primarily lined with housing, but which are of a lowest classification than tertiary and which are not living streets. Using abutters=residential together with tertiary, secondary etc for more major roads which are lined with housing.
                    cost = 0.8
                elif wayType == 'service':
                    # For access roads to, or within an industrial estate, camp site, business park, car park etc. Can be used in conjunction with service=* to indicate the type of usage and with access=* to indicate who can use it and in what circumstances.
                    cost = 0.8
                elif wayType == 'bus_guideway':
                    # A busway where the vehicle guided by the way (though not a railway) and is not suitable for other traffic. Please note: this is not a normal bus lane, use access=no, psv=yes instead!
                    cost = 1000
                elif wayType == 'raceway':
                    # A course or track for (motor) racing
                    cost = 1000
                elif wayType == 'pedestrian':
                    # For roads used mainly/exclusively for pedestrians in shopping and some residential areas which may allow access by motorised vehicles only for very limited periods of the day. To create a 'square' or 'plaza' create a closed way and tag as pedestrian and also with area=yes.
                    cost = 2
                elif wayType == 'track':
                    # Roads for agricultural or forestry uses etc. Often rough with unpaved/unsealed surfaces. Use tracktype=* for tagging to describe the surface.
                    cost = 2.4
                else:
                    # This is the case for unclassified roads. Assign same cost as residential.
                    cost = 2

                edgeCost = length * cost
                edgeStringOut = wayId + ' ' + ndRefList[0] + ' ' + ndRefList[-1] + ' ' + str(edgeCost) + '\n'
                edgesOut.write(edgeStringOut)
                
                # Converting ft to meters then casting to string
                geomStringOut = wayId + wayName + wayType + ' ' + str(length) 

                for ref in ndRefList:
                    try:
                        lat,lon = nodes[ref]
                        geomStringOut = geomStringOut + ' ' + lat + ' ' + lon
                    except:
                        continue

                geomStringOut.strip()
                geomStringOut = geomStringOut + '\n'

                geomOut.write(geomStringOut)

            # Let's reset all variables
            wayFlag = 0
            wayType = ''
            wayId = ''
            wayName = ''
            wayType = ''
            highwayFlag = 0

        elif line[0] == 'nd' and wayFlag == 1:
            # wayFlag will help us get rid of junk data such as the relation data at the end of the grenada osm file
            for part in line:
                # Split each part of the line on the =
                part = part.replace('/', '').strip().split('=')
                if part[0] == 'ref':
                    ndRefList.append(part[1])

        elif line[0] == 'tag':
            # The highway tag is the primary tag used for any kind of street or way.
            if line[1] == 'k=highway':
                highwayFlag = 1
                try:
                    wayType = ' ' + line[2].split('=')[1]                
                except:
                    continue
            if line[1] == 'k=name':
                try:
                    wayName = line[2].split('=')[1]

                    # This block is to account for names with multiple words
                    for part in line[3:]:
                        wayName = wayName +  ' ' + part
                    wayName.rstrip()

                    # Add a space to the beginning for writing to the file
                    wayName = ' ' + wayName
                except:
                    continue

nodesOut.close()
edgesOut.close()
geomOut.close()

print
print
endTime = time.time()
print 'Execution took ' + str(endTime - startTime) + ' seconds.'