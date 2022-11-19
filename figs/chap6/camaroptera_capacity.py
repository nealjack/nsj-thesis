#! /usr/bin/env python3

import matplotlib
matplotlib.use('TKAgg')
from matplotlib import rcParams
font= {'family': 'Arial',
        'size': 14}
matplotlib.rc('font', **font)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fname = 'camaroptera_sweep.pkl'

a = pd.read_pickle(fname)
print(a)
fig, ax = plt.subplots(1, figsize=(12,6))
plt.plot(a['capacity_J']/3.6, 100* a['events_success'] / (a['events_success'] + a['events_missed']), label='% successful events', linewidth=2)
#plt.plot(a['capacity_J']/3.6, 100*a['time_online'], label='% time online')
#plt.plot(a['capacity_J']/3.6, 100*a['used_energy'], label='energy')
plt.xscale("log")
#plt.xlim(0,100)
plt.ylim(0,110)
plt.xlabel("Secondary Size (mWh)")
plt.ylabel("Reliability")
#plt.title("Camaroptera Reliability with Secondary Size")
#plt.axvline(x=64., color = 'b')
plt.axvline(x=138.e-3 / 3.6, color = 'r', linewidth=2)
plt.text(x=150e-3 / 3.6, y=10, s='Camaroptera\nDesigned Capacity', color = 'r', fontsize=12)
#plt.axvline(x= 10.125 / 3.6, color = 'b')
#plt.axvline(x= 200, color = 'g')
plt.grid(True)
#plt.legend(loc='lower right')
#plt.show()
plt.savefig('camaroptera_simulation.png', dpi=300, bbox_inches='tight')

