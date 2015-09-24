#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.astar import AStar
from common.printer import Printer

from module1.gui import Gui
from module1.node import Node

import os
import glob
import platform


class Runner:

    def __init__(self):
        # New instance of the A* Algorithm
        self.a_star = AStar()

        # Set reference in AStar to Node
        AStar.NODE = Node

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
        Printer.print_content('IT3105 :: Module 1 :: A*')
        Printer.print_border_middle()

    def parse_files(self):
        # Set to None to avoid "referenced before assigned" complaint
        input_choice = None

        # Get all boards from directory
        boards = glob.glob('module1/boards/*.txt')

        # Present different boards to the user
        while True:
            Printer.print_content('Available boards: ')
            Printer.print_border_middle()

            # Print list of boards
            idx = 0
            for b in boards:
                Printer.print_content('[' + str(idx) + ']: ' + b, align='left')
                idx += 1
            Printer.print_border_bottom()

            # Get the user input
            input_choice = raw_input('[0-' + str(len(boards) - 1) + ']: ')

            Printer.print_newline()

            # Validate input
            try:
                input_choice = int(input_choice)

                if input_choice < 0 or input_choice >= len(boards):
                    raise AssertionError('')
                break
            except (AssertionError, ValueError):
                Printer.print_border_top()
                Printer.print_content('Invalid input, try again')
                Printer.print_border_middle()

        # Parse the file the user chose
        self.parse_file(str(boards[input_choice]))

    @staticmethod
    def parse_file_line(line):
        # Parse a line from the file, stripping parenthesis, splitting on comma and casting all strings to ints
        return map(int, line.replace('(', '').replace(')', '').replace(' ', '').split(','))

    def parse_file(self, file_name):
        # Read all lines in the file while stripping the ending newline
        lines = [line.rstrip('\n') for line in open(file_name)]

        # Build the grid
        grid_size = Runner.parse_file_line(lines[0])

        # Find start and goal from the file
        start_and_goal = lines[1].replace(' ', '').split(')(')

        # Get start position
        start_node_position = Runner.parse_file_line(start_and_goal[0])
        goal_node_position = Runner.parse_file_line(start_and_goal[1])

        # List for barriers
        barriers = []

        # Add barriers (if any)
        for idx in range(2, len(lines)):
            barriers.append(Runner.parse_file_line(lines[idx]))

        # Create the board
        self.create_board(grid_size[0], grid_size[1], (start_node_position[0], start_node_position[1]),
                          (goal_node_position[0], goal_node_position[1]), barriers)

    def create_board(self, width, height, start, goal, barriers):
        # Loop the height
        for y in range(0, height):
            for x in range(0, width):
                self.a_star.nodes.append(Node((x, y)))

        # Loop barriers and set type to blocked on all involved nodes
        for bar in barriers:
            for x in range(bar[0], (bar[0] + bar[2])):
                for y in range(bar[1], (bar[1] + bar[3])):
                    self.a_star.get_node((x, y)).type = Node.BLOCKED

        # Set the start node
        start_node = self.a_star.get_node((start[0], start[1]))
        start_node.type = Node.START

        # Add start node to the open list
        self.a_star.open.append(start_node)

        # Set goal node
        goal_node = self.a_star.get_node((goal[0], goal[1]))
        goal_node.type = Node.GOAL

        # Set information about the start node
        start_node.g = 0
        start_node.h = start_node.calculate_h(self.a_star)

        # Start the gui
        self.start(width, height)

    def start(self, width, height):
        # Create new instance of GUI
        gui = Gui()

        # Set width and height
        gui.width = width
        gui.height = height

        # Apply the grid as the data source
        gui.set_data_source(self.a_star)

        # Set TKInter to the frontmost process
        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        # Draw the initial GUI
        gui.draw_initial()

        # Start the GUI
        gui.after(0, gui.task)

        # Start the event mainloop here
        gui.mainloop()

        # Set the terminal to the frontmost process (expects iTerm to be the chosen terminal)
        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "iTerm" to true' ''')

        # Check if solution for all boards were found
        if gui.finished:
            # Pretty print
            Printer.print_border_top()
            Printer.print_content('Comparison')

            # Loop all the data
            for data in gui.data:
                # Pretty print
                Printer.print_border_middle()

                # Print the name of the behavior
                Printer.print_content(data.behavior.NAME, align='left')
                Printer.print_empty()

                # Print the stats
                Printer.print_content('Nodes generated: ' + str(len(data.closed) + len(data.open)), align='left')
                Printer.print_content('Solution path length: ' + str(sum(map(lambda x: x.g, data.goal_path()))),
                                      align='left')

            # Print closing border
            Printer.print_border_bottom()

# Start the runner
Runner()
