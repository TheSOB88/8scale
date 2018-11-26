#!/usr/bin/env python

import pygame, os, random, pygame.draw as draw
from pygame.locals import *

globalTicks = -1
keysList = []

def processControls():
    global keysList, globalTicks
    
    newControls = set()#controls pressed this frame
    #get input  
    for event in pygame.event.get():
        if event.type == QUIT:
            return "quit"
        #game buttons
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return "quit"
            else:
                keysList.append( event.key )

def main():
    gameWindow = Rect( 0, 0, 100, 30 )
    clock = pygame.time.Clock()

    main_dir = os.path.split( os.path.abspath( __file__ ) )[0]
    
    # Initialize pygame
    pygame.init()
    if not( pygame.mixer and pygame.mixer.get_init()):
        print ( 'Warning, no sound' )
        pygame.mixer = None    
    pygame.display.set_caption( 'get keys v0.1' )
    
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok( gameWindow.size, winstyle, 32 )
    screen = pygame.display.set_mode( gameWindow.size, winstyle, bestdepth )
		
    ticks = -1
    globalTicks = -1
    
    quitFlag = False
    
    while not quitFlag:
        globalTicks += 1
    
        controlsReturnVal = processControls()
        if controlsReturnVal == "quit":
            quitFlag = True
            print( 'keysList: ' + str( keysList ) )

    pygame.quit()

 
#call the "main" function if running this script
if __name__ == '__main__': main()