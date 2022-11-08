#! /usr/bin/env python3

import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

minorLocator = MultipleLocator(1/4)
yLocator = MultipleLocator(10)

voltages = [1.6223, 1.7489, 1.8431, 1.9180, 1.9838, 2.0463, 2.0983, 2.1442,
        2.1820, 2.2143, 2.2418, 2.2629, 2.2800, 2.2942, 2.3089, 2.3192, 2.3259,
        2.3446, 2.3650, 2.3891, 2.4145, 2.4428, 2.4723, 2.52570, 2.6516]
voltages = np.flip(np.load("measurements_5.0C.npy")[:,2], 0)
v_curve = np.ndarray((len(voltages), 2))
v_curve[:,0] = np.linspace(0,100,v_curve.shape[0])
v_curve[:,1] = voltages

def v_to_soc(voltage):
    # find place in v curve:
    ind = np.where(v_curve[:,1] < voltage)[0]
    mini = v_curve[ind[-1]]
    maxi = v_curve[ind[-1] + 1]
    diff = maxi - mini
    slope = diff[0]/diff[1]
    soc = slope * (voltage - mini[1]) + mini[0]
    return soc

fname = "secondary_voltage-Permamote-c098e5110003_clean.npy"
sname = "c098e5110003_simulated_soc.npy"
lname = "light_irradiance-Permamote-c098e5110003_clean.npy"

a = np.load(fname)
a[:-1] = a[1:]
a[-1] = a[-2]
# average by 10 mins:
print(a.shape)
a = np.reshape(a, (int(a.shape[0]/10), 10))
print(a.shape)
a = np.mean(a, 1)
b = np.ndarray(a.shape)
for i, d in enumerate(a):
    b[i] = v_to_soc(d)
w, h = matplotlib.figure.figaspect(0.44)
fig, ax = plt.subplots(dpi=300,figsize=(10.7,5))
plt.ylim(40, 60)
plt.xlim(0, 7)
plt.grid(True, which='major', ls='-.', alpha=0.5)
#plt.xticks(np.arange(b.size / (60*24)))
#ax.tick_params(axis='x',which='minor')
ax.xaxis.set_minor_locator(minorLocator)
ax.yaxis.set_major_locator(yLocator)
plt.xlabel('Time (Days)')
plt.ylabel('Estimated State\nof Charge (%)')
plt.plot(np.arange(b.size)/(6*24.0), b, label='experiment', lw=2)
c = np.load(sname)
print(c)
print(c.shape)
plt.plot(np.arange(c.size)/(3600*24), 100*c, label='model', lw=2, ls='dashed')
d = np.load(lname)
d[0] = d[1]
print(d)
print(d.shape)
print(d.max())
d = (d < 15).astype('int')
#plt.plot(np.arange(d.size)/(60*24), 100*d, label='light', lw=3)
plt.fill_between(np.arange(d.size)/(60*24), 0, 100*d, color='gray', alpha=.5, lw=0)
#plt.arrow(2.9, 47, .5, 0, color='r', width=.1,head_width=.7, head_length=.05)
#plt.arrow(3.8, 47, .5, 0, color='r', width=.1,head_width=.7, head_length=.05)
#plt.arrow(4.8, 47, .5, 0, color='r', width=.1,head_width=.7, head_length=.05)
#plt.arrow(5.8, 47, .5, 0, color='r', width=.1,head_width=.7, head_length=.05)
plt.plot(2.73, 50.7, 'o', color = 'C2',  fillstyle='none', markersize=25, mew=3)
plt.plot(3.3, 50.7, 's', color = 'C4',  fillstyle='none', markersize=25, mew=3)
lgd = plt.legend()
#plt.show()
plt.savefig('exp_vs_sim_soc.pdf', bbox_inches='tight', format='pdf')
