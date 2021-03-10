#!/usr/bin/env python3

import numpy
import scipy.optimize

#-------------------------------------------------------------
def exempleStandardForm():
    A = numpy.array([[0,0,0,1,0,0],
                     [-1,1,1,0,1,0],
                     [1,1,-1,0,0,1]])
    b = numpy.array([1,0,1])
    c = numpy.array([-1,1,1,1,0,0])
    return (c,None,None,A,b,None)

#-------------------------------------------------------------
def exempleCanonicForm():
    A = numpy.array([[-1,1],
                     [0,-1],
                     [1,1]])
    b = numpy.array([0,0,1])
    c = numpy.array([-1,1])
    bds = [(-numpy.inf,numpy.inf), (-numpy.inf,numpy.inf)]
    return (c,A,b,None,None,bds)

#-------------------------------------------------------------
def findSolution(c, A_ub, b_ub, A_eq, b_eq, bds):
    
    res = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub,
                                 A_eq=A_eq, b_eq=b_eq,
                                 bounds=bds,
                                 options={'bland':True})
    print(res)

    if res.success:
        sol  = "(" + str(res.x[0]) + "," + str(res.x[1]) + ")"
        print("=> optimal solution found", sol)
        print()

#-------------------------------------------------------------
def main():

    findSolution(*exempleStandardForm())
    findSolution(*exempleCanonicForm())
        
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
