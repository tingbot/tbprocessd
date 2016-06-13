from __future__ import print_function
import subprocess, threading, signal
from tingbot.platform_specific.tingbot import register_button_callback

midleft_state = 'up'
midright_state = 'up'

home_event = threading.Event()

def button_callback(button_index, state):
    global midleft_state, midright_state

    if button_index == 1:
        midleft_state = state
    elif button_index == 2:
        midright_state = state

    if midleft_state == 'down' and midright_state == 'down':
        home_event.set()

def respond_to_home_event():
    while True:
        home_event.wait()
        print('Home combo detected')
        subprocess.call(['tbopen', '/apps/home'])
        home_event.clear()

def main():
    register_button_callback(button_callback)
    
    # got to keep the main thread free to respond ot signals e.g. SIGTERM
    # Event.wait() will block signals until set so we push this to its own
    # thread.
    respond_thread = threading.Thread(target=respond_to_home_event)
    respond_thread.daemon = True
    respond_thread.start()

    while True:
        signal.pause()

if __name__ == '__main__':
    main()
