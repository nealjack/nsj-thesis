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

SECONDS_IN_DAY = 60*60*24
SECONDS_IN_YEAR = 60*60*24*365
DAYS_TO_MODEL = 365

trace_fnames = glob('traces/*.npy')
trace_fnames.sort()
trace_fnames = trace_fnames[:-2]
traces = {}

#b = 2*math.pi / SECONDS_IN_DAY
amplitudes = np.logspace(-6, -3, 100) #np.array([x * 1E-6 for x in range(10, 101, 10)])
#seconds = np.array(range(0, DAYS_TO_MODEL * SECONDS_IN_DAY))
margins = [x/10.0 for x in range(0, 10)]#np.array([x/10 for x in range(2,12,2)])
capacities = np.logspace(-3, 3, num=200)
total_runs = len(amplitudes) * len(margins) * len(capacities)
print(total_runs)
#print(len(capacity), len(a), len(disparity))
#
#sine = np.sin(b * seconds + 3/2 * math.pi)
#sine_funcs = np.dot(a.reshape((len(a), 1)), sine.reshape((1, len(sine))))
#for row, value in zip(sine_funcs, a):
#    row += value
#season_sine = np.sin(2*math.pi / SECONDS_IN_YEAR * seconds) + 1
#sine_funcs_season = sine_funcs * season_sine

def load_trace(fname):
    a = np.load(fname)[1:]
    # scale mean to 1
    a = a / np.mean(a)
    times = [30*x for x in range(len(a))]
    newtimes = [x for x in range(times[-1])]
    b = np.interp(newtimes, times, a)
    return (fname.split('.')[0].split('/')[-1], b)

def run(index, amplitude, margin, capacity, trace_name):
    start = time.time()
    trace = traces[trace_name]
    e = np.zeros(trace.shape)
    income = trace * amplitude
    actual_capture = np.zeros(trace.shape)
    workload = amplitude * (1 - margin)


    for ind, i in enumerate(income):
        if ind == 0:
            e[ind] = i - workload
        else:
            e[ind] = e[ind-1] + i - workload

        actual_capture[ind] = i

        if e[ind] >= capacity:
            actual_capture[ind] = capacity - e[ind-1]
            e[ind] = capacity
        elif e[ind] < 0:
            e[ind] = 0

    total = np.sum(income)
    actual = np.sum(actual_capture)

    elapsed = time.time() - start
    print("simulation: {}/{}".format(index, total_runs), trace_name, elapsed)
    result = {"index": index, "income": amplitude, "margin": margin, "capacity": capacity, "workload": workload, "total": total, "actual": actual, "actual_avg": actual/(len(trace)), "type": trace_name}
    return result

#amp = a[4]
#for y in disparity:
#    print(y)
#    r = run(amp, y, 10)
#    print(r['actual_avg'] / r['workload'])
#
#exit()
results = {}
results_fnames = glob('results/*capacity.csv')
results_fnames.sort()
print(trace_fnames)
print(results_fnames)
if len(results_fnames) < len(trace_fnames):
    with Pool() as pool:
        loaded_data = pool.map(load_trace, trace_fnames)
        for d in loaded_data:
            traces[d[0]] = d[1]

    with Pool(processes=20) as pool:
        for trace in traces:
            print(trace)
            execute_list = [[amplitudes[i], y, z, trace] for i,_ in enumerate(amplitudes) for y in margins for z in capacities]
            execute_list = [[x] + y for x,y in enumerate(execute_list)]
            result = list(pool.starmap(run, execute_list))
            print("Done")
            df = pd.DataFrame(result)
            df.to_csv('results/' + trace + "_capacity.csv")
            results[trace] = df

else:
    for fname in results_fnames:
        trace = fname.split('_')[0]
        traces[trace] = []
        results[trace] = pd.read_csv(fname)

df = pd.concat(results.values())
df["actual_avg_vs_work"] = df["actual_avg"] / df["workload"]
print(df)
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

def plot_curve(amplitude):
    fig, ax = plt.subplots(figsize=(10.7, 5), dpi=300)
    dfi = df[df["income"] == amplitude]
    dfi = dfi.sort_values(["capacity", "type"])
    print(amplitude, dfi["income"].iloc[0])
    for typ in traces:
        dfi_type_slice = dfi[dfi["type"] == typ]
        ax.plot(dfi_type_slice["capacity"] / 3600 * 1E3, dfi_type_slice["actual_avg_vs_work"], label=typ)
    ax.set_xscale("log")
    ax.set_xlabel("Capacity (mWh)")
    ax.set_ylabel("Percent Energy Captured (%)")
    ax.legend()
    fig.savefig("percent_v_capacity_" + str(amplitude) + ".pdf", bbox_inches='tight')
    plt.close()

#with Pool() as pool:
#    pool.map(plot_curve, amplitudes)

fig, ax = plt.subplots(figsize=(10.7, 5), dpi=300)

if "margin" in df:
    dfd = df[df["margin"] == 0]
else:
    dfd = df[df["disparity"] == 1]
dfd = dfd.sort_values(["capacity", "income_index", "type"])
print(dfd)

income_v_sufficient_capacity = {}
for typ in traces:
    income_v_sufficient_capacity[typ] = []
for amplitude in pd.unique(dfd["income"]):
    dfd_slice = dfd[dfd["income"] == amplitude]
    income = dfd_slice.iloc[0]["income"]

    for typ in traces:
        dfd_slice_type = dfd_slice[dfd_slice["type"]==typ.split('/')[-1]]
        first_sufficient = dfd_slice_type[dfd_slice_type["actual_avg_vs_work"] >= 1]
        if(len(first_sufficient) == 0):
            print(dfd_slice_type)
            break
        first_sufficient = first_sufficient.iloc[0]["capacity"]
        income_v_sufficient_capacity[typ].append([amplitude, first_sufficient])

#ivsc = pd.DataFrame(income_v_sufficient_capacity)
#print(ivsc)
for x in income_v_sufficient_capacity:
    income_v_sufficient_capacity[x] = np.array(income_v_sufficient_capacity[x])
    line = ax.scatter(income_v_sufficient_capacity[x][:,0], income_v_sufficient_capacity[x][:,1] / 3600 * 1E3, alpha=0.5, s= 8)
    color = line.get_facecolor()
    #line = ax.plot(income_v_sufficient_capacity[x][:,0], income_v_sufficient_capacity[x][:,1] / 3600 * 1E3, label=x)
    #color = line[0].get_color()
    p = np.polyfit(income_v_sufficient_capacity[x][:,0], income_v_sufficient_capacity[x][:,1], 1)
    p[1] = 0
    fit = np.poly1d(p)
    print(fit / 3600 * 1E3)
    name = x[:-1] + " " + x[-1] + ", m = " + "%.1E" % (p[0] / 3600 * 1E3)
    ax.plot(income_v_sufficient_capacity[x][:,0], fit(income_v_sufficient_capacity[x][:,0] / 3600 * 1E3),  color=color, alpha = 1, label=name)
    print(x, p)

ax.set_xlabel("Workload/Income Power (W)")
ax.set_ylabel("Minimum Sufficient Capacity (mWh)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1E-6, 2E-4)
ax.set_ylim(2E-1, 1E2)
ax.legend(loc="lower right")
fig.savefig("required_capacity.pdf", bbox_inches='tight')


exit()
