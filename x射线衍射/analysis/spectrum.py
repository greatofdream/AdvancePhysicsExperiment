import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import argparse
import locale
'''
# python spectrum.py -e Si -s ../data/Si/Si.txt -t ../data/Si/PDF*.txt -p ../data/Si/Si.pid -o ../data/Si/spectrum.png
'''
psr = argparse.ArgumentParser()
psr.add_argument('-s', dest="spectrum", help="input spectrum file")
psr.add_argument('-p', dest="peak", nargs='?', default='', help="input peak result file")
psr.add_argument('-t', dest="stdpeak", nargs='?', default='', help="input std peak result file")
psr.add_argument('-e', dest="element", help="element")
psr.add_argument('-o', dest="opt", help="output png file")
args = psr.parse_args()
#print(locale.getpreferredencoding())
print(args)
def findLineAdd2(file, pattern):
    with open(file, 'r', encoding='gbk') as ipt:
        for n, line in enumerate(ipt):
            #print(line)
            if line.find(pattern)>=0:
                break
    return n+3
def searchPeak(spec):
    peak = np.array([],dtype=[('2theta','<f4'),('heightPercent','<f4')])
    maxspec = np.max(spec['I'])
    for i in range(10, spec['I'].shape[0]-10):
        if (spec['I'][i]>=spec['I'][(i-5):(i+5)]).all() and spec['I'][i]/maxspec>0.02:
            peak = np.append(peak, np.array([(spec['2theta'][i], spec['I'][i]/maxspec*100)],dtype=[('2theta','<f4'),('heightPercent','<f4')]))
    print(peak)
    return peak
spec = pd.read_csv(args.spectrum, index_col=None, sep='\s+', names=['2theta', 'I'], na_values=['NA'])#skipfooter=1,
if args.peak != None:
    peak = pd.read_csv(args.peak, skiprows=9, index_col=None, sep='\s+', names=['2theta', 'd','bkg','height','heightPercent','半峰宽','晶粒(埃)'], usecols=[0, 1,2,3,4], na_values=['NA'])
else:
    peak = searchPeak(spec)
print("sin theta ^2")
print(peak['2theta'])
print(np.sin(peak['2theta']/360*np.pi)**2)

if args.stdpeak != None:
    stdPskip = findLineAdd2(args.stdpeak, "Unit Cell Data")
    stdPeak = pd.read_csv(args.stdpeak, skiprows=stdPskip, index_col=None, sep='\s{2,}', names=['2theta', 'd','heightPercent','hkl','theta','1/2d','2pi/d','n2'], usecols=[0, 1,2,3,4], na_values=['NA'])#, dtype={'heightPercent': np.float64}
    print(np.sin(stdPeak['2theta']/360*np.pi)**2)

fig, ax = plt.subplots()
ax.plot(spec['2theta'], spec['I']/np.max(spec['I'])*100, alpha=0.6, label=args.element+' spectrum') 
ax.scatter(peak['2theta'],peak['heightPercent'], color='r', marker='+', label='peak')
if args.stdpeak != None:
    stdPeak['heightPercent'] = stdPeak['heightPercent'].apply(lambda x: 0 if not isinstance(x,float) and x.find('<')>=0 else np.float64(x))
    print(stdPeak['heightPercent'])
    ax.scatter(stdPeak['2theta'],stdPeak['heightPercent'], color='g', marker='x', alpha=0.8, label='peak in standard card')

ax.set_title(args.element+' spectrum', fontsize='large')
ax.set_xlabel('2theta', fontsize='large')
#ax.xaxis.set_major_locator(MultipleLocator(20))
ax.set_ylabel('I percent %', fontsize='large')
ax.legend()
fig.savefig(args.opt)
plt.close()