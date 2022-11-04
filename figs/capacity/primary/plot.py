#! /usr/bin/env python3
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.lines as lines
import matplotlib.patches as mpatches
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
    text = plt.text(1E-3, 51.5, 'Capacitor',horizontalalignment='center')
    ls.append(lines.Line2D([5E-3, 5E-3], [-2, 52], lw=2, color = 'black', clip_on=False))
    plt.text(6E-2, 51.5, 'Supercap',horizontalalignment='center')
    ls.append(lines.Line2D([.5, .5], [-2, 52], lw=2, color = 'black', clip_on=False))
    plt.text(10, 51.5, 'Battery', horizontalalignment='center')
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

secondary_size_data = []
sensensend = []
dooroccu = []
fnames = glob('./*.npy')
for fname in fnames:
    # get duty cycle:
    period = fname.split('_')[-1].split('.')[0]

    # get setup name:
    setup_name = fname.split('/')[-1].split('_')[0]
    irradiance = setup_name_to_irradiance[setup_name]
    if setup_name == 'SetupC': continue
    to_append = secondary_size_data
    if 'sense_and_send' in fname:
        to_append = sensensend
    elif 'door_occupancy' in fname:
        to_append = dooroccu
    to_append.append([irradiance, period, np.load(fname, allow_pickle=True)])

colors = [x for x in ['C0', 'C1', 'C2'] for _ in range(0, 3)]
#colors = [x for x in [cmap(0.3), cmap(0.4), cmap(0.9)] for _ in range(0, 3)]
markers = ['o', 's', '^'] * (4)

custom_lines = [Line2D([0],[0], color = 'C0', lw=2),
                Line2D([0],[0], color = 'C1', lw=2),
                Line2D([0],[0], marker = markers[0], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[1], color='black', lw=2, markersize=8),
                Line2D([0],[0], marker = markers[2], color='black', lw=2, markersize=8)]
lines_names = [setup_name_to_irradiance["SetupA"],
               setup_name_to_irradiance["SetupD"],
               "CR927",
               "CR2032",
               "CR123A"]

# plot lifetime vs secondary:
plt.figure(dpi=300,figsize=(10.7,5))
plt.grid(True, which='major')
plt.xscale('log')
plt.ylim(-2,50)
plt.xlim(2E-4, 2E2)
#plot_recs(plt)
text = plot_lines(plt)

def label_to_capacity(label):
    lab = 0
    if(label.upper() == 'CR927'):
        lab = 90
    elif label.upper() == 'CR2032':
        lab = 720
    elif label.upper() == 'CR123A':
        lab = 4500
    else:
        print("Do not recognize battery!!!")
        sys.exit(1)
    return lab

for i, data in enumerate(sorted(sensensend, key=lambda x: (float(x[0].split(' ')[0]), label_to_capacity(x[1])))):
    lab = str(label_to_capacity(data[1])) + " mWh"
    print(data[2][-1,1]/data[2][0,1])
    plt.plot(data[2][:,0]/3600*1E3, data[2][:,1], color=colors[i], lw=2, markersize=8, marker=markers[i], label=lab + ', ' + data[0])

plt.xlabel('Rechargeable Energy Capacity (mWh)')
plt.ylabel('Lifetime (years)')
#lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#plt.savefig('sense_and_send_life_vs_sec_size.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight', format='pdf')
lgd = plt.legend(custom_lines, lines_names, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('sense_and_send_life_vs_sec_size.pdf', bbox_extra_artists=(lgd,text), bbox_inches='tight', format='pdf')

# plot lifetime vs secondary:
plt.figure(dpi=300,figsize=(10.7,5))
plt.grid(True, which='major')
plt.xscale('log')
plt.ylim(-2,50)
plt.xlim(2E-4, 2E2)
#plot_recs(plt)
text = plot_lines(plt)
for i, data in enumerate(sorted(dooroccu, key=lambda x: (float(x[0].split(' ')[0]), label_to_capacity(x[1])))):
    lab = str(label_to_capacity(data[1])) + " mWh"

    print(data[2][-1,1]/data[2][0,1])
    plt.plot(data[2][:,0]/3600*1E3, data[2][:,1], color=colors[i], lw=2, markersize=8, marker=markers[i], label=lab + ', ' + data[0])

plt.xlabel('Rechargeable Energy Capacity (mWh)')
plt.ylabel('Lifetime (years)')
lgd = plt.legend(custom_lines, lines_names, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
lgd.set_visible(False)
#lgd = plt.legend(custom_lines, lines_names)
plt.savefig('door_occu_life_vs_sec_size.pdf', bbox_extra_artists=(lgd,text), bbox_inches='tight', format='pdf')

