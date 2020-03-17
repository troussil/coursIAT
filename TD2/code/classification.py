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
                                 options={'bland':True,
                                          'tol':1.0e-15})
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
def getSolFromTwoDataSetsL1(s1, s2):

    """ you must write the code that calls
    'getAndCheckSolution' to get an 
    optimal solution that will be returned
    as a pair of coordinates. 
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
def getArrayFromDataFile(path, delimiter):

    dataFile = open(path,'r')

    dataSet1AsList = []
    dataSet2AsList = []
    for line in dataFile.readlines():
        fields = line.split(delimiter)
        if len(fields) != 3:
            raise ValueError
        x = float(fields[0])
        y = float(fields[1])
        mark = int(fields[2])
        if mark == 1: 
            dataSet1AsList.append( (x,y) )
        elif mark == -1:
            dataSet2AsList.append( (x,y) )
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
    parser.add_argument("-w", "--visualize", help="show the scatter plot of the data",
                        action="store_true")
    args = parser.parse_args()

    #get data, then solution
    try:
        s1, s2 = getArrayFromDataFile(args.datafile, args.delimiter)
        xstar = getSolFromTwoDataSetsL1(s1,s2)
        
        print("minimal solution =", xstar)
        
    except ValueError:
        print("Could not convert data; check the delimiter or the number and type of fields")
        sys.exit(1)
    except SolverError:
        print("Could not solve the problem; check the data or the program!")
        sys.exit(1)
    except:
        print("Unexpected error while reading from the file")
        raise


    #visualizing data
    if args.visualize:
        
        import matplotlib.pyplot as plt
        
        xpos = [x for (x,_) in s1]
        ypos = [y for (_,y) in s1]
        xneg = [x for (x,_) in s2]
        yneg = [y for (_,y) in s2]
        plt.axis('equal')
        plt.scatter(xpos, ypos, marker = '+') 
        plt.scatter(xneg, yneg, marker = '.')
        
        xbar = statistics.mean(xpos+xneg)
        ybar = statistics.mean(ypos+yneg)
        plt.arrow(xbar,ybar,xstar[0],xstar[1],
                  width=0.01, head_width=0.1,
                  length_includes_head=True,
                  overhang=0)
        plt.show()
        plt.close()

    
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
