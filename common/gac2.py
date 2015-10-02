
from gac import GAC

from copy import deepcopy

import sys

class GAC2(GAC):

    def revise(self, variable, constraint):
        variable_clean = int(variable.index.replace(variable.index[0:1], '').split('-')[0])

        new_domain = deepcopy(variable.domain)
        for domain_variable in variable.domain:
            #print 'current index = ' + variable.index
            #print 'checking if ' + str(domain_variable) + ' is valid'
            #print '----------------------------------------'
            valid_domain = False
            for constraint_variable in constraint.vars:
                if constraint_variable != variable:
                    for d in constraint_variable.domain:
                        if constraint.method([domain_variable, d]):
                            #print 'valid constraint method'
                            valid_domain = True
                            break
                        else:
                            pass
                            #print 'invaid constraint method'
                            #print constraint.method_raw

            if not valid_domain:
                for var in self.variables:
                    if var.index[0:1] == 'c':
                        domain_var_clean = int(var.index.replace(var.index[0:1], '').split('-')[0])
                        if domain_var_clean == domain_variable:
                            #print 'matching against = '
                            #print var.index
                            #print var.domain
                            #print domain_var_clean
                            #print '######'
                            for var_domain in var.domain:
                                if var_domain == variable_clean:
                                    #print 'is valid'
                                    valid_domain = True
                                    break
                            #print 'not valid'
                            #print str(variable_clean) +  ' is not in '
                            #print var.domain


            #            variable_clean = int(var.index.replace(var.index[0:1], '').split('-')[0])
            #
            #            if variable_clean in variable.domain:
            #                valid_domain = True
            #                break
            #
            #            #print variable_clean
            ##            for domain_var in var.domain:
            #                if domain_var in variable.domain:
            #                    valid_domain = True
            #                    break


            if not valid_domain:
                new_domain.remove(domain_variable)
        print '-----------------'
        print variable.index
        print 'Before = '
        print variable.domain
        print 'After = '
        print new_domain
        if variable.domain != new_domain:
            print 'CHANGES'

        #sys.exit()
        variable.domain = new_domain

    def rerun(self, variable):
        for constraint in self.constraints:
            for var in constraint.vars:
                self.queue.append((var, constraint))

        # Run domain filtering
        self.domain_filtering()