#! /usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

data = [
["Ceramic",     "47\u03BCF",  0.000000259,  0.032, 6060000,   12100000, 0.16],
["Ceramic",     "100\u03BCF", 0.00000139,   0.069, 6250000,   12500000, 0.31],
["Tantalum",    "100\u03BCF", 0.000000551,  0.030, 2670000,   5340000,  0.28],
["Tantalum",    "220\u03BCF", 0.00000306,   0.034, 1370000,   2740000,  0.37],
["Supercap",    "7.5mF",      0.0000704,    0.980, 4690,      9380,     2.42],
["Supercap",    "33mF",       0.000139,     0.159, 17400,     34800,    8.65],
["Supercap",    "100mF",      0.000420,     0.372, 33.5,      67,       1.10],
["Supercap",    "470mF",      0.00115,      1.17,  16500,     33000,    5.06],
["Li-ion",      "11mAh",      0.0407,       213,   96.9,      387,      4.00],
["Li-ion",      "40Ah",       0.148,        147,   44.4,      276,      1.62],
["Li-ion",      "80mAh",      0.296,        295,   147,       736,      7.00],
["Li-ion",      "40mAh",      0.148,        224,   224,       448,      4.50],
["LTO",         "1.8mAh",     0.0043,       48.9,  489,       978,      1.25],
["LTO",         "20mAh",      0.0480,       70.4,  1410,      2820,     6.75],
["LFP",         "70mAh",      0.224,        143,   1430,      2145,     1.25],
["Solid State", "0.7mAh",     0.00273,      18.8,  134.2,     289,      30.00],
["Solid State", "0.1mAh",     0.00015,      10.3,  2.07,      517,      9.31],
]

for row in data:
    if "Ceramic" in row:
        row += ['tab:blue']
    elif "Tantalum" in row:
        row += ['tab:cyan']
    elif "Supercap" in row:
        row += ['tab:green']
    elif "Li-ion" in row:
        row += ['tab:red']
    elif "LTO" in row:
        row += ['tab:pink']
    elif "LFP" in row:
        row += ['tab:orange']
    elif "Solid State" in row:
        row += ['tab:purple']


data = np.array(data)

fig = plt.figure(figsize=(10.7, 5), dpi=300)
for x in data:
    print(x)
    mean = x[4:6].astype(float).mean()
    mins = x[4].astype(float)
    plt.errorbar(x[3].astype(float), mean, mean-mins, ls='none', linewidth=2, capsize=2, markeredgewidth=2, color=x[-1], label=x[0])
plt.yscale('log')
plt.xscale('log')
plt.grid(True, axis='both', color='lightgray')
plt.xlabel("Energy Density (Wh/L)")
plt.ylabel("Power Density (W/L)")
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
print(by_label)
plt.legend(by_label.values(), by_label.keys(),loc="upper right",prop={'size':10})
plt.savefig("ragone.pdf", bbox_inches='tight')

types = ['Ceramic', 'Tantalum', 'Supercap', 'Li-ion', 'LTO', 'LFP', 'Solid State']
print(types)
avg = []
colors = []
for t in types:
    print(t)
    select = np.where(data[:,0] == t)
    colors += [data[select,-1][0][0]]
    group = data[select,2].astype(float)/ data[select,6].astype(float)
    avg += [group.mean()]
print(avg)
print(colors)
fig = plt.figure(figsize=(10.7, 5), dpi=300)
plt.yscale('log')
plt.scatter(types, avg, linewidth=2, color=colors)
plt.grid(axis='y')
plt.xlabel("Energy Storage Type")
plt.ylabel("Energy Capacity per USD (Wh/$)")
plt.savefig("energy_per_cost.pdf", bbox_inches='tight')
