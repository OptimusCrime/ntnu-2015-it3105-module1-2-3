# -*- coding: utf-8 -*-

from behavior import Behavior


class DepthFirst(Behavior):

    NAME = 'DepthFirst'

    @staticmethod
    def add_handler(queue):
        pass

    @staticmethod
    def add(node, open_nodes):
        open_nodes.append(node)

    @staticmethod
    def get(open_nodes):
        return open_nodes.pop(-1)
