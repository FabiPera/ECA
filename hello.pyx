import numpy as np
cimport numpy as np

DTYPE=np.uint8

ctypedef np.uint8_t DTYPE_t

def primes(int nb_primes):
  cdef int n, i, len_p
  cdef int p[1000]
  
  if(nb_primes > 1000):
    nb_primes=1000

  len_p=0  # The current number of elements in p.
  n=2
  while (len_p < nb_primes):
    # Is n prime?
    for i in p[:len_p]:
      if (n % i == 0):
        break
      # If no break occurred in the loop, we have a prime.
    else:
      p[len_p]=n
      len_p += 1
    n += 1

  # Let's return the result in a python list:
  result_as_list  = [prime for prime in p[:len_p]]
  
  return result_as_list

def intToBin(int n, int size):
  cdef np.ndarray a=np.zeros(size, dtype=DTYPE)
  cdef np.ndarray bits=np.zeros(size, dtype=DTYPE)
  cdef int i=0, j=0
  while(n):
    a[i]=n % 2;
    n //= 2;
    i += 1
  i -= 1

  while(j < size):
    if(i >= 0):
      bits[i]=a[i];
      i -= 1
    else:
      bits[j]=0;
    j += 1
			
  return bits