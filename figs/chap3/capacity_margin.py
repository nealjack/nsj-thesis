#! /usr/bin/env python

import os
import math
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.legend import Legend
from matplotlib.lines import Line2D

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = "14"
plt.rcParams["grid.linewidth"] = "1"

results = pd.read_csv("margin_results/SetupD_capacity.csv",index_col="index")
results = results.sort_values(["capacity", "income", "type"])
results["actual_avg_vs_work"] = results["actual_avg"] / results["workload"]

income_v_sufficient_capacity = {}

fig, ax = plt.subplots(figsize=(10.7, 5), dpi=300)

for margin in [0, 0.2, 0.4, 0.5, 0.6, 0.8]:#pd.unique(results["margin"]):
    print(margin)
    r_slice = results[results["margin"] == margin]
    income_v_sufficient_capacity[margin] = []

    for amplitude in pd.unique(results["income"]):
        print(amplitude)
        r_slice_amp = r_slice[r_slice["income"] == amplitude]
        first_sufficient = r_slice_amp[r_slice_amp["actual_avg_vs_work"] >= 1]
        if(len(first_sufficient) == 0):
            print(r_slice_amp)
            break
        first_sufficient = first_sufficient.iloc[0]["capacity"]
        income_v_sufficient_capacity[margin].append([amplitude, first_sufficient])

    print(income_v_sufficient_capacity[margin])
    array = np.array(income_v_sufficient_capacity[margin])
    p = np.polyfit(array[:,0], array[:,1], 1)
    p[1] = 0
    fit = np.poly1d(p)
    name = "%.1f" % margin + " margin, m = " + "%.1E" % (p[0] / 3600 * 1E3)
    line = ax.scatter(array[:,0], array[:,1] / 3600, alpha=0.5, s=8)
    color = line.get_facecolor()
    ax.plot(array[:,0], fit(array[:,0] / 3600),  color=color, alpha = 1, label=name)

ax.set_xlabel("Income Power (W)")
ax.set_ylabel("Minimum Sufficient Capacity (Wh)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1E-6, 2E-4)
ax.set_ylim(2E-1 / 1E3, 1E2 / 1E3)
ax.legend(loc="lower right")
fig.savefig("capacity_margin.pdf", bbox_inches='tight')
exit()
