# -*- coding: utf-8 -*-

import math


class Node:

    OPEN = 'o'
    BLOCKED = 'x'
    GOAL = 'G'
    START = 'S'

    ARCH_COST_HORIZONTAL = 10
    ARCH_COST_VERTICAL = 14

    def __init__(self, state):
        # The node type
        self.type = Node.OPEN

        # The coordinates
        self.state = state

        # Different scores
        self.h = 0
        self.g = 0

        # The parent nodes
        self.parents = []

        # The kids
        self.kids = []

        # Keep track of dirty nodes (only used for drawing)
        self.dirty = False

    def generate_all_successors(self, astar):
        # Get the size of the board to evaluate if new states are valid or not
        x_min = astar.nodes[0].state[0]
        x_max = astar.nodes[0].state[0]
        y_min = astar.nodes[0].state[1]
        y_max = astar.nodes[0].state[1]

        for node in astar.nodes:
            if node.state[0] < x_min:
                x_min = node.state[0]
            if node.state[0] > x_max:
                x_max = node.state[0]
            if node.state[1] < y_min:
                y_min = node.state[1]
            if node.state[1] > y_max:
                y_max = node.state[1]

        # Calculate successor states
        new_states = []

        for node in astar.nodes:
            if self.state[0] < x_max and node.state[0] == (self.state[0] + 1) and node.state[1] == self.state[1]:
                new_states.append(node)
            if self.state[0] > x_min and node.state[0] == (self.state[0] - 1) and node.state[1] == self.state[1]:
                new_states.append(node)
            if self.state[1] < y_max and node.state[0] == self.state[0] and node.state[1] == (self.state[1] + 1):
                new_states.append(node)
            if self.state[1] > y_min and node.state[0] == self.state[0] and node.state[1] == (self.state[1] - 1):
                new_states.append(node)

        # Return the list of new states
        return new_states

    def __repr__(self):
        return '[' + str(self.state[0]) + ',' + str(self.state[1]) + ']'

    def total_cost(self):
        return self.g + self.h

    def arch_cost(self, node):
        # Check if the two nodes are at the same horizontal or vertical line
        if self.state[0] == node.state[0] or self.state[1] == node.state[1]:
            # Return straight cost
            return Node.ARCH_COST_HORIZONTAL

        # Return the ... other score
        return Node.ARCH_COST_VERTICAL

    def calculate_h(self, astar):
        # Loop all the nodes we have
        for n in astar.nodes:
            # Check if the current node is the goal node
            if n.type == Node.GOAL:
                # Return the calculation
                return math.fabs(self.state[0] - n.state[0]) + math.fabs(self.state[1] - n.state[1]) * 10

        return 0