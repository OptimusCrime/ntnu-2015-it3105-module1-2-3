
from gac import GAC

from copy import deepcopy

import sys

class GAC2(GAC):

    def revise(self, variable, constraint):
        if variable.index == 'r6' or 1 == 1:
            new_domain = []
            print 'test variable = '
            print variable
            print variable.domain
            print ''

            print 'cross index = '
            cross_index = int(variable.index[1:])
            print cross_index
            for domain_variable in variable.domain:
                valid_domain = False
                for constraint_variable in constraint.vars:
                    if constraint_variable != variable and variable.index[0:1] != constraint_variable.index[0:1]:
                        print constraint_variable
                        cross_index_back = int(constraint_variable.index[1:])
                        for d in constraint_variable.domain:

                            if constraint.method([domain_variable[cross_index_back], d[cross_index]]):
                                valid_domain = True
                                break
                        print '---'

                if valid_domain:
                    new_domain.append(domain_variable)
            print 'new domain = '
            print new_domain
            print '------'

            variable.domain = new_domain