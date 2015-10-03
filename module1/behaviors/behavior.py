# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Behavior(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def add_handler(open_nodes):
        pass

    @staticmethod
    @abstractmethod
    def add(node, open_nodes):
        pass

    @staticmethod
    @abstractmethod
    def get(open_nodes):
        pass

