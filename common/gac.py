# -*- coding: utf-8 -*-


class GAC:

    Constraints = []

    def __init__(self):
        self.variables = []
        self.queue = []

    def initialize(self):
        for constraint in GAC.Constraints:
            for var in constraint.vars:
                self.queue.append((var, constraint))

    def domain_filtering(self):
        while len(self.queue) > 0:
            # Pop the node and the constraint
            (x, C) = self.queue.pop(0)

            # Store the old domain here
            old_domain = len(self.variables[x].domain)

            # Run revise
            self.revise(x, C)

            # Check if domain was reduced
            if old_domain != len(self.variables[x].domain):
                for constraint in GAC.Constraints:
                    if x in constraint.vars and constraint != C:
                        for j in constraint.vars:
                            if x != j:
                                self.queue.append((j, constraint))

    def rerun(self, variable):
        # Add to queue
        for constraint in GAC.Constraints:
            if variable in constraint.vars:
                for j in constraint.vars:
                    if variable != j:
                        self.queue.append((j, constraint))

        # Run domain filtering
        self.domain_filtering()

    def check_finished(self):
        for variable in self.variables:
            if len(variable.domain) > 1:
                return False
        return True

    def check_contradictory_state(self):
        for variable in self.variables:
            if len(variable.domain) == 0:
                return True
        return False

    def revise(self, idx, constraint):
        new_domain = []
        for domain_variable in self.variables[idx].domain:
            valid_domain = False
            for constraint_variable in constraint.vars:
                if constraint_variable != idx:
                    for d in self.variables[constraint_variable].domain:
                        if constraint.method([domain_variable, d]):
                            valid_domain = True
                            break

            if valid_domain:
                new_domain.append(domain_variable)

        self.variables[idx].domain = new_domain
