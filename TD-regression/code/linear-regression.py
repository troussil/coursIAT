#!/usr/bin/env python3

import sys
import argparse
import torch
# see for help about pytorch
# https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html

#-------------------------------------------------------------
def getTensorsFromDataFile(path):
    """ Function that reads a file composed of lines containing
    two fields and returns a list containing the values of the 
    two fields.
 
    :param: path, path to the file to read
    :return: a list of tuples (x,y) where x and y are floats.
    """

    # read file
    delimiter = " "
    dataFile = open(path,'r')

    xAsList = []
    yAsList = []
    for line in dataFile.readlines():
        fields = line.split(delimiter)
        if len(fields) != 2:
            raise ValueError
        xAsList.append( float(fields[0]) )
        yAsList.append( float(fields[1]) )

    dataFile.close()

    # create and return tensors
    xData = torch.tensor(xAsList)
    xOnes = torch.ones_like(xData)
    x = torch.stack( (xData, xOnes) )

    y = torch.tensor([yAsList])
    
    return (x, y)

#-------------------------------------------------------------
class LinearModel(object):

    def __init__(self):
        self.w = torch.rand(1,2, requires_grad=True)

    def forward(self, x):
        return torch.matmul(self.w, x)

    def update(self, lr):
        # disable gradient computation for the update
        with torch.no_grad():
            self.w -= lr * self.w.grad

        #reset gradient to zero
        self.w.grad.zero_() 

    def evaluate(self, x):
        with torch.no_grad():
            return self.forward(x)    

    def __repr__(self):
        return f"({self.w[0][0]:.4f}, {self.w[0][1]:.4f})"
        
#-------------------------------------------------------------
def mse(y_pred, y_true):
    return ((y_pred - y_true) ** 2).mean()

#-------------------------------------------------------------
if __name__ == "__main__":
        
    #-------------------------------------------------------------
    # parse command line    
    parser = argparse.ArgumentParser(description="program that computes \
    the regression line that fits the data points")
    parser.add_argument("datafile",
                        help="path to a data file containing two fields \
                        per line: x y")
    parser.add_argument("-n", "--nbEpochs",   
                        help="maximal number of epochs",
                        type=int, default=100)
    parser.add_argument("-r", "--learningRate",   
                        help="learning rate",
                        type=float, default=0.01)
    parser.add_argument("-v", "--visualize",
                        help="show data and model",
                        action="store_true")
    args = parser.parse_args()

    #-------------------------------------------------------------
    # read data        
    x, y = getTensorsFromDataFile(args.datafile)

    #-------------------------------------------------------------
    # learn model by gradient descent
    model = LinearModel()
    
    for epoch in range(args.nbEpochs):

        y_pred = model.forward(x)
        loss = mse(y_pred, y)
        loss.backward() #backpropagation to compute the gradient
        model.update(args.learningRate) #update model paramaters

        # display
        if epoch % 10 == 0:
            print(f"# {epoch}: Loss = {loss.item():.4f}", end=", ")
            print(model)

    #-------------------------------------------------------------
    # visualize data and model
    if args.visualize:
        
        y_pred = model.evaluate(x)
        
        import matplotlib.pyplot as plt

        plt.scatter(x[0], y[0], label="Data")
        plt.plot(x[0], y_pred[0], label="Predictions", color='red')
        plt.show()
        plt.close()
                    
    
