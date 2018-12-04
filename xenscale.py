#!/usr/bin/env python

import pygame, os, random, pygame.draw as draw, pygame.midi
import math
import time
from pygame.locals import *
from fractions import Fraction

from scale import Scale

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit( "Sorry, extended image module required" )
    
keyboard = [ [96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 8], #num row
        [9, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 92], #tab row
        [301, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 13], #caps row
        [304, 122, 120, 99, 118, 98, 110, 109, 44, 46, 47, 303, 273] ] #shift row
keyboard.reverse()

#scales
oncical_scale = Scale( [ 0, 65.52, 161.88, 259.24, 356.6, 453.96, 551.32, 713.2, 810.56, 907.92, 1005.28, 1102.64 ] )
qms = [0, 41.0590, 76.0490, 117.108, 152.098, 158.167, 193.157, 234.216, 269.206, 310.265, 345.255, 351.324,
        386.314, 427.373, 462.363, 503.422, 544.480, 579.471, 620.529, 655.520, 696.578, 737.637, 772.627, 813.686, 848.676, 
        854.745, 889.735, 930.794, 965.784, 1006.84, 1041.83, 1047.90, 1082.89, 1123.95, 1158.94]
qmsc = qms_chromatic = [ qms[i] if i < 20 else qms[i-1] for i in range( 0, len(qms), 3 ) ]
        #[qms[0], qms[3], qms[6], qms[9], qms[12], qms[15], qms[18], qms[20], qms[23], qms[26], qms[29], qms[32]]
qms_diatonic = [ qmsc[i] for i in [0, 2, 4, 5, 7, 9, 11] ]
qms_accidental = [qms[34], qmsc[1], qmsc[3], qms[14], qmsc[6], qmsc[8], qmsc[10]]

qrt_meantone_scale = Scale( qms_chromatic, qms_diatonic, qms_accidental )

ji_ratio = [ 1,  "9/8", "5/4", "4/3", "3/2", "20/12", "15/8" ]
ji_accidental = ["31/16", "17/16", "6/5", "11/8", "45/32", "24/15", "27/16"]
ji_scale = Scale( ji_ratio, ji_ratio.copy(), ji_accidental )

# degrees = 12
# scale = [ Fraction( degrees+i )/degrees for i in range( degrees ) ]
# scale = oncical_scale
# scale = qrt_meantone_scale
scale = ji_scale

diatonic_flag = True
noteShift = -1

note_to_halftones = []#, 0, 2, 4, 5, 7, 9, 9, 10]
bendCents = []
log2, octCents = math.log( 2 ), 1200
for i, j in enumerate( scale.full ):
    noteCents, info = None, None
    if scale.use_ratios:
        info = Fraction( j )
        info = str( j.numerator ) + '/' + str( j.denominator )
        noteCents = math.log( j ) / log2 * octCents
    else:
        noteCents = j
        info = str( noteCents )
    halfTones = round( noteCents / 100 )
    pitchBend = noteCents / 100 - halfTones
    note_to_halftones.append( halfTones )
    bendCents.append( pitchBend )
    print( ( i+1, info, noteCents, halfTones, pitchBend ) )
    
def initPitches( midi ):
    global note_to_halftones
    halfTone = 4096
    for i, bend in enumerate( bendCents ):
        #skip drum channel
        if i > 8:
            i += 1
        midi.pitch_bend( int( halfTone * bend ), i )
        midi.set_instrument( 62, i )

#keeps note within an octave span, updates octave appropriately
def normalize_note( note, octave, span ):
    if note < 0:
        octave -= 1
        note += span
    if note >= span:
        note -= span
        octave += 1
    return (note, octave)

#get scale degree and octave for the key pressed
def get_note_info( evKey, scale ):
    x, y = None, None
    for j, row in enumerate( keyboard ):
        for i, key in enumerate( row ):
            if key == evKey:
                x, y = i + noteShift, j
                break
        if x is not None:
            break
    else:
        x, y = 0, 0
        
    if diatonic_flag:
        row_even = y % 2 == 0
        octave = math.floor( y / 2 )
        x, octave = normalize_note( x, octave, len( scale.diatonic ) )
        if not row_even and x == 0:
            octave -= 1
        note = scale.full.index( (scale.diatonic if row_even else scale.accidental)[x] )
    else:
        note, octave = normalize_note( x, y, scale.degrees )
    return (note, octave)
    
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
                #toggle the note toggle
                if evKey == K_SPACE and event.type == KEYDOWN:
                    toggleNotes = not toggleNotes
                    break
                #stop all notes
                if evKey == K_RALT and event.type == KEYDOWN:
                    for i in range( 0, 16 ):
                        midi.write( [[[0xb0 + i,123,0], time.time()]] )
                        playingNotes = set()
                    initPitches( midi )
                    break
                
                #get note info from key
                scale_note, octave = get_note_info( evKey, scale )
                octave += 3
                chromaticNote = note_to_halftones[scale_note]
                midiNote, midiVel, midiChannel = ( chromaticNote + octave * 12, 90, scale_note )
                #skip drum channel
                if midiChannel >= 9: 
                    midiChannel += 1
                if midiChannel > 15:
                    midiChannel -= 16
                
                #do the note
                note_tuple = (chromaticNote, octave)
                args = ( midiNote, midiVel, midiChannel )
                if toggleNotes:
                    if event.type == KEYDOWN:
                        if note_tuple in playingNotes:
                            playingNotes.remove( note_tuple )
                            midi.note_off( *args )
                        else:
                            playingNotes.add( note_tuple )
                            midi.note_on( *args )
                else:
                    if event.type == KEYDOWN:
                        print( 'note info: ', (scale_note, octave) )
                        print( 'key and midi info: ', evKey, args, chromaticNote, bendCents[scale_note] )
                        midi.note_on( *args )
                    else:
                        midi.note_off( *args )
                        if note_tuple in playingNotes:
                            playingNotes.remove( note_tuple ) 
        clock.tick(60)
    pygame.quit()

 
#call the "main" function if running this script
if __name__ == '__main__': main()