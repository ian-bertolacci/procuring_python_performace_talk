#!/usr/bin/env python
from __future__ import print_function
from builtins import range
from collections import namedtuple
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import random, argparse, copy, time, multiprocessing

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

class jacobi_data_unit:
  def __init__( self, base_i, base_j, end_i, end_j, data ):
    self.base_i = base_i
    self.base_j = base_j
    self.end_i = end_i
    self.end_j = end_j
    self.data = data

def jacobi_work( work_unit ):
  read = work_unit.data
  i = work_unit.base_i
  j = work_unit.base_j
  end_i = work_unit.end_i
  end_j = work_unit.end_j

  new_data = (
        # middle
        read[i+1:end_i-1,j+1:end_j-1] +
        # i offsets
        read[i+2:end_i,j+1:end_j-1] +
        read[i:end_i-2,j+1:end_j-1] +
        # j offsets
        read[i+1:end_i-1,j+2:end_j] +
        read[i+1:end_i-1,j:end_j-2]
      ) * 0.2

  return jacobi_data_unit( work_unit.base_i, work_unit.base_j, work_unit.end_i, work_unit.end_j, new_data )

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "-N", "--grid_size", type=int, default=100 )
  argparser.add_argument( "-T", "--time_steps", type=int, default=100 )
  argparser.add_argument( "-d", "--display", action='store_true' )
  argparser.add_argument( "-p", "--processes", type=int, default=multiprocessing.cpu_count() )
  argparser.add_argument( "-b", "--block_size", type=int, default=-1 )
  args = argparser.parse_args()

  if args.block_size == -1:
    args.block_size = args.grid_size / args.processes

  # Starting grid
  read = np.zeros( (args.grid_size+2, args.grid_size+2 ) )

  # Make it 'hot; on the [0,_] side and cold on the [_,0] side and 'warm' on the [i,N-i] line
  for i in range(args.grid_size+2):
    read[0,i] = 100.0;
    read[i,0] = -100.0;
    read[i,args.grid_size+1-i] = 50.0

  # Write grid
  write = copy.deepcopy( read )

  if args.display:
    plt.matshow( read )

  pool = multiprocessing.Pool( args.processes )

  timer = Timer()

  timer.start()

  # Outer time-stepping loop
  for t in range( args.time_steps ):

    returned_data = pool.map(
      jacobi_work,
      map(
        lambda twople:
          jacobi_data_unit(
            twople[0], # base_i
            twople[1], # base_j
            min( twople[0] + args.block_size, args.grid_size+2),
            min( twople[1] + args.block_size, args.grid_size+2),
            read
          ),
        product( range(0,args.grid_size+2, args.block_size-2), range(0,args.grid_size+2, args.block_size-2) )
      )
    )

    for returned_unit in returned_data:
      write[returned_unit.base_i+1:returned_unit.end_i-1,returned_unit.base_j+1:returned_unit.end_j-1] = returned_unit.data

    # flip the read and write array
    write, read = read, write

  timer.stop()

  print( "Elapsed: {}s".format( timer.elapsed() ) )

  if args.display:
    plt.matshow( read )
    plt.show()

if __name__ == "__main__":
  main()
