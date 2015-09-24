# -*- coding: utf-8 -*-

from behavior import Behavior


class BestFirst(Behavior):

    NAME = 'BestFirst'

    @staticmethod
    def handle(node, queue):
        if node is not None:
            # Add to queue
            queue.append(node)

        # Sort the list
        queue = sorted(queue, key=lambda x: x.total_cost())

        # Dry run inner sort
        lowest_f = queue[0].total_cost()
        inner_sort = []
        for n in queue:
            if lowest_f == n.total_cost() and n != queue[0]:
                inner_sort.append(n)

        # Check if we found anything running the inner sorting
        if len(inner_sort) > 0:
            # Sort the inner list
            inner_sort = sorted(inner_sort, key=lambda x: x.h)

            # Build the final list
            old_queue = queue
            queue = inner_sort
            for n in old_queue:
                if n not in queue:
                    queue.append(n)

        # Return the final, sorted list
        return queue