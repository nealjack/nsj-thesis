#! /usr/bin/env python3
import numpy as np
import matplotlib
import math
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import matplotlib.lines as lines
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection
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

def plot_recs(plt):
    ax = plt.gca()
    patches = []
    cap_rect = mpatches.Rectangle((2E-3, -2), 5E-3 - 2E-3, 104, color = 'white')
    patches.append(cap_rect)
    supercap_rect = mpatches.Rectangle((5E-3, -2), 1 - 5E-3, 104, color = '#CCCCCC')
    patches.append(supercap_rect)
    battery_rect = mpatches.Rectangle((1, -2), 300 - 1, 104, color = '#909090')
    patches.append(battery_rect)
    collection = PatchCollection(patches, match_original=True)
    ax.add_collection(collection)

def plot_lines(plt):
    ax = plt.gca()
    ls = []
    text = plt.text(1E-3, 106, 'Capacitor',horizontalalignment='center')
    ls.append(lines.Line2D([5E-3, 5E-3], [-2, 108], lw=2, color = 'black', clip_on=False))
    plt.text(6E-2, 106, 'Supercap',horizontalalignment='center')
    ls.append(lines.Line2D([.5, .5], [-2, 108], lw=2, color = 'black', clip_on=False))
    plt.text(10, 106, 'Battery', horizontalalignment='center')
    for l in ls:
        ax.add_line(l)
    return text

setup_name_to_irradiance = {
    'SetupA': '15.1 μW/cm$^2$',
    'SetupB': '14.9 μW/cm$^2$',
    'SetupC': '745 μW/cm$^2$',
    'SetupD': '97.4 μW/cm$^2$',
    'SetupE': '142 μW/cm$^2$',
}

np.random.seed(42)

secondary_size_data = []
reliability_vs_secondary_data = []
fnames = glob('./*.npy')
for fname in fnames:
    # get duty cycle:
    period = fname.split('_')[-1].split('.')[0]

    # get setup name:
    setup_name = fname.split('/')[-1].split('_')[0]
    irradiance = setup_name_to_irradiance[setup_name]
    if setup_name == 'SetupC': continue
    to_append = secondary_size_data
    if 'secondary_capacity' in fname:
        to_append = secondary_size_data
    to_append.append([irradiance, period, np.load(fname,allow_pickle=True)])

colors = [x for x in ['C0', 'C1', 'C2'] for _ in range(0, 3)]
#colors = [x for x in [cmap(0.3), cmap(0.4), cmap(0.9)] for _ in range(0, 3)]
markers = ['o', 's', '^'] * (4)

# plot usage vs secondary:
plt.figure(dpi=300,figsize=(10.7,5))
#plt.grid(True, which='both', ls='-.')
plt.grid(True, which='major')
plt.xscale('log')
plt.ylim(0,100)
plt.xlim(2E-4, 2E2)
#plot_recs(plt)
text = plot_lines(plt)
for i, data in enumerate(sorted(secondary_size_data, key=lambda x: (float(x[0].split(' ')[0]), int(x[1])))):
    print(data[1])
    print(data[2][0,2], data[2][-1,2])
    print(data[2][-1,2] / data[2][0,2])
    plt.plot(data[2][:,0]/3600*1E3, 100*data[2][:,2], color=colors[i], lw=2, markersize=8, marker=markers[i], label=data[1] + 's, ' + data[0])
#plt.title('Energy Utilized vs Secondary Capacity')
plt.xlabel('Energy Capacity (mWh)')
plt.ylabel('Ambient Energy Utilized (%)',position=(0,0.42))
#handles, labels = plt.gca().get_legend_handles_labels()
#hanbles = sorted(zip(handles, labels), key=lambda x: int(x[1].split('s')[0]))
#handles = [x[0] for x in hanbles]
#labels  = [x[1] for x in hanbles]
custom_lines = [Line2D([0],[0], color = 'C0', lw=2),
                Line2D([0],[0], color = 'C1', lw=2),
                Line2D([0],[0], marker = markers[0], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[1], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[2], color='black', lw=2, markersize=8)]
lines_names = [setup_name_to_irradiance["SetupA"],
               setup_name_to_irradiance["SetupD"],
               "30s",
               "60s",
               "120s"]

lgd = plt.legend(custom_lines, lines_names, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('usage_vs_secondary_size.pdf', bbox_extra_artists=(lgd,text), bbox_inches='tight', format='pdf')

# plot usage vs secondary:
plt.figure(dpi=300,figsize=(10.7,5))
plt.grid(True, which='major')
plt.xscale('log')
plt.xlim(2E-4, 2E2)
plt.ylim(0,100)
#plot_recs(plt)
text = plot_lines(plt)
print('-')
for i, data in enumerate(sorted(secondary_size_data, key=lambda x: (float(x[0].split(' ')[0]), int(x[1])))):
    print(data[1])
    print(data[2][0,3], data[2][-1,3])
    print(data[2][-1,3] / data[2][0,3])
    plt.plot(data[2][:,0]/3600*1E3, 100*data[2][:,3], color=colors[i], lw=2, markersize=8, marker=markers[i], label=data[1] + 's, ' + data[0])
#plt.title('Reliability vs Secondary Capacity')
plt.xlabel('Energy Capacity (mWh)')
plt.ylabel('Successful Events (%)')
lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('events_vs_secondary_size.pdf', bbox_extra_artists=(lgd,text), bbox_inches='tight', format='pdf')
