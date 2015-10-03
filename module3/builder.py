# -*- coding: utf-8 -*-

from constraint import Constraint
from variable import Variable

import copy
import itertools


class Builder:

    makefunc = None

    def __init__(self):
        pass

    @staticmethod
    def initial_specs(specs):
        initial_specs = []

        # Loop the specs and set the space to one initially
        for i in range(len(specs)):
            if i == 0:
                initial_specs.append([specs[i], 0])
            else:
                initial_specs.append([specs[i], 1])

        # Return the initial specs
        return initial_specs

    @staticmethod
    def specs_combinations(specs, length):
        # Find out how much remaning space we have left
        remaining = length
        for spec in specs:
            remaining -= spec[0] + spec[1]

        # Check if remaining space is 0
        if remaining == 0:
            return [specs]
        else:
            # Calculate the different combinations
            combinations = []
            for i in range(len(specs)):
                for j in range(remaining + 1):
                    new_specs = copy.deepcopy(specs)
                    new_specs[i][1] += j
                    combinations.append(new_specs)

        # Return the combinations
        return combinations

    @staticmethod
    def create_permutations(combinations, length, block_length):
        # Get all the different values from the combinations
        permutation_options = [[] for int in range(len(combinations[0]))]
        for i in range(len(combinations)):
            for j in range(len(combinations[0])):
                # Add the option
                permutation_options[j].append(combinations[i][j][1])

        # Make the permutations unique
        permutation_options_unique = []
        for i in range(len(permutation_options)):
            permutation_options_unique.append(list(set(permutation_options[i])))

        # Use the itertools to create the real permutations
        permutations = list(itertools.product(*permutation_options_unique))

        # Filter out permutations that are too long
        valid_permutations = []
        for permutation in permutations:
            if (sum(permutation) + block_length) <= length:
                valid_permutations.append(permutation)

        return valid_permutations

    @staticmethod
    def permutation_to_domain(blocks, length, permutations):
        domains = []

        # Loop the permutations
        for i in range(len(permutations)):
            # Create empty domain
            domain = [False for bool in range(length)]
            offset = 0

            # Loop over each permutation value
            for j in range(len(permutations[i])):

                # Increase the offset
                offset += permutations[i][j]

                # Handle the length of the block
                for k in range(blocks[j]):
                    domain[offset] = True
                    offset += 1

            # Add domain to domains
            domains.append(domain)

        # Return the calculated domains
        return domains

    @staticmethod
    def build_variables(data):
        variables = []

        index = 0
        for direction in data:
            for i in range(len(direction['specs'])):
                # New instance of variable
                variable = Variable(str(direction['prefix']) + str(i))

                # Get length of block values
                block_length = sum(direction['specs'][i])

                # Stuff we need to do to find the different permutations for this block
                initial_specs = Builder.initial_specs(direction['specs'][i])
                combinations = Builder.specs_combinations(initial_specs, direction['length'])
                permutations = Builder.create_permutations(combinations, direction['length'], block_length)

                # Set the final domain
                variable.domain = Builder.permutation_to_domain(direction['specs'][i], direction['length'],
                                                                permutations)

                # Add variable to list
                variables.append(variable)

                # Increase index value
                index += 1

        return variables

    @staticmethod
    def build_constraints(variables):
        constraints = []

        # Loop all variables
        for i in range(len(variables)):
                # Create new constraint
                constraint = Constraint()
                constraint.method = Builder.makefunc(['n'], 'n[0] == n[1]')

                # Add as constraint
                constraint.vars = [i]

                # Add the other constraints
                for j in range(len(variables)):
                    if j != i and variables[i].index[0:1] != variables[j].index[0:1]:
                        constraint.vars.append(j)

                # Add to constraints
                constraints.append(constraint)

        # Return the list of created constraints
        return constraints
