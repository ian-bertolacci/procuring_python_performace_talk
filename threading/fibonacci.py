#!/usr/bin/env python
from __future__ import print_function

try:
  from builtins import range
except ImportError:
  list_range = range
  range = xrange

from Queue import Queue
import argparse, time, threading

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

def thread_wrapper( func, i, queue ):
  queue.put( (i, func(i) ) )

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
  argparser.add_argument( "--print_values", action="store_true")

  args = argparser.parse_args()

  timer = Timer()

  threads = []
  queue = Queue()

  timer.start()

  for i in range(args.N):
    thread = threading.Thread( target=thread_wrapper, args=(fibonacci_iterative, i,queue) )
    threads.append( thread )
    thread.start()

  for thread in threads:
    thread.join()

  timer.stop()

  print( "Iterative: {}s".format( timer.elapsed() ) )

  if args.print_values:
    # Collect and sort values from queue
    iterative_values = []
    while( not queue.empty() ):
      iterative_values.append( queue.get() )
    iterative_values = sorted( iterative_values, key=lambda twople: twople[0] )
    iterative_values = list( map( lambda twople: twople[1], iterative_values ) )
    print( iterative_values, "\n" )


  threads = []
  queue = Queue()

  timer.start()

  for i in range(args.N):
    thread = threading.Thread( target=thread_wrapper, args=(fibonacci_recursive, i, queue) )
    threads.append( thread )
    thread.start()

  for thread in threads:
    thread.join()

  timer.stop()

  print( "Recursive: {}s".format( timer.elapsed() ) )
  if args.print_values:
    # Collect and sort values from queue
    iterative_values = []
    while( not queue.empty() ):
      iterative_values.append( queue.get() )
    iterative_values = sorted( iterative_values, key=lambda twople: twople[0] )
    iterative_values = list( map( lambda twople: twople[1], iterative_values ) )
    print( iterative_values )


if __name__ == "__main__":
  main()
