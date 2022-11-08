#! /usr/bin/env python3

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
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


def get_times(fname):
    times = np.loadtxt(fname, dtype = 'datetime64[s]', delimiter=',', usecols=0, converters = {0:np.datetime64})
    days = np.unique(times.astype('datetime64[D]'))
    ind = np.logical_and(times >= days[0] -np.timedelta64(8,'h'), times < days[-1]-np.timedelta64(8, 'h'))
    times = times[ind]
    data =  np.loadtxt(fname, dtype = 'int', delimiter=',', usecols=1, converters = {1:np.int64})
    data = data[ind]
    unique, ind= np.unique(data, return_index=True)
    times = times[ind]
    c = np.array([((times - times[0])/np.timedelta64(1, 's')), np.ones(times.size)])
    return c
#minorLocator = MultipleLocator(1/4)
#yLocator = MultipleLocator(10)

fig, ax = plt.subplots(figsize=(10.7,3), dpi=300)
#plt.ylim(0, 100)
#plt.xlim(0, 10)
#plt.xticks(np.arange(b.size / (60*24)))
#ax.tick_params(axis='x',which='minor')
#ax.xaxis.set_minor_locator(minorLocator)
#ax.yaxis.set_major_locator(yLocator)
plt.xlabel('Time (Hour of day)')
#plt.ylabel('Packets',labelpad=10)
plt.xlim(0, 48.1)
plt.ylim(-.75, .25)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_yaxis().set_ticks([])
ax.get_xaxis().set_ticks(range(0,49, 3))
a = get_times('seq_no-Ligeiro-c098e5d00047.csv')
plt.plot(a[0]/(60*60), a[1]-1, label='Intermittent', marker='o', ms=6, fillstyle='full', alpha=.2, linestyle='None')
b = get_times('sequence_number-Permamote-c098e5110002.csv')
plt.plot(b[0]/(60*60), b[1]-1.5, label='Permamote', marker='o', ms=6, fillstyle='full', alpha=.2, linestyle='None')
plt.xticks(np.linspace(0,48,17),[str(x) for x in [0,3,6,9,12,15,18,21,24,3,6,9,12,15,18,21,24]])
text2 = plt.text(32, .1, 'Intermittent', color='C0')
text = plt.text(32, -.4, 'Permamote', color='C1')
plt.tight_layout()
#for lh in lgd.legendHandles:
#    lh._legmarker.set_alpha(1)
plt.savefig('exp_packets_recv.png',  bbox_extra_artists=(text,))
