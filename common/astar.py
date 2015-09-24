# -*- coding: utf-8 -*-

import math


class AStar():

    NODE = None

    def __init__(self):
        # The grid itself
        self.nodes = []

        # The start node
        self.open = []
        self.closed = []

        # Behavior
        self.behavior = None

        # Finished
        self.finished = False

    def agenda_loop(self):
        # Update the open list
        self.open = self.behavior.handle(None, self.open)

        # Get the current node
        current_node = self.open.pop(0)

        # Set node to dirty (used only for GUI drawing)
        current_node.dirty = True

        # Add to closed list
        self.closed.append(current_node)

        # Check if the node we just select is the goal node
        if current_node.type == AStar.NODE.GOAL:
            # We are done!
            self.finished = True

            # Return true
            return True
        else:
            # Get successor nodes
            successor_nodes = current_node.generate_all_successors(self)

            # Loop all successor nodes and check if they are valid or not
            for successor in successor_nodes:
                # If node is valid
                if successor is not None and successor.type is not AStar.NODE.BLOCKED:
                    # Append the current successor as the child to the parent
                    current_node.kids.append(successor)

                    # Set as dirty (used only for GUI drawing)
                    successor.dirty = True

                    # If the successor is not in neither open nor closed
                    if successor not in self.open and successor not in self.closed:
                        # Attach relationship between nodes
                        self.attach_and_eval(successor, current_node)

                        # Use the behavior to modify the open list
                        self.open = self.behavior.handle(successor, self.open)
                    elif successor.g + successor.arch_cost(current_node) < successor.g:
                        # Attach relationship between nodes
                        self.attach_and_eval(successor, current_node)

                        # If the successor is not in closed, then propagate the path backwards
                        if successor in self.closed:
                            AStar.propagate_path_improvements(successor)

        # We are not done yet
        return False

    @staticmethod
    def propagate_path_improvements(parent):
        # Loop all children belonging to the parent
        for child in parent.children:
            # Check if the new score is better than the old
            if parent.g + 10 < child.g:
                # Append parent to child
                child.parents.append(parent)

                # Update g store
                child.g = parent.g + child.arch_cost(parent)

                # Recursive call
                AStar.propagate_path_improvements(child)

    def attach_and_eval(self, child, parent):
        # Add parent to child
        child.parents.append(parent)

        # Set g score
        child.g = parent.g + child.arch_cost(parent)

        # Set h score
        child.h = child.calculate_h(self)

    def get_node(self, state):
        for node in self.nodes:
            if node.state == state:
                return node
        return None

    def goal_path(self):
        # Find the goal node
        backtrack_node = None
        for node in self.nodes:
            if node.type == AStar.NODE.GOAL:
                backtrack_node = node

        # Backtrack the goal path
        goal_path = []
        while True:
            # Check if the node is the start node
            if backtrack_node.type == AStar.NODE.START:
                # Append the current node
                goal_path.append(backtrack_node)

                # Break out of the loop
                break
            else:
                # Double check that we have any parents
                if len(backtrack_node.parents) > 0:
                    # Not the start node, sort the parents
                    parents_sort = sorted(backtrack_node.parents, key=lambda x: x.total_cost(), reverse=True)

                    # Append the current node
                    goal_path.append(backtrack_node)

                    # Swap current node
                    backtrack_node = parents_sort[0]
                else:
                    # Something broke
                    break

        # Return the goal path
        return goal_path