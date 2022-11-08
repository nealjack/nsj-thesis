#! /usr/bin/env python3

import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, MaxNLocator
from glob import glob

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = "14"
plt.rcParams["xtick.major.width"] = "1"
plt.rcParams["xtick.major.size"]  = "6"
plt.rcParams["xtick.minor.width"] = "0.8"
plt.rcParams["xtick.minor.size"] = "4"
plt.rcParams["ytick.major.width"] = "1"
plt.rcParams["ytick.major.size"] = "6"
plt.rcParams["ytick.minor.width"] = "0.8"
plt.rcParams["ytick.minor.size"] = "4"
print(plt.rcParams.keys())
plt.rcParams["grid.linewidth"] = "1"


#minorLocator = MultipleLocator(1/4)
#yLocator = MultipleLocator(10)

fig, ax = plt.subplots(dpi=300,figsize=(10.7,5))
plt.ylim(0, 100)
plt.xlim(0, 24.25)
#plt.grid(True, which='major')
#plt.xticks(np.arange(b.size / (60*24)))
#ax.tick_params(axis='x',which='minor')
#ax.xaxis.set_minor_locator(minorLocator)
#ax.yaxis.set_major_locator(yLocator)
plt.xlabel('Time (Days)')
plt.ylabel('Packets per Hour')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
a = np.load('seq_no-Ligeiro-c098e5d0004a_clean.npy')[1:]
plt.plot(np.arange(a.size)/24,a, label='experiment', color='C0', alpha=1)
b = np.load('seq_no-Ligeiro-c098e5d0004a_sim_clean.npy')[1:]
plt.plot(np.arange(b.size)/24, b, label='model', color='C1', alpha=1, ls='dashed')
lgd = plt.legend(loc=0,ncol=1)
plt.savefig('exp_vs_sim_pkt.pdf', bbox_inches='tight', format='pdf')

a_reshape = np.reshape(a, (24, int(a.shape[0]/24)))
b_reshape = np.reshape(b, (24, int(b.shape[0]/24)))

a_day = np.sum(a_reshape, 0)
b_day = np.sum(b_reshape, 0)

error = np.divide(np.absolute(a_day - b_day), np.absolute(a_day))
print(error)
print(np.mean(error))
print(np.std(error))
print(np.percentile(error, .05))
print(np.percentile(error, .95))
#for i, x in enumerate(a_day):
#    print(a_day[i], b_day[i], error[i])


