from matplotlib import pyplot as plt
import pandas as pd
from glob import glob

fnames = glob("discharge_curve*.csv")
print(fnames)

for fname in fnames:
    data = pd.read_csv(fname, index_col=0)
    plt.plot(data.index, data['Voltage'])
    print(fname)
    t_delta = data.index[-1] - data.index[0]
    print(t_delta/60)
    plt.show()
