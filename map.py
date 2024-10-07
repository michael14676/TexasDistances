import numpy as np
from math import *

# for visualizing graph, not necessary:
import networkx as nx
import matplotlib.pyplot as plt


class Map:
    # creates a graph representing a map using an adjacency matrix
    def __init__(self, cities, roads):
        self.cities = cities
        self.roads = roads
        self.city_names = self.cities['city']

        self.num_cities = len(self.cities['city'])

        # initialize adj matrix
        self.adjacency_matrix = np.zeros((self.num_cities, self.num_cities), dtype=float)

        # add all the roads
        for index, row in self.roads.iterrows():
            self.add_road(row.start, row.end)

    def add_road(self, city1, city2):
        # takes two cities and creates an edge with weight of distance
        i = self.city_names[self.city_names == city1].index[0]
        j = self.city_names[self.city_names == city2].index[0]
        distance = self.get_distance(city1, city2)

        self.adjacency_matrix[i, j] = distance
        self.adjacency_matrix[j, i] = distance  # undirected graph, must go both directions

    def get_coords(self, cityname):
        x = float(self.cities[self.cities['city'] == cityname]['x'].iloc[0])  # latitude
        y = float(self.cities[self.cities['city'] == cityname]['y'].iloc[0])  # longitude
        return x, y

    def get_distance(self, city1, city2):
        # returns haversine distance from 2 pairs of longitude and latitude coordinates

        # in coordinates x is lat, y is lon, in degrees
        lat1 = radians(self.get_coords(city1)[0])
        lon1 = radians(self.get_coords(city1)[1])
        lat2 = radians(self.get_coords(city2)[0])
        lon2 = radians(self.get_coords(city2)[1])
        r = 6371  # radius of the earth in km

        # haversine formula:
        d = 2 * r * asin(sqrt((1 - cos(lat2 - lat1) + cos(lat1) * cos(lat2) * (1 - cos(lon2 - lon1))) / 2))
        return d

    def print_adj_matrix(self):  # for debugging
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if self.adjacency_matrix[i, j] > 0:
                    print(self.city_names[i], self.city_names[j], self.adjacency_matrix[i, j])

    def draw_map(self):
        # visualizing graph
        texas_map = nx.from_numpy_array(self.adjacency_matrix)
        nx.draw(texas_map)
        plt.show()

    def get_roads(self, city):
        # gets the possible roads and their distances, returns in a dictionary
        i = self.city_names[self.city_names == city].index[0]  # gets index of city

        # get the entire list of connections and weights:
        distances = self.adjacency_matrix[i, :]

        # creates a dictionary of possible roads and their distance
        possible_roads = {}
        for i in range(len(distances)):
            if distances[i] > 0.0:
                possible_roads[self.city_names[i]] = distances[i]

        return possible_roads

    def road_distance(self, path):
        # takes a path in form of list in the map and calculates distance
        total_distance = 0
        for i in range(1, len(path)):
            total_distance += self.get_distance(path[i - 1], path[i])
        return total_distance
