#!/usr/bin/env python3

import sys
import argparse
import random
import math
import numpy
import scipy.optimize

#-------------------------------------------------------------
class SolverError(Exception):
    pass

#-------------------------------------------------------------
def getSolution(c, A_ub, b_ub, A_eq, b_eq, bds):
    
    res = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub,
                                 A_eq=A_eq, b_eq=b_eq,
                                 bounds=bds,
                                 method='revised simplex')
    print(res)

    return res

#-------------------------------------------------------------
def getAndCheckSolution(c, A_ub, b_ub, A_eq, b_eq, bds):

    res = getSolution(c, A_ub, b_ub, A_eq, b_eq, bds)
    if res.success:
        return res.x
    else:
        raise SolverError        

#-------------------------------------------------------------
def getSolFromSubProblem(pointSet, c):
    
    nbRows = len(pointSet)
    
    #constraints
    #1d array
    b = numpy.array( [x**2 + y**2 for (x,y) in pointSet ] )
    assert(nbRows == b.shape[0])
    #2d array
    X = numpy.transpose(numpy.array( [-2*x for (x,_) in pointSet ], ndmin=2 ))
    assert(nbRows == X.shape[0])
    Y = numpy.transpose(numpy.array( [-2*y for (_,y) in pointSet ], ndmin=2 ))
    assert(nbRows == Y.shape[0])
    Rho = numpy.full( (nbRows,1), 1 )
    assert(nbRows == Rho.shape[0])
    A = numpy.concatenate( (X,Y,Rho), axis=1 )
    assert(nbRows == A.shape[0])

    #call to solver
    return getAndCheckSolution(c,A,b,None,None,None)

#-------------------------------------------------------------
def gradient(sol):
    return numpy.array( [2*sol[0], 2*sol[1], -sol[2]] )

#-------------------------------------------------------------
def toCircle(sol):
    r2 = sol[0]**2 + sol[1]**2 - sol[2]
    if r2 > 0: 
        return (sol[0], sol[1], math.sqrt(r2))
    else:
        raise ValueError
    

#-------------------------------------------------------------
def main():

    #parse command line    
    parser = argparse.ArgumentParser(description="program that computes \
    the smallest enclosing circle of a set of 2d points")
    parser.add_argument("-w", "--visualize", help="show the scatter plot of the data",
                        action="store_true")
    args = parser.parse_args()

    #constants
    n = 100 #number of points
    r = 100 #radius of the disc in which lie the generated points
    
    try:
        #input data generation
        pointSet = [] #point set (points are pairs of coordinates (x,y))
        random.seed()
        for i in range(n):
            accepted = False
            while not accepted: 
                x = random.random()*2*r
                y = random.random()*2*r
                if (x-r)**2 + (y-r)**2 <= r**2: 
                    accepted = True
            pointSet.append((x,y))

        # #initial solution
        # dmax = 0
        # for (x,y) in pointSet:
        #     d = x**2 + y**2
        #     if d > dmax:
        #         dmax = d
        # initialSol = numpy.array( [0,0,-dmax] )
        # print(initialSol, toCircle(initialSol))

        initialSol = numpy.array( [0,0,-1] )

        #solve
        sol = getSolFromSubProblem(pointSet, initialSol)
        #print(sol, toCircle(sol))

    except ValueError:
        print("Negative radius")
        sys.exit(1)        
    except SolverError:
        print("Could not solve the problem")
        sys.exit(1)        
    except:
        print("Unexpected error")
        raise

    #visualizing data
    if args.visualize:
        
        import matplotlib.pyplot as plt

        #data points
        x = [x for (x,_) in pointSet]
        y = [y for (_,y) in pointSet]
        plt.scatter(x, y, color = "red", marker = '+')
        #circles
        circle0 = plt.Circle((0, 0), math.sqrt(dmax), color='b', fill=False)
        circle = plt.Circle((r, r), r, color='r', fill=False)
        plt.gca().add_patch(circle0)
        plt.gca().add_patch(circle)
        #labels
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
        plt.close()
    
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
