# -*- coding: utf-8 -*-

class Node():

    def __init__(self, index):
        self.index = index
        self.state = None
        self.domain = []

    def __repr__(self):
        return 'nodeid = ' + str(self.index)