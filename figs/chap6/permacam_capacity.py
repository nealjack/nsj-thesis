#! /usr/bin/env python3

import matplotlib
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob

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
plt.rcParams["grid.linewidth"] = "1"

fnames = glob.glob('permacam*.pkl')
fnames.sort()
order = ['cr2032', 'cr2477', 'cr123a']
print(fnames)
fig, ax = plt.subplots(1, figsize=(10.7,5))

fnames_sorted = []

for o in order:
    for fname in fnames:
        if o not in fname:
            continue
        fnames_sorted.append(fname)

for fname in fnames_sorted:
    a = pd.read_pickle(fname)
    split_fname = fname.split('.')[0].split('_')
    bat_type = split_fname[-1].upper()
    ax.plot(a['capacity_J']/3.6, a['lifetime'], linewidth=2, label=bat_type + ' + harvest')
    #ax.plot(a['capacity_J']/3.6, 100 * a['secondary_end_energy'] / a['secondary_start_energy'], label='% successful events', linewidth=2)
    #plt.plot(a['capacity_J']/3.6, 100*a['time_online'], label='% time online')
    #plt.plot(a['capacity_J']/3.6, 100*a['used_energy'], label='energy')


ax.set_xscale("log")
plt.xlim(0.1,1000)
ax.set_ylim(0,10)
ax.set_xlabel("Secondary Size (mWh)")
ax.set_ylabel("Lifetime")
#plt.title("Camaroptera Reliability with Secondary Size")
#plt.axvline(x=64., color = 'b')
#ax.axvline(x=.1485 / 3.6, color = 'C3', linewidth=2)
ax.axvline(x=385, color = 'C4', linewidth=2)

ax.axhline(y=0.5, color =  'C0', linewidth=2, linestyle='dashed', label = 'CR2032 only')
ax.axhline(y=2.06, color = 'C1', linewidth=2, linestyle='dashed', label = 'CR2477 only')
ax.axhline(y=3.06, color = 'C2', linewidth=2, linestyle='dashed', label = 'CR123A only')

#ax.text(x=.17 / 3.6, y=64, s='Camaroptera\nDesigned Capacity', color = 'C3', weight='bold')
ax.text(x=350, y=9, s='Heuristic\nEstimated Capacity', color = 'C4', weight='bold', horizontalalignment='right')
#plt.axvline(x= 10.125 / 3.6, color = 'b')
#plt.axvline(x= 200, color = 'g')
ax.grid(True, alpha=0.75)
#plt.legend(loc='lower right')
#plt.show()
ax.legend()
plt.savefig('permacam_simulation.pdf', bbox_inches='tight')

