#!/usr/bin/env python3

import sys
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
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument("datafile",
                        help="path to a data file (containing 2 observations per line)")
    parser.add_argument("-d", "--delimiter",
                        help="delimiter used in the data file",
                        default=" ")
    parser.add_argument("-n", "--maxiters",
                        help="maximum number of iterations",
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
                                 "SGD", "SGDMomentum", "SGDMiniBatch"],
                        default="GivenStep")
    parser.add_argument("-s", "--step",
                        help="step size multiplier (also called learning rate)",
                        type=float,
                        default=1)
    parser.add_argument("-a", "--alpha",
                        help="decay factor for momentum method (between 0 and 1)",
                        type=float,
                        default=0.5)
    parser.add_argument("-b", "--batchSize",
                        help="batch size for mini-batch method",
                        type=int,
                        default=32)

    args = parser.parse_args()

    #TODO check whether the values of the input parameters are valid or not
    
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

    #function provider (to solve the least square problem)
    functionProvider = LeastSquare2d.LeastSquare2d(array)

    #analytical optimal solution
    optSol = functionProvider.analyticalOptimum()
    print( "#analytical optimum = ", nparray21toString(optSol) )

    #starting solution 
    startingSol = numpy.array([[args.x],[args.y]], dtype=float)
    
    #gradient descent methods
    if args.method == "GivenStep":
        computeNextSol = GradientDescent.nextByGivenStep(args.step)
    elif args.method == "NormalizedStep":
        computeNextSol = GradientDescent.nextByNormalizedStep(args.step)
    elif args.method == "DecreasingStep":
        computeNextSol = GradientDescent.nextByDecreasingStep()
    elif args.method == "Newton":
        computeNextSol = GradientDescent.nextByNewton(functionProvider.hessian)
    elif args.method == "Momentum" or args.method == "SGDMomentum":
        computeNextSol = GradientDescent.nextByMomentum(args.step, args.alpha)
    elif args.method == "SGD" or args.method == "SGDMiniBatch":
        computeNextSol = GradientDescent.nextByGivenStep(args.step)
    else:
        print("Unknown method; use option -h")
        sys.exit(1)
    
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

    print( "#", (len(sols)-1), "iterations, last solution = ", nparray21toString(sols[-1]) )
    
#TODO
#(steepest),
#time, exemple
#documentation
