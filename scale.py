from fractions import Fraction

class Scale:
    full, diatonic, accidental = [], [], []
    use_ratios = False
    degrees = 0
    
    #WAYS TO INIT:
    #  full = diatonic
    #  accidental = full - diatonic
    #  diatonic + accidental != full
    def __init__( self, diatonic, accidental = [] ):
        self.full, self.diatonic, self.accidental = [], [], []
        self.use_ratios = isinstance( diatonic[1], str ) or diatonic[1] < 2
        for i in diatonic:
            val = Fraction( i ) if self.use_ratios else i
            self.full.append( val )
            self.diatonic.append( val )
        for i in accidental:
            val = Fraction( i ) if self.use_ratios else i
            self.full.append( val )
            self.accidental.append( val )
        
        # if self.use_ratios:
            # for i, note in enumerate( full ):
                # full[i] = Fraction( note )

        self.degrees = len( self.full )
        self.is_diatonic = len( accidental ) > 0
        #accidental = full - diatonic
        # if len( accidental ) == 0:
            # self.accidental = self.full.copy()
            # for i in diatonic:
                # self.accidental.remove( i )
        #full = diatonic
        # else:
            # self.diatonic = full.copy()
            # self.accidental = []
        # if self.use_ratios:
            # for i, note in enumerate( diatonic ):
                # diatonic[i] = Fraction( note )
            # for i, note in enumerate( accidental ):
                # accidental[i] = Fraction( note )
