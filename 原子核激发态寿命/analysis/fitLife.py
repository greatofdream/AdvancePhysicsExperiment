import pandas as pd, numpy as np
from scipy.linalg import lstsq
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import argparse
'''
# python fitLife.py -n ../data/dingbiao.csv -t ../data/tau.csv -o ../data/fit.png
'''
psr = argparse.ArgumentParser()
psr.add_argument('-n', dest="normal", help="input normal xlsx file")
psr.add_argument('-t', dest="tau", help="input tau xlsx file")
psr.add_argument('-o', dest="opt", help="output png file")
args = psr.parse_args()
normal = pd.read_csv(args.normal, header=0, index_col=None, names=['channel', 't'], na_values=['NA'])
tau = pd.read_csv(args.tau, skiprows=12, index_col=None, sep='\s+', names=['address', 'entries'], na_values=['NA'], nrows=500)

A = np.ones((normal['channel'].shape[0], 2))
A[:,1] = normal['channel']
sol, r, rank, s = lstsq(A, np.array(normal['t']))
print(sol)
'''
fig, ax = plt.subplots()
ax.scatter(normal['channel'], normal['t'], label='t/ns-address') 
ax.plot(normal['channel'], np.dot(A, sol), label='fit line')
ax.set_title('tau distribution', fontsize='large')
ax.set_xlabel('address', fontsize='large')
ax.set_ylabel('t/ns', fontsize='large')
ax.legend()
fig.savefig(args.opt.replace('fit.png', 'normal.png'))
plt.close()

fig, ax = plt.subplots()
ax.plot(tau['address'][1:251], np.log(tau['entries'][1:251]), label='t distribution') 
ax.set_title('tau distribution', fontsize='large')
ax.set_xlabel('address', fontsize='large')
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.set_ylabel('log(entries)', fontsize='large')
ax.legend()
fig.savefig(args.opt)
plt.close()
'''
# choose range (35, 50), initial value n0=2000, tau=10, n_rc=20
def likelihood(paras, *args):
    (observe,t0) = args
    x = np.arange(t0, t0+observe.shape[0])
    estimate = paras[0]*np.exp(-x/paras[1])+paras[2]
    return -np.sum(observe*np.log(estimate)-estimate)
paras0=[2000, 10, 20]
result = minimize(likelihood, paras0, method='SLSQP', args= (np.array(tau['entries'])[35:51], 35), bounds=((5000,500000),(1,100),(0,100)),options={'maxiter':5000})
print(result)
rx = result.x
fig, ax = plt.subplots()
ax.errorbar(np.array(tau['address'][0:100]), np.array(tau['entries'][0:100]), xerr=None, yerr=np.sqrt(np.array(tau['entries'])[0:100]), label='t distribution') 
ax.plot(np.array(tau['address'][35:51]), rx[0]*np.exp(-np.array(tau['address'][35:51])/rx[1])+rx[2], label= 'fit line')
ax.set_title('tau distribution', fontsize='large')
ax.set_xlabel('address', fontsize='large')
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.set_ylabel('entries', fontsize='large')
ax.legend()
fig.savefig(args.opt.replace('fit.png', 'tau.png'))
plt.close()
