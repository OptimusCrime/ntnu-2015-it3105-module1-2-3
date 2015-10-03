# -*- coding: utf-8 -*-


class Variable:

    def __init__(self, index):
        self.index = index
        self.state = None
        self.domain = []

    def __repr__(self):
        return str(self.index)
