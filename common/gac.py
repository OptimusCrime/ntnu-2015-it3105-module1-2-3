# -*- coding: utf-8 -*-

import inspect

class GAC:

    def __init__(self):
        self.variables = []
        self.queue = []
        self.constraints = []

    def initialize(self):
        for constraint in self.constraints:
            for var in constraint.vars:
                self.queue.append((var, constraint))

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

    def rerun(self, variable):
        # Add to queue
        for constraint in self.constraints:
            if variable in constraint.vars:
                for j in constraint.vars:
                    if variable != j:
                        self.queue.append((j, constraint))

        # Run domain filtering
        self.domain_filtering()

    def check_finished(self):
        print 'check finished goes here'
        for variable in self.variables:
            print len(variable.domain)
            if len(variable.domain) > 1:
                return False
        return True

    def check_contradictory_state(self):
        for variable in self.variables:
            if len(variable.domain) == 0:
                return True
        return False

    def revise(self, variable, constraint):
        new_domain = []
        for domain_variable in variable.domain:
            valid_domain = False
            for constraint_variable in constraint.vars:
                if constraint_variable != variable:
                    for d in constraint_variable.domain:
                        if constraint.method([domain_variable, d]):
                            valid_domain = True
                            break

            if valid_domain:
                new_domain.append(domain_variable)

        variable.domain = new_domain
