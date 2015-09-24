# -*- coding: utf-8 -*-

from behavior import Behavior


class DepthFirst(Behavior):

    NAME = 'DepthFirst'

    @staticmethod
    def handle(node, queue):
        if node is None:
            return queue
        return [node] + queue