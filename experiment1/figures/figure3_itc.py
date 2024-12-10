import pandas as pd
from scipy.io import loadmat
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from scipy.stats import wilcoxon
from statistics import mean, stdev
from numpy import sqrt

matplotlib.use('Qt5Agg')

path = 'file_directory'

method = 'EEG'
chan = 'PO8'
subject = '8'

itc_eeg = np.real(loadmat(path + '/phase_ITC_analysis/itc_' + method + '_' + chan + '.mat')['allITC'])
subITC_left = loadmat(path + '/phase_ITC_analysis/sub' + subject + '_itc_left_' + chan + '.mat')['itc_left'].T
subITC_right = loadmat(path + '/phase_ITC_analysis/sub' + subject + '_itc_right_' + chan + '.mat')['itc_right'].T

sampleCols = ['s' + str(item) for item in np.arange(1,201)]
itc_eeg = pd.DataFrame(itc_eeg, columns=sampleCols + ['subject', 'condition', 'frequency'])
itc_eeg = itc_eeg.astype(float).drop(columns=itc_eeg.iloc[:,150:200])
itc_eeg = itc_eeg.astype({'subject': int, 'condition': int, 'frequency': int})

sampleCols = ['s' + str(item) for item in np.arange(1, subITC_left.shape[1] + 1)]
subITC_left = pd.DataFrame(subITC_left, columns=sampleCols)
subITC_left = subITC_left.astype(float)
sampleCols = ['s' + str(item) for item in np.arange(1, subITC_right.shape[1] + 1)]
subITC_right = pd.DataFrame(subITC_right, columns=sampleCols)
subITC_right = subITC_right.astype(float)

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 16}

matplotlib.rc('font', **font)

fig, ax = plt.subplots(nrows=2, ncols=1)
im = ax[0].imshow(subITC_left.iloc[0:70,500:750], cmap='RdBu_r', vmin=-12, vmax=12, aspect=1.25)
ax[0].set(xticks=[])
ax[0].axvline(x=125, linewidth=1, linestyle="--", color='black', clip_on=False)
im = ax[1].imshow(subITC_right.iloc[0:70,500:750], cmap='RdBu_r', vmin=-12, vmax=12, aspect=1.25)
ax[1].set(xticks=np.arange(0, 275, 25), xticklabels=[str(item) for item in np.arange(-500, 600, 100)],
          xlabel='time (ms)', ylabel='                              epochs')
ax[1].axvline(x=125, linewidth=1, linestyle="--", color='black', clip_on=False)
plt.subplots_adjust(hspace=-.105)

fig.savefig(path + '/plots/figure3/sub' + subject + '_' + method + 'trials_' + chan + '_phaseOrdered.pdf', bbox_inches='tight')

#######

from matplotlib import cm, colors

cNorm = colors.Normalize(vmin=-12, vmax=12)
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='vertical')
cb1.set_label('amplitude (μV)')
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*3.5, bb, ww*.07, hh])
cb1.set_ticks([-12, -8, -4, 0, 4, 8, 12])
cb1.set_ticklabels(['-12', '-8', '-4', '0', '4', '8', '12'])
#cb1.ax.set_position([ll*1.4, bb*1.15, ww*.85, hh*0.1]) # horizontal
fig.savefig(path + '/plots/figure3/eeg_cbar.pdf', bbox_inches='tight')

########

method = 'MEG'
chan = 'MRO21-2511'

itc_meg = np.real(loadmat(path + '/phase_ITC_analysis/itc_' + method + '_poc.mat')['allITC'])
subITC_left = loadmat(path + '/phase_ITC_analysis/sub' + subject + '_itc_left_' + chan + '.mat')['itc_left'].T
subITC_right = loadmat(path + '/phase_ITC_analysis/sub' + subject + '_itc_right_' + chan + '.mat')['itc_right'].T

sampleCols = ['s' + str(item) for item in np.arange(1,201)]
itc_meg = pd.DataFrame(itc_meg, columns=sampleCols + ['subject', 'condition', 'frequency'])
itc_meg = itc_meg.astype(float).drop(columns=itc_meg.iloc[:,150:200])
itc_meg = itc_meg.astype({'subject': int, 'condition': int, 'frequency': int})

sampleCols = ['s' + str(item) for item in np.arange(1, subITC_left.shape[1] + 1)]
subITC_left = pd.DataFrame(subITC_left, columns=sampleCols)
subITC_left = subITC_left.astype(float)
sampleCols = ['s' + str(item) for item in np.arange(1, subITC_right.shape[1] + 1)]
subITC_right = pd.DataFrame(subITC_right, columns=sampleCols)
subITC_right = subITC_right.astype(float)

fig, ax = plt.subplots(nrows=2, ncols=1)
im = ax[0].imshow(subITC_left.iloc[0:70,1200:1800], cmap='RdBu_r', vmin=-20e-14, vmax=20e-14, aspect=3)
ax[0].set(xticks=[])
ax[0].axvline(x=300, linewidth=1, linestyle="--", color='black', clip_on=False)
im = ax[1].imshow(subITC_right.iloc[0:70,1200:1800], cmap='RdBu_r', vmin=-20e-14, vmax=20e-14, aspect=3)
ax[1].set(xticks=np.arange(0, 660, 60), xticklabels=[str(item) for item in np.arange(-500, 600, 100)],
          xlabel='time (ms)', ylabel='                              epochs')
ax[1].axvline(x=300, linewidth=1, linestyle="--", color='black', clip_on=False)
plt.subplots_adjust(hspace=-.1)

fig.savefig(path + '/plots/figure3/sub' + subject + '_' + method + 'trials_' + chan + '_phaseOrdered.pdf', bbox_inches='tight')

#######

cNorm = colors.Normalize(vmin=-150, vmax=150)
cmap = matplotlib.cm.RdBu_r

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='vertical')
cb1.set_label('amplitude (fT)')
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_position([ll*3.5, bb, ww*.07, hh])
#cb1.ax.set_position([ll*1.4, bb*1.15, ww*.85, hh*0.1]) # horizontal
fig.savefig(path + '/plots/figure3/meg_cbar.pdf', bbox_inches='tight')

###

itc_eeg['method'] = 'eeg'
itc_meg['method'] = 'meg'
itc_eeg['peak'] = itc_eeg.iloc[:,80:100].max(axis=1)
itc_eeg['peak_latency'] = ((itc_eeg.iloc[:,80:100].idxmax(axis=1).str.replace("s","").astype(int)/200)*311.15)*(1/250)*1000-372.3 # formula: ((time/200)*311.15)*(1/250) * 1000 - 372.3
itc_meg['peak'] = itc_meg.iloc[:,80:100].max(axis=1)
itc_meg['peak_latency'] = ((itc_meg.iloc[:,80:100].idxmax(axis=1).str.replace("s","").astype(int)/200)*771.96)*(1/600)*1000-393.3 # formula: ((time/200)*771.96)*(1/600) * 1000 - 393.3

itc = pd.concat([itc_eeg, itc_meg], axis=0)
itc['id'] = itc.reset_index().index
itc = pd.wide_to_long(itc, stubnames='s', i='id', j='sample').reset_index()

itc = itc.astype({'peak': float, 'peak_latency': float})

sns.catplot(x='condition', y='peak', kind='bar', col='method', orient='v',
            data=itc[itc['frequency'].isin([4, 5, 6, 7, 8, 9, 10, 11, 12])], ci=None)

sns.catplot(x='condition', y='peak_latency', kind='bar', col='method', orient='v',
            data=itc[itc['frequency'].isin([4, 5, 6, 7, 8, 9, 10, 11, 12])], ci=None)

###########


method = 'meg'
measure = 'itc_peakLatency'


path = path + '/phase_ITC_analysis/'

itc_stats = pd.read_csv(path + 'itc_peakLat_' + method + '.txt', delimiter='\t')

x = itc_stats[itc_stats['condition'] == 1][measure]
y = itc_stats[itc_stats['condition'] == 2][measure]

w, p = wilcoxon(x=x, y=y, alternative='less', mode="approx")

# Descriptive stats

z = np.mean([x,y], axis=0)
np.mean(z)
np.std(z)

np.mean(x)
np.std(x)

np.mean(y)
np.std(y)

np.mean(x-y)
np.std(x-y)

cohens_d = (mean(x) - mean(y)) / (sqrt((stdev(x) ** 2 + stdev(y) ** 2) / 2))
