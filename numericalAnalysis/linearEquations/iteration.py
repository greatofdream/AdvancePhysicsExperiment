import numpy as np
import time
class SparseMatrix(object):
    def __init__(self, size):
        self.shape = size
def decomposeDLU(A):
    return np.diag(A.diagonal()), -np.tril(A,-1), -np.triu(A,1)
def Jacobi(A, b, x0, epsilon=1e-5, maxiters=1000):
    # initialize xk,rk; r=1
    xkList = []
    rkList = []
    xk = x0
    rk = 1
    times = 0
    # initialize the iteration matrix
    size = b.shape[0]
    D, L, U = decomposeDLU(A)
    Dinv =  np.linalg.inv(D)
    Bj = np.identity(size) - np.dot(Dinv, A)
    fj = np.dot(Dinv, b)
    # iteration
    while abs(rk)>epsilon and times<maxiters:
        xkList.append(xk)
        xk1 = np.dot(Bj,xk)+fj
        rk = np.max(xk1-xk)
        rkList.append(rk)
        xk = xk1
        times += 1
    xkList.append(xk1)
    return np.array(xkList), np.array(rkList), Bj
def GaussSeidel(A, b, x0, epsilon=1e-5, maxiters=1000):
    # return SOR(A, b, x0, omega=1,epsilon=1e-5, maxiters=1000)
    # initialize xk,rk; r=1
    xkList = []
    rkList = []
    xk = x0
    rk = 1
    times = 0
    # initialize the iteration matrix
    size = b.shape[0]
    D, L, U = decomposeDLU(A)
    Dinv =  np.linalg.inv(D-L)
    Bj = np.identity(size) - np.dot(Dinv, A)
    fj = np.dot(Dinv, b)
    # iteration
    while abs(rk)>epsilon and times<maxiters:
        xkList.append(xk)
        xk1 = np.dot(Bj,xk)+fj
        rk = np.max(xk1-xk)
        rkList.append(rk)
        xk = xk1
        times += 1
    xkList.append(xk1)
    return np.array(xkList), np.array(rkList), Bj
def SOR(A, b, x0, omega, epsilon=1e-5, maxiters=1000):
    # initialize xk,rk; r=1
    xkList = []
    rkList = []
    xk = x0
    rk = 1
    times = 0
    # initialize the iteration matrix
    size = b.shape[0]
    D, L, U = decomposeDLU(A)
    Dinv =  np.linalg.inv(D-omega*L)
    Lomega = np.dot(Dinv,(1-omega)*D+omega*U)
    fomega = omega*np.dot(Dinv, b)
    # iteration
    while abs(rk)>epsilon and times<maxiters:
        xkList.append(xk)
        xk1 = np.dot(Lomega,xk)+fomega
        rk = np.max(xk1-xk)
        rkList.append(rk)
        xk = xk1
        times += 1
    xkList.append(xk1)
    return np.array(xkList), np.array(rkList), Lomega
def SORbestStep(A, b, x0, omega1=0.2, omega2=1.8, step=0.01, epsilon=1e-5, maxiters=1000):
    # caculate for each omega
    D, L, U = decomposeDLU(A)
    omegas = np.arange(omega1, omega2, step)
    rhoLs = np.zeros(omegas.shape)
    for i, omega in enumerate(omegas):
        Dinv =  np.linalg.inv(D-omega*L)
        Lomega = np.dot(Dinv,(1-omega)*D+omega*U)
        eig, eigvector = np.linalg.eig(Lomega)
        rhoLs[i] = np.max(abs(eig))
    omega = omegas[np.argmin(rhoLs)]
    return SOR(A, b, x0, omega, epsilon, maxiters), omegas, rhoLs
    # iteration
    return np.array(xkList), np.array(rkList), Lomega
def JacobiSparse(A, b, x0, epsilon=1e-5, maxiters=1000):
    # initialize xk,rk; r=1
    xkList = []
    rkList = []
    xk = x0
    rk = 1
    timeBegin = time.time()

    times = 0
    # initialize the iteration matrix
    size = b.shape[0]
    # iteration
    while abs(rk)>epsilon and times<maxiters:
        # xkList.append(xk)
        xk1 = A.jiter(xk)
        rk = np.max(xk1-xk)
        rkList.append(rk)
        xk = xk1
        times += 1
    #xkList.append(xk1)
    timeEnd = time.time()
    cpuTime = timeEnd - timeBegin
    return xk1, np.array(rkList), cpuTime
def conjugateGradientSparse(A, b, x0, epsilon=1e-6, maxiters=1000):
    # initialize xk,rk; r=1
    xkList = []
    rkList = []
    timeBegin = time.time()

    xk = x0
    rk = 1
    r = (b - A.dot(x0))
    p = r.copy()
    times = 0
    # initialize the iteration matrix
    size = b.shape[0]
    while abs(rk)>epsilon and times<maxiters:
        Ap = A.dot(p)
        if (r<1e-7).all() or (np.dot(p.T,Ap)<1e-7).all():
            break
        #xkList.append(xk)
        alpha = np.dot(r.T,r)/np.dot(p.T,Ap)
        xk1 = xk + alpha*p
        r1 = r - alpha*Ap
        beta = np.dot(r1.T,r1)/np.dot(r.T,r)
        p = r1 + beta*p
        rk = np.max(xk1-xk)
        rkList.append(rk)
        xk = xk1
        r = r1
        times += 1
    #xkList.append(xk1)
    timeEnd = time.time()
    cpuTime = timeEnd - timeBegin
    # iteration
    #print(xkList)
    return xk1, np.array(rkList), cpuTime
def conjugateGradient(A, b, x0, epsilon=1e-9, maxiters=1000):
    # this part is same as conjugateGradientSparse, but not return the cputime because useless
    # initialize xk,rk; r=1
    xkList = []
    rkList = []

    xk = x0
    rk = 1
    r = (b - A.dot(x0))
    p = r.copy()
    times = 0
    # initialize the iteration matrix
    size = b.shape[0]
    while abs(rk)>epsilon and times<maxiters:
        Ap = A.dot(p)
        if (r<1e-7).all() or (np.dot(p.T,Ap)<1e-7).all():
            break
        xkList.append(xk)
        alpha = np.dot(r.T,r)/np.dot(p.T,Ap)
        xk1 = xk + alpha*p
        r1 = r - alpha*Ap
        beta = np.dot(r1.T,r1)/np.dot(r.T,r)
        p = r1 + beta*p
        rk = np.max(xk1-xk)
        rkList.append(rk)
        xk = xk1
        r = r1
        times += 1
    xkList.append(xk1)
    # iteration
    #print(xkList)
    return np.array(xkList), np.array(rkList)