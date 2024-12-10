import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors

import mne

######

powtype = 'evoked'

path = 'file_directory'

powtype = 'evoked'

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 28}
matplotlib.rc('font', **font)

################# Load data

chan = 'E160'

twin = -.1, .6
vlim = -.15, .15
lim = [1, 50]

conds = ['right_maze', 'left_maze', 'right_nomaze', 'left_nomaze']
subs = [3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30]

right_maze_all = np.zeros(shape=(len(subs), 50, 5001))
left_maze_all = np.zeros(shape=(len(subs), 50, 5001))
right_nomaze_all = np.zeros(shape=(len(subs), 50, 5001))
left_nomaze_all = np.zeros(shape=(len(subs), 50, 5001))

s = 0

for sub in subs:
    right_maze = mne.time_frequency.read_tfrs(path + '/EEG/tf/sub' + str(sub) + '_right_maze_evoked-tfr.h5')[0].pick_channels([chan])
    left_maze = mne.time_frequency.read_tfrs(path + '/EEG/tf/sub' + str(sub) + '_left_maze_evoked-tfr.h5')[0].pick_channels([chan])
    right_maze_all[s, :, :] = np.squeeze(right_maze.data)
    left_maze_all[s, :, :] = np.squeeze(left_maze.data)

    right_nomaze = mne.time_frequency.read_tfrs(path + '/EEG/tf/sub' + str(sub) + '_right_nomaze_evoked-tfr.h5')[0].pick_channels([chan])
    left_nomaze = mne.time_frequency.read_tfrs(path + '/EEG/tf/sub' + str(sub) + '_left_nomaze_evoked-tfr.h5')[0].pick_channels([chan])
    right_nomaze_all[s, :, :] = np.squeeze(right_nomaze.data)
    left_nomaze_all[s, :, :] = np.squeeze(left_nomaze.data)

    s = s + 1

right_maze = mne.time_frequency.read_tfrs(path + 'right_maze_evoked-tfr.h5')[0]
left_maze = mne.time_frequency.read_tfrs(path + 'left_maze_evoked-tfr.h5')[0]
right_maze.data[0,:,:] = np.squeeze(np.mean(right_maze_all, axis=0))
left_maze.data[0,:,:] = np.squeeze(np.mean(left_maze_all, axis=0))
right_nomaze = mne.time_frequency.read_tfrs(path + 'right_nomaze_evoked-tfr.h5')[0]
left_nomaze = mne.time_frequency.read_tfrs(path + 'left_nomaze_evoked-tfr.h5')[0]
right_nomaze.data[0,:,:] = np.squeeze(np.mean(right_nomaze_all, axis=0))
left_nomaze.data[0,:,:] = np.squeeze(np.mean(left_nomaze_all, axis=0))

maze = right_maze.copy()
nomaze = right_maze.copy()
allCond = right_maze.copy()
maze.data[0,:,:] = np.squeeze(np.mean(np.concatenate([right_maze_all, left_maze_all], axis=0), axis=0))
nomaze.data[0,:,:] = np.squeeze(np.mean(np.concatenate([right_nomaze_all, left_nomaze_all], axis=0), axis=0))
allCond.data[0,:,:] = np.squeeze(np.mean(np.concatenate([right_maze_all, left_maze_all,
                                                         right_nomaze_all, left_nomaze_all], axis=0), axis=0))

fig, ax = plt.subplots()
maze.plot(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False,
                  title='', vmin=vlim[0], vmax=vlim[1], colorbar=False, picks=['E1'],
                  cmap='RdBu_r', axes=ax)
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure6/maze_spectrogram.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
nomaze.plot(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False,
                  title='', vmin=vlim[0], vmax=vlim[1], colorbar=False, picks=['E1'],
                  cmap='RdBu_r', axes=ax)
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure6/nomaze_spectrogram.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
allCond.plot(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False,
                  title='', vmin=vlim[0], vmax=vlim[1], colorbar=False, picks=['E1'],
                  cmap='RdBu_r', axes=ax)
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure6/all_spectrogram.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
right_maze.plot(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False,
                  title='', vmin=vlim[0], vmax=vlim[1], colorbar=False, picks=['E1'],
                  cmap='RdBu_r', axes=ax)
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure6/right_maze_spectrogram.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
left_maze.plot(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False,
                  title='', vmin=vlim[0], vmax=vlim[1], colorbar=False, picks=['E1'],
                  cmap='RdBu_r', axes=ax)
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='frequency (Hz)',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure6/left_maze_spectrogram.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
right_nomaze.plot(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False,
                  title='', vmin=vlim[0], vmax=vlim[1], colorbar=False, picks=['E1'],
                  cmap='RdBu_r', axes=ax)
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure6/right_nomaze_spectrogram.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
left_nomaze.plot(fmin=lim[0], fmax=lim[1], tmin=twin[0], tmax=twin[1], show=False,
                  title='', vmin=vlim[0], vmax=vlim[1], colorbar=False, picks=['E1'],
                  cmap='RdBu_r', axes=ax)
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='frequency (Hz)',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure6/left_nomaze_spectrogram.pdf', bbox_inches='tight')

########

cNorm = colors.Normalize(vmin=vlim[0], vmax=vlim[1])
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='vertical')
cb1.set_label('decibel (dB)')
cb1.set_ticks([-0.2, -0.1, 0, 0.1, 0.2])
cb1.set_ticklabels(['-0.2', '-0.1', '0', '0.1', '0.2'])
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*3.5, bb, ww*.07, hh])
fig.savefig(path + '/plots/figure6/color_scale.pdf', bbox_inches='tight')

########

fig, ax = plt.subplots()
right = mne.read_evokeds(path[:-3] + '\\evoked\\right-ave.fif')[0].pick_channels([chan])
right.plot_sensors(axes=ax, show_names=False)

fig.savefig(path + '/plots/figure6/2d_topo_right.pdf', bbox_inches='tight')
