import sys

"""
Pre-condition: A tuple with stations listed one after another where adjacent
               elements represent the stations we can reach by one-hop
               An empty dictionary that we will add to
Post-condition: A graph represented as a dictionary(key/value pair) with
                key - a single station. Every available station will be a key once
                value - A LIST of stations that can be reached in one hop from key
Intent: Add or update the routes between stations for a given route
        Values in global dictionary stations_reachability are added/updated
Constructs used: Tuple - to represent a route
                 List - To represent the list of stations that can be reached in one hop
                 Dictionary - To store the mapping of station number to list of reachable stations in one-hop
"""
def add_to_graph(route):
    for station in range(len(route)):
        element = route[station]
        if element in stations_reachability:
            can_reach = stations_reachability[element]
        else:
            can_reach = []

        if station == 0:
            if route[1] not in can_reach:
                can_reach.append(route[1])
        elif station == (len(route) - 1):
            if route[len(route) - 2] not in can_reach:
                can_reach.append(route[len(route) - 2])
        else:
            if route[station + 1] not in can_reach:
                can_reach.append(route[station + 1])
            if route[station - 1] not in can_reach:
                can_reach.append(route[station - 1])

        stations_reachability[route[station]] = can_reach

'''
Pre-condition: A string representing a station names
Post-condition: A number which corresponds to the given staton name in the dictionary with mapping between station name and number
                                        or
                -1 if the station name is not found in the mapping
Intent: Check if the station name is known.
        return station number if known or -1 otherwise
Constructs used: Dictionary : Map from station name to number
'''
def Validate_getNum(s_name):
    s_name = s_name.lower()
    if s_name in station_Name_Number:
        s_num = int (station_Name_Number[s_name])
    else:
        s_num = int (-1)
    return s_num

"""
Pre-condition: A graph represented as a dictionary with reachability information for each available station,
               starting station number
               Ending station number
Post-condition: A LIST of stations including the starting and ending station numbers that need to be traversed to reach end from start
Intent: Find the shortest path between start and end in given graph
Constructs used: List - to return the shortest path
                 Dictionary - To represent graph
"""
def find_shortest_path(graph, start, end, path=[]):
    """
    __source__='https://www.python.org/doc/essays/graphs/'
    __author__='Guido van Rossum'
    """

    """ path is n empty list to start with. We add start to it"""
    path = path + [start]
    ''' If start is the same as end, return path which is the list with only start '''
    if start == end:
        return path
    ''' If start is not a key in the graph, then we cannot calculate the path. So return None '''
    if not start in graph:
        return None
    ''' Start with None as shortest path and loop through each directly connected node '''
    shortest = None
    for node in graph[start]:
         ''' If a directly connected node is not in the shortest path, try to recursively find shortest path from this node to end '''
         if node not in path:
             newpath = find_shortest_path(graph, node, end, path)
             if newpath:
                  if not shortest or len(newpath) < len(shortest):
                       shortest = newpath
    ''' Finally return the shortest path which is a list of station numbers '''
    return shortest

''' Initializing dictionaries to store mapping between station names that user provides (and identifies) and station number we will use in the graph and vice-versa '''
station_Number_Name = {}
station_Name_Number = {}

''' Graph in the form of a dictionary '''
stations_reachability = {}

''' The names of all MBTA stations.
    prerequisite: The file below should exist in the same directory as this script '''
file_with_station_names = "mbta_stations.txt"
fh = open(file_with_station_names)

count = 0
for name in fh:
    count = count + 1
    name = name.rstrip()
    name = name.lower()
    station_Number_Name[count] = name

for key in station_Number_Name.keys():
    station_Name_Number[station_Number_Name[key]] = key

''' Train routes for different lines represented as station numbers  '''
train_routes = {
    'red_mattapan': (70, 28, 111, 31, 72, 27, 29, 7, 97, 49, 95, 61, 5, 24, 98, 43, 83, 32, 62, 30, 54, 85, 41, 3),
    'red_braintree': (21, 87, 88, 117, 77, 61, 5, 24, 98, 43, 83, 32, 62, 30, 54, 85, 41, 3 ),
    'orange': (80, 68, 116, 8, 105, 38, 78, 57, 102, 43, 35, 110, 10, 69, 94, 93, 60, 103, 52, 50),
    'blue': (118, 90, 12, 104, 81, 119, 2, 71, 1, 102, 51, 19),
    'green_bc': (83, 20, 6, 40, 59, 63, 14, 17, 16, 18, 101, 84, 9, 82, 55, 53, 4, 113, 115, 107, 36, 34, 99, 15),
    'green_cc':  (78, 57, 51, 83, 20, 6, 40, 59, 63, 100, 56, 64, 101, 39, 106, 22, 46, 114, 109, 42, 45, 37),
    'green_heath': (65, 96, 78, 57, 51, 83, 20, 6, 40, 86, 108, 79, 74, 67, 23, 48, 73, 92, 11, 58),
    'green_riverside': (83, 20, 6, 40, 59, 63, 47, 66, 26, 25, 13, 89, 33, 75, 76, 44, 112, 120, 91)
}

"""Create a graph with information of connectivity from all routes"""
for route in train_routes.keys():
    add_to_graph(train_routes[route])

''' Get the start and destination station names from user. Validate the name entered. If either name is bad, exit '''
start = input("Where to start? ")
start_num = Validate_getNum(start)

if start_num == -1:
    print("Invalid start station name entered. Exiting ...")
    sys.exit(1)

end = input("Where do you want to go? ")
end_num = Validate_getNum(end)
if end_num == -1:
    print("Invalid destination station name entered. Exiting ...")
    sys.exit(1)

"""If the start and destination stations are valid, find and print the list of stations
    forming the shortest path between start and destination including both """
path_list = find_shortest_path(stations_reachability, start_num, end_num)
path=""
for s in range(len(path_list) - 1):
    s_name = station_Number_Name[path_list[s]]
    path = path + s_name + " -> "

path = path + station_Number_Name[path_list[len(path_list) - 1]]
print(path)