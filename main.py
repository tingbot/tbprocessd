#!/usr/bin/env python3

import os, time, socket, subprocess, logging

from http.server import HTTPServer, BaseHTTPRequestHandler
from fcntl import fcntl, F_GETFL, F_SETFL
from select import select

HOME_APP = os.environ.get('HOME_APP', 'testing/home.py')

def main():
    http_setup()
    udp_setup()

    try:
        run_loop()
    finally:
        if app_is_running():
            app_stop()

def run_loop():
    while True:
        http_loop()
        app_loop()

        # pause the run loop until we see any new inputs
        # this is more efficient than a sleep, since it only wakes the process when
        # there's something to do
        select([httpd, app_process.stdout, app_process.stderr], [], [])

########
# HTTP #
########

httpd = None

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/run':
            self.send_response(200)
            self.end_headers()

            content_length = self.headers['Content-Length']

            if content_length:
                app_path = self.rfile.read(int(content_length))

                app_start(app_path=app_path)

                self.request.sendall(b'OK')
                return
            else:
                self.send_error(400)

        self.send_error(404)

def http_setup():
    global httpd

    bind_address = ('localhost', 10451)

    httpd = HTTPServer(bind_address, Handler)
    httpd.timeout = 0

def http_loop():
    httpd.handle_request()

#######
# APP #
#######

app_process = None

def app_setup():
    pass

def app_loop():
    if not app_is_running():
        app_start(HOME_APP)
    app_pipe_output()

def app_start(app_path):
    global app_process
    if app_process:
        app_stop()

    app_process = subprocess.Popen([app_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # set the stdout and stderr pipes to be non-blocking
    flags = fcntl(app_process.stdout, F_GETFL)
    fcntl(app_process.stdout, F_SETFL, flags | os.O_NONBLOCK)
    flags = fcntl(app_process.stderr, F_GETFL)
    fcntl(app_process.stderr, F_SETFL, flags | os.O_NONBLOCK)


def app_stop():
    global app_process

    # pipe any remaining output before killing the process
    app_pipe_output()

    app_process.poll()
    if app_process.returncode is None:
        app_process.terminate()
        # wait for termination (2 seconds)
        wait_start = time.perf_counter()

        while app_is_running() and time.perf_counter() < wait_start + 2.0:
            app_pipe_output()
            time.sleep(0.02)

        if app_is_running():
            logging.warning('App did not terminate 2 seconds after SIGTERM. Sending SIGKILL...')
            # send SIGKILL and wait indefinitely for termination
            app_process.kill()

            while app_is_running():
                app_pipe_output()
                time.sleep(0.02)

    app_process = None

def app_is_running():
    if app_process is None:
        return False
    app_process.poll()
    return app_process.returncode is None

def app_pipe_output():
    try:
        stdout = os.read(app_process.stdout.fileno(), 65535)
        if len(stdout) > 0:
            print('out: %s' % stdout.decode('utf-8', 'replace'))
            udp_send(stdout)
    except BlockingIOError:
        pass

    try:
        stderr = os.read(app_process.stderr.fileno(), 65535)
        if len(stderr) > 0:
            print('err: %s' % stderr.decode('utf-8', 'replace'))
            udp_send(stderr)
    except BlockingIOError:
        pass

#######
# UDP #
#######

udp_socket = None

def udp_setup():
    global udp_socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def udp_send(msg):
    udp_socket.sendto(msg, ('127.0.0.1', 10452))

########
# MAIN #
########

if __name__ == '__main__':
    main()
