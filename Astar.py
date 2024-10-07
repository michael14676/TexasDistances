import pandas as pd
import queue
import argparse

from map import Map
from node import Node

cities = pd.read_csv('cities.csv', header=None)
cities.columns = ['city', 'x', 'y']

roads = pd.read_csv('roads.csv', header=None)
roads.columns = ['start', 'end']

map = Map(cities, roads)

# accepting arguments from command line
parse = argparse.ArgumentParser()

parse.add_argument('city_name_1', type=str)
parse.add_argument('city_name_2', type=str)
args = parse.parse_args()

city1 = args.city_name_1
city2 = args.city_name_2


def f_n(node, destination):
    # takes the current node and destination, and outputs the heuristic f(n):
    g = map.road_distance(node.get_path())  # path from start to node n
    h = map.get_distance(node.curr_city, destination)  # estimated shortest path. straight line distance in this case
    return g + h


def astar(start, end):
    # a star searching algorithm

    start_node = Node(start)

    if start == end:
        return [start]

    frontier = queue.PriorityQueue()
    frontier.put((0, start_node))  # tuple of f(n) and node

    parent_child = {}  # index of child returns parent
    explored = []

    isDone = False
    while not isDone:
        if frontier.empty():
            print('Path not found!')
            exit()
        else:
            if (0, start_node) in frontier.queue:
                # initialize start node
                node = start_node
                frontier.get()

            else:
                temp_node = frontier.get()[1]
                node = Node(temp_node, parent=parent_child[temp_node])
                # print(f'{node.curr_city} has been popped. ')

            possible_roads = map.get_roads(node.curr_city)
            explored.append(node.curr_city)

            for next_city in possible_roads:
                child = Node(next_city, parent=node)
                child.f = f_n(child, end)
                parent_child[child] = node

                if (child.f, child) not in frontier.queue and child.curr_city not in explored:
                    if next_city == end:
                        return child.get_path()
                    frontier.put((child.f, child))  # put the child in the frontier
                    explored.append(child.curr_city)


route = astar(city1, city2)
distance = map.road_distance(route)

output_route = ' - '.join(route)
output_route = output_route.replace('_', ' ')

# once finished:
print(output_route)  # replace _ with space
print(f'Total Distance - {distance} km')
