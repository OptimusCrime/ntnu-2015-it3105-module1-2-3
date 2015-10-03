# -*- coding: utf-8 -*-

import math


class State:

    OPEN = 'o'
    BLOCKED = 'x'
    GOAL = 'G'
    START = 'S'

    ARCH_COST_HORIZONTAL = 10
    ARCH_COST_VERTICAL = 14

    def __init__(self, id):
        # The node type
        self.type = State.OPEN

        # The coordinates
        self.id = id

        # Different scores
        self.h = 0
        self.g = 0

        # The parent states
        self.parents = []

        # The children states
        self.children = []

        # Keep track of dirty state (only used for drawing)
        self.dirty = False

    def generate_all_successors(self, astar):
        # Get the size of the board to evaluate if new states are valid or not
        x_min = astar.states[astar.states.keys()[0]].id[0]
        x_max = astar.states[astar.states.keys()[0]].id[0]
        y_min = astar.states[astar.states.keys()[0]].id[1]
        y_max = astar.states[astar.states.keys()[0]].id[1]

        for key, value in astar.states.iteritems():
            if value.id[0] < x_min:
                x_min = value.id[0]
            if value.id[0] > x_max:
                x_max = value.id[0]
            if value.id[1] < y_min:
                y_min = value.id[1]
            if value.id[1] > y_max:
                y_max = value.id[1]

        # Calculate successor states
        new_states = []

        if self.id[0] + 1 <= x_max:
            new_states.append(State((self.id[0] + 1, self.id[1])))
        if self.id[0] - 1 >= x_min:
            new_states.append(State((self.id[0] - 1, self.id[1])))
        if self.id[1] + 1 <= y_max:
            new_states.append(State((self.id[0], self.id[1] + 1)))
        if self.id[1] - 1 >= y_min:
            new_states.append(State((self.id[0], self.id[1] - 1)))

        # Return the list of new states
        return new_states

    def __repr__(self):
        return '[' + str(self.id[0]) + ',' + str(self.id[1]) + ']'

    def total_cost(self):
        return self.g + self.h

    def arch_cost(self, node):
        # Check if the two nodes are at the same horizontal or vertical line
        if self.id[0] == node.id[0] or self.id[1] == node.id[1]:
            # Return straight cost
            return State.ARCH_COST_HORIZONTAL

        # Return the ... other score
        return State.ARCH_COST_VERTICAL

    def calculate_h(self, astar):
        # Loop all the nodes we have
        for key, value in astar.states.iteritems():
            # Check if the current node is the goal state
            if value.type == State.GOAL:
                # Return the calculation
                return math.fabs(self.id[0] - value.id[0]) + math.fabs(self.id[1] - value.id[1]) * 10

        return 0

    def get_hash(self):
        return State.hash(self.id)

    @staticmethod
    def hash(key):
        return str(key[0]) + '-' + str(key[1])

    def __lt__(self, compare):
        # Compare cost
        if self.total_cost() < compare.total_cost():
            return True
        elif self.total_cost() > compare.total_cost():
            return False

        # Compare h
        if self.h > compare.h:
            return False
        else:
            return True
