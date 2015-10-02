# -*- coding: utf-8 -*-

import copy


class GACState:

    START = 'S'
    GOAL = 'g'
    BLOCKED = 'x'

    def __init__(self):
        # Link to a gac instance
        self.gac = None

        # For integrating with AStar
        self.type = None
        self.f = 0
        self.g = 0
        self.kids = []
        self.parents = []

    def total_cost(self):
        return 100

    def generate_all_successors(self, astar):
        print 'Running generate all sucessors'
        states = []

        # Find the node with smallest domain that is not 0
        smallest_domain_variable_index = None
        for i in range(len(self.gac.variables)):
            if len(self.gac.variables[i].domain) > 1:
                if smallest_domain_variable_index is None:
                    smallest_domain_variable_index = i

                if len(self.gac.variables[i].domain) < len(self.gac.variables[smallest_domain_variable_index].domain):
                    smallest_domain_variable_index = i

        if smallest_domain_variable_index is None:
            return []
        for domain in self.gac.variables[smallest_domain_variable_index].domain:
            # Deep copy self
            new_gac = copy.deepcopy(self.gac)

            # Force the newly generated state and value to a singleton set
            new_gac.variables[smallest_domain_variable_index].domain = [domain]

            # Valid state, run rerun on the node we just updated
            new_gac.rerun(new_gac.variables[smallest_domain_variable_index])

            # Double check that this state is in fact not invalid
            if not new_gac.check_contradictory_state():
                gac_state = GACState()
                gac_state.gac = new_gac

                # Set the correct type
                if new_gac.check_finished():
                    gac_state.type = GACState.GOAL
                else:
                    gac_state.type = self.type

                gac_state.f = self.f
                gac_state.g = self.g
                self.kids = []
                self.parents = []

                # Append the new state
                states.append(gac_state)
            else:
                print 'fucked sucessor'
        print "Genererte totalt" + str(len(states))

        # Return the actual states
        return states


    def arch_cost(self, node):
        return 10

    def calculate_h(self, astar):
        sum = 0
        for variable in self.gac.variables:
            sum += len(variable.domain) - 1

        return sum
