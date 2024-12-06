import pandas as pd
from scipy.io import loadmat
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from statannot import add_stat_annotation

matplotlib.use('Qt5Agg')

method = 'EEG'
chan = 'PO8'
measure = 2
freqs = [8, 10]

path = 'file_directory'

phaseStats = loadmat(path + '/phase_ITC_analysis/phaseResults_' + method + '_' + chan + '.mat')['allAngleData']
circMean = loadmat(path + '/phase_ITC_analysis/circularMean_' + method + '_' + chan + '.mat')['All_Subject_Left_Right_Data8Hz']

phaseStats = pd.DataFrame(phaseStats, columns=['subject', 'condition', 'frequency', 'window', 'angle'])
phaseStats = phaseStats.astype({'subject': int, 'condition': int, 'frequency': int, 'window': int, 'angle': float})

circMean = pd.DataFrame(circMean, columns=['subject', 'condition', 'frequency', 'window', 'measure', 'angle'])
circMean['condition'][circMean['condition']==1] = 'left'
circMean['condition'][circMean['condition']==2] = 'right'
circMean = circMean.astype({'subject': int, 'condition': str, 'frequency': int, 'window': int, 'measure': int, 'angle': float})
circMean['condition'] = circMean['condition'] + '_' + circMean['frequency'].astype({'frequency': str})

plotData = circMean[circMean['measure'] == measure][circMean['frequency'].isin(freqs)][circMean['window'] == 1]

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 38}

matplotlib.rc('font', **font)

# Initialize the FacetGrid object
pal1 = sns.cubehelix_palette(6, start=0, rot=-.15, light=.7)
pal2 = sns.cubehelix_palette(6, start=.4, rot=.15, light=.7)

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.[pal2[1], pal1[1]]
ax = sns.violinplot(x='condition', y='angle', alpha=.6, saturation=.6,
                    data=plotData,
                    palette=[pal2[0], pal1[0], pal2[0], pal1[0]],
                    order=['left_8', 'right_8', 'left_10', 'right_10'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y='angle', data=plotData,
              palette=[pal2[1], pal1[1]], alpha=0.8, size=16,
              order=['left_8', 'right_8', 'left_10', 'right_10'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y='angle', saturation=.4, data=plotData,
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=16, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2),
            )

ax.set(xlabel='', xticks=[0, 1, 2, 3], xticklabels=['8 Hz', '8 Hz', '10 Hz', '10 Hz'],
       ylabel='resultant vector length',
       ylim=[0, 1], title='pre-feedback (EEG) \n\n')
add_stat_annotation(ax, data=plotData.groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y='angle', use_fixed_offset=False, order=['left_8', 'right_8', 'left_10', 'right_10'],
                    box_pairs=[('right_8', 'left_8'), ('right_10', 'left_10')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=False, right=True, top=True, offset=5, trim=True)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure4/RVL_pre_eeg.pdf', bbox_inches='tight')

#####

plotData = circMean[circMean['measure'] == measure][circMean['frequency'].isin(freqs)][circMean['window'] == 2]

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.
ax = sns.violinplot(x='condition', y='angle', alpha=.6, saturation=.6,
                    data=plotData,
                    palette=[pal2[0], pal1[0], pal2[0], pal1[0]],
                    order=['left_8', 'right_8', 'left_10', 'right_10'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y='angle', data=plotData,
              palette=[pal2[1], pal1[1]], alpha=0.8, size=16,
              order=['left_8', 'right_8', 'left_10', 'right_10'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y='angle', saturation=.4, data=plotData,
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=16, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2)
            )

ax.set(xlabel='', xticks=[0, 1, 2, 3], xticklabels=['8 Hz', '8 Hz', '10 Hz', '10 Hz'],
       ylabel='',
       ylim=[0, 1], title='post-feedback (EEG) \n\n')
add_stat_annotation(ax, data=plotData.groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y='angle', use_fixed_offset=False, order=['left_8', 'right_8', 'left_10', 'right_10'],
                    box_pairs=[('right_8', 'left_8'), ('right_10', 'left_10')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=False, right=True, top=True, offset=5, trim=True)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure4/RVL_post_eeg.pdf', bbox_inches='tight')

#####

method = 'MEG'
chan = 'poc'

phaseStats = loadmat(path + '/phase_ITC_analysis/phaseResults_' + method + '_' + chan + '.mat')['allAngleData']
circMean = loadmat(path + '/phase_ITC_analysis/circularMean_' + method + '_' + chan + '.mat')['All_Subject_Left_Right_Data8Hz']

phaseStats = pd.DataFrame(phaseStats, columns=['subject', 'condition', 'frequency', 'window', 'angle'])
phaseStats = phaseStats.astype({'subject': int, 'condition': int, 'frequency': int, 'window': int, 'angle': float})

circMean = pd.DataFrame(circMean, columns=['subject', 'condition', 'frequency', 'window', 'measure', 'angle'])
circMean['condition'][circMean['condition']==1] = 'left'
circMean['condition'][circMean['condition']==2] = 'right'
circMean = circMean.astype({'subject': int, 'condition': str, 'frequency': int, 'window': int, 'measure': int, 'angle': float})
circMean['condition'] = circMean['condition'] + '_' + circMean['frequency'].astype({'frequency': str})

plotData = circMean[circMean['measure'] == measure][circMean['frequency'].isin(freqs)][circMean['window'] == 1]

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.
ax = sns.violinplot(x='condition', y='angle', alpha=.6, saturation=.6,
                    data=plotData,
                    palette=[pal2[0], pal1[0], pal2[0], pal1[0]],
                    order=['left_8', 'right_8', 'left_10', 'right_10'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y='angle', data=plotData,
              palette=[pal2[1], pal1[1]], alpha=0.8, size=16,
              order=['left_8', 'right_8', 'left_10', 'right_10'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y='angle', saturation=.4, data=plotData,
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=16, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2)
            )

ax.set(xlabel='', xticks=[0, 1, 2, 3], xticklabels=['8 Hz', '8 Hz', '10 Hz', '10 Hz'],
       ylabel='',
       ylim=[0, 1], title='pre-feedback (MEG) \n\n')
add_stat_annotation(ax, data=plotData.groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y='angle', use_fixed_offset=False, order=['left_8', 'right_8', 'left_10', 'right_10'],
                    box_pairs=[('right_8', 'left_8'), ('right_10', 'left_10')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=False, right=True, top=True, offset=10, trim=True)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure4/RVL_pre_meg.pdf', bbox_inches='tight')

#####

plotData = circMean[circMean['measure'] == measure][circMean['frequency'].isin(freqs)][circMean['window'] == 2]

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.
ax = sns.violinplot(x='condition', y='angle', alpha=.6, saturation=.6,
                    data=plotData,
                    palette=[pal2[0], pal1[0], pal2[0], pal1[0]],
                    order=['left_8', 'right_8', 'left_10', 'right_10'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y='angle', data=plotData,
              palette=[pal2[1], pal1[1]], alpha=0.8, size=16,
              order=['left_8', 'right_8', 'left_10', 'right_10'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y='angle', saturation=.4, data=plotData,
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=16, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2)
            )

ax.set(xlabel='', xticks=[0, 1, 2, 3], xticklabels=['8 Hz', '8 Hz', '10 Hz', '10 Hz'],
       ylabel='',
       ylim=[0, 1], title='post-feedback (MEG) \n\n')
add_stat_annotation(ax, data=plotData.groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y='angle', use_fixed_offset=False, order=['left_8', 'right_8', 'left_10', 'right_10'],
                    box_pairs=[('right_8', 'left_8'), ('right_10', 'left_10')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=False, right=True, top=True, offset=5, trim=True)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure4/RVL_post_meg.pdf', bbox_inches='tight')
