
def jacobi( read, write, N):
  for i in range( 1, N+1 ):
    for j in range( 1, N+1 ):
      # Jacobi stencil
      write[i][j] = (                read[i-1][j  ] + \
                    read[i  ][j-1] + read[i  ][j  ] + read[i  ][j+1] + \
                                     read[i+1][j  ] ) \
                    * (1.0/5.0)
