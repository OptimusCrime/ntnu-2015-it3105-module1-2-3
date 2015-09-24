# -*- coding: utf-8 -*-

import copy


class CSP():

    def __init__(self):
        self.nodes = []
        self.queue = []
        self.constraints = []

    def initialize(self):
        for constraint in self.constraints:
            for var in constraint.vars:
                self.queue.append((var, constraint))

        #self.queue[0][0].domain = [0]

    def domain_filtering(self):
        while len(self.queue) > 0:
            # Pop the node and the constraint
            (x, C) = self.queue.pop(0)

            # Store the old domain here
            old_domain = len(x.domain)

            # Run revise
            self.revise(x, C)

            # Check if domain was reduced
            if old_domain != len(x.domain):
                for constraint in self.constraints:
                    if x in constraint.vars and constraint != C:
                        for j in constraint.vars:
                            if x != j:
                                self.queue.append((j, constraint))

    def rerun(self, node):
        # Add to queue
        for constraint in self.constraints:
            if node in constraint.vars:
                for j in constraint.vars:
                    if node != j:
                        self.queue.append((j, constraint))

        # Run domain filtering
        self.domain_filtering()

    def check_finished(self):
        for node in self.nodes:
            if len(node.domain) > 1:
                return False
        return True

    def check_contradictory_state(self):
        for node in self.nodes:
            if len(node.domain) == 0:
                return True
        return False

    def revise(self, node, constraint):
        new_domain = []
        for domain_node in node.domain:
            valid_domain = False
            for constraint_node in constraint.vars:
                if constraint_node != node:
                    for d in constraint_node.domain:
                        if constraint.method([domain_node, d]):
                            valid_domain = True
                            break

            if valid_domain:
                new_domain.append(domain_node)

        node.domain = new_domain