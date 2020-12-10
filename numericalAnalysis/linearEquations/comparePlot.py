import h5py,argparse
import matplotlib.pyplot as plt
import numpy as np
def printLatexTable(xk, rk):
    print('{}&{}&{}&{}&{}\\\\'.format('k','rk','xk[1]','xk[2]','xk[3]'))
    for i in range(rk.shape[0]):
        print('{}&{:.3f}&{:.3f}&{:.3f}&{:.3f}\\\\'.format(i, rk[i], xk[i,0], xk[i,1], xk[i,2]))
    print('{}&{:.3f}&{:.3f}&{:.3f}&{:.3f}\\\\'.format(i, rk[i], xk[i,0], xk[i,1], xk[i,2]))
def caculateRho(eig):
    rho = np.max(abs(eig))
    print('rho(B): {:.3f};convergence velocity:{:.3f}'.format(rho, -np.log(rho)))
    return rho
psr = argparse.ArgumentParser()
psr.add_argument('-i', dest="input", nargs='+', help="input h5 file, order is Jacobi, GS, SOR, SORbest")
psr.add_argument('-o', dest="output", help="output png")
psr.add_argument('-w', dest="omegas", nargs='+', help="omegas list")
args = psr.parse_args()
inputh5 = args.input
omegas = np.array([np.float(i) for i in args.omegas])

fig, ax = plt.subplots()
ax.set_title("rk vs iteration times")
# plot the Jacobi covergence curve; output the covergence result
print("Jacobi")
with h5py.File(inputh5[0],'r') as opt:
    xk = opt['xk'][:]
    rk = opt['rk'][:]
    eig = opt['eig'][:]
    printLatexTable(xk,rk)
    JacobiRho = caculateRho(eig)
    ax.plot(rk,label='Jacobi')
JacobiTimes = rk.shape[0]

# plot the GS covergence curve
print("GaussSeidel")
with h5py.File(inputh5[1],'r') as opt:
    xk = opt['xk'][:]
    rk = opt['rk'][:]
    eig = opt['eig'][:]
    printLatexTable(xk,rk)
    GSRho = caculateRho(eig)
    ax.plot(rk,label='GaussSeidel')
GSTimes = rk.shape[0]
# plot the SOR covergence curve
SORTimes = []
with h5py.File(inputh5[2],'r') as opt:
    for omega in omegas:
        print('SOR{:.1f}'.format(omega))
        xk = opt['{:.1f}/xk'.format(omega)][:]
        rk = opt['{:.1f}/rk'.format(omega)][:]
        eig = opt['{:.1f}/eig'.format(omega)][:]
        printLatexTable(xk,rk)
        caculateRho(eig)
        ax.plot(rk,label='SOR omega={}'.format(omega))
        SORTimes.append(rk.shape[0])
# plot the SOR best convergence curve
with h5py.File(inputh5[3],'r') as opt:
    omega = opt.attrs['omega']
    print('SOR{:.1f}'.format(omega))
    xk = opt['xk'][:]
    rk = opt['rk'][:]
    eig = opt['eig'][:]
    SORomegas = opt['omegas'][:]
    SORrhos = opt['rhoLs'][:]
    printLatexTable(xk,rk)
    caculateRho(eig)
    ax.plot(rk,label='SOR omega={}'.format(omega))
    SORTimes.append(rk.shape[0])
    omegas = np.append(omegas,omega)
ax.set_xlabel('k')
ax.set_ylabel('rk')
ax.legend()
fig.savefig(args.output.replace('.png','YLinear.png'))
ax.set_yscale('log')
fig.savefig(args.output)
plt.close()

# plot the \omega vs times curve
fig, ax = plt.subplots()
ax.set_title('SOR omega vs times')
ax.scatter(omegas, SORTimes)
ax.axhline(JacobiTimes, label='Jacobi',linestyle='dashed')
ax.axhline(GSTimes, label='GaussSeidel',linestyle='dashed')
ax.set_xlabel('omega')
ax.set_ylabel('times')
ax.legend()
fig.savefig("omegaTimes.png")
plt.close()
# plot the \omega vs times curve
fig, ax = plt.subplots()
ax.set_title('SOR omega vs rho(L)')
ax.scatter(SORomegas, SORrhos)
ax.axhline(JacobiRho, label='Jacobi',linestyle='dashed')
ax.axhline(GSRho, label='GaussSeidel',linestyle='dashed')
ax.set_xlabel('omega')
ax.set_ylabel('rhoL')
ax.legend()
fig.savefig("omegaRho.png")
plt.close()