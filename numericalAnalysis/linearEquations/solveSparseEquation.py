import numpy as np, argparse
from iteration import JacobiSparse, conjugateGradientSparse, SparseMatrix
import h5py
class bMatrix(SparseMatrix):
    def __init__(self, size):
        super().__init__(size)
        self.half = int(size[0]/2)-1
    def __getitem__(self, i):
        if i==0 or i==self.shape[0]-1:
            return 2.5
        elif i==self.half or i==self.half+1:
            return 1
        else:
            return 1.5
def bmatrix(n):
    b = np.ones(n)*1.5
    b[0] = 2.5
    b[n-1] = 2.5
    b[int(n/2)-1] = 1
    b[int(n/2)] = 1
    return b
class AMatrix(SparseMatrix):
    def __init__(self, size):
        super().__init__(size)
        self.half = int(size[0]/2)-1
    def dot(self, b):
        b1 = np.zeros(b.shape)
        left = -1
        right = -1
        diag = 3
        andiag = 0.5
        i = 0
        b1[i] = diag*b[i] + right*b[i+1] + andiag*b[self.shape[0]-i-1]
        for i in range(1,self.half-1):
            b1[i] = diag*b[i] + left*b[i-1] + right*b[i+1] + andiag*b[self.shape[0]-i-1]
        i = self.half-1
        b1[i] = diag*b[i] + left*b[i-1] + right*b[i+1]
        i = self.half
        b1[i] = diag*b[i] + left*b[i-1] + right*b[i+1]
        for i in range(self.half+1,self.shape[0]-1):
            b1[i] = diag*b[i] + left*b[i-1] + right*b[i+1] + andiag*b[self.shape[0]-i-1]
        i = self.shape[0]-1
        b1[i] = diag*b[i] + left*b[i-1] + andiag*b[self.shape[0]-i-1]
        return b1
    def jiter(self, x):
        x1 = np.zeros(x.shape)
        left = -1
        right = -1
        diag = 3
        andiag = 0.5
        i = 0
        x1[i] = (b[i] -right*x[i]-andiag*x[self.shape[0]-i-1])/diag
        for i in range(1,self.half-1):
            x1[i] = (b[i] - left*x[i-1] - right*x[i+1] - andiag*x[self.shape[0]-i-1])/diag
        i = self.half-1
        x1[i] = (b[i] - left*x[i-1] - right*x[i+1])/diag
        i = self.half
        x1[i] = (b[i] - left*x[i-1] - right*x[i+1])/diag
        for i in range(self.half+1,self.shape[0]-1):
            x1[i] = (b[i] - left*x[i-1] - right*x[i+1] - andiag*x[self.shape[0]-i-1])/diag
        i = self.shape[0]-1
        x1[i] = (b[i] - left*x[i-1] - andiag*x[self.shape[0]-i-1])/diag
        return x1

def readEquation(n):
    A = AMatrix((n,n))
    # b = bMatrix((n,))
    # b use array
    b = bmatrix(n)
    return A, b
psr = argparse.ArgumentParser()
psr.add_argument('-i', dest="initial", nargs='+',  help="initial position", default=[0,0,0])
psr.add_argument('-n', dest="equation", help="size of matrix A", type=int)
psr.add_argument('-m', dest='method', help="iteration method", default="Jacobi")
psr.add_argument('-o', dest="opt", help="output h5 file")
args = psr.parse_args()
A, b = readEquation(args.equation)
# x0 = np.array([np.float(i) for i in args.initial])
x0 = np.zeros(args.equation)
method = args.method
print("begin {}".format(method))
if method=="Jacobi":
    xk, rk, time= JacobiSparse(A, b, x0)
elif method=="CG":
    xk, rk, time = conjugateGradientSparse(A, b, x0)
else:
    print('{} not support'.format(method))
    exit(0)
print('xk {}'.format(xk))
print('consume cpu time is {}'.format(time))
with h5py.File(args.opt,'w') as opt:
    #opt.create_dataset('xk',data=xk,compression='gzip')
    opt.create_dataset('rk',data=rk,compression='gzip')
print("finish {}".format(method))