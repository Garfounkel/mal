import readline
import atexit
import os


def init_readline():
    history_file = os.path.expanduser('~/.PFMal_history')
    history_buffer_size = 1000

    readline.set_history_length(history_buffer_size)
    readline.parse_and_bind('tab: complete')

    if os.path.exists(history_file):
        try:
            readline.read_history_file(history_file)
        except IOError:
            pass

    atexit.register(readline.write_history_file, history_file)
