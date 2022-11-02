#! /usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use('Agg')

import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator
import itertools
import re
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

def round_sigfigs(num, sig_figs):
    """Round to specified number of sigfigs.

    >>> round_sigfigs(0, sig_figs=4)
    0
    >>> int(round_sigfigs(12345, sig_figs=2))
    12000
    >>> int(round_sigfigs(-12345, sig_figs=2))
    -12000
    >>> int(round_sigfigs(1, sig_figs=2))
    1
    >>> '{0:.3}'.format(round_sigfigs(3.1415, sig_figs=2))
    '3.1'
    >>> '{0:.3}'.format(round_sigfigs(-3.1415, sig_figs=2))
    '-3.1'
    >>> '{0:.5}'.format(round_sigfigs(0.00098765, sig_figs=2))
    '0.00099'
    >>> '{0:.6}'.format(round_sigfigs(0.00098765, sig_figs=3))
    '0.000988'
    """
    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0  # Can't take the log of 0

setup_name_to_irradiance = {
    'SetupA': '15.1 μW/cm$^2$',
    'SetupB': '14.9 μW/cm$^2$',
    'SetupC': '745 μW/cm$^2$',
    'SetupD': '97.4 μW/cm$^2$',
    'SetupE': '142 μW/cm$^2$',
}

period_data = []
reliability_vs_secondary_data = []
fnames = glob('./*.npy')
for fname in fnames:
    # get secondary size:
    secondary_size = fname.split('_')[-1].split('.n')[0]

    # get setup name:
    setup_name = fname.split('/')[-1].split('_')[0]
    irradiance = setup_name_to_irradiance[setup_name]
    if setup_name == 'SetupC': continue

    to_append = period_data
    if 'period' in fname:
        to_append = period_data
    to_append.append([irradiance, secondary_size, np.load(fname, allow_pickle=True)])

colors = [x for x in ['C0', 'C1', 'C2'] for _ in range(0, 5)]
#colors = [x for x in [cmap(0.3), cmap(0.4), cmap(0.9)] for _ in range(0, 5)]
markers = ['x', 'o', 's', '^', 'D'] * (4)

custom_lines = [Line2D([0],[0], color = 'C0', lw=2),
                Line2D([0],[0], color = 'C1', lw=2),
                Line2D([0],[0], marker = markers[1], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[2], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[3], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[4], color='black', lw=2, markersize=8)]
lines_names = [setup_name_to_irradiance["SetupA"],
               setup_name_to_irradiance["SetupD"],
               "0.0028 mWh",
               "0.028 mWh",
               "0.28 mWh",
               "2.8 mWh"]

# plot usage vs period:
#plt.figure()
#plt.grid(True, which='both', ls='-.', alpha=0.5)
#plt.xscale('log')
#for i, data in enumerate(sorted(period_data)):
#    plt.plot(data[2][:,0], 100*data[2][:,2], color=colors[i], marker=markers[i], label=data[1] + ' J, ' + data[0])
#plt.title('Energy Utilized vs Workload Period')
#plt.xlabel('Workload Period (s)')
#plt.ylabel('Energy Utilized (%)')
##handles, labels = plt.gca().get_legend_handles_labels()
##hanbles = sorted(zip(handles, labels), key=lambda x: int(x[1].split('s')[0]))
##handles = [x[0] for x in hanbles]
##labels  = [x[1] for x in hanbles]
#lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#plt.savefig('usage_vs_period', bbox_extra_artists=(lgd,), bbox_inches='tight')

# plot reliability vs period:
plt.figure(dpi=300,figsize=(10.7,5))
plt.grid(True, which='major')
plt.xscale('log')
plt.ylim(-2,102)
for i, data in enumerate(sorted(period_data, key=lambda x: (float(x[0].split(' ')[0]), float(x[1])))):
    if i % 5 == 0:
        continue
    plt.plot(data[2][:,0], 100*data[2][:,3], color=colors[i], lw=2, markersize=8, marker=markers[i], label=str(round_sigfigs(float(data[1])/3600*1E3, 2)) + ' mWh, ' + data[0])
#plt.title('Reliability vs Workload Period')
plt.xlabel('Workload Period (s)')
plt.ylabel('Successful Events (%)')
#lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
lgd = plt.legend(custom_lines, lines_names, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('events_vs_period.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight', format='pdf')
