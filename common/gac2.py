
from gac import GAC

from copy import deepcopy

import sys

class GAC2(GAC):

    def revise(self, variable, constraint):
        new_domain = []

        #print variable
        #print variable.domain

        cross_index = int(variable.index[1:])

        for domain_variable in variable.domain:
            valid_domain = False
            for constraint_variable in constraint.vars:
                if constraint_variable != variable and variable.index[0:1] != constraint_variable.index[0:1]:
                    cross_index_back = int(constraint_variable.index[1:])
                    for d in constraint_variable.domain:

                        #print 'cross index back = '
                        #print cross_index_back
                        #print 'domain_variable = '
                        #print domain_variable
                        #print 'cross index = '
                        #print cross_index
                        #print 'd = '
                        #print d
                        if constraint.method([domain_variable[cross_index_back], d[cross_index]]):
                            valid_domain = True
                            break

            if valid_domain:
                new_domain.append(domain_variable)

        #if  variable.domain != new_domain:
        #    print '---------------------------------'
        #    print variable.domain
        #    print new_domain
        #print variable.domain
        ##print 'After = '
        #print new_domain

        variable.domain = new_domain