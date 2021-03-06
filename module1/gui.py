# -*- coding: utf-8 -*-

from state import State

from behaviors.best_first import BestFirst
from behaviors.breadth_first import BreadthFirst
from behaviors.depth_first import DepthFirst

from Tkinter import *
import copy
import math


class Gui(Tk):

    SQUARE_SIZE = 25

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Init empty list of solvers
        self.data = []

        # Set size
        self.width = None
        self.height = None

        # Force fullscreen
        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth() - 3, self.winfo_screenheight() - 3))

        # Set TKinter title
        self.title("IT3105 :: Module 1 :: A* :: Thomas Gautvedt :: Close with <Escape> or <q>")

        # Bind keys to close
        self.bind("<Escape>", lambda x: self.destroy())
        self.bind("q", lambda x: self.destroy())

        # Set canvas to None before starting to draw
        self.canvas = Canvas(self, bg='white')

        # Store all elements on canvas
        self.elements = {}

        # Stores the state of the program
        self.finished = False

    def set_data_source(self, source):
        # Loop all the behaviors
        for behavior in [BestFirst, BreadthFirst, DepthFirst]:
            # Copy the data source
            new_data = copy.deepcopy(source)

            # Set the specified behavior
            new_data.set_behavior(behavior)

            # Add the data to the list
            self.data.append(new_data)

    def draw(self):
        # Keep track of element index
        element_index = 0

        # Loop the grids
        for idx, data in enumerate(self.data):
            # Loop the grid for this solver
            for key, value in data.states.iteritems():
                # Only update dirty nodes
                if value.dirty:
                    # Reset the dirty bit
                    value.dirty = False

                    # Get the correct code
                    fill = Gui.get_color(value, data)

                    # Draw the rect
                    self.canvas.itemconfig(self.elements[str(idx) + value.get_hash()], fill='#' + fill)

                # Update index
                element_index += 1

    def draw_path(self):
        # Loop the grids
        for idx, data in enumerate(self.data):
            goal_path = data.goal_path()

            # Calculate this grid offset
            grid_offset = (idx * self.width * Gui.SQUARE_SIZE) + (idx * 10) + 10

            # Loop nodes in the goal path
            for value in goal_path:
                # Generate the positions
                top = (self.height - value.id[1] - 1) * Gui.SQUARE_SIZE + 10
                left = value.id[0] * Gui.SQUARE_SIZE + grid_offset
                bottom = (self.height - value.id[1] - 1) * Gui.SQUARE_SIZE + Gui.SQUARE_SIZE - 2 + 10
                right = value.id[0] * Gui.SQUARE_SIZE + Gui.SQUARE_SIZE - 2 + grid_offset

                # Draw the oval
                self.canvas.create_oval(left, top, right, bottom, fill="#0000ff")

            # Pack
            self.canvas.pack(fill=BOTH, expand=True)

            # Set finished to true
            self.finished = True

    def draw_initial(self):
        # Loop the grids
        for idx, data in enumerate(self.data):
            # Calculate this grid offset
            grid_offset = (idx * self.width * Gui.SQUARE_SIZE) + (idx * 10) + 10

            # Loop the grid for this solver
            for key, value in data.states.iteritems():
                # Define the various coordinates
                top = (self.height - value.id[1] - 1) * Gui.SQUARE_SIZE + 10
                left = value.id[0] * Gui.SQUARE_SIZE + grid_offset
                bottom = (self.height - value.id[1] - 1) * Gui.SQUARE_SIZE + Gui.SQUARE_SIZE - 2 + 10
                right = value.id[0] * Gui.SQUARE_SIZE + Gui.SQUARE_SIZE - 2 + grid_offset

                # Get the correct code
                fill = Gui.get_color(value, data)

                # Draw the rect
                self.elements[str(idx) +  value.get_hash()] = self.canvas.create_rectangle(left, top, right, bottom, fill='#' + fill)

        # Pack
        self.canvas.pack(fill=BOTH, expand=True)

        # Update
        self.canvas.update()

    def task(self):
        # Loop all data things
        for data in self.data:
            # Check if this data is finished or not
            if not data.finished:
                # Run the agenda loop
                data.agenda_loop()

        # Check if all are finished
        finished = True
        for data in self.data:
            if not data.finished:
                finished = False
                break

        # Draw once we are finished
        self.draw()

        # Check if we should do some more
        if not finished:
            self.after(50, self.task)
        else:
            self.draw_path()

    @staticmethod
    def get_color(node, data):
        # Define standard fill
        fill = 'ffffff'

        # Check if the node is blocked or not
        if node.type == State.BLOCKED:
            fill = '000000'
        elif node.type == State.START:
            fill = '0000ff'
        elif node.type == State.GOAL:
            fill = '0000ff'
        else:
            # Check in open
            if node in data.open:
                fill = 'cccccc'
            elif node in data.closed:
                fill = Gui.calculate_fill_color(data, node.h)

        # Return the final color
        return fill

    @staticmethod
    def calculate_fill_color(data, value):
        # Find total cost for start node
        highest_h = data.states[data.states.keys()[0]].h
        for key, v in data.states.iteritems():
            if v.h > highest_h:
                highest_h = v.h

        # Calculate the RBG colors to generate a heat map from red to green
        r = math.fabs(int((255 * value) / highest_h))
        g = math.fabs(int((255 * (highest_h - value)) / highest_h))

        # RBG -> HEX
        return '%02x%02x%02x' % (r, g, 0)
