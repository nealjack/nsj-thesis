#! /usr/bin/env python3
import numpy as np
import matplotlib

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

trace_name_to_alias = {
        "SetupA": "Shaded",
        "SetupB": "Artificial",
        "SetupC": "Near Window H",
        "SetupD": "Near Window L",
        }

secondary_size_data = []
data = []
fnames = glob('./*.npy')
for fname in fnames:
    # get duty cycle:
    lmbda = fname.split('_')[-1].split('.')[0]

    # get setup name:
    setup_name = fname.split('/')[-1].split('_')[0]

    if setup_name != 'SetupD': continue

    ttc_data = np.load(fname, allow_pickle=True)
    print(ttc_data)

    #bins = np.histogram(np.hstack((ttc_data[1][-1], ttc_data[2][-1], ttc_data[3][-1])), bins=100)[1]
    bins = np.logspace(0, 5, 50)
    print(bins)

    fig, ax = plt.subplots(figsize=(10.7, 5), dpi=300)
    ax.hist(ttc_data[3][-1], bins, label="0.3 mWh".format(ttc_data[3][0]/3.6) )
    ax.hist(ttc_data[2][-1], bins, label="0.03 mWh".format(ttc_data[2][0]/3.6) )
    ax.hist(ttc_data[1][-1], bins, label="0.003 mWh".format(ttc_data[1][0]/3.6) )
    ax.set_xscale('log')
    ax.set_xlim(4, 10**5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Number of Events Completed')
    ax.axvline(x=60     , color='C4')
    ax.text(45, 20, '1 minute', weight='bold', color='C4', rotation=90)
    ax.axvline(x=3600   , color='C4')
    ax.text(45*60, 20, '1 hour', weight='bold', color='C4', rotation=90)
    ax.axvline(x=3600*12, color='C4')
    ax.text(45*60*12, 20 , '12 hours', weight='bold', color='C4', rotation=90)
    ax.legend(frameon=False)
    plt.savefig('ttc_histogram.png', dpi=300, bbox_inches='tight')
    plt.savefig('ttc_histogram.pdf', bbox_inches='tight')
    exit()
#colors = [x for x in [cmap(0.3), cmap(0.4), cmap(0.9)] for _ in range(0, 3)]
#markers = ['o', 's', '^'] * (4)
#
## plot usage vs secondary:
#plt.figure()
#plt.grid(True, which='both', ls='-.', alpha=0.5)
#plt.xscale('log')
#for i, x in enumerate(sorted(data)):
#    plt.plot(x[2][:,0], 100*x[2][:,2], color=colors[i], marker=markers[i], label=x[1] + ', ' + x[0])
#plt.title('Energy Utilized vs Secondary Capacity')
#plt.xlabel('Energy Capacity (J)')
#plt.ylabel('Energy Utilized (%)')
##handles, labels = plt.gca().get_legend_handles_labels()
##hanbles = sorted(zip(handles, labels), key=lambda x: int(x[1].split('s')[0]))
##handles = [x[0] for x in hanbles]
##labels  = [x[1] for x in hanbles]
#lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#plt.savefig('usage_vs_secondary_size', bbox_extra_artists=(lgd,), bbox_inches='tight')

colors = ['C0', 'C1']
markers = ['o', 's', '^', 'D']

custom_lines = [Line2D([0],[0], color = 'C0', lw=2),
                Line2D([0],[0], color = 'C1', lw=2),
                Line2D([0],[0], marker = markers[0], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[1], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[2], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[3], color='black', lw=2, markersize=8)]
lines_names = [trace_name_to_alias["SetupA"],
               trace_name_to_alias["SetupD"],
               "0.00028 mWh",
               "0.0028 mWh",
               "0.028 mWh",
               "0.28 mWh"]


# plot ttc
plt.figure(num=None, dpi=300,figsize=(10.7,5))
plt.grid(True, which='major')
plt.xscale('log')
plt.ylim(0,1)
print(data[0])
exit()
for i, irr_data in enumerate(sorted(data, key=lambda x: (float(x[0].split(' ')[0]), float(x[1])))):
    for j, size_data in enumerate(irr_data[2]):
        X = np.sort(size_data[5])
        F = np.array(range(1, size_data[5].size + 1))/float(size_data[5].size)
        plt.plot(X, F,  color=colors[i], lw=2, markersize=8, marker=markers[j], label=str(round_sigfigs(float(size_data[0])/3600.0*1E3, 2))+ ' mWh, ' + irr_data[0])
    #plt.plot(data[2][:,0], 100*data[2][:,2], color=colors[i], marker=markers[i], label=data[1] + ', ' + data[0])
#plt.title('Event Time to Completion')
plt.xlabel('Event Time to Completion (s)')
plt.ylabel('Ratio of Events')
#handles, labels = plt.gca().get_legend_handles_labels()
#hanbles = sorted(zip(handles, labels), key=lambda x: int(x[1].split('s')[0]))
#handles = [x[0] for x in hanbles]
#labels  = [x[1] for x in hanbles]
#lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
lgd = plt.legend(custom_lines, lines_names, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('ttc_histogram.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight', format='pdf')

