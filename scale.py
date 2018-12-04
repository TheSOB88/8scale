from fractions import Fraction

class Scale:
    full, diatonic, accidental = [], [], []
    use_ratios = False
    degrees = 0
    
    #WAYS TO INIT:
    #  full = diatonic
    #  accidental = full - diatonic
    #  diatonic + accidental != full
    def __init__( self, full, diatonic = [], accidental = [] ):
        self.full = full
        self.use_ratios = isinstance( full[1], str ) or full[1] < 2
        if self.use_ratios:
            for i, note in enumerate( full ):
                full[i] = Fraction( note )

        self.degrees = len( full )
        if len( diatonic ) > 0:
            self.diatonic = diatonic
            #diatonic + accidental != full
            if len( accidental ) > 0:
                self.accidental = accidental
                for i in accidental:
                    if i not in full:
                        full.append( Fraction( i ) if self.use_ratios else i )
            #accidental = full - diatonic
            else:
                self.accidental = full.copy()
                for i in diatonic:
                    self.accidental.remove( i )
        #full = diatonic
        else:
            self.diatonic = full.copy()
            self.accidental = []
        if self.use_ratios:
            for i, note in enumerate( diatonic ):
                diatonic[i] = Fraction( note )
            for i, note in enumerate( accidental ):
                accidental[i] = Fraction( note )
