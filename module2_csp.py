#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.astarcsp import AStarCSP
from common.csp import CSP
from common.cspstate import CSPState
from common.printer import Printer

from module2.constraint import Constraint
from module2.gui import Gui
from module2.node import Node
from module2.makefunc import makefunc

import os
import glob
import platform

class Runner:

    def __init__(self):
        self.astar_csp = AStarCSP()

        # Set the function for our nodes to run the CV problem
        Constraint.method = staticmethod(makefunc(['n'], 'n[0] != n[1]'))

        # This method is just used to print the introduction and chose the parser
        self.start()

    def start(self):
        # Print introduction lines
        Runner.print_introduction()

        # Present different parser options
        self.parse_files()

    @staticmethod
    def print_introduction():
        Printer.print_border_top()
        Printer.print_content('IT3105 :: Module 1 :: GAC + A*')
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
        graph_suggested_k = int(graphs[input_choice_graph].split('.')[0].split('-')[-1].replace('k', ''))

        # Get the K value
        Printer.print_border_top()
        while True:
            Printer.print_content('Set K value for this graph, suggested value is ' + str(graph_suggested_k))
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
        csp = CSP()

        # Read all lines in the file while stripping the ending newline
        lines = [line.rstrip('\n') for line in open(file_name)]
        vertices_and_edges = map(int, lines[0].split(' '))

        # Create vertices
        for i in range(1, vertices_and_edges[0] + 1):
            # Get the state
            state = map(float, lines[i].split(' '))

            # Init new Node and set the correct values
            node = Node(i)
            node.state = (state[1], state[2])
            node.domain = range(k_value)

            # Add node to CSP class
            csp.nodes.append(node)

        # Create constraints
        for i in range(vertices_and_edges[0] + 1, len(lines)):
            new_constraint = Constraint()

            # Get the constraint line
            constraint_line = map(int, lines[i].split(' '))

            # Loop all vars in the constraint
            for var in constraint_line:
                new_constraint.vars.append(csp.nodes[var])

            # Apply the new constraint to the list
            csp.constraints.append(new_constraint)

        # Create the initial csp state
        csp_state = CSPState()
        csp_state.csp = csp
        csp_state.type = CSPState.START

        # Set the csp state to astar_csp
        self.astar_csp.csp_state = csp_state

        # Begin CSP
        self.astar_csp.start()

        # Run the GUI
        self.run()

    def run(self):
        # Create new instance of GUI
        gui = Gui()

        # Set reference to AStarCSP here
        gui.astar_csp = self.astar_csp

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

Runner()