#!/usr/bin/env python3

from math import sqrt
import numpy as np

#-------------------------------------------------------------
def distance(a, b):
    x1 = a[0]-b[0]
    x2 = a[1]-b[1]
    return sqrt(x1*x1 + x2*x2)

#-------------------------------------------------------------
def main():
    #description of Philadelphia instances
    #see http://fap.zib.de/problems/Philadelphia/
    
    #nodes of the network structure
    #basis vectors
    e1 = np.array([1,0])
    e2 = np.array([1/2.0,sqrt(3)/2.0])
    #line by line definition
    nodes = [] + \
        [ np.array([k,0]) for k in range(5) ] + \
        [ np.array([k,0])-e2-e1 for k in range(7) ] + \
        [ np.array([k,0])-2*e2-e1 for k in range(6) ] + \
        [ np.array([k,0])-3*e2+2*e1 for k in range(3) ]
    
    #reuse distances
    seqs = [ [2*sqrt(3), sqrt(3), 1, 1, 1, 0],
             [sqrt(7), sqrt(3), 1, 1, 1, 0],
             [2*sqrt(3), 2, 1, 1, 1, 0] ]
    
    #matrices
    for s in seqs: 
        for v1 in nodes:
            for v2 in nodes:
                d = distance(v1,v2)
                for k, threshold in enumerate(s):
                    if d >= threshold:
                        print("{} ".format(k), end="")
                        break
            print()
        print()
        print()
    
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
