'''
Keylogger for Ubuntu
Adapted from https://github.com/nesl/KeyLogger_Python
Originally written by Vikranth
'''

from pynput import keyboard
import Xlib
import Xlib.display
import logging
import os

cwd = os.getcwd()
log_directory = os.path.join(cwd, "Key_logs")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

os.chdir(log_directory)

i = 0
while os.path.exists("key_log%s.txt" % i):
    i += 1

#log_dir = ""
#logging.basicConfig(filename = (log_dir + "key_log%s.txt" % i), level=logging.INFO, format='%(asctime)s.%(msecs)03d,%(message)s', datefmt='%s')

formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d,%(message)s', datefmt='%s')


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


key_logger = setup_logger('key_logger', 'key_log%s.txt' % i)

left = ['1', '2', '3', '4', '5', '!', '@', '#', '$', '%', 'q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f',
        'g', 'z', 'x', 'c', 'v', 'b', 'Q', 'W', 'E', 'R', 'T', 'A', 'S', 'D', 'F', 'G', 'Z', 'X', 'C', 'V', 'B']
right = ['6', '7', '8', '9', '0', '^', '&', '*', '(', ')', 'y', 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l',
         ';', 'n', 'm', ',', '.', '/', 'Y', 'U', 'I', 'O', 'P', 'H', 'J', 'K', 'L', ':', 'N', 'M', '<', '>', '?']


def get_active_app_name():
    try:
        display = Xlib.display.Display()
        root = display.screen().root
        window_id = root.get_full_property(display.intern_atom(
            '_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]
        window = display.create_resource_object('window', window_id)

        return window.get_wm_class()[1]
    except Xlib.error.BadWindow:
        return 'loading'


def on_press(key):
    try:
        active_app_name = get_active_app_name()
        if key.char in left:
            key = 'left'
        elif key.char in right:
            key = 'right'
        else:
            key = key

        key_logger.info('{0}, pressed, {1}'.format(key, active_app_name))

    except AttributeError:
        key_logger.info('{0}, pressed, {1}'.format(key, active_app_name))


def on_release(key):
    try:
        active_app_name = get_active_app_name()
        if key.char in left:
            key = 'left'
        elif key.char in right:
            key = 'right'
        else:
            key = key

        key_logger.info('{0}, released, {1}'.format(key, active_app_name))

    except AttributeError:
        key_logger.info('{0}, released, {1}'.format(key, active_app_name))


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
