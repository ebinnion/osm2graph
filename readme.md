#Problem Statement
This project is the result of a contest from my Spatial Data Mining class at Midwestern State University, taught by Professor Griffin.

Read in an Open Street Map defined file (OSM / XML / Shapefile) for Texas and create a file structure as defined in "File Definitions". Notice how I used the word defined (not similar to). Your input file can be any of the above mentioned file structures, they can even be in a compressed form, or whatever you think MAY speed up your processing time. Pre-Processing will count as part of the processing time. The contest results will be determined by a class vote based on the following criteria:

- Build time, 
- Awesomeness of Pythonic-ness, 
- Correctness (although there will be some leeway for easily correctable misunderstandings due to the rush or ambiguity on my part).

Only one real restriction: your code must be a genuine creation of your group. OF COURSE you can use libraries, but not as the main power behind your solution. I want to see clever, thoughtful, logical solutions. I would like to see pure string parsing (no xml elementree libraries, etc.), but whatever:)

#Osm 2 Graph
This is the project that I turned in after for the contest. It is not perfect, and needs work. Currently, it takes approximately 300 seconds to parse a ~3.45 Gb file and print data to the 3 separate files.

This script is known to break with large file sizes (size > 4 Gb) and the processing time could be cut down significantly. Future iterations of this script should likely include:

- **Threading** - Due to the way OSM files are organized, it would make sense to thread the reading in and processing of the node tags, but not the way tags. Also, I would like to test how fast the script would run if I put all output into a buffer, and used a separate thread to print each file.
- **Database Support** - Due to the large file sizes of OSM files (~28 Gb for the bzipped planet file), this script should likely make use of some type of database so as not to run out of memory. I did test this script with an SQLite database, but run time was approximately 20x longer in my tests, so the idea was scrapped.

#File Definitions

##Nodes.txt

This text file contains the nodes of the road network. The file defines all nodes (basically intersections), with each row representing a single node and containing the following fields seperated by a single space:

    <NodeId> <lat> <long>

Where:

- <NodeId>: An integer value specifying the unique identification number of the node within the road network.
- <lat>: This value specifies the latitudinal location of the node within the road network in degrees.
- <long>: This value specifies the longitudinal location of the node within the road network in degrees.
Example:
    81633740 33.074845 -97.322028

##Edges.txt

This text file contains the "rough" edges of the road network. Each row representing a single edge and contains four values separated by a single space.

    <EdgeId> <from> <to> <cost>

- <EdgeId>: An integer value specifying the unique identification number of the edge within the road network. It is not related in any way to NodeId.
- <from>: This value represents the id of the node that is at the head of the edge. If the edge is defined as (u,v), <from> is u. These node id values correspond to the <NodeId> values in Nodes.txt.
- <to>: This value represents id of the node that is at the tail of the edge. If the edge is defined as (u,v), <to> is v. These node id values correspond to the <NodeId> values in Nodes.txt.
- <cost>: This value defines the actual cost of a vehicle to traverse from one end of the edge to the other end. It is a cost function based on length of the edge and the speed limit on the road segment the edge represents.

Note that the road network graph is a directed graph. The edge that goes from node u to node v has a different <EdgeId> from the edge that goes in the other direction (from node v to node u).

##EdgeGeometry.txt

This text files contains the geometry data of each edge in the road network. The edge geometry makes a best attempt to define the polyline of the actual road that the edge is representing. Each row contains a minimum of eight values, with each value being separated by a caret (^). Each entry defines n different points along the edge by specifying the point’s latitude and longitude values. There will be more than eight values in a single entry if the entry contains longitude/latitude information about more than just the first and last points of the edge. The form of an edge geometry row is:

    <EdgeId>^<Name>^<Type>^<Length>^<Lat_1>^<Lon_1>^...^<Lat_n>^<Lon_n>

- <EdgeId>: An integer value specifying the unique identification number of the edge within the road network. This value will match a single edge defined in the Edges.txt file.
- <Name>: This value describes the real-world name of the road segment that this specific edge represents. If no name is defined, the attribute will contain an empty string.
- <Type>: This value describes the type of road that is represented by the edge. Some common values are:
    - motorway
    - motorwaylink
    - primary
    - primarylink
    - secondary
    - secondarylink
    - tertiary
    - residential
    - livingstreet
    - service
    - trunk
    - trunk_link
    - unclassified
- <Length>: This value is the length, in meters, of the edge.
- <Lat_1>: This value is the latitude of the first point of the edge. 
If the edge is defined as (u,v), <Lat_1> is the latitude value of u.
- <Lon_1>: This value is the longitude of the first point of the edge. 
If the edge is defined as (u,v), <Lon_1> is the longitude value of v.
....<Lat_i><Lon_i>....: The latitude and longitude values for several points between the first and the last points of the edge. These points are optional and the number of optional points varies according to the geometry of the represented edge.
- <Lat_n> : This value is the latitude of the last point of the edge. 
If the edge is defined as (u,v), <Lat_n> is the latitude value of v.
- <Lon_n> : This value is the longitude of the last point of the edge. 
If the edge is defined as (u,v), <Lon_n> is the longitude value of v.