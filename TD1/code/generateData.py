#!/usr/bin/env python3

import sys
import argparse
import numpy

import matplotlib.pyplot as plt 

import LeastSquare2d

#-------------------------------------------------------------
if __name__ == "__main__":

    #parse command line    
    parser = argparse.ArgumentParser(description="\
    generate a point cloud around a straight line \
    and write each point to the standard output")
    
    parser.add_argument("-n", "--number",
                        help="number of samples",
                        type=int,
                        default=1000)
    parser.add_argument("-a", "--slope",
                        help="slope of the straight line",
                        type=float,
                        default=0.5)
    parser.add_argument("-b", "--intercept",
                        help="intercept of the straight line",
                        type=float,
                        default=0.)

    args = parser.parse_args()

    #creating data
    mean_u = 0
    var_u = 2
    cov_uv = var_u * args.slope
    mean_v = args.intercept + args.slope * mean_u
    var_v = 2 * cov_uv / var_u 

    mean = numpy.array([mean_u, mean_v])
    cov = numpy.array([[var_u, cov_uv], [cov_uv, var_v]]) 
    data = numpy.random.multivariate_normal(mean, cov, args.number) 

    #analytical optimal solution
    computer = LeastSquare2d.LeastSquare2d(data) 
    print(computer.analyticalOptimum())

    
    
    #visualising data 
    plt.scatter(data[:500, 0], data[:500, 1], marker = '.') 
    plt.show() 
