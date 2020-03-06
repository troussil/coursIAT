import numpy

class LeastSquare2d(object):

    def __init__(self, array2d): 
        self.a = array2d

    def size(self):
        return self.a.shape[0]; 
        
    def shuffle(self):
        numpy.random.shuffle(self.a)

    def oneGradient(self, sol, idx):
        
        x1 = sol[0][0]
        x2 = sol[1][0]
        
        ui = self.a[idx,0]
        vi = self.a[idx,1]
        
        dui = 2 * ui * ((ui*x1 + x2) - vi)
        dvi = 2 * ((ui*x1 + x2) - vi)

        return numpy.array( [[dui],[dvi]] )
            
    def batchGradient(self, sol, idxStart, idxEnd): 

        x1 = sol[0][0]
        x2 = sol[1][0]
        
        u = self.a[idxStart:idxEnd,0]
        v = self.a[idxStart:idxEnd,1]
        
        du = 2 * numpy.multiply(u, numpy.subtract( (u*x1 + x2), v) )
        dv = 2 * numpy.subtract( (u*x1 + x2), v)

        return numpy.array( [[sum(du)],[sum(dv)]] )

    def gradient(self, sol):

        return self.batchGradient( sol, 0, self.size() )

    def hessian(self, sol):

        x1 = sol[0][0]
        x2 = sol[1][0]
        
        u = self.a[:,0]
        v = self.a[:,1]

        du2 = 2 * numpy.multiply(u, u)
        duv = 2 * u
        dv2 = 2 * numpy.ones( u.shape )

        return numpy.array( [[sum(du2), sum(duv)],[sum(duv), sum(dv2)]] )

    def analyticalOptimum(self):

        nbRows, nbCols = self.a.shape 
        u = self.a[:,0]
        v = self.a[:,1]

        num = nbRows*sum(numpy.multiply(u,v)) - sum(u)*sum(v)
        den = nbRows*sum(numpy.multiply(u,u)) - sum(u)*sum(u)
        x1 = num / den

        x2 = ( sum(v) - sum(u * x1) ) / nbRows

        return numpy.array( [[x1], [x2]] ) 
    
