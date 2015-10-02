#!/usr/bin/python
# -*- coding: utf-8 -*-

from module2.makefunc import makefunc
from module2.constraint import Constraint
from module3.node import Node
from module3.gui import Gui
from module3.builder import Builder

from common.astargac import AStarGAC
from common.printer import Printer
from common.gac2 import GAC2
from common.gacstate import GACState

import os
import glob
import platform


class Module3Runner:

    def __init__(self):
        self.astar_gac = AStarGAC()

        # This method is just used to print the introduction and chose the parser
        self.start()

    def start(self):
        # Print introduction lines
        Module3Runner.print_introduction()

        # Present different parser options
        self.parse_files()

    @staticmethod
    def print_introduction():
        Printer.print_border_top()
        Printer.print_content('IT3105 :: Module 3 :: GAC + A* + Nonogram')
        Printer.print_border_middle()

    def parse_files(self):
        # Set to None to avoid "referenced before assigned" complaint
        input_choice_graph = None

        # Get all boards from directory
        graphs = glob.glob('module3/grams/*.txt')

        # Present different graphs to the user
        while True:
            Printer.print_content('Available nonograms: ')
            Printer.print_border_middle()

            # Print list of boards
            idx = 0
            for b in graphs:
                Printer.print_content('[' + str(idx) + ']: ' + b, align='left')
                idx += 1
            Printer.print_border_bottom()

            # Get the user input
            input_choice_graph = raw_input('[0-' + str(len(graphs) - 1) + ']: ')
            Printer.print_newline()

            # Validate input
            try:
                input_choice_graph = int(input_choice_graph)

                if input_choice_graph < 0 or input_choice_graph >= len(graphs):
                    raise AssertionError('')
                break
            except (AssertionError, ValueError):
                Printer.print_border_top()
                Printer.print_content('Invalid input, try again')
                Printer.print_border_middle()

        # Parse the file the user chose
        self.parse_file(str(graphs[input_choice_graph]))

    def parse_file(self, file_name):
        # Read all lines in the file while stripping the ending newline
        lines = [line.rstrip('\n') for line in open(file_name)]
        rows_and_columns = map(int, lines[0].split(' '))

        # Store board data
        board_data = []

        # Add row specs to board data
        row_specs = []
        for line in lines[1:rows_and_columns[1] + 1]:
            row_specs.append(map(int, line.split(' ')))

        board_data.append({
            'specs': row_specs[::-1],
            'prefix': 'r',
            'length': rows_and_columns[0]
        })

        # Add column specs to board data
        column_specs = []
        for line in lines[rows_and_columns[0] + 2:]:
            column_specs.append(map(int, line.split(' ')))

        board_data.append({
            'specs': column_specs,
            'prefix': 'c',
            'length': rows_and_columns[1]
        })

        # Set references to the Builder class
        Builder.Node = Node
        Builder.Constraint = Constraint
        Builder.makefunc = staticmethod(makefunc)

        # Fix permutations for the initial domains and the constraints
        variables = Builder.build_domains(board_data)
        constraints = Builder.build_constraints(variables)

        # Gac stuff
        gac = GAC2()
        gac.variables = variables
        gac.constraints = constraints

        gac_state = GACState()
        gac_state.gac = gac
        gac_state.type = GACState.START

        self.astar_gac.gac_state = gac_state

        # Begin CSP
        self.astar_gac.start()

        # Run the GUI
        self.run()

    def run(self):
        # Create new instance of GUI
        gui = Gui()

        # Set reference to AStarCSP here
        gui.astar_gac = self.astar_gac

        # Draw the initial drawing
        gui.draw_once()

        # If OS X, swap to TKInter window
        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        # Start the GUI
        gui.after(0, gui.task)

        # Start the event mainloop here
        gui.mainloop()

        # Set the terminal to the frontmost process (expects iTerm to be the chosen terminal)
        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "iTerm" to true' ''')





Module3Runner()