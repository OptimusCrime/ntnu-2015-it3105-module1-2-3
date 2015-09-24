# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Behavior(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def handle(node, queue):
        pass