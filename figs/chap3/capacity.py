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
a = np.logspace(-6, -4, 5) #np.array([x * 1E-6 for x in range(10, 101, 10)])
seconds = np.array(range(0, DAYS_TO_MODEL * SECONDS_IN_DAY))
disparity = [1]#np.array([x/10 for x in range(2,12,2)])
capacity = np.logspace(-3, 1, num=5)
print(len(capacity), len(a), len(disparity))

sine = np.sin(b * seconds + 3/2 * math.pi)
sine_funcs = np.dot(a.reshape((len(a), 1)), sine.reshape((1, len(sine))))
for row, value in zip(sine_funcs, a):
    row += value
sine_funcs *= np.sin(2*math.pi / SECONDS_IN_YEAR * seconds) + 1
#print(a[0], np.mean(sine_funcs[0]))
#plt.plot(sine_funcs[0])
#plt.show()
#exit()

random_funcs = []
np.random.seed(42)
for value in a:
    random_funcs.append(np.abs(np.random.normal(value, value/2, len(seconds))))
random_funcs = np.array(random_funcs)

def run(a_i, a, d, c):
    e = np.zeros(seconds.shape)
    # model income as sinusoid with day period and shifted to be positive
    income = sine_funcs[a_i]
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

    result = {"income": a, "income_index": a_i, "disparity": d, "capacity": c, "workload": w, "total": total, "actual": actual, "actual_avg": actual/(DAYS_TO_MODEL*SECONDS_IN_DAY)}

    return result

#amp = a[4]
#for y in disparity:
#    print(y)
#    r = run(amp, y, 10)
#    print(r['actual_avg'] / r['workload'])
#
#exit()

if not os.path.isfile("capacity.csv"):

    with Pool() as pool:
        execute_list = [(i, a[i], y, z) for i,_ in enumerate(a) for y in disparity for z in capacity]
        print(len(execute_list), len(disparity))
        results = list(pool.starmap(run, execute_list))
        print("Done")
    df = pd.DataFrame(results)
    df.to_csv("capacity.csv")

else:
    df = pd.read_csv("capacity.csv")

print(df)

#for i in df.income.unique():
#    dfi = df[df["income"] == i]
#
#    fig, ax = plt.subplots()
#
#    for d in dfi.disparity.unique():
#        dfid = dfi[dfi["disparity"] == d]
#        dfid = dfid.sort_values("capacity")
#        #print(dfid)
#        ax.plot(dfid["capacity"], dfid["actual_avg"] / (dfid["workload"]), label=str(d))
#    ax.set_xlabel("Capacity (J)")
#    ax.set_ylabel("Workload captured (%)")
#    ax.set_xscale("log")
#    ax.legend()
#    fig.savefig(("%.1E" % i).replace(".", "o") + "_test")

fig, ax = plt.subplots()

df["actual_avg_vs_work"] = df["actual_avg"] / df["workload"]
dfd = df[df["disparity"] == 1.0]
dfd = dfd.sort_values(["capacity", "income_index"])

income_v_sufficient_capacity = []
for ind in range(0, len(a)):
    dfd_slice = dfd[dfd["income_index"] == ind]
    income = dfd_slice.iloc[0]["income"]
    print(ind, income)


    first_sufficient = dfd_slice[dfd_slice["actual_avg_vs_work"] > 0.9]
    first_sufficient = first_sufficient.iloc[0]["capacity"]
    print(ind, first_sufficient)
    print()
    income_v_sufficient_capacity.append([a[ind], first_sufficient])

income_v_sufficient_capacity = np.array(income_v_sufficient_capacity)
print(income_v_sufficient_capacity)
ax.plot(income_v_sufficient_capacity[:,0], income_v_sufficient_capacity[:,1])
ax.set_xlabel("Workload/Income Power (W)")
ax.set_ylabel("Minimum Capacity for 99% Workload Capture (J)")
ax.set_xscale("log")
fig.savefig("required_capacity", bbox_inches='tight')


exit()
