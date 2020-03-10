#!/usr/bin/env python3

import argparse
import random

#-------------------------------------------------------------
if __name__ == "__main__":

    #parse command line    
    parser = argparse.ArgumentParser(description="\
    generates a point cloud around a straight line \
    and writes each point to the standard output")
    
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
    parser.add_argument("-s", "--sigma",
                        help="standard deviation of the y-coordinate predication error",
                        type=float,
                        default=0.01)
    parser.add_argument("-l", "--lowerBound",
                        help="minimal x-coordinate",
                        type=float,
                        default=0.)
    parser.add_argument("-u", "--upperBound",
                        help="maximal x-coordinate",
                        type=float,
                        default=5.)
    parser.add_argument("-w", "--visualize", help="show the scatter plot of the point cloud",
                        action="store_true")

    args = parser.parse_args()

    #creating data
    xList = []
    yList = []
    for _ in range(args.number):
        error = random.gauss(0, args.sigma)
        x = random.uniform(args.lowerBound, args.upperBound)
        xList.append(x)
        y = args.slope * x + args.intercept + error
        yList.append(y) 

    #output data
    for (x,y) in zip(xList, yList):
        print(x, y)
        
    #visualizing data
    if args.visualize:
        
        import matplotlib.pyplot as plt 

        plt.scatter(xList, yList, marker = '.') 
        plt.show() 
