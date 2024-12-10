import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from statannot import add_stat_annotation

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 40}

matplotlib.rc('font', **font)

path = 'file_directory'

allDat = pd.read_csv(path + '/EEG/tf/dataAlleysEvoked_long_100350_max.csv')
allDat['condition'] = allDat['alley'] + '_' + allDat['block']
allDat['peakLatency'] = allDat['peakLatency'] + 100
subs = [3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30]

peakLim = [-.15, 1]
peakTicks = np.arange(0, 0.8, .25)
peakTickLabels = ['0', '0.25', '0.5', '0.75']
latLim = [75, 400]
latTicks = np.arange(100, 351, 50)
latTickLabels = ['100', '150', '200', '250', '300', '350']

pal1 = sns.cubehelix_palette(6, start=0, rot=-.15, light=.7)
pal2 = sns.cubehelix_palette(6, start=.4, rot=.15, light=.7)
pal3 = sns.cubehelix_palette(6, start=.1, rot=-.1, light=.7)
pal4 = sns.cubehelix_palette(6, start=.7, rot=.1, light=.7)

powtype = 'evoked'
measure = 'peakLatency'
PO8 = ['E160']

plotData = allDat[(allDat['block'] == 'maze') & (allDat['channel'].isin(PO8)) & (allDat['frequency'] == 'animalTheta')]

fig = plt.figure(figsize=(9, 8))
ax = sns.violinplot(x='alley', y=measure, alpha=.2,
                    data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    palette=[pal2[0], pal1[0]], order=['left', 'right'],
                    cut=0, inner=None, width=.65, linewidth=1.5)

for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))
                       
num_items = len(ax.collections)
sns.stripplot(x='alley', y=measure, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
              palette=[pal2[3], pal1[3]], alpha=0.8, size=14, order=['left', 'right'])

for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

plt.boxplot(plotData.groupby(['subject', 'alley'], as_index=False).mean().pivot(index='subject', columns='alley', values=measure),
            showfliers=False, showmeans=True, patch_artist=False,
            meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                           markersize=20, zorder=3, markeredgewidth=2),
            boxprops=dict(linewidth=6, zorder=3, color='dimgrey', alpha=0.9),
            whiskerprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            capprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            medianprops=dict(color='dimgrey', linewidth=6, alpha=0.9),
            positions=[0.15, 1.15])

ax.set(xlabel='', xticks=[0, 1], xticklabels=['leftward', 'rightward'], ylabel='peak latency (ms) ',
       ylim=latLim, yticks=latTicks, yticklabels=latTickLabels)
add_stat_annotation(ax, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    x="alley", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='t-test_paired',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=True, right=False, top=True, offset=10, trim=True)
ax.yaxis.set_ticks_position("right")
ax.yaxis.set_label_position("right")
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure6/rainplot_maze_latency_rightHemi.pdf', bbox_inches='tight')

##################

measure = 'peak'

fig = plt.figure(figsize=(9, 8))

ax = sns.violinplot(x='alley', y=measure, alpha=.2,
                    data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    palette=[pal2[0], pal1[0]], order=['left', 'right'],
                    cut=0, inner=None, width=.65, linewidth=1.5)

for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

num_items = len(ax.collections)
sns.stripplot(x='alley', y=measure, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
              palette=[pal2[3], pal1[3]], alpha=0.8, size=14, order=['left', 'right'])

for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

plt.boxplot(plotData.groupby(['subject', 'alley'], as_index=False).mean().pivot(index='subject', columns='alley', values=measure),
            showfliers=False, showmeans=True, patch_artist=False,
            meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                           markersize=20, zorder=3, markeredgewidth=2),
            boxprops=dict(linewidth=6, zorder=3, color='dimgrey', alpha=0.9),
            whiskerprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            capprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            medianprops=dict(color='dimgrey', linewidth=6, alpha=0.9),
            positions=[0.15, 1.15])

ax.set(xlabel='', xticks=[0, 1], xticklabels=['leftward', 'rightward'], ylabel='peak \u0394 power (ratio)',
       ylim=peakLim, yticks=peakTicks, yticklabels=peakTickLabels)
add_stat_annotation(ax, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    x="alley", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='t-test_paired',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)
sns.despine(right=True, top=True, offset=10, trim=True)

fig.savefig(path + '/plots/figure6/rainplot_maze_peaks_rightHemi.pdf', bbox_inches='tight')

##################

measure = 'peakLatency'
plotData = allDat[(allDat['block'] == 'nomaze') & (allDat['channel'].isin(PO8)) & (allDat['frequency'] == 'animalTheta')]

fig = plt.figure(figsize=(9, 8))

ax = sns.violinplot(x='alley', y=measure, alpha=.2,
                    data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    palette=[pal4[0], pal3[0]], order=['left', 'right'],
                    cut=0, inner=None, width=.65, linewidth=1.5)

for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

num_items = len(ax.collections)
sns.stripplot(x='alley', y=measure, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
              palette=[pal4[3], pal3[3]], alpha=0.8, size=14, order=['left', 'right'])

for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

plt.boxplot(plotData.groupby(['subject', 'alley'], as_index=False).mean().pivot(index='subject', columns='alley', values=measure),
            showfliers=False, showmeans=True, patch_artist=False,
            meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                           markersize=20, zorder=3, markeredgewidth=2),
            boxprops=dict(linewidth=6, zorder=3, color='dimgrey', alpha=0.9),
            whiskerprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            capprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            medianprops=dict(color='dimgrey', linewidth=6, alpha=0.9),
            positions=[0.15, 1.15])

ax.set(xlabel='', xticks=[0, 1], xticklabels=['leftward', 'rightward'], ylabel='peak latency (ms) ',
       ylim=latLim, yticks=latTicks, yticklabels=latTickLabels)
add_stat_annotation(ax, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    x="alley", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='t-test_paired',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=True, right=False, top=True, offset=10, trim=True)
ax.yaxis.set_ticks_position("right")
ax.yaxis.set_label_position("right")
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure6/rainplot_nomaze_latency_rightHemi.pdf', bbox_inches='tight')

##################

measure = 'peak'

fig = plt.figure(figsize=(9, 8))

ax = sns.violinplot(x='alley', y=measure, alpha=.2,
                    data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    palette=[pal4[0], pal3[0]], order=['left', 'right'],
                    cut=0, inner=None, width=.65, linewidth=1.5)

for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

num_items = len(ax.collections)
sns.stripplot(x='alley', y=measure, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
              palette=[pal4[3], pal3[3]], alpha=0.8, size=14, order=['left', 'right'])

for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

plt.boxplot(plotData.groupby(['subject', 'alley'], as_index=False).mean().pivot(index='subject', columns='alley', values=measure),
            showfliers=False, showmeans=True, patch_artist=False,
            meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                           markersize=20, zorder=3, markeredgewidth=2),
            boxprops=dict(linewidth=6, zorder=3, color='dimgrey', alpha=0.9),
            whiskerprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            capprops=dict(linewidth=6, color='dimgrey', alpha=0.9),
            medianprops=dict(color='dimgrey', linewidth=6, alpha=0.9),
            positions=[0.15, 1.15])

ax.set(xlabel='', xticks=[0, 1], xticklabels=['leftward', 'rightward'], ylabel='peak \u0394 power (ratio)',
       ylim=peakLim, yticks=peakTicks, yticklabels=peakTickLabels)
add_stat_annotation(ax, data=plotData.groupby(['subject', 'alley'], as_index=False).mean(),
                    x="alley", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='t-test_paired',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)
sns.despine(right=True, top=True, offset=10, trim=True)

fig.savefig(path + '/plots/figure6/rainplot_nomaze_peaks_rightHemi.pdf', bbox_inches='tight')
