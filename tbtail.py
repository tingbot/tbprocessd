#!/usr/bin/python

import json, sys, zmq
from optparse import OptionParser


class terminal_colors:
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    cyan = '\033[36m'
    bright_red = '\033[91m'
    bright_green = '\033[92m'

    bold = '\033[1m'
    faint = '\033[2m'

    end = '\033[0m'


def main():
    parser = OptionParser()

    parser.add_option('', '--raw',
        dest='raw', action='store_true',
        help='output raw JSON objects, rather than parsing the log output', default=False)

    options, args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:10452')
    socket.setsockopt(zmq.SUBSCRIBE, '')

    while True:
        line = socket.recv()
        if options.raw:
            sys.stdout.write(line)
        else:
            message = json.loads(line)

            if 'stdout' in message:
                sys.stdout.write(message['stdout'])
                sys.stdout.flush()
            if 'stderr' in message:
                sys.stdout.write(terminal_colors.red + message['stderr'] + terminal_colors.end)
                sys.stdout.flush()


if __name__ == '__main__':
    main()
