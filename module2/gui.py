# -*- coding: utf-8 -*-

from Tkinter import *


class Gui(Tk):

    NODE_SIZE = 15
    COLORS = ['#ff8080', '#ffcc80', '#99ff80', '#80ffff', '#9980ff', '#ff80cc', '#e5ff80', '#80b3ff', '#e680ff']
    GAC = None

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Set size
        self.astar_gac = None

        # Force fullscreen
        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth() - 3, self.winfo_screenheight() - 3))

        # Set TKinter title
        self.title("IT3105 :: Module 2 :: CPS w/A* :: Thomas Gautvedt :: Close with <Escape> or <q>")

        # Bind keys to close
        self.bind("<Escape>", lambda x: self.destroy())
        self.bind("q", lambda x: self.destroy())

        # Store all the elements drawn on the canvas
        self.elements = []
        self.elements_color = []
        self.element_label_var = None

        # Set canvas to None before starting to draw
        self.canvas = Canvas(self, bg='white')

    def get_node_idx_pos(self, idx):
        return self.get_node_pos(self.astar_gac.gac_state.gac.variables[idx])

    def get_node_pos(self, node):
        x_min = self.astar_gac.gac_state.gac.variables[0].state[0]
        x_max = self.astar_gac.gac_state.gac.variables[0].state[0]

        y_min = self.astar_gac.gac_state.gac.variables[0].state[1]
        y_max = self.astar_gac.gac_state.gac.variables[0].state[1]

        for n in self.astar_gac.gac_state.gac.variables:
            if n.state[0] > x_max:
                x_max = n.state[0]
            if n.state[0] < x_min:
                x_min = n.state[0]
            if n.state[1] > y_max:
                y_max = n.state[1]
            if n.state[1] < y_min:
                y_min = n.state[1]

        # Calculate the offset
        X_OFFSET = 0
        Y_OFFSET = 0

        if x_min < 0:
            X_OFFSET = -x_min
        if y_min < 0:
            Y_OFFSET = -y_min

        # Check if we need to change the scaling variable
        X_SCALE = 1
        Y_SCALE = 1

        if (20 + (X_OFFSET + x_max) * 15) > (self.winfo_screenwidth() - 100):
            X_SCALE = (self.winfo_screenwidth() - 100) / (20 + (X_OFFSET + x_max) * 15)
        if (20 + (Y_OFFSET + y_max) * 15) > (self.winfo_screenheight() - 100):
            Y_SCALE = (self.winfo_screenheight() - 100) / (20 + (Y_OFFSET + y_max) * 15)

        left = 20 + (20 + (X_OFFSET + node.state[0]) * 15) * X_SCALE
        right = left + Gui.NODE_SIZE
        top = 20 + (20 + (Y_OFFSET + node.state[1]) * 15) * Y_SCALE
        bottom = top + Gui.NODE_SIZE

        # Return the final calculated posisions
        return left, right, top, bottom

    @staticmethod
    def get_color(node):
        if len(node.domain) == 1:
            return Gui.COLORS[node.domain[0]]
        return '#000000'

    def draw_once(self):
        # Draw the nodes
        for node in self.astar_gac.gac_state.gac.variables:
            # Get the positions
            left, right, top, bottom = self.get_node_pos(node)

            # Get color
            color = Gui.get_color(node)

            # Do the actual drawing here
            self.elements.append(self.canvas.create_oval(left, top, right, bottom, fill=color))
            self.elements_color.append(color)

        # Draw the constraints / arcs
        for constraint in Gui.GAC.Constraints:
            # Get the arc positions
            arc_start_left, arc_start_right, arc_start_top, arc_start_bottom = self.get_node_idx_pos(constraint.vars[0])
            arc_end_left, arc_end_right, arc_end_top, arc_end_bottom = self.get_node_idx_pos(constraint.vars[1])

            self.canvas.create_line(arc_start_left + (Gui.NODE_SIZE / 2),
                                    arc_start_top + (Gui.NODE_SIZE / 2),
                                    arc_end_left + (Gui.NODE_SIZE / 2),
                                    arc_end_top + (Gui.NODE_SIZE / 2), fill='#000000')

        # Set the label
        self.element_label_var = StringVar()
        self.element_label_var.set('0 / ' + str(len(self.astar_gac.gac_state.gac.variables)))

        # Apply the var to the label
        text_label = Label(self.canvas, textvariable=self.element_label_var)
        text_label.place(x=0, y=0)

        # Pack
        self.canvas.pack(fill=BOTH, expand=True)

        # Update
        self.canvas.update()

    def draw(self):
        # Store number of colored nodes
        colored_nodes = 0

        # Draw the nodes
        for element_index in range(len(self.astar_gac.gac_state.gac.variables)):
            # Get color
            color = self.get_color(self.astar_gac.gac_state.gac.variables[element_index])

            # Check if the current node is colored or not
            if len(self.astar_gac.gac_state.gac.variables[element_index].domain) == 1:
                colored_nodes += 1

            # Check if the new color is different from the old color
            if color != self.elements_color[element_index]:
                # Update color
                self.canvas.itemconfig(self.elements[element_index], fill=color)

        # Update the label
        self.element_label_var.set(str(colored_nodes) + ' / ' + str(len(self.astar_gac.gac_state.gac.variables)))

    def task(self):
        finished = self.astar_gac.run()

        # Draw
        self.draw()

        # Check if we should do some more
        if not finished:
            self.after(10, self.task)
        else:
            self.element_label_var.set(str(len(self.astar_gac.gac_state.gac.variables)) + ' / ' +
                                       str(len(self.astar_gac.gac_state.gac.variables)) + ' - Finished!')
