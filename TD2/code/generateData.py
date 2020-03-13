#!/usr/bin/env python3

import argparse
import random
import math

#-------------------------------------------------------------
if __name__ == "__main__":

    #parse command line    
    parser = argparse.ArgumentParser(description="\
    generates a point cloud around a straight line \
    and writes each point to the standard output")
    
    parser.add_argument("-n", "--number",
                        help="number of samples",
                        type=int,
                        default=500)
    parser.add_argument("-a", "--slope",
                        help="slope of the straight line",
                        type=float,
                        default=0.5)
    parser.add_argument("-b", "--intercept",
                        help="intercept of the straight line",
                        type=float,
                        default=0.)
    parser.add_argument("-d", "--maxDistance",
                        help="maximal orthogonal distance to the straight line",
                        type=float,
                        default=3.)
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
    data = []
    for _ in range(args.number):
        #take a random point on the straight line
        x = random.uniform(args.lowerBound, args.upperBound)
        y = args.slope * x + args.intercept
        #shift it along the orthogonal direction
        orthDirNorm = math.sqrt(args.slope**2 + 1)
        label = 1
        if random.gauss(0, 1) < 0:
            label = -1
        shift = label * random.uniform(0, args.maxDistance)
        x += -args.slope * shift / orthDirNorm 
        y += shift / orthDirNorm
        #store the point
        data.append( (x,y,label) ) 

    #output data
    for (x, y, label) in data:
        print(x, y, label)
        
    #visualizing data
    if args.visualize:
        
        import matplotlib.pyplot as plt 

        plt.scatter([x for (x,_,l) in data if l == 1],
                    [y for (_,y,l) in data if l == 1], marker = '+') 
        plt.scatter([x for (x,_,l) in data if l == -1],
                    [y for (_,y,l) in data if l == -1], marker = '.') 
        plt.show() 
