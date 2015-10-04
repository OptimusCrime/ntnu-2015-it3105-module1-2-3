#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.astargac import AStarGAC
from common.gac import GAC
from common.gacstate import GACState
from common.printer import Printer
from common.makefunc import makefunc

from module2.constraint import Constraint
from module2.gui import Gui
from module2.variable import Variable

import os
import glob
import platform

class Module2Runner:

    def __init__(self):
        self.astar_gac = AStarGAC()

        # This method is just used to print the introduction and chose the parser
        self.start()

    def start(self):
        # Print introduction lines
        Module2Runner.print_introduction()

        # Present different parser options
        self.parse_files()

    @staticmethod
    def print_introduction():
        Printer.print_border_top()
        Printer.print_content('IT3105 :: Module 2 :: GAC + A*')
        Printer.print_border_middle()

    def parse_files(self):
        # Set to None to avoid "referenced before assigned" complaint
        input_choice_graph = None
        input_choice_k = None

        # Get all boards from directory
        graphs = glob.glob('module2/graphs/*.txt')

        # Present different graphs to the user
        while True:
            Printer.print_content('Available graphs: ')
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

        # Get suggested K value for this graph
        graph_suggested_k = None
        graph_suggested_k_temp = graphs[input_choice_graph].split('.')[0].split('-')[-1]
        if 'k' in graph_suggested_k_temp:
            graph_suggested_k = int(graph_suggested_k_temp.replace('k', ''))

        # Get the K value
        Printer.print_border_top()
        while True:
            if graph_suggested_k is not None:
                Printer.print_content('Set K value for this graph, suggested value is ' + str(graph_suggested_k))
            else:
                Printer.print_content('Set K value for this graph')

            Printer.print_border_bottom()

            # Get the user input
            input_choice_k = raw_input('[4-9]: ')
            Printer.print_newline()

            # Validate input
            try:
                input_choice_k = int(input_choice_k)

                if input_choice_k < 4 or input_choice_k > 9:
                    raise AssertionError('')
                break
            except (AssertionError, ValueError):
                Printer.print_border_top()
                Printer.print_content('Invalid input, try again')
                Printer.print_border_middle()

        # Parse the file the user chose
        self.parse_file(str(graphs[input_choice_graph]), input_choice_k)

    def parse_file(self, file_name, k_value):
        gac = GAC()

        # Read all lines in the file while stripping the ending newline
        lines = [line.rstrip('\n') for line in open(file_name)]
        vertices_and_edges = map(int, lines[0].split(' '))

        # Create vertices
        for i in range(1, vertices_and_edges[0] + 1):
            # Get the state
            state = map(float, lines[i].split(' '))

            # Init new Node and set the correct values
            variable = Variable(i)
            variable.state = (state[1], state[2])
            variable.domain = range(k_value)

            # Add node to CSP class
            gac.variables.append(variable)

        # Create constraints
        for i in range(vertices_and_edges[0] + 1, len(lines)):
            new_constraint = Constraint()

            # Set the correct constraint
            new_constraint.method = makefunc(['n'], 'n[0] != n[1]')

            # Get the constraint line
            constraint_line = map(int, lines[i].split(' '))

            # Loop all vars in the constraint
            for var in constraint_line:
                new_constraint.vars.append(var)

            # Apply the new constraint to the list
            GAC.Constraints.append(new_constraint)

        # Set the correct gac for GACState
        GACState.GAC = GAC

        # Create the initial csp state
        gac_state = GACState()
        gac_state.gac = gac
        gac_state.type = GACState.START

        # Set the csp state to astar_gac
        self.astar_gac.gac_state = gac_state

        # Begin CSP
        self.astar_gac.start()

        # Run the GUI
        self.run()

    def run(self):
        # Set reference to GAC
        Gui.GAC = GAC

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

        # Pretty print
        Printer.print_border_top()
        Printer.print_content('Counts')
        Printer.print_border_middle()

        # Get verticies without color
        uncolored = 0
        for var in gui.astar_gac.gac_state.gac.variables:
            if len(var.domain) != 1:
                uncolored += 1

        # Print the stats
        Printer.print_content('Unsatisfied constraints: ' + str(0), align='left') # If we get here it is impossible to have unsatisfied constraints
        Printer.print_content('Vertices without color: ' + str(uncolored), align='left')
        Printer.print_content('Nodes in search tree (A* generated states): ' + str(len(gui.astar_gac.astar.states)), align='left')
        Printer.print_content('Nodes popped and expanded (A* open closed list): ' + str(len(gui.astar_gac.astar.closed)), align='left')
        Printer.print_content('Solution path length: ' + str(len(gui.astar_gac.astar.goal_path())), align='left')

        # Print closing border
        Printer.print_border_bottom()

Module2Runner()