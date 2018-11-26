#!/usr/bin/env python

import pygame, os, random, pygame.draw as draw, pygame.midi
import math
from pygame.locals import *
from fractions import Fraction

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit( "Sorry, extended image module required" )
    
keyboard = [ [96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 8], #num row
        [9, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 92], #tab row
        [301, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 13], #caps row
        [304, 122, 120, 99, 118, 98, 110, 109, 44, 46, 47, 303, 273] ] #shift row
keyboard.reverse()

degrees = 12
scale = [ Fraction( degrees+i )/degrees for i in range( degrees ) ]
scale = [ 0, 65.52, 161.88, 259.24, 356.6, 453.96, 551.32, 713.2, 810.56, 907.92, 1005.28, 1102.64 ]
degrees = len( scale )
noteShift = 1

diatonicToChromatic = [0]#, 0, 2, 4, 5, 7, 9, 9, 10]
bendCents = [0]
log2, octCents = math.log( 2 ), 1200
for i, j in enumerate( scale ):
    noteCents, info = None, None
    if scale[1] < 2:
        info = Fraction( j )
        info = str( j.numerator ) + '/' + str( j.denominator )
        noteCents = math.log( j ) / log2 * octCents
    else:
        noteCents = j
        info = str( noteCents )
    halfTones = math.floor( noteCents / 100 )
    pitchBend = noteCents / 100 - halfTones
    diatonicToChromatic.append( halfTones )
    bendCents.append( pitchBend )
    print( ( i+1, info, noteCents, halfTones, pitchBend ) )
    
def initPitches( midi ):
    global diatonicToChromatic
    halfTone = 4096
    for i, bend in enumerate( bendCents ):
        if i > 8:
            i += 1
        midi.pitch_bend( int( halfTone * bend ), i )
        midi.set_instrument( 62, i )

def getKeyInfo( evKey ):
    note, octave = 0, 0
    for j, row in enumerate( keyboard ):
        for i, key in enumerate( row ):
            if key == evKey:
                note, octave = i + noteShift, j
                break
                break
    if not note:
        #return -1
        pass
    if note == 0:
        octave -= 1
        note = degrees
    if note > degrees:
        note -= degrees
        octave += 1
        
    return( note, octave )
    
globalTicks = -1
                
def main():
    gameWindow = Rect( 0, 0, 100, 30 )
    clock = pygame.time.Clock()

    main_dir = os.path.split( os.path.abspath( __file__ ) )[0]
    
    # Initialize pygame
    pygame.init()
    if not( pygame.mixer and pygame.mixer.get_init()):
        print ( 'Warning, no sound' )
        pygame.mixer = None 
    pygame.midi.init()
    midi = pygame.midi.Output( 0 )
    initPitches( midi )
    pygame.display.set_caption( 'xenscale v0.2' )
    
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok( gameWindow.size, winstyle, 32 )
    screen = pygame.display.set_mode( gameWindow.size, winstyle, bestdepth )
		
    ticks = -1
    globalTicks = -1
    
    quitFlag = False
    playingNotes = set()
    
    toggleNotes = False
    
    while not quitFlag:
        globalTicks += 1
    
        #get input  
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            #game buttons
            if event.type in ( KEYDOWN, KEYUP ):
                evKey = event.key
                if evKey == K_ESCAPE:
                    quitFlag = True
                    print( 'quittin\'' )
                    break
                if evKey == K_SPACE and event.type == KEYDOWN:
                    toggleNotes = not toggleNotes
                    break
                diatonicNote, octave = getKeyInfo( evKey )
                octave += 2
                chromaticNote = diatonicToChromatic[diatonicNote]
                midiNote, midiVel, midiChannel = ( chromaticNote + octave * 12, 90, diatonicNote )
                #skip drum channel
                if midiChannel >= 9: 
                    midiChannel += 1
                if midiChannel > 15:
                    midiChannel -= 16
                args = ( midiNote, midiVel, midiChannel )
                if toggleNotes:
                    if event.type == KEYDOWN:
                        if evKey in playingNotes:
                            playingNotes.remove( evKey )
                            midi.note_off( *args )
                        else:
                            playingNotes.add( evKey )
                            midi.note_on( *args )
                else:
                    if event.type == KEYDOWN:
                        midi.note_on( *args )
                    else:
                        midi.note_off( *args )
        clock.tick(60)
    pygame.quit()

 
#call the "main" function if running this script
if __name__ == '__main__': main()