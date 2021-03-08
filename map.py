import random, os, argparse
from collections import deque

def addElements(map, elements, num_per_type):
    map_height, map_width = len(map), len(map[0])
    for _ in range(num_per_type):
        for e in elements:
            while(True):
                i, j = random.randint(1, map_height-1), random.randint(1, map_width-1)
                if map[i][j] == " ":
                    map[i][j] = e
                    break
    
def getObjects(map):
    objs = {}
    for i in range(len(map)):
        for j in range(len(map[i])):
            e = map[i][j]
            if e == "A": agent = i,j
            elif e not in " X":
                if e not in objs: objs[e] = []
                objs[e].append((i,j))
    return objs, agent  

def createMap(conf_params, seed, show):
    # configuration parameters
    map_width, map_height, resources, fancy_resources, workstations, num_resource_per_type, num_fancy_resources_per_type, num_workstations_per_type, shelter_locations, tasks = conf_params
    random.seed(seed)
    
    # Creating a new map layout
    map = [["X"]+[" " for _ in range(map_width-2)]+["X"] for _ in range(map_height)]
    map[0] = ["X" for _ in range(map_width)]
    map[-1] = ["X" for _ in range(map_width)]

    # Adding the agent in a corner
    map[map_height//2][map_width//2] = "A"
    agent_i, agent_j = map_height//2, map_width//2

    # Adding the Shelter
    for i,j in shelter_locations:
        map[i][j] = "s"

    # Adding the work stations
    addElements(map, workstations, num_workstations_per_type)
    
    # Adding resources
    addElements(map, resources, num_resource_per_type)
    addElements(map, fancy_resources, num_fancy_resources_per_type)
    
    # Printing the map
    if show:
        # showing the map
        for row in map:
            print("".join(row))
   
if __name__ == '__main__':

    # configuration parameters for creating a map
    map_width  = 21
    map_height = 21
    resources = 'adf'
    fancy_resources = 'gh'
    workstations = 'bce'

    num_resource_per_type = 5
    num_fancy_resources_per_type = 2
    num_workstations_per_type = 2
    shelter_locations = [(i,j) for i in range(8,13) for j in range(11,20)]

    tasks = ["ab", "ac", "de", "db", "fae", "abdc", "acfb", "acfc", "faeg", "acfbh"] 
    conf_params = map_width, map_height, resources, fancy_resources, workstations, num_resource_per_type, num_fancy_resources_per_type, num_workstations_per_type, shelter_locations, tasks

seed = input("Enter a seed value:" )
print('Map computed ...')
createMap(conf_params, seed, show=True)

