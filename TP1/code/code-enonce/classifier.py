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
    """ TODO
    you must write the code that calls
    'getAndCheckSolution' to get an 
    optimal solution. 
    The input parameters of the function 
    'getAndCheckSolution' must be deduced
    from s1 and s2, two numpy arrays for 
    the set of positive and negative 
    observations respectively. """

    """ 
    Useful fields and methods to use 
    numpy arrays: 
    .shape
    array
    zeros
    ones
    full
    concatenate
    ...
    see
    https://docs.scipy.org/doc/numpy/reference/routines.array-creation.html
    https://docs.scipy.org/doc/numpy/reference/routines.array-manipulation.html
    """
    return None
    
#-------------------------------------------------------------
def getSolFromTwoDataSetsLinf(s1, s2):
    """
    TODO see getSolFromTwoDataSetsL1
    """
    return None

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
        
