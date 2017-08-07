def fibonacci_recursive( i ):
  if i <= 1:
    return i
  else:
    return fibonacci_recursive( i-1 ) + fibonacci_recursive( i-2 )

def fibonacci_iterative( i ):
  if i <= 1:
    return i
  cdef int n_0 = 0
  cdef int n_1 = 1
  cdef f_i = 1
  for i in range(1,i):
    f_i = n_0 + n_1
    n_0 = n_1
    n_1 = f_i
  return f_i
