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
args = psr.parse_args()
inputh5 = args.input

fig, ax = plt.subplots()
ax.set_title("rk vs iteration times")
# plot the Jacobi covergence curve; output the covergence result
print("Jacobi")
with h5py.File(inputh5[0],'r') as opt:
    rk = opt['rk'][:]
    ax.plot(rk,label='Jacobi')
JacobiTimes = rk.shape[0]

# plot the GS covergence curve
print("ConjugateGradient")
with h5py.File(inputh5[1],'r') as opt:
    rk = opt['rk'][:]
    ax.plot(rk,label='CG')
GSTimes = rk.shape[0]
print('Jacobi {}, CG {}'.format(JacobiTimes,GSTimes))
ax.set_xlabel('k')
ax.set_ylabel('rk')
ax.legend()
fig.savefig(args.output.replace('.png','YLinear.png'))
ax.set_yscale('log')
fig.savefig(args.output)
plt.close()
