# -*- coding: utf-8 -*-

from behavior import Behavior

from heapq import heappush, heappop, heapify


class BestFirst(Behavior):

    NAME = 'BestFirst'

    @staticmethod
    def add_handler(open_nodes):
        heapify(open_nodes)

    @staticmethod
    def add(node, open_nodes):
        heappush(open_nodes, node)

    @staticmethod
    def get(open_nodes):
        return heappop(open_nodes)
