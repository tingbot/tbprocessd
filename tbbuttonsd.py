from __future__ import print_function

import subprocess, threading, signal, json, os, shlex, Queue

from tingbot.platform_specific.tingbot import register_button_callback

button_states = ['up', 'up', 'up', 'up']
actions = {}
queue = Queue.Queue()

def button_callback(button_index, state):
    button_states[button_index] = state

    queue.put(tuple(button_states))

def process_combo_events():
    while True:
        combo = queue.get()
        action = actions.get(combo)

        if action:
            print('Combo detected:')
            print(combo)
            print('Action:')
            print(action)
            subprocess.call(action)

        queue.task_done()

def load_json(filename):
    try:
        with open(filename, 'r') as fp:
            return json.load(fp)
    except ValueError:
        raise ValueError('Failed to load %s because it\'s not a valid JSON file' % filename)

def load_config():
    if os.path.exists('tbbuttonsd.conf'):
        config = load_json('tbbuttonsd.conf')
    elif os.path.exists('/etc/tbbuttonsd.conf'):
        config = load_json('/etc/tbbuttonsd.conf')
    else:
        raise Exception('Config file not found')

    for action in config:
        actions[tuple(action["combo"])] = action["command"]
     
def main():
    load_config()
    register_button_callback(button_callback)
    
    # got to keep the main thread free to respond ot signals e.g. SIGTERM
    # Event.wait() will block signals until set so we push this to its own
    # thread.
    respond_thread = threading.Thread(target=process_combo_events)
    respond_thread.daemon = True
    respond_thread.start()

    while True:
        signal.pause()

if __name__ == '__main__':
    main()
