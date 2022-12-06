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

fnames = glob.glob('camaroptera_capacity_sweep_*.pkl')

fig, ax = plt.subplots(1, figsize=(10.7,5))
labels = ['10 mW/cm\u00b2', '50 mW/cm\u00b2']

for fname, label in zip(fnames, labels):
    a = pd.read_pickle(fname)
    for col in a.columns:
        print(col)
    print(a)
    print(a['events_success'] / (a['events_missed']+ a['events_success']))
    print(a['capacity_J'])
    ax.plot(a['capacity_J']/3.6, 100* a['events_success'] / (a['events_success'] + a['events_missed']), label=label, linewidth=2)
    #ax.plot(a['capacity_J']/3.6, 100 * a['secondary_end_energy'] / a['secondary_start_energy'], label='% successful events', linewidth=2)
    #plt.plot(a['capacity_J']/3.6, 100*a['time_online'], label='% time online')
    #plt.plot(a['capacity_J']/3.6, 100*a['used_energy'], label='energy')

ax.set_xscale("log")
#plt.xlim(0,100)
ax.set_ylim(0,110)
ax.set_xlabel("Secondary Size (mWh)")
ax.set_ylabel("Availability")
#plt.title("Camaroptera Reliability with Secondary Size")
#plt.axvline(x=64., color = 'b')
ax.axvline(x=.1485 / 3.6, color = 'C3', linewidth=2)
ax.axvline(x=3920, color = 'C4', linewidth=2)
ax.text(x=.17 / 3.6, y=64, s='Camaroptera\nDesigned Capacity', color = 'C3', weight='bold')
ax.text(x=2800, y=64, s='Heuristic\nEstimated Capacity', color = 'C4', weight='bold', horizontalalignment='right')
#plt.axvline(x= 10.125 / 3.6, color = 'b')
#plt.axvline(x= 200, color = 'g')
ax.grid(True, alpha=0.75)
#plt.legend(loc='lower right')
#plt.show()
ax.legend()
plt.savefig('camaroptera_simulation.pdf', bbox_inches='tight')

