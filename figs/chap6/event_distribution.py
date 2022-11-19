import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

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

start_date = '11/6/2009 00:00:09'

results10 = np.load('sim_result_10.npy', allow_pickle=True).item()
results50 = np.load('sim_result_50.npy', allow_pickle=True).item()
results = [results10, results50]
labels = ['10 mW/cm\u00b2', '50 mW/cm\u00b2']
orders = [1, 0]

fig, ax = plt.subplots(figsize=(10.7,5))

for result, label, order in zip(results, labels, orders):
    print('utilized', result['fraction_energy_utilized'])
    event_trace = result['events_trace']
    event_ttc = result['event_ttc_raw']

    times = pd.date_range(start_date, periods=event_trace[-1]+1, freq="S")
    indexes = np.arange(0, event_trace[-1] + 1)
    events = np.zeros(len(indexes))
    events[event_trace] = 1
    print(events)
    data_dict = {'time': times, 'events':events}
    df = pd.DataFrame(data_dict)
    df = df.set_index('time')
    print(df)

    df = df.resample('H', level='time').sum()
    print(df)

    df_time_group = df.groupby(df.index.hour).mean()
    ax.bar(df_time_group.index, df_time_group.events, label=label, zorder=order)
ax.legend()
ax.xaxis.set_ticks(np.arange(0, 23, 2))
ax.set_xlim(0,23)
ax.set_ylim(0)
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Images Captured and Sent")
fig.savefig("camaroptera_performance.pdf", bbox_inches='tight')
