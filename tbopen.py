#!/usr/bin/python

import threading, requests, sys, json, os, zmq
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

def parse_arguments():
    """ returns a tuple (options, app_path) """
    parser = OptionParser(usage="usage: %prog [options] app_path")

    parser.add_option('', '--follow',
        dest='follow', action='store_true',
        help='output the opened app\'s output until it exits', default=False)

    parser.add_option('', '--raw',
        dest='raw', action='store_true',
        help='when following output raw JSON objects, rather than parsing the log output', default=False)

    options, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    return options, args[0]


def main():
    options, app_path = parse_arguments()

    if options.follow:
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://127.0.0.1:10452')
        socket.setsockopt(zmq.SUBSCRIBE, '')

    r = requests.post('http://127.0.0.1:10451/run', data=app_path)
    r.raise_for_status()

    if options.follow:
        app_has_started = False

        while True:
            line = socket.recv()
            message = json.loads(line)

            if not app_has_started:
                if 'started' in message and message['path'] == app_path:
                    if options.raw:
                        sys.stdout.write(json.dumps(message) + '\n')
                    else:
                        print 'tbopen: App started as PID %i' % message['started']
                    app_has_started = True
            else:
                if options.raw:
                    sys.stdout.write(json.dumps(message) + '\n')
                else:
                    if 'stdout' in message:
                        sys.stdout.write(message['stdout'])
                        sys.stdout.flush()
                    if 'stderr' in message:
                        sys.stdout.write(terminal_colors.red + message['stderr'] + terminal_colors.end)
                        sys.stdout.flush()
                    if 'ended' in message:
                        print 'tbopen: App ended with code: %i' % message['code']
                if 'ended' in message:
                    break

if __name__ == '__main__':
    main()
