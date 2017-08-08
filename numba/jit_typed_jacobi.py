#!/usr/bin/env python
from __future__ import print_function

from builtins import range
import matplotlib.pyplot as plt
import numpy as np
import random, argparse, copy, time
from numba import *

# Timer class
class Timer:
  def __init__( self ):
    self.begin = 0
    self.end = 0

  def start( self ):
    self.begin = time.time()

  def stop( self ):
    self.end = time.time()

  def elapsed( self ):
    return self.end - self.begin

@jit(void(list(list(float64)),list(list(float64)),int64))
def jacobi_iteration( read, write, N ):
  #Iterate over inner (1..N)x(1..N) portion of grid
  for i in range( 1, N+1 ):
    for j in range( 1, N+1):
      # Jacobi stencil
      write[i][j] = (                read[i-1][j  ] + \
                    read[i  ][j-1] + read[i  ][j  ] + read[i  ][j+1] + \
                                     read[i+1][j  ] ) \
                    * (0.2)

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "-N", "--grid_size", type=int, default=100 )
  argparser.add_argument( "-T", "--time_steps", type=int, default=100 )
  argparser.add_argument( "-d", "--display", action='store_true' )
  args = argparser.parse_args()

  # Starting grid
  read = [ [ 0.0 for _ in range(args.grid_size+2)] for _ in range(args.grid_size+2)]

  # Make it 'hot; on the [0][_] side and cold on the [_][0] side and 'warm' on the [i][N-i] line
  for i in range(args.grid_size+2):
    read[0][i] = 100.0;
    read[i][0] = -100.0;
    read[i][args.grid_size+1-i] = 50.0

  # Write grid
  write = copy.deepcopy( read )

  if args.display:
    plt.matshow( read )

  timer = Timer()

  timer.start()
  # Outer time-stepping loop
  for t in range( args.time_steps ):
    jacobi_iteration( read, write, args.grid_size )

    # flip the read and write array
    write, read = read, write

  timer.stop()

  print( "Elapsed: {}s".format( timer.elapsed() ) )

  if args.display:
    plt.matshow( read )
    plt.show()

if __name__ == "__main__":
  main()
