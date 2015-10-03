# -*- coding: utf-8 -*-

from gac import GAC


class GAC2(GAC):

    def revise(self, idx, constraint):
        new_domain = []

        # Get the cross index
        cross_index = int(self.variables[idx].index[1:])

        for domain_variable in self.variables[idx].domain:
            valid_domain = False
            for constraint_variable in constraint.vars:
                if constraint_variable != idx and self.variables[idx].index[0:1] != \
                        self.variables[constraint_variable].index[0:1]:
                    other_cross_index = int(self.variables[constraint_variable].index[1:])

                    # Check if the constraint domain is already reduced
                    if len(self.variables[constraint_variable].domain) == 1:
                        if self.variables[constraint_variable].domain[0][cross_index] == \
                                domain_variable[other_cross_index]:
                            valid_domain = True
                    else:
                        # Matching variable is not reduced, see if we have a union state
                        values_intersection_true = 0
                        values_intersection_false = 0

                        # Loop all the permutations for this crossing constraint and check if either True or False is
                        # used exclusivly
                        for permutation in self.variables[constraint_variable].domain:
                            if permutation[cross_index]:
                                values_intersection_true += 1
                            else:
                                values_intersection_false += 1

                        # Check the values from the check
                        if values_intersection_true == (values_intersection_true + values_intersection_false):
                            if not domain_variable[other_cross_index]:
                                break
                        elif values_intersection_false == (values_intersection_true + values_intersection_false):
                            if domain_variable[other_cross_index]:
                                break

                        # We can't reduce this
                        valid_domain = True

            if valid_domain:
                new_domain.append(domain_variable)

        # Set the new domain
        self.variables[idx].domain = new_domain
