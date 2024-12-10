import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mne

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 28}

matplotlib.rc('font', **font)

path = 'file_directory'

vminEEG, vmaxEEG = -1, 1
vminMEG, vmaxMEG = -0.7, 0.7

right = mne.time_frequency.read_tfrs(path + '/tf/right_tmaze_eeg64_evoked-tfr.h5')[0]
left = mne.time_frequency.read_tfrs(path + '/tf/left_tmaze_eeg64_evoked-tfr.h5')[0]

picks = ['PO8']

fig, ax = plt.subplots()
right.copy().plot(picks, baseline=None, fmin=1, fmax=50, show=False, axes=ax,
                  vmin=vminEEG, vmax=vmaxEEG, colorbar=False, cmap='RdBu_r', tmin=-.1, tmax=.6);
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure2/spectro_right_PO8_eeg.pdf', bbox_inches='tight')

fig = right.plot_topomap(fmin=4, fmax=12, tmin=.175, tmax=.225, vlim=(vminEEG, vmaxEEG), contours=5,
                   colorbar=False, sensors=True, cmap='RdBu_r')
fig.savefig(path + '/plots/figure2/topo_right_eeg.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
left.copy().plot(picks, baseline=None, fmin=1, fmax=50, show=False, axes=ax,
                 vmin=vminEEG, vmax=vmaxEEG, colorbar=False, cmap='RdBu_r', tmin=-.1, tmax=.6);
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='frequency (Hz)',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure2/spectro_left_PO8_eeg.pdf', bbox_inches='tight')

fig = left.plot_topomap(fmin=4, fmax=12, tmin=.175, tmax=.225, vlim=(vminEEG, vmaxEEG), contours=5,
                   colorbar=False, sensors=True, cmap='RdBu_r')
fig.savefig(path + '/plots/figure2/topo_left_eeg.pdf', bbox_inches='tight')

from matplotlib import cm, colors

cNorm = colors.Normalize(vmin=vminEEG, vmax=vmaxEEG)
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='vertical')
cb1.set_label('power change (AU)')
cb1.set_ticks([-1, -0.5, 0, 0.5, 1])
cb1.set_ticklabels(['-1', '-0.5', '0', '0.5', '1'])
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*3.5, bb, ww*.07, hh])
#cb1.ax.set_position([ll*1.4, bb*1.15, ww*.85, hh*0.1]) # horizontal
fig.savefig(path + '/plots/figure2/colorbar_eeg.pdf', bbox_inches='tight')

###################

chanKey = {1: 'MRO21-2511', 2: 'MRO33-2511', 3: 'MRO22-2511', 4: 'MRO32-2511', 5: 'MRO32-2511', 6: 'MZO01-2511',
           7: 'MLO21-2511', 8: 'MRO21-2511', 9: 'MRO32-2511', 10: 'MRO33-2511', 11: 'MRO21-2511'}

right_all = np.zeros(shape=(11, 50, 3001))
left_all = np.zeros(shape=(11, 50, 3001))

for sub in np.arange(1,12):
    right = mne.time_frequency.read_tfrs(path + '/tf/sub' + str(sub) + '_right_tmaze_meg_evoked-tfr.h5')[0].pick_channels([chanKey[sub]])
    left = mne.time_frequency.read_tfrs(path + '/tf/sub' + str(sub) + '_left_tmaze_meg_evoked-tfr.h5')[0].pick_channels([chanKey[sub]])
    right_all[sub-1, :, :] = np.squeeze(right.data)
    left_all[sub-1, :, :] = np.squeeze(left.data)

right = mne.time_frequency.read_tfrs(path + '/tf/right_tmaze_meg_evoked-tfr.h5')[0]
left = mne.time_frequency.read_tfrs(path + '/tf/left_tmaze_meg_evoked-tfr.h5')[0]
right.data[108,:,:] = np.squeeze(np.mean(right_all, axis=0))
left.data[108,:,:] = np.squeeze(np.mean(left_all, axis=0))

fig, ax = plt.subplots()
right.copy().plot(['MRO33-2511'], baseline=None, fmin=1, fmax=50, show=False, axes=ax,
                  vmin=vminEEG, vmax=vmaxEEG, colorbar=False, cmap='RdBu_r', tmin=-.1, tmax=.6);
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure2/spectro_right_MRO32_meg.pdf', bbox_inches='tight')

right = mne.time_frequency.read_tfrs(path + '/tf/right_tmaze_meg_evoked-tfr.h5')[0]
fig = right.plot_topomap(fmin=4, fmax=12, tmin=.175, tmax=.225, vlim=(vminMEG, vmaxMEG), contours=5,
                   colorbar=False, sensors=True, cmap='RdBu_r')
fig.savefig(path + '/plots/figure2/topo_right_meg.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
left.copy().plot(['MRO33-2511'], baseline=None, fmin=1, fmax=50, show=False, axes=ax,
                  vmin=vminEEG, vmax=vmaxEEG, colorbar=False, cmap='RdBu_r', tmin=-.1, tmax=.6);
ax.set(xticklabels=['', '0', '200', '400', '600'], xlabel='time (ms)', ylabel='frequency (Hz)',
       yticks=np.arange(10,51,10), yticklabels=['10', '20', '30', '40', '50'])
fig.savefig(path + '/plots/figure2/spectro_left_MRO32_meg.pdf', bbox_inches='tight')

left = mne.time_frequency.read_tfrs(path + '/tf/left_tmaze_meg_evoked-tfr.h5')[0]
fig = left.plot_topomap(fmin=4, fmax=12, tmin=.175, tmax=.225, vlim=(vminMEG, vmaxMEG), contours=5,
                   colorbar=False, sensors=True, cmap='RdBu_r')
fig.savefig(path + '/plots/figure2/topo_left_meg.pdf', bbox_inches='tight')

from matplotlib import cm, colors

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)

cNorm = colors.Normalize(vmin=vminMEG, vmax=vmaxMEG)
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='horizontal')
cb1.set_label('\u0394 power (ratio)')
cb1.set_ticks([-0.7, -0.35, 0, 0.35, 0.7])
cb1.set_ticklabels(['-0.7', '-0.35', '0', '0.35', '0.7'])
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*1.4, bb*1.15, ww*.85, hh*0.07])
fig.savefig(path + '/plots/figure2/colorbar_meg.pdf', bbox_inches='tight')

##### horizontal bar

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)

cNorm = colors.Normalize(vmin=vminEEG, vmax=vmaxEEG)
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='horizontal')
cb1.set_label('\u0394 power (ratio)')
cb1.set_ticks([-1, -0.5, 0, 0.5, 1])
cb1.set_ticklabels(['-1', '-0.5', '0', '0.5', '1'])
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*1.4, bb*1.15, ww*.85, hh*0.07]) # horizontal
fig.savefig(path + '/plots/figure2/colorbar_horizontal.pdf', bbox_inches='tight')

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='horizontal')
cb1.set_label('\u0394 power (ratio)')
cb1.set_ticks([-1, -0.5, 0, 0.5, 1])
cb1.set_ticklabels(['-1', '-0.5', '0', '0.5', '1'])
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*0.6, bb*1.15, ww*1.1, hh*0.07]) # horizontal
fig.savefig(path + '/plots/figure2/colorbar_horizontal_thin.pdf', bbox_inches='tight')
