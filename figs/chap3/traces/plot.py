#! /usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
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
plt.rcParams["grid.linewidth"] = "1"

seconds_in_day = 60*60*24

traces = ['SetupA.npy','SetupB.npy','SetupC.npy','SetupD.npy']
lines = []

fig, axes = plt.subplots(2,2,figsize=(10.7, 5), dpi=300, sharex=True, sharey=True, gridspec_kw= {'wspace':0.05, 'hspace':0.2})

for fname, ax in zip(sorted(traces), [x for sl in axes for x in sl]):
    print(ax)
    a = np.load(fname)[1:]
    a = (a - np.min(a)) / (np.max(a) - np.min(a))
    print(fname, np.mean(a))
    print(len(a) * 30 /seconds_in_day)
    time = np.array([x*30 for x in range(0,len(a))])
    data = pd.DataFrame({"time": time, "irradiance":a})
    data["moving_avg"] = data.rolling(window=int(seconds_in_day/30)).mean()["irradiance"]
    #a = a[:int(int(len(a) / (seconds_in_day / 30)) * (seconds_in_day / 30))]
    #a = a.reshape(-1, int(seconds_in_day / 30))
    #a = np.mean(a, 1)
    length = 365 * int(seconds_in_day / 30)
    #x = 300 * np.sin(time * 2 * math.pi + 1.25 * math.pi) - 160
    #x[x < 0] = 0
    #x *= np.mean(a) / np.mean(x)
    #print(np.mean(x))

    line, = ax.plot(data["time"][:length] / seconds_in_day, data["irradiance"][:length], linewidth=0.5)
    line, = ax.plot(data["time"][:length] / seconds_in_day, data["moving_avg"][:length], linewidth=1)
    #ax.plot(b[:length], x[:length])
    #line, = plt.plot(a, label=fname.split('.')[0])
    ax.yaxis.set_visible(False)
    title = fname.split('.')[0]
    title = " ".join([title[:-1], title[-1:]])
    ax.set_title(title, fontsize=10)
    lines.append(line)
    #ax.set_ylabel('µW/cm^2')
    #ax.set_xlabel('day')

fig.supxlabel('day')
fig.supylabel('irradiance', x=0.08)
fig.savefig('traces.pdf', bbox_inches="tight")
