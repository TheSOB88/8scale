from math import pow, log, exp, sin, cos, tan

def factor( a ):
    pass
    
def ratios( scale, i ):
    out = []
    i = scale[i]
    for j in scale:
        out.append( i/j if i>j else j/i )
    return out

