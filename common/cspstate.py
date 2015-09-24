# -*- coding: utf-8 -*-

import copy


class CSPState:

    START = 'S'
    GOAL = 'g'
    BLOCKED = 'x'

    def __init__(self):
        # Link to a csp instance
        self.csp = None

        # For integrating with AStar
        self.type = None
        self.f = 0
        self.g = 0
        self.kids = []
        self.parents = []


    def total_cost(self):
        return 100

    def generate_all_successors(self, astar):
        states = []

        # Find the node with smallest domain that is not 0
        smallest_domain_node_index = None
        for i in range(len(self.csp.nodes)):
            if len(self.csp.nodes[i].domain) > 1:
                if smallest_domain_node_index is None:
                    smallest_domain_node_index = i

                if len(self.csp.nodes[i].domain) < len(self.csp.nodes[smallest_domain_node_index].domain):
                    smallest_domain_node_index = i

        if smallest_domain_node_index is None:
            return []

        for domain in self.csp.nodes[smallest_domain_node_index].domain:
            # Deep copy self
            new_csp = copy.deepcopy(self.csp)

            # Force the newly generated state and value to a singleton set
            new_csp.nodes[smallest_domain_node_index].domain = [domain]

            # Valid state, run reun on the node we just updated
            new_csp.rerun(new_csp.nodes[smallest_domain_node_index])

            # Double check that this state is in fact not invalid
            if not new_csp.check_contradictory_state():
                csp_state = CSPState()
                csp_state.csp = new_csp

                # Set the correct type
                if new_csp.check_finished():
                    csp_state.type = CSPState.GOAL
                else:
                    csp_state.type = self.type

                csp_state.f = self.f
                csp_state.g = self.g
                self.kids = []
                self.parents = []

                # Append the new state
                states.append(csp_state)

        # Return the actual states
        return states


    def arch_cost(self, node):
        return 10

    def calculate_h(self, astar):
        sum = 0
        for node in self.csp.nodes:
            sum += len(node.domain) - 1

        return sum
