import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import argparse
'''
# python energyCut.py -l ../data/lowenergy.csv -u ../data/highEnergy.csv -o ../data/energyCut.png
'''
psr = argparse.ArgumentParser()
psr.add_argument('-l', dest="low", help="input low xlsx file")
psr.add_argument('-u', dest="high", help="input high xlsx file")
psr.add_argument('-o', dest="opt", help="output png file")
args = psr.parse_args()
low = pd.read_csv(args.low, skiprows=12, index_col=None, sep='\s+', names=['address', 'entries'], na_values=['NA'])
high = pd.read_csv(args.high, skiprows=12, index_col=None, sep='\s+', names=['address', 'entries'], na_values=['NA'])

fig, ax = plt.subplots()
ax.plot(low['address'][0:200], low['entries'][0:200], label='low energy') 
ax.plot(high['address'][0:200], high['entries'][0:200], label='high energy') 
ax.set_title('energy cut', fontsize='large')
ax.set_xlabel('address', fontsize='large')
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.set_ylabel('entries', fontsize='large')
ax.legend()
fig.savefig(args.opt)
plt.close()