from fractions import Fraction
import math
import consts

class Scale:
    #full, diatonic, accidental = [], [], []
    #use_ratios = False, is_diatonic = True
    #degrees = 0
    #note_to_halftones, bend_cents = [], []
    #info = ''
    
    #WAYS TO INIT:
    #  full = diatonic
    #  accidental = full - diatonic
    #  diatonic + accidental != full
    def __init__( self, diatonic, accidental = [] ):
        self.full, self.diatonic, self.accidental = [], [], []
        self.use_ratios = isinstance( diatonic[1], str ) or diatonic[1] < 2
        self.note_to_halftones, self.bend_cents, self.note_channel = [], [], []
        self.info = ''
        
        for i in diatonic:
            val = Fraction( i ) if self.use_ratios else i
            self.full.append( val )
            self.diatonic.append( val )
        for i in accidental:
            val = Fraction( i ) if self.use_ratios else i
            self.full.append( val )
            self.accidental.append( val )

        self.degrees = len( self.full )
        self.is_diatonic = len( accidental ) > 0
        
        log2, octCents = math.log( 2 ), 1200
        for i, j in enumerate( self.full ):
            noteCents, note_info = None, None
            if self.use_ratios:
                note_info = Fraction( j )
                note_info = str( j.numerator ) + '/' + str( j.denominator )
                noteCents = math.log( j ) / log2 * octCents
            else:
                noteCents = j
                note_info = str( noteCents )
            halfTones = round( noteCents / 100 )
            pitchBend = round( noteCents / 100 - halfTones, 4 )
            
            note_channel = i
            if pitchBend in self.bend_cents:
                note_channel = self.bend_cents.index( pitchBend )
            if note_channel > 8: #skip drum channel
                note_channel += 1
                
            self.note_to_halftones.append( halfTones )
            self.bend_cents.append( pitchBend )
            self.note_channel.append( note_channel )
            
            self.info += str( ( i+1, note_info, noteCents, halfTones, pitchBend ) ) + '\n'
        
    def initPitches( self, midi ):
        halfTone = 4096
        for i in set( self.note_channel ):
            bend = self.bend_cents[ self.note_channel[i] ]
            midi.pitch_bend( int( halfTone * bend ), i )
            midi.set_instrument( consts.instrument, i )

    #keeps note within an octave span, updates octave appropriately
    def normalize_note( self, note, octave, span ):
        if note < 0:
            octave -= 1
            note += span
        if note >= span:
            note -= span
            octave += 1
        return (note, octave)

    #get scale degree and octave for the key pressed
    def get_note_info( self, evKey ):
        x, y = None, None
        for j, row in enumerate( consts.keyboard ):
            for i, key in enumerate( row ):
                if key == evKey:
                    x, y = i + consts.noteShift, j
                    break
            if x is not None:
                break
        else:
            x, y = 0, 0
            
        if self.is_diatonic:
            row_even = y % 2 == 0
            octave = math.floor( y / 2 )
            x, octave = self.normalize_note( x, octave, len( self.diatonic ) )
            # if not row_even and x == 0:
                # octave -= 1
            note = self.full.index( (self.diatonic if row_even else self.accidental)[x] )
        else:
            note, octave = self.normalize_note( x, y, self.degrees )
        return (note, octave, self.note_channel[note])