#!/usr/bin/python
from glob import glob
import os
import subprocess

os.environ['PATH'] += ':.'

folder = os.path.dirname(__file__)

print ''
print 'Home screen'
print '-----------'
print ''
print 'Available apps:'

apps = glob(os.path.join(folder, '*.py'))

for i, app in enumerate(apps):
    print '%i: %s' % (i, app)

app_index = raw_input('\nChoose an app: ')

app = apps[int(app_index)]

subprocess.call(['tbopen', app])
