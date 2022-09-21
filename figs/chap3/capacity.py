#! /usr/bin/env python

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from multiprocessing import Pool

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

SECONDS_IN_DAY = 60*60*24
SECONDS_IN_YEAR = 60*60*24*365
DAYS_TO_MODEL = 365

b = 2*math.pi / SECONDS_IN_DAY
a = np.logspace(-6, -4, 10) #np.array([x * 1E-6 for x in range(10, 101, 10)])
seconds = np.array(range(0, DAYS_TO_MODEL * SECONDS_IN_DAY))
disparity = [1]#np.array([x/10 for x in range(2,12,2)])
capacity = np.logspace(-3, 3, num=100)
print(len(capacity), len(a), len(disparity))

sine = np.sin(b * seconds + 3/2 * math.pi)
sine_funcs = np.dot(a.reshape((len(a), 1)), sine.reshape((1, len(sine))))
for row, value in zip(sine_funcs, a):
    row += value
season_sine = np.sin(2*math.pi / SECONDS_IN_YEAR * seconds) + 1
sine_funcs_season = sine_funcs * season_sine

random_funcs = []
np.random.seed(42)
for value in a:
    random_funcs.append(np.abs(np.random.normal(value, value/2, len(seconds))))
random_funcs = np.array(random_funcs)

def run(a_i, a, d, c, typ):
    e = np.zeros(seconds.shape)
    # model income as sinusoid with day period and shifted to be positive
    if typ == "season":
        income = sine_funcs_season[a_i]
    elif typ == "diurnal":
        income = sine_funcs[a_i]
    else:
        print("No valid type")
        exit()
    actual_work = np.zeros(seconds.shape)
    w = a * d
    print("settings: ", w, a, c)


    for ind, i in enumerate(income):
        if ind == 0:
            e[ind] = i - w
        else:
            e[ind] = e[ind-1] + i - w

        actual_work[ind] = w

        if e[ind] > c:
            e[ind] = c
        elif e[ind] < 0:
            e[ind] = 0
            actual_work[ind] = 0

    total = np.sum(income)
    actual = np.sum(actual_work)

    result = {"income": a, "income_index": a_i, "disparity": d, "capacity": c, "workload": w, "total": total, "actual": actual, "actual_avg": actual/(DAYS_TO_MODEL*SECONDS_IN_DAY), "type": typ}

    return result

#amp = a[4]
#for y in disparity:
#    print(y)
#    r = run(amp, y, 10)
#    print(r['actual_avg'] / r['workload'])
#
#exit()

if not os.path.isfile("capacity_season.csv") and not os.path.isfile("capacity_diurnal.csv"):

    with Pool() as pool:
        season_execute_list = [(i, a[i], y, z, "season") for i,_ in enumerate(a) for y in disparity for z in capacity]
        diurnal_execute_list = [(i, a[i], y, z, "diurnal") for i,_ in enumerate(a) for y in disparity for z in capacity]
        season_results = list(pool.starmap(run, season_execute_list))
        diurnal_results = list(pool.starmap(run, diurnal_execute_list))
        print("Done")
    df_season = pd.DataFrame(season_results)
    df_season.to_csv("capacity_season.csv")
    df_diurnal = pd.DataFrame(diurnal_results)
    df_diurnal.to_csv("capacity_diurnal.csv")

else:
    df_season = pd.read_csv("capacity_season.csv")
    df_diurnal = pd.read_csv("capacity_diurnal.csv")

if "type" not in df_season:
    df_season["type"] = ["season"] * len(df_season)
    df_season.to_csv("capacity_season.csv")
    print(df_season)
if "type" not in df_diurnal:
    df_diurnal["type"] = ["diurnal"] * len(df_diurnal)
    df_diurnal.to_csv("capacity_diurnal.csv")
    print(df_diurnal)

frames = [df_season, df_diurnal]
df = pd.concat(frames)

#fig, ax = plt.subplots(figsize=(10.7, 5), dpi=300)
#for i in df.income.unique():
#    dfi = df[df["income"] == i]
#
#
#    for d in dfi.disparity.unique():
#        dfid = dfi[dfi["disparity"] == d]
#        dfid = dfid.sort_values("capacity")
#        #print(dfid)
#        ax.plot(dfid["capacity"], dfid["actual_avg"] / (dfid["workload"]), label=str(d) + " " + str(i))
#
#ax.set_xlabel("Capacity (J)")
#ax.set_ylabel("Workload captured (%)")
#ax.set_xscale("log")
#ax.legend()
#fig.savefig("percent_workload")

fig, ax = plt.subplots(figsize=(10.7, 5), dpi=300)

df["actual_avg_vs_work"] = df["actual_avg"] / df["workload"]
dfd = df[df["disparity"] == 1.0]
dfd = dfd.sort_values(["capacity", "income_index"])
print(dfd)
income_v_sufficient_capacity = {}
for typ in ["diurnal", "season"]:
    income_v_sufficient_capacity[typ] = []
for ind in range(0, len(a)):
    dfd_slice = dfd[dfd["income_index"] == ind]
    income = dfd_slice.iloc[0]["income"]
    print(ind, income)

    for typ in ["diurnal", "season"]:
        dfd_slice_type = dfd_slice[dfd_slice["type"]==typ]
        first_sufficient = dfd_slice_type[dfd_slice_type["actual_avg_vs_work"] > 0.9]
        first_sufficient = first_sufficient.iloc[0]["capacity"]
        income_v_sufficient_capacity[typ].append([a[ind], first_sufficient])

for x in income_v_sufficient_capacity:
    print(x)
    income_v_sufficient_capacity[x] = np.array(income_v_sufficient_capacity[x])
    print(income_v_sufficient_capacity[x])
    ax.plot(income_v_sufficient_capacity[x][:,0], income_v_sufficient_capacity[x][:,1], label=x)

    p = np.polyfit(income_v_sufficient_capacity[x][:,0], income_v_sufficient_capacity[x][:,1], 1)
    print(x, p)

ax.set_xlabel("Workload/Income Power (W)")
ax.set_ylabel("Minimum Sufficient Capacity (J)")
#ax.set_xscale("log")
#ax.set_yscale("log")
fig.savefig("required_capacity", bbox_inches='tight')


exit()
