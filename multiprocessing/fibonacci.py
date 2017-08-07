#!/usr/bin/env python
from __future__ import print_function

try:
  from builtins import range
except ImportError:
  list_range = range
  range = xrange

import argparse, time, multiprocessing

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

def fibonacci_recursive( i ):
  if i <= 1:
    return i
  else:
    return fibonacci_recursive( i-1 ) + fibonacci_recursive( i-2 )


def fibonacci_iterative( i ):
  if i <= 1:
    return i
  n_0 = 0
  n_1 = 1
  f_i = 1
  for i in range(1,i):
    f_i = n_0 + n_1
    n_0 = n_1
    n_1 = f_i
  return f_i

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "-N", type=int, default=10 )
  argparser.add_argument( "-p", "--processes", type=int, default=multiprocessing.cpu_count() )
  argparser.add_argument( "--print_values", action="store_true")

  args = argparser.parse_args()

  timer = Timer()

  pool = multiprocessing.Pool( args.processes )

  timer.start()

  iterative_values = pool.map(
    fibonacci_recursive,
    range(args.N)
  )
  timer.stop()

  print( "Iterative: {}s".format( timer.elapsed() ) )
  if args.print_values:
    print( iterative_values, "\n" )

  timer.start()
  iterative_values = pool.map(
    fibonacci_recursive,
    range(args.N)
  )
  timer.stop()

  print( "Recursive: {}s".format( timer.elapsed() ) )
  if args.print_values:
    print( iterative_values )


if __name__ == "__main__":
  main()
