# -*- coding: utf-8 -*-

from behavior import Behavior


class BreadthFirst(Behavior):

    NAME = 'BreadthFirst'

    @staticmethod
    def add_handler(open_nodes):
        pass

    @staticmethod
    def add(node, open_nodes):
        open_nodes.append(node)

    @staticmethod
    def get(open_nodes):
        return open_nodes.pop(0)
