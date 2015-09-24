# -*- coding: utf-8 -*-

from module1.behaviors.best_first import BestFirst

from astar import AStar
from cspstate import CSPState

import copy

class AStarCSP:

    def __init__(self):
        # Keep track of all the nodes in the system
        self.nodes = []

        # Set node type for AStar
        AStar.NODE = CSPState

        # Reference to AStar and CSP
        self.astar = AStar()
        self.csp_state = None

        # Set behavior
        self.astar.behavior = BestFirst

    def start(self):
        # Run CSP-initialize and CSP-domain-filtering-loop
        self.csp_state.csp.initialize()
        self.csp_state.csp.domain_filtering()

        # Assign the current state to AStar and begin to solve
        self.astar.nodes.append(self.csp_state)
        self.astar.open.append(self.csp_state)

        # Check if we are finished or if the current state is invalid
        if self.csp_state.csp.check_finished() or self.csp_state.csp.check_contradictory_state():
            if self.csp_state.csp.check_finished:
                return True
            return False

    def run(self):
        # Do one step in the agenda loop
        finished = self.astar.agenda_loop()

        # Update the CSP state
        self.csp_state = self.astar.closed[-1]

        # Return the result from the agenda loop
        return finished
