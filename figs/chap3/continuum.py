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
from multiprocessing import Pool

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = "14"
#plt.rcParams["xtick.major.width"] = "0.5"
#plt.rcParams["xtick.major.size"]  = "6"
#plt.rcParams["xtick.minor.width"] = "0.8"
#plt.rcParams["xtick.minor.size"] = "4"
#plt.rcParams["ytick.major.width"] = "1"
#plt.rcParams["ytick.major.size"] = "6"
#plt.rcParams["ytick.minor.width"] = "0.8"
#plt.rcParams["ytick.minor.size"] = "4"
plt.rcParams["grid.linewidth"] = "1"

caps = np.array([0.1, 10, 100, 1000, 100000, 1E6])
caps *= 1E-6
energy = 1/2 * caps * (3.3**2 - 1.8**2)

def to_mWh(joule):
    return joule / 3600 * 1E3

def decouple_to_period(cap):
    return cap / 10E-3 * (2 * math.pi * 3.3)

periods = decouple_to_period(caps)
mwh_energies = to_mWh(energy)

print("capacitance", caps)
print("energy mWh", mwh_energies)
print("period", periods)
scale = (mwh_energies[0] / periods[0])
day = 24*3600*scale
week = day * 7
month = week * 4
season = month * 3
print(day, week, month, season)
fig, ax = plt.subplots(figsize=(10.7,5))
ax.scatter(mwh_energies/2, periods)
ax.set_ylim(1E-5, 1E7)
ax.set_xlim(1E-7, 1E2)
ax.set_xscale('log')
ax.set_yscale('log')
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.set_yticks([1E-3, 1, 60, 3600, 24*3600, 30*24*3600, 3*30*24*3600])
ax.set_yticklabels(['millisecond', 'second', 'minute', 'hour', 'day', 'month', 'season'])
ax.set_ylabel("Scale of Temporal Variation")
ax.set_xlabel("Energy Capacity (mWh)")
plt.savefig("continuum.pdf", bbox_inches="tight")
