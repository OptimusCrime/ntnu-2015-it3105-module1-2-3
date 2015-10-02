# -*- coding: utf-8 -*-

import copy
import itertools

class Builder:

    Node = None
    Constraint = None
    makefunc = None

    @staticmethod
    def max_expand(size, specs):
        used = 0
        for spec in specs:
            used += spec['length'] + spec['space']
        return size - used

    @staticmethod
    def calcolate_row_specs(size, index, specs):
        # Copy the specs
        new_specs = copy.deepcopy(specs)

        # Keep track of all initial combinations
        combination = []

        for i in range(Builder.max_expand(size, new_specs)):
            # Get a copy of the specs
            new_specs = copy.deepcopy(new_specs)

            # Increase the space with one
            new_specs[index]['space'] += 1

            # Add to list
            combination.append(new_specs)

            # Reccurssive call on all other specs
            for j in range(len(specs)):
                if j != index:
                    reccurrsive_row_specs = Builder.calcolate_row_specs(size, j, new_specs)
                    if len(reccurrsive_row_specs) > 0:
                        combination.extend(reccurrsive_row_specs)

        return combination

    @staticmethod
    def combination_to_representation(size, combinations):
        representation = []

        for combination in combinations:
            new_line = [0] * size
            current_index = 0
            for spec in combination:
                current_index += spec['space']
                for j in range( spec['length']):
                    new_line[current_index] = 1
                    current_index += 1
            representation.append(new_line)
        return representation


    @staticmethod
    def calculate_rows(size, specs):
        initial_specs = []
        for i in range(len(specs)):
            if i == 0:
                initial_specs.append({'length': specs[i], 'space': 0})
            else:
                initial_specs.append({'length': specs[i], 'space': 1})

        #print initial_specs
        #print combination_to_representation(size, [initial_specs])

        specs_combinations = copy.deepcopy([initial_specs])
        for i in range(len(initial_specs)):
            #print 'expand = ' + str(i)
            new_row = Builder.calcolate_row_specs(size, i, initial_specs)
            #print new_row
            if len(new_row) > 0:
                specs_combinations.extend(new_row)
        #print ' '
        #print 'Calculated this: '
        specs_representation = Builder.combination_to_representation(size, specs_combinations)
        #for representation in specs_representation:
        #    print representation
        #    print ' '
        return specs_combinations

    #
    # Stuff goes here
    #

    @staticmethod
    def build_domains(data):
        real_nodes = []

        for direction in data:
            for i in range(len(direction['specs'])):
                # Get the total row

                calculated_rows = Builder.calculate_rows(direction['length'], direction['specs'][i])

                #   print calculated_rows
                #print '.---------'
                #print calculated_rows
                #print '-----'

                # Find the number of variables in this row
                variable_nums = len(calculated_rows[0])

                nodes = []
                nodes_length = []
                for x in range(variable_nums):
                    nodes.append(set())
                    nodes_length.append(0)


                # Loop all calculated rows
                for j in range(len(calculated_rows)):

                    #print calculated_rows[j]
                    offset = 0

                    # Loop individual start in the current calculated
                    for k in range(len(calculated_rows[j])):
                        nodes[k].add(offset + calculated_rows[j][k]['space'])
                        nodes_length[k] = calculated_rows[j][k]['length']
                        offset += calculated_rows[j][k]['space'] + calculated_rows[j][k]['length']

                set_to_list = []
                for node in nodes:
                    set_to_list.append(list(node))



                permuations = list(itertools.product(*set_to_list))
                permuations_real = []

                #print 'filtering permutations for = '
                #print permuations

                for perm in permuations:
                    invalid = False
                    for k in range(1, len(perm)):
                        if perm[k - 1] == perm[k] or (perm[k - 1] - 1) == perm[k] or (perm[k - 1] + 1) == perm[k]:
                            invalid = True

                    if not invalid:
                        permuations_real.append(perm)
                    #else:
                       # print 'invalid permuation = '
                        #print perm


                # fuckyeah
                fuckyeah = []
                #print direction['specs'][i]
                #print permuations_real
                for perm in permuations_real:
                    perm_binary = [False] * (direction['length'])
                    #print 'Perm = '
                    for perm_index in range(len(perm)):
                        for k in range(direction['specs'][i][perm_index]):
                            perm_binary[perm[perm_index] + k] = True

                    fuckyeah.append(perm_binary)

                real_node = Builder.Node(str(direction['prefix']) + str(i))
                real_node.domain = copy.deepcopy(fuckyeah)

                real_nodes.append(real_node)

        return real_nodes


    @staticmethod
    def build_constraints(variables):
        constraints = []
        # Create all constraints
        for variable in variables:
            constraint = Builder.Constraint()
            constraint.vars = [variable]
            for var in variables:
                if variable.index[0:1] != var.index[0:1]:
                    constraint.vars.append(var)
            constraint.method = Builder.makefunc(['x'], 'x[0] == x[1]')
            #print constraint.vars
            constraints.append(constraint)

        return constraints