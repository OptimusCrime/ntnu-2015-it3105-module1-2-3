# -*- coding: utf-8 -*-

from behavior import Behavior


class BreadthFirst(Behavior):

    NAME = 'BreadthFirst'

    @staticmethod
    def handle(node, queue):
        if node is not None:
            # Append to list
            queue.append(node)

        # Return the new list
        return queue