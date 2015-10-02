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

        # The kids states
        self.kids = []

        # Keep track of dirty state (only used for drawing)
        self.dirty = False

    def generate_all_successors(self, astar):
        # Get the size of the board to evaluate if new states are valid or not
        x_min = astar.states[0].id[0]
        x_max = astar.states[0].id[0]
        y_min = astar.states[0].id[1]
        y_max = astar.states[0].id[1]

        for state in astar.states:
            if state.id[0] < x_min:
                x_min = state.id[0]
            if state.id[0] > x_max:
                x_max = state.id[0]
            if state.id[1] < y_min:
                y_min = state.id[1]
            if state.id[1] > y_max:
                y_max = state.id[1]

        # Calculate successor states
        new_states = []

        for state in astar.states:
            if self.id[0] < x_max and state.id[0] == (self.id[0] + 1) and state.id[1] == self.id[1]:
                new_states.append(state)
            if self.id[0] > x_min and state.id[0] == (self.id[0] - 1) and state.id[1] == self.id[1]:
                new_states.append(state)
            if self.id[1] < y_max and state.id[0] == self.id[0] and state.id[1] == (self.id[1] + 1):
                new_states.append(state)
            if self.id[1] > y_min and state.id[0] == self.id[0] and state.id[1] == (self.id[1] - 1):
                new_states.append(state)

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
        for n in astar.states:
            # Check if the current node is the goal state
            if n.type == State.GOAL:
                # Return the calculation
                return math.fabs(self.id[0] - n.id[0]) + math.fabs(self.id[1] - n.id[1]) * 10

        return 0
