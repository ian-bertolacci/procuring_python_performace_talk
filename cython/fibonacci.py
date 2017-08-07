#!/usr/bin/env python
from __future__ import print_function

try:
  from builtins import range
except ImportError:
  list_range = range
  range = xrange

import argparse, time

# Cython import
from cython_fibonacci import *

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

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "-N", type=int, default=10 )
  argparser.add_argument( "--print_values", action="store_true")

  args = argparser.parse_args()

  timer = Timer()

  timer.start()
  iterative_values = [ fibonacci_iterative( i ) for i in range(args.N) ]
  timer.stop()

  print( "Iterative: {}s".format( timer.elapsed() ) )
  if args.print_values:
    print( iterative_values, "\n" )

  timer.start()
  iterative_values = [ fibonacci_recursive( i ) for i in range(args.N) ]
  timer.stop()

  print( "Recursive: {}s".format( timer.elapsed() ) )
  if args.print_values:
    print( iterative_values )


if __name__ == "__main__":
  main()
