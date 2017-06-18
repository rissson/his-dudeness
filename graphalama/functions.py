# -*- coding: utf-8 -*-
import math as m
import random
from math import floor
import time
import tkinter.filedialog as fd
import tkinter as tk
from graphalama.borg import Borg
from graphalama.CONSTANTS import MULTIPLY, DIVIDE, PROPORTION


borg_baby = Borg()


def print_ret(function):
    def new_function(*args, **kwargs):
        print('function', function)
        print('arguments : ')
        for key in args:
            print(type(key), key)
        for key in kwargs:
            print(type(kwargs[key], key, args[key]))
        ret = function(*args, **kwargs)
        print('return : ', type(ret), ret)
        return ret
    return new_function


# Put this in time
def get_HHMM():
    ti = time.localtime()
    hour = str(ti.tm_hour)
    if ti.tm_min == 0:
        min = '00'
    elif ti.tm_min < 10:
        min = '0' + str(ti.tm_min)
    else:
        min = str(ti.tm_min)

    return hour + ':' + min

def time_to_str(milliseconds):
    """Take a integer that represents the time in milliseconds as parameter
    and returns a string that looks like HH:MM:ss (HH only if needed)"""
    seconds = int(milliseconds/1000)
    minutes = seconds // 60
    seconds %= 60
    hours = minutes // 60
    minutes %= 60
    if seconds < 10:
        sec_str = '0'+str(seconds)
    else:
        sec_str = str(seconds)
    if minutes < 10:
        min_str = '0'+str(minutes)
    else:
        min_str = str(minutes)
    str_final = min_str+':'+sec_str
    if hours > 0:
        if hours < 10:
            h_str = '0' + str(hours)
        else:
            h_str = str(hours)
        return h_str+':'+str_final
    return str_final


def search_string_in_list(string, list_of_strings):
    """ search for 'string' in 'list' and returns 2 elements : the postion of the item in the list and its value
    returns 'nothing found' if nothing has been found + the length of the list
    has to be in a thread
    """
    i = 0
    length = len(list_of_strings)
    for item in list_of_strings:
        if item.lower().find(string.lower()) != -1:
            return i, item[i]
        elif i > length:
            return '404 not found', length
        i += 1


def get_location(inputs, default_location, title_window):
    """ has to be in a thread """
    inputs['screen']['change'] = True
    inputs['screen']['fullscreen'] = False
    root = tk.Tk()
    root.withdraw()
    directory = fd.askdirectory(initialdir=default_location, parent=root, title=title_window)
    root.destroy()
    return directory + "/"


def get_string_match(str1, str2):
    """
    Return the percentage of similarities between the two strings
    0 is the lowest / 1 is the highest
    see http://www.catalysoft.com/articles/StrikeAMatch.html for more information
    """

    def get_bigrams(string):
        s = string.lower()
        return [s[i:i + 2] for i in range(len(s) - 1)]

    pairs1 = get_bigrams(str1)
    pairs2 = get_bigrams(str2)
    union = len(pairs1) + len(pairs2)
    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                break
    return (2.0 * hit_count) / union


_chars = [chr(i) for i in range(ord('!'), ord('~'))] + ['€'] + [chr(i) for i in range(ord('¿'), ord('ʬ'))]

def random_string(len):
    s = ''
    for i in range(len):
        s += random.choice(_chars)

    return s


# @print_ret
def scale(dims, coefficients, flags=MULTIPLY):
    if DIVIDE in flags:
        def operation(x, y):
            return x / y
    else:
        def operation(x, y):
            return m.ceil(x * y)

    if PROPORTION in flags:
        if type(coefficients) == list or type(coefficients) == tuple:
            coefficients = min(coefficients)

    if isinstance(dims, (list, tuple)):
        if len(dims) == 2:
            if isinstance(coefficients, int):
                return [operation(dims[0], coefficients), operation(dims[1], coefficients)]
            elif isinstance(coefficients, (tuple, list)):
                return [operation(dims[0], coefficients[0]), operation(dims[1], coefficients[1])]
            else:
                raise TypeError

        if len(dims) == 4:
            if isinstance(coefficients, int):
                new_x = operation(dims[0], coefficients)
                new_y = operation(dims[1], coefficients)
                new_w = operation(dims[2], coefficients)
                new_h = operation(dims[3], coefficients)
                return [new_x, new_y, new_w, new_h]

            elif len(coefficients) == 2:
                coefficient = min(coefficients)
                new_x = scale(dims[0], coefficients[0])
                new_y = scale(dims[1], coefficients[1])
                new_w = scale(dims[2], coefficient)
                new_h = scale(dims[3], coefficient)
                return [new_x, new_y, new_w, new_h]

            else:
                new_x = operation(dims[0], coefficients[0])
                new_y = operation(dims[1], coefficients[1])
                new_w = operation(dims[2], coefficients[0])
                new_h = operation(dims[3], coefficients[1])
                return [new_x, new_y, new_w, new_h]

    else:
        if type(coefficients) == list or type(coefficients) == tuple:
            coefficients = min(coefficients)
        return operation(dims, coefficients)


def to_pixels(value, base_of_prop=None):
    """this returns value correctly sized (if not integer or if proportional (here base_of_prop will be used
    to scale the value))"""

    if base_of_prop is None:
        base_of_prop = borg_baby.SCREEN_SIZE

    if -1 <= value <= 1:
        value = scale(value, base_of_prop)
    elif value > 1:
        value = m.ceil(value)
    elif value < -1:
        value = floor(value)  # to round every tie in the same direction
    else:
        print('Ta gueule')
        raise Exception
    return value


def to_prop(value, base_of_prop):
    if value > 1:
        value = scale(value, base_of_prop, DIVIDE)
    elif value <= 1:
        value = round(value, 5)
    else:
        print('Ta gueule')
        raise Exception

    return value


def only_if_object_changes(function):
    """
    A decorator that call the function only if the abject have changed
    Call this before every function who must be called only if an home made object had any change.
    This function who is decorated like that mustn't return anything
    """

    def new_function(self, *args, **kwargs):

        if self.previous_state != self.__state__():  # we test if any important thing have changed
            function(self, *args, **kwargs)  # we execute the function
            self.previous_state = self.__state__()  # if yes, we need to update this attr
            return 'Done'
    return new_function


def only_if_object_change_forced_repr(repr_function_to_use):
    def decorator(function):
        def new_function(self, *args, **kwargs):
            ret = None
            if self.previous_self != repr_function_to_use(self):  # we test if any important thing have changed
                ret = function(self, *args, **kwargs)  # we execute the function
                self.previous_self = repr_function_to_use(self)  # if yes, we need to update this attr
                # print(self)
            return ret
        return new_function
    return decorator


def execution_number(function):
    def new_functon(*args, **kwargs):
        ret = function(*args, **kwargs)

        if function in execution_numbers:
            execution_numbers[function] += 1
        else:
            execution_numbers[function] = 1

        return ret
    return new_functon

execution_numbers = dict()
_execution_times = dict()


def execution_time(function):
    """ a decorator who'll print the time taken by the function """

    def new_function(*args, **kwargs):
        start_time = time.time()
        ret = function(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        if exec_time > 10**(-7):
            if function in _execution_times:
                executions = _execution_times[function][0]
                moy = _execution_times[function][1]
                moy = (moy * executions + exec_time) / (executions + 1)
                _execution_times[function][0] += 1
                _execution_times[function][1] = moy
            else:
                _execution_times[function] = [1, exec_time]
                moy = exec_time

            print(function, exec_time, 'Moy :', moy, 'Delta :', moy - exec_time)
        return ret

    return new_function


__all__ = ['scale', 'to_pixels', 'to_prop', 'only_if_object_changes', 'execution_time', 'execution_number',
           'execution_numbers', 'get_HHMM', 'search_string_in_list', 'get_location', 'random_string',
           'get_string_match']
