# -*- coding: utf-8 -*-
import time
import os
import logging
from logging.handlers import RotatingFileHandler

# http://sametmax.com/ecrire-des-logs-en-python/
# https://docs.python.org/3/howto/logging.html

if not os.path.isdir('assets/logs'):
    os.mkdir('assets/logs')

list_of_files = os.listdir('assets/logs')
# print(list_of_files)
# FIXME: make this work
for file in list_of_files:
    if os.path.getctime('assets/logs/' + file) >= time.time() + 604800:  # older than 7 days
        os.remove('assets/logs/' + file)

# init
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)
# for the files :
_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
_file_handler = RotatingFileHandler('assets/logs/'+os.getlogin()+'--'+time.strftime('%Y_%m_%d__%H_%M_%S')+'.log',
                                    'a', 10000000, 1)
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(_formatter)
_logger.addHandler(_file_handler)
# for the CLI, optional (comment to deactivate):
# _steam_handler = logging.StreamHandler()
# _steam_handler.setLevel(logging.DEBUG)
# _logger.addHandler(_steam_handler)
# TODO : for the syslog, not ready until the server comes back alive...
# https://docs.python.org/3/library/logging.handlers.html#sysloghandler

# TODO: automatically create the folder where the logs will be saved, if it doesn' exist already


def log(message_level, message, *args):
    """
    Use this to log everything in a file !
    Here are the different message levels and what they correspond to (you should pass there number to the function):
    CRITICAL :: 50 :: The whole program will soon explode
    ERROR :: 40 :: An operation failed
    WARNING :: 30 :: Something need your attention : special mode started, rare situation detected, optional lib can be
    installed...
    INFO :: 20 :: Inform on where the program is : 'Creating the menu", 'Entering __init__ of tabs/TabPhotos'...
    DEBUG :: 10 :: Dump infos week debugging : for example, what this fucking dictionnary contains
    :param message_level: this should be a number
    :param message: the message to log
    :type message_level: int
    :type message: str

    :Example:

    >>> log(50, "FUCK THIS IS WRONG")
    >>> log(10, "dictionnary", example_dict)
    >>> log(30, "Params not loaded correctly, using defaults")

    ..warnings:: DO NOT PUT ANYTHING PRIVATE IN THE LOGS
    """
    if args is not None:
        message_to_log = message + " :: " + " :: ".join(map(str, args))
    else:
        message_to_log = message
    if message_level == 50:
        _logger.critical(message_to_log)
    elif message_level == 40:
        _logger.error(message_to_log)
    elif message_level == 30:
        _logger.warning(message_to_log)
    elif message_level == 20:
        _logger.info(message_to_log)
    elif message_level == 10:
        _logger.debug(message_to_log)
    else:
        _logger.warning("Error with the logging: message_level: " + str(message_level) + " message: " + message_to_log)

__all__ = ['log']
