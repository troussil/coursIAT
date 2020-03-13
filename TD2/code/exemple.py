#!/usr/bin/env python3

import numpy
import scipy.optimize

#-------------------------------------------------------------
def exemple():
    A = numpy.array([[0,0,0,1,0,0],
                     [-1,1,1,0,1,0],
                     [1,1,-1,0,0,1]])
    b = numpy.array([1,0,0])
    c = numpy.array([-1,1,1,1,0,0])
    return (A,b,c)

#-------------------------------------------------------------
def main():

    A, b, c = exemple()
    res = scipy.optimize.linprog(c, A_eq=A, b_eq=b, options={'bland':True})
    print(res)

    x = numpy.array([1,0,1,1,0,0])
    print( c.dot(x) )
    print(A)
    print(A.dot(x), b)

    if res.success:
        print("#optimal solution",res.x)

        
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
