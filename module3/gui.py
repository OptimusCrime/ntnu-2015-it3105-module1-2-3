# -*- coding: utf-8 -*-

from Tkinter import *


class Gui(Tk):

    SQUARE_SIZE = 50

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Set size
        self.astar_gac = None

        # Force fullscreen
        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth() - 3, self.winfo_screenheight() - 3))

        # Set TKinter title
        self.title("IT3105 :: Module 3 :: GAC + A* + Nonograms :: Thomas Gautvedt :: Close with <Escape> or <q>")

        # Bind keys to close
        self.bind("<Escape>", lambda x: self.destroy())
        self.bind("q", lambda x: self.destroy())

        # Set canvas to None before starting to draw
        self.canvas = Canvas(self, bg='white')

        # Store all elements on canvas
        self.elements = []
        self.elements_color = []

        # Stores the state of the program
        self.finished = False

    def draw(self):
        # Draw the nodes
        for i in range(len(self.astar_gac.gac_state.gac.variables)):
            # Store stuff just for now
            variable = self.astar_gac.gac_state.gac.variables[i]

            # Check if this row/column is solved
            if len(variable.domain) == 1:
                # Check if we should solve for row or column
                if variable.index[0:1] == 'r':
                    # Simply loop the variable and colorize like we normally would
                    for j in range(len(variable.domain[0])):
                        # Check if we should update the current color
                        if variable.domain[0][j] != self.elements_color[i][j]:
                            # Check what color to draw
                            fill = 'ffffff'
                            if variable.domain[0][j]:
                                fill = 'cccccc'

                            # Update the stored color
                            self.elements_color[i][j] = variable.domain[0][j]

                            # Update rect color
                            self.canvas.itemconfig(self.elements[i][j], fill='#' + fill)
                else:
                    pass

    def draw_initial(self):
        # Draw the nodes
        for i in range(len(self.astar_gac.gac_state.gac.variables)):
            # Store stuff just for now
            variable = self.astar_gac.gac_state.gac.variables[i]

            # Check if we are drawing a row or column
            if variable.index[0:1] == 'r':
                inner_elements = []
                print variable.domain
                inner_elements_color = [False] * len(variable.domain[0])
                for j in range(len(variable.domain[0])):
                    top = i * Gui.SQUARE_SIZE + 10
                    left = j * Gui.SQUARE_SIZE + 10
                    bottom = top + Gui.SQUARE_SIZE - 2
                    right = left + Gui.SQUARE_SIZE - 2

                    inner_elements.append(self.canvas.create_rectangle(left, top, right, bottom, fill='#ffffff'))

                # Add to outer elements list
                self.elements.append(inner_elements)

                # Add initial color to the list
                self.elements_color.append(inner_elements_color)

        # Pack
        self.canvas.pack(fill=BOTH, expand=True)

        # Update
        self.canvas.update()

        # Call draw to colorize (in case we are finished)
        self.draw()

    def task(self):
        finished = self.astar_gac.run()

        # Draw
        self.draw()

        # Check if we should do some more
        if not finished:
            self.after(50, self.task)