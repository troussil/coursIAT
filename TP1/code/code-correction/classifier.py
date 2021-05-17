#!/usr/bin/env python3

import sys
import statistics
import argparse
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
def getSolFromTwoDataSets(s1, s2, norm):
    if norm == "L1":
        return getSolFromTwoDataSetsL1(s1, s2)
    elif norm == "Linf":
        return getSolFromTwoDataSetsLinf(s1,s2)
    else:
        raise ValueError()
    
#-------------------------------------------------------------
def getSolFromTwoDataSetsL1(s1, s2):

    nbRowsS1, _ = s1.shape
    nbRowsS2, _ = s2.shape

    #1d arrays
    c = numpy.array([0,0,0,0,-1,1])
    b = numpy.zeros(nbRowsS1 + nbRowsS2 + 1)
    b[-1] = 1

    #2d array
    zp_top = numpy.full( (nbRowsS1,1), 1 )
    zm_top = numpy.zeros( (nbRowsS1,1) )
    A_top = numpy.concatenate( (-s1, s1, zp_top, zm_top), axis=1 )
    zp_bot = numpy.zeros( (nbRowsS2,1) )
    zm_bot = numpy.full( (nbRowsS2,1), -1 )
    A_bot = numpy.concatenate( (s2, -s2, zp_bot, zm_bot), axis=1 )
    L1constraint = numpy.array([[1,1,1,1,0,0]])
    A = numpy.concatenate( (A_top, A_bot, L1constraint), axis=0 )
    
    #bounds
    rpos = (0,numpy.inf)
    r = (-numpy.inf,numpy.inf)
    bounds = [rpos, rpos, rpos, rpos, r, r]

    sol = getAndCheckSolution(c,A,b,None,None,bounds)
    return numpy.array([sol[0] - sol[2], sol[1] - sol[3], sol[4], sol[5]])
    
#-------------------------------------------------------------
def getSolFromTwoDataSetsLinf(s1, s2):
    
    nbRowsS1, _ = s1.shape
    nbRowsS2, _ = s2.shape

    #1d arrays
    c = numpy.array([0,0,-1,1])
    b = numpy.zeros(nbRowsS1 + nbRowsS2)
    
    #2d array
    zp_top = numpy.full( (nbRowsS1,1), 1 )
    zm_top = numpy.zeros( (nbRowsS1,1) )
    A_top = numpy.concatenate( (-s1, zp_top, zm_top), axis=1 )
    zp_bot = numpy.zeros( (nbRowsS2,1) )
    zm_bot = numpy.full( (nbRowsS2,1), -1 )
    A_bot = numpy.concatenate( (s2, zp_bot, zm_bot), axis=1 )
    A = numpy.concatenate( (A_top, A_bot), axis=0 )
    
    #bounds
    r1 = (-1,1)
    r = (-numpy.inf,numpy.inf)
    bounds = [r1, r1, r, r]

    sol = getAndCheckSolution(c,A,b,None,None,bounds)
    return numpy.array([sol[0], sol[1], sol[2], sol[3]])

#-------------------------------------------------------------
def getArrayFromDataFile(path, delimiter):

    dataFile = open(path,'r')

    dataSet1AsList = []
    dataSet2AsList = []
    for line in dataFile.readlines():
        fields = line.split(delimiter)
        if len(fields) != 3:
                    raise ValueError
        x1 = float(fields[0])
        x2 = float(fields[1])
        mark = int(fields[2])
        if mark == 1: 
            dataSet1AsList.append( (x1,x2) )
        elif mark == -1:
            dataSet2AsList.append( (x1,x2) )
        else:
            raise ValueError

    dataFile.close()
        
    return ( numpy.array( dataSet1AsList ),
             numpy.array( dataSet2AsList ) )

#-------------------------------------------------------------
def main():

    #parse command line    
    parser = argparse.ArgumentParser(description="program that computes \
    the straight line that separates one set of positive observations \
    and one set of negative observations (if the two sets are linearly \
    separable)")
    parser.add_argument("datafile",
                        help="path to a data file containing 3 fields per line: x, y {-1,1}")
    parser.add_argument("-d", "--delimiter",
                        help="delimiter used in the data file",
                        default=" ")
    parser.add_argument("-n", "--norm",help="norm used to normalize the optimization problem",
                    choices=["L1","Linf"],default="L1")
    parser.add_argument("-w", "--visualize", help="show the scatter plot of the data",
                        action="store_true")
    args = parser.parse_args()

    #get data, then solution
    try:
        s1, s2 = getArrayFromDataFile(args.datafile, args.delimiter)
        x1, x2, zp, zm = getSolFromTwoDataSets(s1,s2,args.norm)
        x = numpy.array([x1, x2])
        print("#final solution={}".format(x))
        l1 = numpy.linalg.norm(x, 1)
        l2 = numpy.linalg.norm(x)
        linf = numpy.linalg.norm(x, numpy.inf)
        print("#norm: L1 {} L2 {} Linf {} ".format(l1, l2, linf))
        print("#margin: {}".format( (zp-zm)/l2 ))
        
    except ValueError:
        print("Could not convert data")
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
        xpos = [x for (x,_) in s1]
        ypos = [y for (_,y) in s1]
        xneg = [x for (x,_) in s2]
        yneg = [y for (_,y) in s2]
        plt.scatter(xpos, ypos, color = "red", marker = '+') 
        plt.scatter(xneg, yneg, color = "blue", marker = '.')
        
        #separating lines
        if x2 != 0: 
            a = - x1 / x2
            bpos = zp / x2
            bneg = zm / x2
            xmin = min(xpos + xneg)
            xmax = max(xpos + xneg)
            p1 = numpy.linspace(xmin,xmax,100)
            p2pos = a*p1+bpos
            plt.plot(p1, p2pos, "-r")
            p2neg = a*p1+bneg
            plt.plot(p1, p2neg, "-b")
            
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.show()
        plt.close()
    
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
