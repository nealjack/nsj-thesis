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
["Ceramic",     "47\u03BCF",  0.032, 6060000,   12100000],
["Ceramic",     "100\u03BCF", 0.069, 6250000,   12500000],
["Tantalum",    "100\u03BCF", 0.030, 2670000,   5340000],
["Tantalum",    "220\u03BCF", 0.034, 1370000,   2740000],
["Supercap",    "7.5mF",      0.980, 4690,      9380],
["Supercap",    "33mF",       0.159, 17400,     34800],
["Supercap",    "100mF",      0.372, 33.5,      67],
["Supercap",    "470mF",      1.17,  16500,     33000],
["Li-ion",      "11mAh",      213,   96.9,      387],
["Li-ion",      "40Ah",       147,   44.4,      276],
["Li-ion",      "80mAh",      295,   147,       736],
["LiPo",        "40mAh",      224,   224,       448],
["LTO",         "1.8mAh",     48.9,  489,       978],
["LTO",         "20mAh",      70.4,  1410,      2820],
["LiFePO4",     "70mAh",      143,   1430,      2145],
]

for row in data:
    if "Ceramic" in row:
        row += ['tab:blue']
    elif "Tantalum" in row:
        row += ['tab:purple']
    elif "Supercap" in row:
        row += ['tab:green']
    elif "Li-ion" in row or "LiPo" in row:
        row += ['tab:orange']
    elif "LTO" in row:
        row += ['tab:red']
    elif "LiFePO4" in row:
        row += ['tab:pink']


data = np.array(data)

fig = plt.figure(figsize=(10.7, 5), dpi=300)
for x in data:
    print(x)
    mean = x[3:5].astype(float).mean()
    mins = x[3].astype(float)
    plt.errorbar(x[2].astype(float), mean, mean-mins, ls='none', linewidth=2, capsize=2, markeredgewidth=2, color=x[-1], label=x[0])
plt.yscale('log')
plt.xscale('log')
plt.grid(True, axis='both', color='lightgray')
plt.xlabel("Energy Density (Wh/L)")
plt.ylabel("Power Density (W/L)")
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
print(by_label)
plt.legend(by_label.values(), by_label.keys())
plt.savefig("ragone.pdf", bbox_inches='tight')

