#!/usr/bin/env python3

#****************************************************************************
# A simple script for testing the effect of numba on the creation of 
# pseudo-random numbers in python.
#
# Usage: ./numba_test.py <number of iterations>
#****************************************************************************

import sys
import numpy
from numba import jit
from timeit import default_timer as timer
from random import randint

def no_numba(iterations):
    for i in range(0, iterations):
        rando = randint(0, 128)

@jit(nopython=True)
def with_numba(iterations):
    for i in range(0, iterations):
        rando2 = randint(0, 128)

def with_numpy(iterations):
    for i in range(0, iterations):
        rando3 = numpy.random.randint(0,128)

@jit(nopython=True)
def with_numba_numpy(iterations):
    for i in range(0, iterations):
        rando4 = numpy.random.randint(0,128)

if __name__ == "__main__":
    num_iterations = int(sys.argv[1])

    # Without numba
    start = timer()
    no_numba(num_iterations)
    end = timer()
    elapsed = end - start
    print(f"Without numba: {num_iterations} calls took {elapsed} seconds.")
    
    # With numba
    start = timer()
    with_numba(num_iterations)
    end = timer()
    elapsed = end - start
    print(f"With numba: {num_iterations} calls took {elapsed} seconds.")

    # Without numba but with numpy
    start = timer()
    with_numpy(num_iterations)
    end = timer()
    elapsed = end - start
    print(f"Without numba but using numpy: {num_iterations} calls took {elapsed} seconds.")

    # With numba and numpy
    start = timer()
    with_numba_numpy(num_iterations)
    end = timer()
    elapsed = end - start
    print(f"With numba and numpy: {num_iterations} calls took {elapsed} seconds.")