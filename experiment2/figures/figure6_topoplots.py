import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors

import mne

######

powtype='evoked'

path = 'file_directory'

powtype = 'evoked'

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 32}
matplotlib.rc('font', **font)

###### Load data

allDat = pd.read_csv(path + '/EEG/tf/tfr_stats_alleys_evoked.csv')

bandDict = {"animalTheta": [4, 12]}
bands = ["animalTheta"]

twin = .15, .2
vlim = -.15, .15

conds = ['right_maze', 'left_maze', 'right_nomaze', 'left_nomaze']

for band in bands:

    lim = bandDict[band]

    file1 = path + conds[0] + '_' + powtype + '-tfr.h5'
    file3 = path + conds[2] + '_' + powtype + '-tfr.h5'

    right_maze = mne.time_frequency.read_tfrs(file1)[0]
    right_nomaze = mne.time_frequency.read_tfrs(file3)[0]

    file2 = path + conds[1] + '_' + powtype + '-tfr.h5'
    file4 = path + conds[3] + '_' + powtype + '-tfr.h5'

    left_maze = mne.time_frequency.read_tfrs(file2)[0]
    left_nomaze = mne.time_frequency.read_tfrs(file4)[0]

    fig, ax = plt.subplots()
    left_maze.plot_topomap(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False, #unit='decibel',
                     cbar_fmt='%3.3f', vlim=[vlim[0], vlim[1]], colorbar=False, sensors=True,
                     cmap='RdBu_r', axes=ax, contours=4);
    fig.savefig(path + '/plots/figure6/left_maze_' + band + '.pdf', bbox_inches='tight')

    fig, ax = plt.subplots()
    right_maze.plot_topomap(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False, #unit='decibel',
                     cbar_fmt='%3.3f', vlim=[vlim[0], vlim[1]], colorbar=False, sensors=True,
                     cmap='RdBu_r', axes=ax, contours=4);
    fig.savefig(path + '/plots/figure6/right_maze_' + band + '.pdf', bbox_inches='tight')

    fig, ax = plt.subplots()
    left_nomaze.plot_topomap(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False, #unit='decibel',
                     cbar_fmt='%3.3f', vlim=[vlim[0], vlim[1]], colorbar=False, sensors=True,
                     cmap='RdBu_r', axes=ax, contours=4);
    fig.savefig(path + '/plots/figure6/left_nomaze_' + band + '.pdf', bbox_inches='tight')

    fig, ax = plt.subplots()
    right_nomaze.plot_topomap(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False, #unit='decibel',
                     cbar_fmt='%3.3f', vlim=[vlim[0], vlim[1]], colorbar=False, sensors=True,
                     cmap='RdBu_r', axes=ax, contours=4);
    fig.savefig(path + '/plots/figure6/right_nomaze_' + band + '.pdf', bbox_inches='tight')

    dat = np.zeros(shape=(256, 50, 5001, 2))
    dat[:, :, :, 0] = right_maze.data
    dat[:, :, :, 1] = left_maze.data

    maze = right_maze.copy()
    maze.data = np.mean(dat, axis=3)

    dat = np.zeros(shape=(256, 50, 5001, 2))
    dat[:, :, :, 0] = right_nomaze.data
    dat[:, :, :, 1] = left_nomaze.data

    nomaze = right_nomaze.copy()
    nomaze.data = np.mean(dat, axis=3)

    fig, ax = plt.subplots()
    maze.plot_topomap(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False, #unit='decibel',
                     cbar_fmt='%3.3f', vlim=[vlim[0], vlim[1]], colorbar=False, sensors=True,
                     cmap='RdBu_r', axes=ax, contours=4);
    ax.set_title(str(lim[0]) + '-' + str(lim[1]) + ' Hz')
    fig.savefig(path + '/plots/figure6/maze_' + band + '.pdf', bbox_inches='tight')

    fig, ax = plt.subplots()
    nomaze.plot_topomap(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False, #unit='decibel',
                     cbar_fmt='%3.3f', vlim=[vlim[0], vlim[1]], colorbar=False, sensors=True,
                     cmap='RdBu_r', axes=ax, contours=4);
    ax.set_title(str(lim[0]) + '-' + str(lim[1]) + ' Hz')
    fig.savefig(path + '/plots/figure6/nomaze_' + band + '.pdf', bbox_inches='tight')

    dat = np.zeros(shape=(256, 50, 5001, 2))
    dat[:, :, :, 0] = maze.data
    dat[:, :, :, 1] = nomaze.data

    all = maze.copy()
    all.data = np.mean(dat, axis=3)

    fig, ax = plt.subplots()
    all.plot_topomap(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False, #unit='decibel',
                     cbar_fmt='%3.3f', vlim=[vlim[0], vlim[1]], colorbar=False, sensors=True,
                     cmap='RdBu_r', axes=ax, contours=4);

#######

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)

cNorm = colors.Normalize(vmin=-.15, vmax=.15)
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='horizontal')
cb1.set_label('\u0394 power (ratio)')
cb1.set_ticks([-0.15, -0.075, 0, 0.075, 0.15])
cb1.set_ticklabels(['-0.15', '-0.075', '0', '0.075', '0.15'])
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*1.4, bb*1.15, ww*.85, hh*0.07])

fig.savefig(path + '/plots/figure6/colorbar.pdf', bbox_inches='tight')
