# -*- coding: utf-8 -*-


class Node():

    def __init__(self, index):
        self.index = index
        self.state = None
        self.domain = []
        self.length = 1

    def __repr__(self):
        return str(self.index)
