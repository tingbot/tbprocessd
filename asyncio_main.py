#!python3

import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep
import subprocess
import udp
from fcntl import fcntl, F_GETFL, F_SETFL
import os 

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/run':
            self.send_response(200)
            self.end_headers()

            content_length = self.headers['Content-Length']

            if content_length:
                app_path = self.rfile.read(15)

                asyncio.async(run_app(app_path=app_path))

                self.request.sendall(b'OK')
                return
            else:
                self.send_error(400)

        self.send_error(404)

app_process = None
httpd = None
loop = asyncio.get_event_loop()
current_transport = None

@asyncio.coroutine
def http():
    bind_address = ('localhost', 10451)

    global httpd
    httpd = HTTPServer(bind_address, Handler)
    httpd.timeout = 0
    udp.setup()

    while True:
        httpd.handle_request()
        yield from asyncio.sleep(0.02)

def main():
    asyncio.async(http())
    asyncio.async(run_app('testing/home.py'))

    loop.run_forever()

class ChildProtocol(asyncio.SubprocessProtocol):
    def connection_made(self, transport):
        print('connection_made')
    def connection_lost(self, exc):
        print('connection_lost')
    def pipe_connection_lost(self, fd, exc):
        print('pipe_connection_lost')
    def pipe_data_received(self, fd, data):
        print('fd: %i: %s' % (fd, data))
        udp.send(data)
    def process_exited(self):
        print('process_exited')

@asyncio.coroutine
def run_app(app_path):
    yield from stop_app()

    global current_transport
    transport, protocol = yield from loop.subprocess_exec(ChildProtocol, app_path)

    current_transport = transport

    print('running')

# def stop_app():
#     global app_process
#     app_process.poll()
#     if app_process.returncode is None:
#         try:
#             app_process.terminate()
#             # wait for termination (2 seconds)
#             sleep(1)
#             app_process.wait()
#         except subprocess.TimeoutExpired:
#             # send SIGKILL and wait indefinitely for termination
#             app_process.kill()
#             outs, errs = app_process.communicate()
#     app_process = None

@asyncio.coroutine
def stop_app():
    transport = current_transport
    if transport is None:
        return

    if transport.get_returncode() is not None:
        return

    transport.terminate()

    yield from asyncio.sleep(1)

    if transport.get_returncode() is None:
        transport.kill()

if __name__ == '__main__':
    main()
