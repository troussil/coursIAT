import numpy
import random

#-------------------------------------------------------------
def nextByGivenStep(step):
    def f(sol, grad):
        return sol - step * grad
    return f

#-------------------------------------------------------------
def nextByNormalizedStep(step):
    def f(sol, grad):
        return sol - (step / numpy.linalg.norm(grad)) * grad
    return f

#-------------------------------------------------------------
class nextByDecreasingStep(object):
    
    def __init__(self):
        self.counter = 0

    def __call__(self, sol, grad):
        self.counter += 1
        return sol - (1. / (self.counter * numpy.linalg.norm(grad))) * grad

#-------------------------------------------------------------
def nextByNewton(hessianF):
    def f(sol, grad):
        H = hessianF(sol)
        return sol - numpy.linalg.inv(H).dot(grad)
    return f

#-------------------------------------------------------------
class nextByMomentum(object):
    
    def __init__(self, step, decayFactor):
        self.step = step
        self.alpha = decayFactor
        self.lastVariation = 0
        
    def __call__(self, sol, grad):
        variation = self.step * grad + self.alpha * self.lastVariation
        self.lastVariation = variation
        return sol - self.lastVariation

#-------------------------------------------------------------
def gradientDescent(maxiters, epsilon, gradientF, currentSol, nextSolF):

    sols = [currentSol]
    
    for _ in range(maxiters):

        grad = gradientF( currentSol )
        currentSol = nextSolF(currentSol, grad)

        sols.append(currentSol)

        if numpy.linalg.norm(grad) < epsilon:
            break

    return sols

#-------------------------------------------------------------
def sgd(maxiters, dataSize, gradientF, currentSol, nextSolF):

    sols = [currentSol]
    
    for _ in range(maxiters):

        for i in random.sample(range(dataSize), dataSize): 
            grad = gradientF( currentSol, i )
            currentSol = nextSolF(currentSol, grad)

        sols.append(currentSol)

    return sols

#-------------------------------------------------------------
def sgdMiniBatch(maxiters, batchSize, objectiveFunction, currentSol, nextSolF):

    sols = [currentSol]
    
    for _ in range(maxiters):

        objectiveFunction.shuffle()
        nbBatches = objectiveFunction.size() // batchSize

        for i in range(nbBatches):
            idxStart = i * batchSize
            idxEnd = idxStart + batchSize
            grad = objectiveFunction.batchGradient( currentSol, idxStart, idxEnd )
            currentSol = nextSolF(currentSol, grad)

        sols.append(currentSol)

    return sols
    
