#! /usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
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

