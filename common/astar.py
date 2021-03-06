# -*- coding: utf-8 -*-


class AStar:

    State = None

    def __init__(self):
        # All generated states
        self.states = {}

        # Lists with the open and closed states
        self.open = []
        self.closed = []

        # Behavior
        self.behavior = None

        # Finished
        self.finished = False

    def set_behavior(self, behavior):
        # Set th behavior
        self.behavior = behavior

        # Add the handler
        self.behavior.add_handler(self.open)

    def agenda_loop(self):
        # Get the current state
        current_state = self.behavior.get(self.open)

        # Set node to dirty (used only for GUI drawing)
        current_state.dirty = True

        # Add to closed list
        self.closed.append(current_state)

        # Check if the node we just select is the goal state
        if current_state.type == AStar.State.GOAL:
            # We are done!
            self.finished = True

            # Return true
            return True
        else:
            # Get successor nodes
            successor_states = current_state.generate_all_successors(self)

            # Loop all successor nodes and check if they are valid or not
            for successor in successor_states:
                # Check if this state has already been generated
                if self.states.has_key(successor.get_hash()):
                    # Swap for successor in the state dictionary
                    successor = self.states[successor.get_hash()]

                    # If state is valid
                    if successor.type is not AStar.State.BLOCKED:
                        # Append the current successor as the child to the parent
                        current_state.children.append(successor)

                        # Set as dirty (used only for GUI drawing)
                        successor.dirty = True

                        # If the successor is not in neither open nor closed
                        if successor not in self.open and successor not in self.closed:
                            # Attach relationship between states
                            self.attach_and_eval(successor, current_state)

                            # Use the behavior to modify the open list
                            self.behavior.add(successor, self.open)
                        elif current_state.g + successor.arch_cost(current_state) < successor.g:
                            # Attach relationship between states
                            self.attach_and_eval(successor, current_state)

                            # If the successor is not in closed, then propagate the path backwards
                            if successor in self.closed:
                                AStar.propagate_path_improvements(successor)
                else:
                    # Add to states
                    self.states[successor.get_hash()] = successor

                    # Attach and eval the new successor
                    self.attach_and_eval(successor, current_state)

                    # Add the successor
                    self.behavior.add(successor, self.open)

                current_state.children.append(successor)

        return False

    @staticmethod
    def propagate_path_improvements(parent):
        # Loop all children belonging to the parent
        for child in parent.children:
            # Check if the new score is better than the old
            if parent.g + child.arch_cost(parent) < child.g:
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

    def get_state(self, state_id):
        return self.states[state_id]

    def goal_path(self):
        # Find the goal state
        backtrack_state = None
        for key, value in self.states.iteritems():
            if value.type == AStar.State.GOAL:
                backtrack_state = value

        # Backtrack the goal path
        goal_path = []
        while True:
            # Check if the node is the start state
            if backtrack_state.type == AStar.State.START:
                # Append the current state
                goal_path.append(backtrack_state)

                # Break out of the loop
                break
            else:
                # Double check that we have any parents
                if len(backtrack_state.parents) > 0:
                    # Not the start node, sort the parents
                    parents_sort = sorted(backtrack_state.parents, key=lambda x: x.total_cost(), reverse=True)

                    # Append the current state
                    goal_path.append(backtrack_state)

                    # Swap current state
                    backtrack_state = parents_sort[0]
                else:
                    # Something broke
                    break

        # Return the goal path
        return goal_path
