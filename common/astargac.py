# -*- coding: utf-8 -*-

from module1.behaviors.best_first import BestFirst

from astar import AStar
from gacstate import GACState


class AStarGAC:

    def __init__(self):
        # Keep track of all the nodes in the system
        self.nodes = []

        # Set node type for AStar
        AStar.State = GACState

        # Reference to AStar and CSP
        self.astar = AStar()
        self.gac_state = None

        # Set behavior
        self.astar.behavior = BestFirst

    def start(self):
        # Run CSP-initialize and CSP-domain-filtering-loop
        self.gac_state.gac.initialize()
        self.gac_state.gac.domain_filtering()

        # Assign the current state to AStar and begin to solve
        self.astar.states[self.gac_state.get_hash()] = self.gac_state
        self.astar.open.append(self.gac_state)

        # Check if we are finished or if the current state is invalid
        if self.gac_state.gac.check_finished() or self.gac_state.gac.check_contradictory_state():
            if self.gac_state.gac.check_finished():
                return True
            return False

    def run(self):
        if self.gac_state.gac.check_finished():
            return True

        # Do one step in the agenda loop
        finished = self.astar.agenda_loop()

        # Update the CSP state
        self.gac_state = self.astar.closed[-1]

        # Return the result from the agenda loop
        return finished
