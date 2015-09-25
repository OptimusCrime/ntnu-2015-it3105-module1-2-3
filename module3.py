#!/usr/bin/python
# -*- coding: utf-8 -*-

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

print row_specs
print column_specs