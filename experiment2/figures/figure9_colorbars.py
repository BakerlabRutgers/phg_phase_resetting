from nilearn import plotting

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm, colors

matplotlib.use('Qt5Agg')
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 28}

matplotlib.rc('font', **font)

path = 'file_directory'

cNorm = colors.Normalize(vmin=-.2, vmax=.2)
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='horizontal')
cb1.set_label('beta weights')
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_xticks([-0.2, -0.1, 0, 0.1, 0.2])
cb1.ax.set_xticklabels(['-0.2', '-0.1', '0', '0.1', '0.2'])
cb1.ax.set_position([ll*1.4, bb*1.15, ww*1.05, hh*0.06]) # horizontal
fig.savefig(path + '/plots/figure9/colorbar_glassBrain.pdf', bbox_inches='tight')

cNorm = colors.Normalize(vmin=-.15, vmax=.15)

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='horizontal')
cb1.set_label('beta weights')
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_xticks([-0.15, 0, 0.15])
cb1.ax.set_xticklabels(['-0.15', '0', '0.15'])
cb1.ax.set_position([ll*1.4, bb*1.15, ww*1.05, hh*0.06]) # horizontal
fig.savefig(path + '/plots/figure9/colorbar_phg.pdf', bbox_inches='tight')
