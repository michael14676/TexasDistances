class Node:
    # node object represents cities
    def __init__(self, state, parent = None):
        # parent should be a node object that was the last city, state is the current city

        self.f = 0 # only for astar

        self.curr_city = state
        # print('state ',state)
        # self.last_road = action # i think action is not necessary?

        if parent is None: # if the root node
            # self.distance = 0
            self.curr_city = state
            self.parent = None
        else:
            self.parent = parent
            try:
                self.curr_city = state.curr_city
                # print('hope this works ',self.curr_city)
            except AttributeError: # if only given a string for a state
                self.curr_city = state
            self.last_city = self.parent.curr_city
            # self.distance = self.parent.distance + map.road_distance([self.last_city, self.curr_city])

    def get_path(self):
        # call if the current node is the solution, will return the path

        # recursively iterate through parent nodes to get the path? how?
        if self.parent == None:
            # list of self
            path = [self.curr_city]
        else:
            # return concatenated list of parent node with current node
            path = self.parent.get_path() + [self.curr_city]

        return path