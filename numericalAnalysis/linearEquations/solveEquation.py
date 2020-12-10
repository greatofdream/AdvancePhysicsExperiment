import numpy as np, argparse
from iteration import Jacobi, GaussSeidel, SOR, SORbestStep
import h5py
def readEquation(equationCsv):
    Ab = np.loadtxt(equationCsv,delimiter=',')
    return Ab[:,:-1],Ab[:,-1]
psr = argparse.ArgumentParser()
psr.add_argument('-i', dest="initial", nargs='+',  help="initial position", default=[0,0,0])
psr.add_argument('-e', dest="equation", help="equation coefficients")
psr.add_argument('-m', dest='method', help="iteration method", default="Jacobi")
psr.add_argument('-o', dest="opt", help="output h5 file")
psr.add_argument('-w', dest="omegas", nargs='+', help="the SOR omega")
args = psr.parse_args()
A, b = readEquation(args.equation)
x0 = np.array([np.float(i) for i in args.initial])
method = args.method
print("begin {}".format(method))
if method=="Jacobi":
    xk, rk, B = Jacobi(A, b, x0)
    eig, eigvector = np.linalg.eig(B)
elif method=="GS":
    xk, rk, B = GaussSeidel(A, b, x0)
    eig, eigvector = np.linalg.eig(B)
elif method=="SOR":
    omegas = np.array([np.float(i) for i in args.omegas])
    with h5py.File(args.opt, 'w') as opt:
        for omega in omegas:
            xk, rk, B = SOR(A, b, x0, omega)
            opt.create_dataset('{:.1f}/xk'.format(omega), data=xk,compression='gzip')
            opt.create_dataset('{:.1f}/rk'.format(omega), data=rk,compression='gzip')
            eig, eigvector = np.linalg.eig(B)
            opt.create_dataset('{:.1f}/eig'.format(omega), data=eig, compression='gzip')
            opt.create_dataset('{:.1f}/eigvector'.format(omega), data=eigvector, compression='gzip')
            opt.create_dataset('{:.1f}/B'.format(omega), data=B, compression='gzip')
    print("finish {}".format(method))
    exit(0)
elif method=="SORbest":
    (xk, rk, B), omegas, rhoLs = SORbestStep(A, b, x0)
    eig, eigvector = np.linalg.eig(B)
    with h5py.File(args.opt, 'w') as opt:
        opt.attrs['omega'] = omegas[np.argmin(rhoLs)]
        opt.create_dataset('xk',data=xk,compression='gzip')
        opt.create_dataset('rk',data=rk,compression='gzip')
        opt.create_dataset('B',data=B,compression='gzip')
        opt.create_dataset('eig',data=eig,compression='gzip')
        opt.create_dataset('eigvector',data=eigvector,compression='gzip')
        opt.create_dataset('rhoLs',data=rhoLs,compression='gzip')
        opt.create_dataset('omegas', data=omegas, compression='gzip')
    print("finish {}".format(method))
    exit(0)
else:
    print('{} not support'.format(method))
    exit(0)

with h5py.File(args.opt,'w') as opt:
    opt.create_dataset('xk',data=xk,compression='gzip')
    opt.create_dataset('rk',data=rk,compression='gzip')
    opt.create_dataset('B',data=B,compression='gzip')
    opt.create_dataset('eig',data=eig,compression='gzip')
    opt.create_dataset('eigvector',data=eigvector,compression='gzip')
print("finish {}".format(method))