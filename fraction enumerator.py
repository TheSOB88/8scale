from fractions import Fraction as fr

def mixFactors( factors ):
  out = set()
  for i in factors:
    for j in factors:
      out.add( i * j )
  return out

primes = [1, 2, 3, 5, 7, 9, 11, 13, 17, 19]

comps = set( primes[0:2] )
comps = mixFactors( comps )
comps.add( primes[2] )
comps = mixFactors( comps )
comps.add( primes[3] )
comps.add( primes[4] )
comps.add( primes[5] )
comps = mixFactors( comps )

fractions = []
for i in comps:
  for j in comps:
    fractions.append( fr( i ) / j )
fractions.sort()

streng = ''
for i in fractions:
  streng += str( i.numerator ) + '/' + str( i.denominator ) + ', '

