# -*- coding: utf-8 -*-
from .CONSTANTS import *


class Borg:
    """
    Two borg instances are the same everywhere in the code. It can be really useful to pass variables trough modules,
    functions...
    """
    __shared_state = {'error_screen_message': None}

    def __init__(self):
        self.SCREEN_SIZE = []
        self.inputs = None
        self.display = None
        self.conns = None
        self.version = None
        self.__dict__ = self.__shared_state


class Queue(dict):
    """
    Use the Queue to execute functions at another moment of program's execution.
    Queue.add(function, priority) adds a function who'll be exxecuter when you do Queue.execute(priority)
    """

    def add(self, function, priority):
        """
        Adds a function to the queue. to execute later the function do   Queue.execute(priority)
        """

        if priority in self:
            self[priority].append(function)
        else:
            self[priority] = [function]

    def execute(self, priority=ALL):
        """
        This execute the all functions that have the same priority as the arg.
        If the arg is set to ALL, then every fun ction will be executed
        """

        if priority == ALL:
            for key in self:
                while len(self[key]) > 0:
                    self[key][0].pop()()
                del self[key]
        else:
            while len(self[priority]) > 0:
                self[priority].pop()()
            del self[priority]


__all__ = ['Borg']
