# -*- coding: utf-8 -*-

from common.astarcsp import AStarCSP
from common.csp import CSP
from common.cspstate import CSPState

from module2.constraint import Constraint
from module2.gui import Gui
from module2.node import Node

import copy
import os
import itertools
import platform

class Runner:

    K_OPTIONS = ['red', 'green', 'blue', 'pink', 'orange', 'brown']
    K_VALUE = 6

    def __init__(self):
        self.astar_csp = AStarCSP()

        # Build everything
        self.build()

        # Begin CSP
        self.astar_csp.start()

        # Start the GUI
        self.run()

    def build(self):
        csp = CSP()

        # Read all lines in the file while stripping the ending newline
        lines = [line.rstrip('\n') for line in open('module2/graphs/graph-color-5-k6.txt')]
        vertices_and_edges = map(int, lines[0].split(' '))

        # Create vertices
        for i in range(1, vertices_and_edges[0] + 1):
            # Get the state
            state = map(float, lines[i].split(' '))

            # Init new Node and set the correct values
            node = Node(i)
            node.state = (state[1], state[2])
            node.domain = range(Runner.K_VALUE)

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

Runner()