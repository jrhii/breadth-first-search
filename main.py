# File: main.py
# Author: James Harter
# Purpose: Demonstrate a breadth first search.
# Usage: A corresponding json file, mapinfo.json, must be included.  It should
#   have the following structure: {
#       "<INT>": {
#           "name": <STRING>,
#           "neighbors": [
#               <INT>
#           ]
#       }
#   }

from classes import NetworkNode, OneWayTreeNode
from collections import deque
import json
import sys

# I have chosen to organize the cities by a key to allow for the potential of duplicate city names
START_KEY = 2
GOAL_KEY = 3

# Here is our BTS funciton.  It is generic, and not specific to our Romanian Map problem.
# As long as the initialNode has a key and a list of connected nodes ("key" and "links" respectively), it functions.
# Note: under its current version it also needs a property named "value" and that property must be a string,
# but that is only for demonstration purposes of printing information, and can be removed
def breadthFirstSearch(initialNode, goalNodeKey):
    exploredNodes = []
    searchQueue = deque([initialNode])
    # dictionary, where each entry is a OneWayTreeNode that you can route to the initialNode
    pathHistory = {
        str(initialNode.key): OneWayTreeNode(initialNode.key, initialNode.value)
    }

    # iterate through queue
    while len(searchQueue) > 0:
        currentNode = searchQueue.popleft()
        # check if we are at goal state, and exit loop if we are
        if currentNode.key == goalNodeKey:
            break

        # explore neighbor nodes
        for link in currentNode.links:
            isExplored = False

            # check that we haven't already explored this node
            if link.key in exploredNodes:
                isExplored = True

            # if we haven't explored this not, add it to the queue and the path history
            if not isExplored:
                pathHistory[str(link.key)] = OneWayTreeNode(
                    link.key, link.value, pathHistory[str(currentNode.key)])
                searchQueue.append(link)

    # at this point, we have either exited the above loop after finding our goal,
    # or searched every possible node and not found our goal
    # if we have found our goal, the goalNodeKey will be a key in the pathHistory
    if str(goalNodeKey) in pathHistory:
        pathTree = pathHistory[str(goalNodeKey)]
        bestPath = deque([pathTree])
        pathCost = 0

        # We now just need to navigate upward to root to create our path
        while pathTree.parent != None:
            pathCost = pathCost + 1
            pathTree = pathTree.parent
            bestPath.appendleft(pathTree)

        # and print out the information
        print("The following shortest path was found at the cost of " +
              str(pathCost) + ":")
        for node in bestPath:
            print(str(node.key) + ":" + node.value)
    else:
        print("No path to goal was found")

# this function is used to convert a dictionary built from JSON info to a network of linked nodes


def buildMap(mapInfo):
    cities = []

    # Build Node list of all cities
    for key, city in mapInfo.items():
        # validate to ensure mapInfo is valid
        if "name" not in city:
            sys.exit("Value 'name' missing from key '" +
                     key + "' in mapinfo, please correct!")
        if "name" not in city:
            sys.exit("Value 'neighbors' missing from key '" +
                     key + "' in mapinfo, please correct!")

        cities.append(NetworkNode(int(key), city["name"]))

    # catalogue all neighbors for each city
    for cityIndex, cityItem in enumerate(mapInfo.items()):
        city = cityItem[1]
        for neighborKey in city["neighbors"]:
            # find neighbor node in list
            neighborCityIndex = cities.index(neighborKey)
            neighborCity = cities[neighborCityIndex]

            # add neighbor node to this city's list of neighbors
            cities[cityIndex].links.append(neighborCity)

    # return first node
    return cities


# grab the map file
with open('mapinfo.json') as rawMapInfo:
    mapInfo = json.load(rawMapInfo)

# build it into a network
areaMap = buildMap(mapInfo)
startCity = areaMap[areaMap.index(START_KEY)]

# run our BTS
breadthFirstSearch(startCity, GOAL_KEY)