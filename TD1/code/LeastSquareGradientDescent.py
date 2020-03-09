#!/usr/bin/env python3

import sys
import time
import argparse
import numpy

import LeastSquare2d
import GradientDescent

#-------------------------------------------------------------

def getArrayFromDataFile(path, delimiter):

    dataFile = open(path,'r')

    dataAsList = []
    for line in dataFile.readlines():
        data = [ float(s) for s in line.split(delimiter) ]
        if len(data) != 2:
            raise ValueError
        dataAsList.append( data )

    dataFile.close()
        
    return numpy.array( dataAsList )

#-------------------------------------------------------------

def nparray21toString(array):
    return "(" + str(array[0][0]) + "," + str(array[1][0]) + ")" 
    
#-------------------------------------------------------------
if __name__ == "__main__":

    #parse command line    
    parser = argparse.ArgumentParser(description="program that computes \
    the least-square optimal solution from a set of two observation by  \
    gradient descent")
    parser.add_argument("datafile",
                        help="path to a data file (containing 2 observations per line)")
    parser.add_argument("-d", "--delimiter",
                        help="delimiter used in the data file",
                        default=" ")
    parser.add_argument("-n", "--maxiters",
                        help="maximum number of iterations (also called epochs)",
                        type=int,
                        default=100)
    parser.add_argument("-e", "--epsilon",
                        help="desired precision of result",
                        type=float,
                        default=0.001)
    parser.add_argument("-x", "--x",
                        help="x-coordinate of the starting solution",
                        type=float,
                        default=0)
    parser.add_argument("-y", "--y",
                        help="y-coordinate of the starting solution",
                        type=float,
                        default=0)
    parser.add_argument("-m", "--method",
                        help="method to be used",
                        choices=["GivenStep", "NormalizedStep", "DecreasingStep", "Newton", "Momentum",
                                 "SGD", "SGDMomentum", "SGDMiniBatch", "RMSProp", "SGDRMSProp"],
                        default="GivenStep")
    parser.add_argument("-s", "--step",
                        help="step size multiplier (also called learning rate)",
                        type=float,
                        default=0.5)
    parser.add_argument("-a", "--alpha",
                        help="forgetting factor for momentum and RMSProp method (between 0 and 1)",
                        type=float,
                        default=0.5)
    parser.add_argument("-b", "--batchSize",
                        help="batch size for mini-batch method",
                        type=int,
                        default=32)
    parser.add_argument("-v", "--verbose", help="print to the standard output the successive solutions",
                        action="store_true")
    parser.add_argument("-w", "--visualize", help="show the path to the optimal solution",
                        action="store_true")

    args = parser.parse_args()
    
    #get data
    try: 
        array = getArrayFromDataFile(args.datafile, args.delimiter)
        nbRows, nbCols = array.shape
    except ValueError:
        print("Could not convert data; check the delimiter or the number and type of fields")
        sys.exit(1)
    except:
        print("Unexpected error while reading from the file")
        raise

    #function provider devoted to the least-square problem
    functionProvider = LeastSquare2d.LeastSquare2d(array)

    #analytical optimal solution
    optSol = functionProvider.analyticalOptimum()
    print( "#analytical minimum = ", nparray21toString(optSol) )

    #starting solution 
    startingSol = numpy.array([[args.x],[args.y]], dtype=float)
    
    #gradient descent methods
    if args.method == "GivenStep":
        computeNextSol = GradientDescent.nextByGivenStep(args.step)
    elif args.method == "NormalizedStep":
        computeNextSol = GradientDescent.nextByNormalizedStep(args.step)
    elif args.method == "DecreasingStep":
        computeNextSol = GradientDescent.nextByDecreasingStep(args.step)
    elif args.method == "Newton":
        computeNextSol = GradientDescent.nextByNewton(functionProvider.hessian)
    elif args.method == "Momentum" or args.method == "SGDMomentum":
        computeNextSol = GradientDescent.nextByMomentum(args.step, args.alpha)
    elif args.method == "RMSProp" or args.method == "SGDRMSProp":
        computeNextSol = GradientDescent.nextByRMSProp(args.step, args.alpha)
    elif args.method == "SGD" or args.method == "SGDMiniBatch":
        computeNextSol = GradientDescent.nextByGivenStep(args.step)
    else:
        print("Unknown method; use option -h")
        sys.exit(1)

        
    start_time = time.time()
    if args.method == "SGD" or args.method == "SGDMomentum": 
        sols = GradientDescent.sgd(args.maxiters,
                                   nbRows,
                                   functionProvider.oneGradient,
                                   startingSol,
                                   computeNextSol)
    elif args.method == "SGDMiniBatch":
        sols = GradientDescent.sgdMiniBatch(args.maxiters,
                                            args.batchSize,
                                            functionProvider,
                                            startingSol,
                                            computeNextSol)
    else: 
        sols = GradientDescent.gradientDescent(args.maxiters,
                                               args.epsilon,
                                               functionProvider.gradient,
                                               startingSol,
                                               computeNextSol)

    #print to standard output
    print( f"#{(len(sols)-1)} iterations, time {(time.time() - start_time)} seconds" )
    lastSol = sols[-1]
    print( f"#last solution = {nparray21toString(lastSol)}" )
    print( f"#grad norm = {numpy.linalg.norm(functionProvider.gradient(lastSol))}" )
    print( f"#dist to analytical minimum = {numpy.linalg.norm(lastSol - optSol)}" )

    if args.verbose:
        for (k,s) in enumerate(sols):
            print( k, nparray21toString(s) )

    #visualize
    if args.visualize:
         
        import matplotlib.pyplot as plt 

        plt.plot([s[0][0] for s in sols],
                 [s[1][0] for s in sols],
                 '.r-') 
        plt.show()
