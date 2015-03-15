#!/usr/bin/python
from glob import glob
import os
import subprocess
import pygame

def screen():
    pygame.init()
    pygame.font.init()

    surface = pygame.display.set_mode((320, 240))

    font = pygame.font.Font(None, 32)
    surface.fill((255,255,255))
    surface.blit(font.render('Home screen', 1, (0,0,0)), (50, 50))
    pygame.display.update()

# screen()

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
