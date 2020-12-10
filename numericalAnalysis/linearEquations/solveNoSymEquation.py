import numpy as np, argparse
from iteration import conjugateGradient, decomposeDLU
import h5py
def readEquation(equationCsv):
    Ab = np.loadtxt(equationCsv,delimiter=',')
    return Ab[:,:-1],Ab[:,-1]
psr = argparse.ArgumentParser()
psr.add_argument('-i', dest="initial", nargs='+',  help="initial position", default=[0,0,0])
psr.add_argument('-e', dest="equation", help="equation coefficients")
psr.add_argument('-m', dest='method', help="iteration method", default="Jacobi")
psr.add_argument('-o', dest="opt", help="output h5 file")
args = psr.parse_args()
A, b = readEquation(args.equation)
# check the A symetry and positive
if ((A-A.T)!=0).any():
    A1 = np.dot(A.T, A)
    b1 = np.dot(A.T, b)
    print(A1)
    print(b1)
else:
    A = A1
    b = b1
x0 = np.array([np.float(i) for i in args.initial])
method = args.method
print("begin {}".format(method))
if method=="CG":
    xk, rk = conjugateGradient(A1, b1, x0)
else:
    print('{} not support'.format(method))
    exit(0)

with h5py.File(args.opt,'w') as opt:
    opt.create_dataset('xk',data=xk,compression='gzip')
    opt.create_dataset('rk',data=rk,compression='gzip')
print("finish {}".format(method))