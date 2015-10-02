#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy

from module2.makefunc import makefunc
from module2.constraint import Constraint
from module3.node import Node

from common.astargac import AStarGAC
from common.gac2 import GAC2
from common.gacstate import GACState

# Read all lines in the file while stripping the ending newline
lines = [line.rstrip('\n') for line in open('module3/grams/example.txt')]
rows_and_columns = map(int, lines[0].split(' '))

# Get row specs
row_specs = []
for line in lines[1:rows_and_columns[1] + 1]:
    row_specs.append(map(int, line.split(' ')))

# Get column specs
column_specs = []
for line in lines[rows_and_columns[0] + 2:]:
    column_specs.append(map(int, line.split(' ')))

def row_has_space(size, specs):
    return row_max_expand(size, specs) >= size

def row_max_expand(size, specs):
    used = 0
    for spec in specs:
        used += spec['length'] + spec['space']
    return size - used

def calcolate_row_specs(size, index, specs):
    new_specs = copy.deepcopy(specs)

    combination = []

    for i in range(row_max_expand(size, new_specs)):
        # Get a copy of the specs
        new_specs = copy.deepcopy(new_specs)

        # Increase the space with one
        new_specs[index]['space'] += 1

        # Add to list
        combination.append(new_specs)

        # Reccurssive call on all other specs
        for j in range(len(specs)):
            if j != index:
                reccurrsive_row_specs = calcolate_row_specs(size, j, new_specs)
                if len(reccurrsive_row_specs) > 0:
                    combination.extend(reccurrsive_row_specs)

    return combination


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


# Trying to calculate rows
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
        new_row = calcolate_row_specs(size, i, initial_specs)
        #print new_row
        if len(new_row) > 0:
            specs_combinations.extend(new_row)
    #print ' '
    #print 'Calculated this: '
    specs_representation = combination_to_representation(size, specs_combinations)
    #for representation in specs_representation:
    #    print representation
    #    print ' '
    return specs_combinations

#
# Stuff goes here
#

print row_specs
row_specs = row_specs[::-1]
print row_specs

nodes_real = []
constraints_real = []
for i in range(len(row_specs)):
    # Get the total row
    calculated_rows = calculate_rows(rows_and_columns[0], row_specs[i])
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
    print 'row sets'
    print nodes
    print '-------------'
    for node_index in range(len(nodes)):
        node = Node('r' + str(i) + '-' + str(node_index))
        node.domain = list(nodes[node_index])
        node.length = nodes_length[node_index]

        constraint = Constraint()


        if node_index > 0:
            constraint.vars = [nodes_real[-1], node]
            constraint.method = makefunc(['x'], 'x[1] > x[0] + ' + str(nodes_length[node_index]))
        else:
            constraint.vars = [node]
            constraint.method = makefunc(['x'], 'True')


            constraints_real.append(constraint)

        nodes_real.append(node)
for i in range(len(column_specs)):
    # Get the total row
    calculated_rows = calculate_rows(rows_and_columns[1], column_specs[i])
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

    for node_index in range(len(nodes)):
        node = Node('c' + str(i) + '-' + str(node_index))
        node.domain = list(nodes[node_index])

        if node_index > 0:
            constraint = Constraint()
            constraint.vars = [nodes_real[-1], node]

            constraint.method = makefunc(['x'], 'x[1] > x[0] + ' + str(nodes_length[node_index]))
            constraint.method_raw = 'x[1] > x[0] + ' + str(nodes_length[node_index])

            constraints_real.append(constraint)

        nodes_real.append(node)


for node in nodes_real:
    print node
    print node.domain


print 'constraints: '
for constraint in constraints_real:
    print constraint.vars
print '----'

def print_state(astar_gac):
    global rows_and_columns
    print_nodes = []
    for i in range(rows_and_columns[1]):
        print_nodes_inner = []
        for j in range(rows_and_columns[0]):
            print_nodes_inner.append('-')
        print_nodes.append(print_nodes_inner)

    for node in astar_gac.gac_state.gac.variables:
        if node.index[0:1] == 'r':
            print node.index
            print node.domain
            if len(node.domain) > 0:
                node_index = int(node.index[1:].split('-')[0])
                for node_completes in range(node.domain[0], node.domain[0] + node.length):
                    print_nodes[node_index][node_completes] = 'x'

    for line in (print_nodes):
        print line

# Gac stuff
gac = GAC2()
gac.variables = nodes_real
gac.constraints = constraints_real

gac_state = GACState()
gac_state.gac = gac
gac_state.type = GACState.START

astar_gac = AStarGAC()
astar_gac.gac_state = gac_state
astar_gac.start()

num = 0
astar_gac.run()
print_state(astar_gac)
#astar_gac.run()
#print_state(astar_gac)
#astar_gac.run()
#print_state(astar_gac)
'''while True:
    if astar_gac.run():
        break
    else:
        print_state(astar_gac)
'''

#for var in astar_gac.gac_state.gac.variables:
#    print var
#    print var.domain
