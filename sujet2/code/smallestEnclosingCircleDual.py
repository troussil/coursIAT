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
def getSolFromSubProblem(pointSet, sol):
    
    nbCols = len(pointSet)

    #objective function
    #warning: opposite sign to get max instead of min
    lst = []
    for i, p in enumerate(pointSet):
        sumTerm = 0
        for j, q in enumerate(pointSet):
            if j != i: 
                sumTerm += 2*sol[j]*(p[0]*q[0]+p[1]*q[1])
        lst.append( - (p[0]**2 + p[1]**2)*(1-2*sol[i]) + sumTerm )
    c = numpy.array( lst )
    print("#c", c)
    
    #constraints
    #1d array
    b = numpy.array( [1] )
    #2d array
    A = numpy.array( [ [1]*nbCols ] )

    #bounds
    bounds = (0, None) #applies to all variables
    
    #call to solver
    return getAndCheckSolution(c,None,None,A,b,bounds)

#-------------------------------------------------------------
def getSolByFrankWolfe(pointSet, sol, nbSteps = 50):

    currentSol = sol
    
    k = 1
    while k <= nbSteps:
        print("#step {}".format(k))
        s = getSolFromSubProblem(pointSet, currentSol)
        alpha = 2/(k+2)
        currentSol = currentSol + alpha*(s - currentSol)
        print(alpha)
        print(currentSol)
        k += 1

    return currentSol

#-------------------------------------------------------------
def farthestFromPoint(pointSet, pointIdx):

    point = pointSet[pointIdx]
    
    dmax = 0
    imax = pointIdx
    for i, p in enumerate(pointSet):
        d = (p[0]-point[0])**2 + (p[1]-point[1])**2
        if d > dmax:
            dmax = d
            imax = i

    return imax
            
#-------------------------------------------------------------
def getInitialSolution(pointSet):

    i1 = farthestFromPoint(pointSet, 0)
    i2 = farthestFromPoint(pointSet, i1)
    
    initialSol = numpy.zeros( len(pointSet) )
    #initialSol[i1] = 0.5
    #initialSol[i2] = 0.5
    initialSol[0] = 1

    return initialSol

#-------------------------------------------------------------
def getParameters(pointSet, sol):

    part1 = 0
    cx = cy = 0
    for i, p in enumerate(pointSet):
        part1 += sol[i]*(p[0]**2 + p[1]**2)
        cx += sol[i]*p[0]
        cy += sol[i]*p[1]

    part2 = cx**2 + cy**2

    #x-coordinate, y-coordinate of the center and squared radius
    return (cx, cy, part1-part2)

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

        #-----------------------------------
        #function
        def phi(u):
            part1 = 0
            cx = cy = 0
            for i, p in enumerate(pointSet):
                part1 += u[i]*(p[0]**2 + p[1]**2)
                cx += u[i]*p[0]
                cy += u[i]*p[1]

            part2 = cx**2 + cy**2
            return part1-part2
        
        def phi2(u):
            part1 = 0
            for i, p in enumerate(pointSet):
                part1 += u[i]*(p[0]**2 + p[1]**2)

            part2 = 0
            for j1, p1 in enumerate(pointSet):
                for j2, p2 in enumerate(pointSet):
                    part2 += u[j1]*u[j2] \
                        *(p1[0]*p2[0] + p1[1]*p2[1])
                    
            return part1-part2
            
        # #gradient
        # lst = []
        # for i, p in enumerate(pointSet):
        #     sumTerm = 0
        #     for j, q in enumerate(pointSet):
        #         if j != i: 
        #             sumTerm += 2*sol[j]*(p[0]*q[0]+p[1]*q[1])
        #     lst.append( (p[0]**2 + p[1]**2)*(1-sol[i]) - sumTerm )
        # c = numpy.array( lst )
        # print("#c", c)


        #-----------------------------------
    

        #initial solution
        sol = getInitialSolution(pointSet)
        print(sol, phi(sol), phi2(sol))
        assert(abs(phi(sol) - phi2(sol)) < 0.001)
        cx, cy, r2 = getParameters(pointSet, sol)
        print("#cx={}, cy={}, r={}, r^2={}".format(cx, cy, math.sqrt(r2), r2))
        #solve
        sol = getSolByFrankWolfe(pointSet, sol)
        print(sol, phi(sol), phi2(sol))
        assert(abs(phi(sol) - phi2(sol)) < 0.001)
        cx, cy, r2 = getParameters(pointSet, sol)
        print("#cx={}, cy={}, r={}, r^2={}".format(cx, cy, math.sqrt(r2), r2))

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
        
        #generating circle
        circle = plt.Circle((r, r), r, color='r', fill=False)
        plt.gca().add_patch(circle)
        
        #computed solution
        cx, cy, r2 = getParameters(pointSet, sol)
        print("#cx={}, cy={}, r={}, r^2={}".format(cx, cy, math.sqrt(r2), r2))
        circleSol = plt.Circle((cx, cy), math.sqrt(r2), color='b', fill=False)
        plt.gca().add_patch(circleSol)
        
        #labels
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
        plt.close()
    
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
