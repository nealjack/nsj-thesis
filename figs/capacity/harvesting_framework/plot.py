#!/usr/bin/env python3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = "14"
plt.rcParams["xtick.major.width"] = "0.8"
plt.rcParams["xtick.major.size"]  = "6"
plt.rcParams["xtick.minor.width"] = "0.8"
plt.rcParams["xtick.minor.size"] = "4"
plt.rcParams["ytick.major.width"] = "0.8"
plt.rcParams["ytick.major.size"] = "6"
plt.rcParams["ytick.minor.width"] = "0.8"
plt.rcParams["ytick.minor.size"] = "4"
plt.rcParams["grid.linewidth"] = "1"

# Tableau Color Blind 10
t10_blind = [(0.0, 0.41960, 0.64313), (1.0, 0.50196, 0.05490), (0.67058, 0.67058, 0.670588),
            (0.34901, 0.34901, 0.34901), (0.37254, 0.619607, 0.819607), (0.784313, 0.32156, 0.0),
            (0.53725, 0.53725, 0.537254), (0.63921, 0.78431, 0.925490), (1.0, 0.73725, 0.474509),
            (0.811764, 0.811764, 0.8117647)]

#Tableau 10 (which is neither as greyscale or colorblind safe)
t10 = plt.cm.tab10.colors

#Here are the default color index for 10 - they apply to some of the colorblind version
blue = 0
orange = 1
green = 2
red = 3
purple = 4
brown = 5
pink = 6
grey = 7
yellow = 8
cyan = 9

#test plot 1
plt.figure(figsize=(10.7,5))
plt.ylabel("Harvester\nInput Power",position=(-0.2,0.5),labelpad=10,fontweight=550,fontsize=14)
plt.xlabel("Energy Storage Capacity",labelpad=50,fontsize=14)
plt.axis([0,1,0,1])
ax = plt.subplot(111)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tick_params(axis='x',which='both',bottom=False,labelbottom=False)
plt.tick_params(axis='y',which='both',left=False,labelleft=False)
plt.tight_layout(rect=(0.03,0,1,1))

#draw the lines
#max power
plt.plot([0, 1],[0.9,0.9],color='black',linewidth=0.5)
plt.fill([0,0,1,1],[0.9,1,1,0.9],color=t10[green],alpha=0.5,linewidth=0)
plt.text(-0.11,0.84,'max sensor\npower',multialignment='right', fontsize=12)
art = plt.plot([-0.007, 0.007],[0.9,0.9],color='black',linewidth=1)
art[0].set_clip_on(False)
plt.text(0.455,0.94,'Always on',multialignment='center')

#infeasible
plt.plot([0.05, 0.05],[0.9,0.1],color='black',linewidth=0.5)
plt.plot([0.05, 0.05],[0.1,0],color='black',linewidth=0.5,linestyle='--')
plt.plot([0, 0.05],[0.1,0.1],color='black',linewidth=0.5,linestyle='--')
plt.plot([0.05, 1],[0.1,0.1],color='black',linewidth=0.5)
plt.fill([0,0,0.05,0.05],[0.1,0.9,0.9,0.1],color=t10[red],alpha=0.5,linewidth=0)
plt.fill([0,0,1,1],[0,0.1,0.1,0],color=t10[red],alpha=0.5,linewidth=0)
plt.text(-0.08,0.09,'leakage',multialignment='right',fontsize=12)
art = plt.plot([-0.007, 0.007],[0.1,0.1],color='black',linewidth=1)
art[0].set_clip_on(False)
plt.text(0.009,-0.13,'energy of\nlargest atomic\noperation',multialignment='center',fontsize=10)
art = plt.plot([0.05, 0.05],[-0.007,0.007],color='black',linewidth=1)
art[0].set_clip_on(False)
plt.text(0.20,0.03,'Infeasible',multialignment='center')
#plt.text(0.005,0.32,'Infeasible',multialignment='center',rotation=90)

#state retention
plt.plot([0.5, 0.5],[0.9,0.1],color='black',linewidth=0.5,zorder=2000)
plt.plot([0.5, 0.5],[0.1,0],color='black',linewidth=0.5,linestyle='--')
plt.fill([0.05,0.05,0.5,0.5],[0.1,0.9,0.9,0.1],color=t10[blue],alpha=0.5,linewidth=0)
plt.text(0.455,-0.13,'energy of\nsum of atomic\noperations',multialignment='center',fontsize=10)
art = plt.plot([0.5, 0.5],[-0.007,0.007],color='black',linewidth=1)
art[0].set_clip_on(False)
plt.text(0.18,0.45,'State retention\nrequired',multialignment='center',zorder=2000)

#hysterysis management
plt.plot([0.0, 1],[0.2,0.2],color='black',linewidth=0.5, linestyle='--')
plt.fill([0.05,0.05,1,1],[0.1,0.2,0.2,0.1],color=t10[purple],alpha=0.5,linewidth=0)
plt.text(-0.105,0.185,'deep sleep',multialignment='right',fontsize=12)
art = plt.plot([-0.007, 0.007],[0.2,0.2],color='black',linewidth=1)
art[0].set_clip_on(False)
t = plt.text(0.1,0.13,'Hysteresis management helpful',multialignment='center', zorder=2000)
#t.set_bbox(dict(facecolor='#9f9f9f', alpha=0.5, edgecolor=None,linewidth=0,pad=0.1))
t= plt.text(0.1,0.23,'Hysteresis management less helpful',multialignment='center',zorder=2000)
#t.set_bbox(dict(facecolor='#9f9f9f', alpha=0.5, edgecolor=None,linewidth=0,pad=0.1))
#plt.text(0.33,0.6,'Checkpointing not required\nHysteresis management marginally helpful',multialignment='center',zorder=2000)
plt.text(0.68,0.45,'State retention\nnot required',multialignment='center',zorder=2000)
art = plt.plot([-0.007, 0.007],[0.1,0.1],color='black',linewidth=1)
art[0].set_clip_on(False)

plt.plot([0.8, 0.8],[0.2,0],color='black',linewidth=0.5,linestyle='--')
art = plt.plot([0.8, 0.8],[-0.007,0.007],color='black',linewidth=1)
art[0].set_clip_on(False)
plt.text(0.775,-0.13,'sufficient\ncapacity\nto sleep',multialignment='center',fontsize=10)

#hysterysis management 2
path = Path([[0.05,0.2],[0.05,0.3],[.5,0.3],[0.8,0.2]])
patch = PathPatch(path, facecolor='none',edgecolor='none')
ax.add_patch(patch)
Z = np.zeros((300,1000))
for i in range(0,300):
    Z[i,:] = i/300.0
Z = np.flip(Z, 0)
colors = np.array([t10[purple],t10[purple]])
cm = LinearSegmentedColormap.from_list('cm',colors)
my_cmap = cm(np.arange(cm.N))
my_cmap[:,-1] = np.linspace(0, 0.5, cm.N)
my_cmap = ListedColormap(my_cmap)
im = plt.imshow(Z, interpolation='bilinear', origin='lower', cmap=my_cmap, clip_path=patch, clip_on=True, aspect='auto',extent=[0.026,0.8,0.2,0.3],zorder=1000)
#im.set_clip_path(patch)

#plt.fill([0.0476,0.0266,1,1],[0.1,0.4,0.4,0.1],color=t10[purple],alpha=0.5,linewidth=0)
plt.savefig('framework.pdf',bbox_inches="tight")
