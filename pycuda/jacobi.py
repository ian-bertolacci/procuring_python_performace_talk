#!/usr/bin/env python
from __future__ import print_function
from builtins import range
import matplotlib.pyplot as plt
import numpy as np
import random, argparse, copy, time, math
import pycuda.autoinit
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule

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

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "-N", "--grid_size", type=int, default=100 )
  argparser.add_argument( "-T", "--time_steps", type=int, default=100 )
  argparser.add_argument( "-d", "--display", action='store_true' )
  args = argparser.parse_args()

  # Starting grid
  read = np.zeros( (args.grid_size+2, args.grid_size+2 ) ).astype( np.float32 )

  # Make it 'hot; on the [0,_] side and cold on the [_,0] side and 'warm' on the [i,N-i] line
  for i in range(args.grid_size+2):
    read[0,i] = 100.0;
    read[i,0] = -100.0;
    read[i,args.grid_size+1-i] = 50.0

  # Write grid
  write = copy.deepcopy( read )

  if args.display:
    pass
    #plt.matshow( read )


  module = SourceModule("""
  __global__ void jacobi(float *read, float *write, int N, int leading_dim){
    const int i = (blockIdx.x * blockDim.x + threadIdx.x)+1;
    const int j = (blockIdx.y * blockDim.y + threadIdx.y)+1;
    if( 1 <= i && i <= N && 1 <= j && j <= N ){
      write[i + j*leading_dim] = (      read[(i  )+(j-1)*leading_dim] +
        read[(i-1)+(j  )*leading_dim] + read[(i  )+(j  )*leading_dim] + read[(i+1)+(j  )*leading_dim] +
                                        read[(i  )+(j+1)*leading_dim] ) * (0.2) ;
    }
  }
  """)

  jacobi = module.get_function("jacobi")
  row_memory_size = np.int32(args.grid_size+2)
  N = np.int32(args.grid_size)
  block_size = min( 32, args.grid_size )
  grid_size = int(math.ceil(float(args.grid_size)/block_size))

  print( "Block size: {}\nGrid Size: {}".format(block_size, grid_size) )
  timer = Timer()

  timer.start()

  gpu_read = gpuarray.to_gpu( read )
  gpu_write = gpuarray.to_gpu( write )

  # Outer time-stepping loop
  for t in range( args.time_steps ):

    jacobi( gpu_read, gpu_write, N, row_memory_size, block=(block_size,block_size,1), grid=(grid_size,grid_size,1) )

    # flip the read and write array
    gpu_write, gpu_read = gpu_read, gpu_write

  read = gpu_read.get()
  timer.stop()

  print( "Elapsed: {}s".format( timer.elapsed() ) )

  if args.display:
    plt.matshow( read )
    plt.show()

if __name__ == "__main__":
  main()
