import pandas as pd
from scipy.io import loadmat
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from statannot import add_stat_annotation

matplotlib.use('Qt5Agg')

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 38}

matplotlib.rc('font', **font)

path = 'file_directory'

itc_eeg = pd.read_csv(path + '/phase_ITC_analysis/itc_peakLat_eeg.txt', delimiter='\t')
itc_meg = pd.read_csv(path + '/phase_ITC_analysis/itc_peakLat_meg.txt', delimiter='\t')

plotData = pd.concat([itc_eeg, itc_meg]).reset_index(drop=True)
plotData['modality'] = 'EEG'
plotData['modality'].iloc[22:44] = 'MEG'

# Initialize the FacetGrid object
pal1 = sns.cubehelix_palette(6, start=0, rot=-.15, light=.7)
pal2 = sns.cubehelix_palette(6, start=.4, rot=.15, light=.7)

measure = 'itc_peak'
modality = 'EEG'

fig = plt.figure(figsize=(9, 9))

ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=plotData[plotData['modality'] == modality],
                    palette=[pal2[0], pal1[0]], order=[1, 2],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width / 2, height,
                                     transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure,
              data=plotData[plotData['modality'] == modality],
              palette=[pal2[1], pal1[1]], alpha=0.8, size=16, order=[1, 2])

# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4,
            data=plotData[plotData['modality'] == modality], fliersize=12,
            width=0.12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=18, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2)
            )

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak ITC',
       ylim=[0.2, 1], yticks=[0.2, 0.4, 0.6, 0.8, 1])

add_stat_annotation(ax, data=plotData[plotData['modality'] == modality], perform_stat_test=False,
                    x="condition", y=measure, use_fixed_offset=False, order=[1, 2],
                    box_pairs=[(1, 2)], pvalues=[0.031],
                    text_format='star', loc='outside', verbose=2, linewidth=3)

sns.despine(left=False, right=True, top=True, offset=5, trim=True)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure3/rainplot_eeg_itc_peak.pdf', bbox_inches='tight')

measure = 'itc_peakLatency'

fig = plt.figure(figsize=(9, 9))

ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=plotData[plotData['modality'] == modality],
                    palette=[pal2[0], pal1[0]], order=[1, 2],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width / 2, height,
                                     transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure,
              data=plotData[plotData['modality'] == modality],
              palette=[pal2[1], pal1[1]], alpha=0.8, size=14, order=[1, 2])

# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4,
            data=plotData[plotData['modality'] == modality], fliersize=12,
            width=0.12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=18, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2)
            )

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak ITC latency (ms)',
       ylim=[100, 300], yticks=[100, 150, 200, 250, 300])

add_stat_annotation(ax, data=plotData[plotData['modality'] == modality], perform_stat_test=False,
                    x="condition", y=measure, use_fixed_offset=False, order=[1, 2],
                    box_pairs=[(1, 2)], pvalues=[0.014],
                    text_format='star', loc='outside', verbose=2, linewidth=3)

sns.despine(left=True, right=False, top=True, offset=5, trim=True)
ax.yaxis.set_ticks_position("right")
ax.yaxis.set_label_position("right")
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure3/rainplot_eeg_itc_peakLatency.pdf', bbox_inches='tight')

######

measure = 'itc_peak'
modality = 'MEG'

fig = plt.figure(figsize=(9, 9))

ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=plotData[plotData['modality'] == modality],
                    palette=[pal2[0], pal1[0]], order=[1, 2],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width / 2, height,
                                     transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure,
              data=plotData[plotData['modality'] == modality],
              palette=[pal2[1], pal1[1]], alpha=0.8, size=14, order=[1, 2])

# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4,
            data=plotData[plotData['modality'] == modality], fliersize=12,
            width=0.12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=18, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2)
            )

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak ITC',
       ylim=[0.2, 1], yticks=[0.2, 0.4, 0.6, 0.8, 1])

add_stat_annotation(ax, data=plotData[plotData['modality'] == modality], perform_stat_test=False,
                    x="condition", y=measure, use_fixed_offset=False, order=[1, 2],
                    box_pairs=[(1, 2)], pvalues=[0.016],
                    text_format='star', loc='outside', verbose=2, linewidth=3)

sns.despine(left=False, right=True, top=True, offset=5, trim=True)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure3/rainplot_meg_itc_peak.pdf', bbox_inches='tight')

measure = 'itc_peakLatency'

fig = plt.figure(figsize=(9, 9))

ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=plotData[plotData['modality'] == modality],
                    palette=[pal2[0], pal1[0]], order=[1, 2],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width / 2, height,
                                     transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure,
              data=plotData[plotData['modality'] == modality],
              palette=[pal2[1], pal1[1]], alpha=0.8, size=14, order=[1, 2])

# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4,
            data=plotData[plotData['modality'] == modality], fliersize=12,
            width=0.12, boxprops={'zorder': 2, 'linewidth': 2}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=18, zorder=3, markeredgewidth=1.5),
            whiskerprops=dict(linewidth=2), capprops=dict(linewidth=2), medianprops=dict(linewidth=2)
            )

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak ITC latency (ms)',
       ylim=[100, 300], yticks=[100, 150, 200, 250, 300])

add_stat_annotation(ax, data=plotData[plotData['modality'] == modality], perform_stat_test=False,
                    x="condition", y=measure, use_fixed_offset=False, order=[1, 2],
                    box_pairs=[(1, 2)], pvalues=[0.52],
                    text_format='star', loc='outside', verbose=2, linewidth=3)

sns.despine(left=True, right=False, top=True, offset=5, trim=True)
ax.yaxis.set_ticks_position("right")
ax.yaxis.set_label_position("right")
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure3/rainplot_meg_itc_peakLatency.pdf', bbox_inches='tight')
