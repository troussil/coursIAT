#!/usr/bin/env python3

import argparse
import random
import math

#-------------------------------------------------------------
def main():

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
                        default=1.)
    parser.add_argument("-b", "--intercept",
                        help="intercept of the straight line",
                        type=float,
                        default=0.)
    parser.add_argument("-m", "--minDistance",
                        help="minimal vertical distance to the straight line",
                        type=float,
                        default=0.5)
    parser.add_argument("-M", "--maxDistance",
                        help="maximal vertical distance to the straight line",
                        type=float,
                        default=3.5)
    parser.add_argument("-l", "--lowerBound",
                        help="minimal x-coordinate",
                        type=float,
                        default=-2.5)
    parser.add_argument("-u", "--upperBound",
                        help="maximal x-coordinate",
                        type=float,
                        default=2.5)
    parser.add_argument("-w", "--visualize", help="show the scatter plot of the point cloud",
                        action="store_true")
    args = parser.parse_args()

    #creating data
    data = []
    for _ in range(args.number):
        #take a random x-coordinate
        x = random.uniform(args.lowerBound, args.upperBound)
        #take a random label
        label = 1
        if random.gauss(0, 1) < 0:
            label = -1
        #compute the y-coordinate
        shift = label * random.uniform(args.minDistance, args.maxDistance)
        y = args.slope * x + args.intercept + shift
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
        plt.close()
        
#-------------------------------------------------------------
if __name__ == "__main__":
    main()
        
        
