class Scale:
    full, diatonic, accidental = [], [], []
    use_ratios = False
    
    
    #WAYS TO INIT:
    #  full = diatonic
    #  accidental = full - diatonic
    #  diatonic + accidental != full
    def __init__( self, full, diatonic = None, accidental = None ):
        self.full = full
        if diatonic is not None:
            self.diatonic = diatonic
            #  diatonic + accidental != full
            if accidental is not None:
                self.accidental = accidental
                for i in accidental:
                    if i not in full:
                        full.append( i )
            #accidental = full - diatonic
            else:
                self.accidental = full.copy()
                for i in diatonic:
                    self.accidental.remove( i )
        #full = diatonic
        else:
            self.diatonic = full.copy()
            self.accidental = []
        
        self.use_ratios = full[1] < 2