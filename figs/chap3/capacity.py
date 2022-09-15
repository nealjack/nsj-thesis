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
DAYS_TO_MODEL = 30

b = 2*math.pi / SECONDS_IN_DAY
a = np.array([x * 1E-6 for x in range(10, 101, 10)])
seconds = np.array(range(0, DAYS_TO_MODEL * SECONDS_IN_DAY))
disparity = np.array([x/10 for x in range(2,12,2)])
capacity = np.logspace(-2, 1, num=10)
print(len(capacity), len(a), len(disparity))

def run(a, d, c):
    e = np.zeros(seconds.shape)
    full = np.zeros(seconds.shape)
    # model income as sinusoid with day period and shifted to be positive
    income = a * np.sin(b * seconds + 3/2 * math.pi) + a
    w = a * d
    print("settings:", w, a, c)

    total = 0

    for ind, i in enumerate(income):
        total += i
        if ind == 0:
            e[ind] = i - w
        else:
            e[ind] = e[ind-1] + i - w

        if e[ind] > c:
            e[ind] = c
        elif e[ind] < 0:
            e[ind] = 0

    total = np.sum(income)
    actual = np.sum(income[full < 1])

    plt.plot(income)
    plt.plot(e)
    plt.show()

    result = {"income": a, "disparity": d, "capacity": c, "workload": w, "total": total, "actual": actual, "actual_avg": actual/(DAYS_TO_MODEL*SECONDS_IN_DAY)}

    return result

amp = a[4]
for y in disparity:
    for z in capacity:
        r = run(amp, y, z)

exit()


if not os.path.isfile("capacity.csv"):

    with Pool() as pool:
        execute_list = [(x, y, z) for x in a for y in disparity for z in capacity]
        print(len(execute_list), len(disparity))
        results = list(pool.starmap(run, execute_list))

    df = pd.DataFrame(results)
    df.to_csv("capacity.csv")

else:
    df = pd.read_csv("capacity.csv")

print(df)

for i in df.income.unique():
    dfi = df[df["income"] == i]

    fig, ax = plt.subplots()

    for d in dfi.disparity.unique():
        dfid = dfi[dfi["disparity"] == d]
        dfid = dfid.sort_values("capacity")
        print(dfid)
        ax.plot(dfid["capacity"], dfid["actual_avg"] / (dfid["income"] * d), label=str(d))
    ax.set_xlabel("Capacity (J)")
    ax.set_ylabel("Workload captured (%)")
    ax.set_xscale("log")
    ax.legend()
    fig.savefig(("%.1E" % i).replace(".", "o") + "_test")
    exit()

fig, ax = plt.subplots()

for d in df.disparity.unique():
    dfd = df[df["disparity"] == d]
    dfd = dfd.sort_values("capacity")

    dfd0 = dfd[dfd["income"] == dfd.income.unique()[0]]
    dfdlast = dfd[dfd["income"] == dfd.income.unique()[-1]]

    dfd0percent = dfd0["actual_avg"] / (dfd0["income"] * d)
    dfdlastpercent = dfdlast["actual_avg"] / (dfdlast["income"] * d)

    dfd0["actual_avg_vs_work"] = dfd0percent
    dfdlast["actual_avg_vs_work"] = dfdlastpercent

    print(d)
    print(dfd0)
    print(dfdlast)

    #print(d)
    #print(dfd0[dfd0percent > 0.99])
    #print(dfdlast[dfdlastpercent > 0.99])

    ax.plot(dfd0["capacity"],  dfd0percent, label=str(d) + " " + "%.1E" % dfd.income.unique()[0])
    ax.plot(dfdlast["capacity"], dfdlastpercent, label=str(d) + " " + "%.1E" % dfd.income.unique()[-1])

ax.set_xlabel("Capacity (J)")
ax.set_ylabel("(%)")
ax.set_xscale("log")
ax.legend()
fig.savefig("test")



exit()






























colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc948', '#b07aa1', 'ff9da7', '#9c755f', '#bab0ac']

compound = False
battery_density = 653E-3 #W/cm3
solar_efficiency = .17
seconds_in_year = 3600*24*365

workloadss = [
        np.array([25E-6, 100E-6]),
        np.array([20E-9, 100E-9])]
labels = ['micro', 'nano']
c_i = 1

for label, workloads in zip(labels, workloadss):
    irradiance = np.array([10E-6, 100E-6]) # W/cm2
    lengths = np.array([l * 1E-3 for l in range(0, 8001,1)]) # cm

    b_energy = battery_density * np.power(lengths, 3) * 1E3 / 3600
    b_leakage = b_energy * 0.01 / seconds_in_year

    fig = plt.figure(figsize=(10.7, 5), dpi=300)
    ax = plt.gca()
    b_line = plt.plot(lengths, b_energy/3600*1E3, label='battery', linewidth=3)
    solid_line = Line2D([0],[0], color='k', label='high light solar')
    dotted_line = Line2D([0], [0], color='k', linestyle='--', label='low light solar')
    plt.yscale('log')
    if label == 'nano':
        plt.xlim(0,1)
        plt.ylim(1E-6, 1)
    else:
        plt.xlim(0, 8)
        plt.ylim(1E-2, 1E3)
    plt.ylabel("Energy (mWh)")
    plt.xlabel("Principal Node Dimension (cm)")
    lines = []

    for w in workloads:
        s_power_min = irradiance[0] * np.power(lengths, 2) * solar_efficiency
        s_power_max = irradiance[1] * np.power(lengths, 2) * solar_efficiency

        deficit_min = w - s_power_min
        deficit_min[deficit_min < 0] = 0
        deficit_min += b_leakage

        deficit_max = w - s_power_max
        deficit_max[deficit_max < 0] = 0
        deficit_max += b_leakage

        if compound:
            lifetimes_min = np.multiply(b_energy, np.reciprocal(deficit_min))
            lifetimes_max = np.multiply(b_energy, np.reciprocal(deficit_max))
        else:
            lifetimes_min = np.multiply(b_energy, np.reciprocal(w))
            lifetimes_max = np.multiply(b_energy, np.reciprocal(w))

        s_energy_min = np.multiply(s_power_min, lifetimes_min) * 1E3 / 3600
        s_energy_max = np.multiply(s_power_max, lifetimes_max) * 1E3 / 3600
        #s_percent_min = np.divide(s_energy_min, b_energy) * 100
        #s_percent_max = np.divide(s_energy_max, b_energy) * 100
        color = colors[c_i]
        c_i+=1
        #plt.fill_between(lengths, s_energy_min, s_energy_max, alpha=0.2, color=color)
        plt.plot(lengths, s_energy_min, '--', color=color)
        if label == 'nano':
            lines += plt.plot(lengths, s_energy_max, label='{} nW workload'.format(str(int(1E9*w))), color=color)
        else:
            lines += plt.plot(lengths, s_energy_max, label='{} μW workload'.format(str(int(1E6*w))), color=color)

    ax.legend(handles = [b_line[0], solid_line, dotted_line] + lines, loc='lower right', frameon=False)
    plt.savefig("is_eh_worth_it_"+label+".png", bbox_inches='tight')

