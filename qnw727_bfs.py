import argparse
from map import Map
from node import Node
import pandas as pd

cities = pd.read_csv('cities.csv', header=None)
cities.columns = ['city', 'x', 'y']

roads = pd.read_csv('roads.csv', header=None)
roads.columns = ['start','end']


map = Map(cities, roads)

# accepting arguments from command line
parse= argparse.ArgumentParser()

parse.add_argument('city_name_1', type=str)
parse.add_argument('city_name_2', type=str)
args = parse.parse_args()

city1 = args.city_name_1
city2 = args.city_name_2


def bfs(start, end):
    start_node = Node(start)

    if start == end:
        return [start]

    parent_child = {}  # index of child returns parent

    frontier = [start_node]
    explored = []

    isDone = False
    while not isDone:
        if not frontier:
            print('Path not found!')
            exit()
        else:
            if frontier[0] == start_node:
                # initialize start node
                node = start_node
                frontier.pop(0)

            else:

                # print(f'{frontier[0].curr_city} has been popped. ')
                temp_node = frontier.pop(0)
                node = Node(temp_node, parent=parent_child[temp_node])

            possible_roads = map.get_roads(node.curr_city) # choose the shallowest
            explored.append(node.curr_city)

            for next_city in possible_roads:
                child = Node(next_city, parent=node)
                parent_child[child] = node
                if child not in frontier and child.curr_city not in explored:
                    if next_city == end:
                        return child.get_path()
                    frontier.append(child)  # put the child in the frontier
                    explored.append(child.curr_city)


route = bfs(city1, city2)
distance = map.road_distance(route)

output_route = ' - '.join(route)
output_route = output_route.replace('_',' ')

# once finished:
print(output_route)  # replace _ with space
print(f'Total Distance - {distance} km')