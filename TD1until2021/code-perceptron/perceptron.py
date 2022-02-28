#!/usr/bin/env python3

import sys
import statistics
import argparse
import numpy

#-------------------------------------------------------------
def learning(learningSet, learningRate):
    """ Function that learns the weights and bias of a perceptron
    from a given learning set.

    :param: learningSet, list of tuples (x1,x2,y), where x1 and x2
    are the components of the input vector and y is the output
    :param: learningRate, learning rate
    :return: the weight (as a 2d numpy array) and the bias
    """
    #weigts = numpy vector of two components
    w = numpy.array([[0.0],[0.0]])
    #bias = scalar
    b = 1.0
    #learning loop
    c = 1
    flagCont = True
    while flagCont:
        print("#{}".format(c))
        flagCont = False
        for (x1, x2, y) in learningSet:
            x = numpy.array([[x1],[x2]])
            if y*(numpy.dot(w.T,x)+b) < 0:
                w += learningRate*y*x
                b += learningRate*y
                flagCont = True
        c += 1
    return w, b
        
#-------------------------------------------------------------
def getArrayFromDataFile(path, delimiter):
    """ Function that reads a file composed of lines containing
    at least three fields and returns a list containing the values
    of the three first fields.
 
    :param: path, path to the file to read
    :param: delimiter, character used to delimit the fields
    :return: a list of tuple (x1,x2,y) where x1 and x2 are floats
    and y is an integer either equal to 1 or -1. 
    """

    dataFile = open(path,'r')

    dataSetAsList = []
    for line in dataFile.readlines():
        fields = line.split(delimiter)
        if len(fields) != 3:
            raise ValueError
        x1 = float(fields[0])
        x2 = float(fields[1])
        y = int(fields[2])
        if y != 1 and y != -1:
            raise ValueError
        dataSetAsList.append( (x1,x2,y) )

    dataFile.close()

    return dataSetAsList

#-------------------------------------------------------------
def main():

    #parse command line    
    parser = argparse.ArgumentParser(description="program that computes \
    the straight line that separates one set of positive observations \
    and one set of negative observations (if the two sets are linearly \
    separable)")
    parser.add_argument("datafile",
                        help="path to a data file containing 3 fields per line: x y {-1,1}")
    parser.add_argument("-d", "--delimiter",
                        help="delimiter used in the data file",
                        default=" ")
    parser.add_argument("-w", "--visualize", help="show the scatter plot of the data",
                        action="store_true")
    parser.add_argument("-r", "--learningRate", type=float, default=0.5,  
                        help="learning rate")
    args = parser.parse_args()

    #get data, then solution
    try:
        
        learningSet = getArrayFromDataFile(args.datafile, args.delimiter)
        weights, bias = learning(learningSet, args.learningRate)
        print("#Perceptron weights = {} and bias = {}".format(weights, bias))
        
    except ValueError:
        print("Could not convert data; check the delimiter or the number and type of fields")
        sys.exit(1)
    except:
        print("Unexpected error while reading from the file")
        raise

    #visualizing data
    if args.visualize:
        
        import matplotlib.pyplot as plt

        #data points
        plt.scatter([x for (x,_,l) in learningSet if l == 1],
                    [y for (_,y,l) in learningSet if l == 1], marker = '+') 
        plt.scatter([x for (x,_,l) in learningSet if l == -1],
                    [y for (_,y,l) in learningSet if l == -1], marker = '.') 

        #separating line
        a = - weights[0] / weights[1]
        b = - bias / weights[1]
        xmin = min([x for (x,_,_) in learningSet])
        xmax = max([x for (x,_,_) in learningSet])
        x1 = numpy.linspace(xmin,xmax,100)
        x2 = a*x1+b
        plt.plot(x1, x2, "-r", label="x2={}x1+{}".format(a,b))
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.legend(loc="upper left")
        plt.show()
        plt.close()
    
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
