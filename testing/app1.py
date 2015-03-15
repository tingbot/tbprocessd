#!/usr/bin/python

def screen():
    pygame.init()
    pygame.font.init()

    surface = pygame.display.set_mode((320, 240))

    font = pygame.font.Font(None, 32)
    surface.fill((255,255,255))
    surface.blit(font.render('App 1', 1, (0,0,0)), (50, 50))
    pygame.display.update()

screen()

print 'I am app1'

print 'press return to exit'

raw_input('')
