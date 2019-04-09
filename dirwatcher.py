__author__ = "Michael McKenzie"


import signal
import logging
import sys
import argparse
import time
import os
exit_flag = False


# creates new logger __name__
logger = logging.getLogger(__name__)
# sets log level
logger.setLevel(logging.INFO)
# the logger format
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
# creates a specific logger so it's not just the root logger
file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def create_parser():
    """Monitors a given directory and returns filename and line number where the magic text is found"""
    parser = argparse.ArgumentParser(
        description='Monitor directory files looking for magic string')
    parser.add_argument('directory', help='enter your directory to monitor')
    parser.add_argument('magic_text', help='enter your magic string')
    parser.add_argument('polling_interval',
                        help='enter a time (sec) for the polling loop interval')
    parser.add_argument('file_extension_type',
                        help='specify what file extension type to search within')
    return parser


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    logger.warn('Received ' + str(sig_num))
    # log the signal name (the python2 way)
    signames = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                    if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received ' + signames[sig_num])
    exit_flag = True

# def find_files(args):
#     global directory, polling_interval, magic_text, file_extension_type
#     directory, polling_interval, magic_text, file_extension_type = namespace.directory, namespace.polling_interval, namespace.magic_text,  namespace.file_extension_type
#     for filename in os.listdir(directory):
#         if filename.endswith(file_extension_type) and filename not in dir_files:
#             logger.info('New file found: {}'.format(filename))


def main(args):
    file_dict = {}
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    namespace = parser.parse_args(args)
    global directory, polling_interval, magic_text, file_extension_type
    directory, polling_interval, magic_text, file_extension_type = namespace.directory, namespace.polling_interval, namespace.magic_text,  namespace.file_extension_type

    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these to my process.
    while not exit_flag:
        try:
            for filename in os.listdir(directory):
                if filename.endswith(file_extension_type) and filename not in dir_files:
                    with open(directory + '/' + filename) as filepath:
                        for line_count, line in enumerate(filepath.readlines()):
                            if magic_text in line:
                                if filename not in file_dict.keys():
                                    file_dict[filename] = line_count
                                    # if line_count > file_dict[filepath]:
                                    logger.info('Magic text {} found in file {} on line {}'.format(
                                        magic_text, file_dict.keys(), line_count + 1))

        # call my directory watching function..
        except Exception as e:
            logger.exception(type(e))
            logger.exception("Exception!")
        logger.info('Searching...')
        time.sleep(float(polling_interval))
        # Log an ERROR level message here
        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        #     time.sleep(polling_interval)

        # final exit point happens here
        # Log a message that we are shutting down
        # Include the overall uptime since program start.


if __name__ == '__main__':
    main(sys.argv[1:])
