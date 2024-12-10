import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from statannot import add_stat_annotation

matplotlib.use('Qt5Agg')

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 42}

matplotlib.rc('font', **font)

path = 'file_directory'

allDat = pd.read_csv(path + '/tf/dataAlleysEvoked_eegmeg_peaksLat.csv')
allDat = allDat[allDat['channel'] == 'PO8']

# Initialize the FacetGrid object
pal1 = sns.cubehelix_palette(6, start=0, rot=-.15, light=.7)
pal2 = sns.cubehelix_palette(6, start=.4, rot=.15, light=.7)

powtype = 'evoked'
measure = 'latency'

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.
ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    palette=[pal2[0], pal1[0]],
                    order=['left', 'right'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure, data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
              palette=[pal2[1], pal1[1]], alpha=0.8, size=14,
              order=['left', 'right'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4, data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 3}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=22, zorder=3, markeredgewidth=2),
            whiskerprops=dict(linewidth=3), capprops=dict(linewidth=3), medianprops=dict(linewidth=3),
            )

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak latency (ms) ',
       ylim=[100, 300])
add_stat_annotation(ax, data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=True, right=False, top=True, offset=5, trim=True)
ax.yaxis.set_ticks_position("right")
ax.yaxis.set_label_position("right")
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path = '/plots/figure2/rainplot_eeg_latency.pdf', bbox_inches='tight')

measure = 'peak'

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.
ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    palette=[pal2[0], pal1[0]],
                    order=['left', 'right'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure, data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
              palette=[pal2[1], pal1[1]], alpha=0.8, size=14,
              order=['left', 'right'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4, data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 3}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=22, zorder=3, markeredgewidth=2),
            whiskerprops=dict(linewidth=3), capprops=dict(linewidth=3), medianprops=dict(linewidth=3),
            )

sns.despine(right=True, top=True, offset=5, trim=True)

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak \u0394 power (ratio)',
       ylim=[0, 5])
add_stat_annotation(ax, data=allDat[allDat['modality'] == 'EEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure2/rainplot_eeg_power.pdf', bbox_inches='tight')

##################

allDat = pd.read_csv(path + 'dataAlleysEvoked_eegmeg_peaksLat.csv')

measure = 'latency'

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.
ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    palette=[pal2[0], pal1[0]],
                    order=['left', 'right'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure, data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
              palette=[pal2[1], pal1[1]], alpha=0.8, size=14,
              order=['left', 'right'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4, data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 3}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=22, zorder=3, markeredgewidth=2),
            whiskerprops=dict(linewidth=3), capprops=dict(linewidth=3), medianprops=dict(linewidth=3),
            )

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak latency (ms) ',
       ylim=[100, 300])
add_stat_annotation(ax, data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)

sns.despine(left=True, right=False, top=True, offset=5, trim=True)
ax.yaxis.set_ticks_position("right")
ax.yaxis.set_label_position("right")
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure2/rainplot_meg_latency.pdf', bbox_inches='tight')

measure = 'peak'

fig = plt.figure(figsize=(9, 9))
# Create violin plots without mini-boxplots inside.
ax = sns.violinplot(x='condition', y=measure, alpha=.6, saturation=.6,
                    data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    palette=[pal2[0], pal1[0]],
                    order=['left', 'right'],
                    cut=0, inner=None, width=.85, linewidth=0)

# Clip the lower half of each violin.
for item in ax.collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height,
                       transform=ax.transData))

# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(ax.collections)
sns.stripplot(x='condition', y=measure, data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
              palette=[pal2[1], pal1[1]], alpha=0.8, size=14,
              order=['left', 'right'])
# Shift each strip plot strictly below the correponding volin.
for item in ax.collections[num_items:]:
    item.set_offsets(item.get_offsets() + [0.15, 0])

sns.boxplot(x='condition', y=measure, saturation=.4, data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
            width=0.15, fliersize=12, boxprops={'zorder': 2, 'linewidth': 3}, palette=[pal2[1], pal1[1]],
            showmeans=True, meanprops=dict(marker='o', markerfacecolor='lightsteelblue',
                                           alpha=0.7, markersize=22, zorder=3, markeredgewidth=2),
            whiskerprops=dict(linewidth=3), capprops=dict(linewidth=3), medianprops=dict(linewidth=3),
            )

sns.despine(right=True, top=True, offset=5, trim=True)

ax.set(xlabel='', xticks=[0, 1], xticklabels=['left alley', 'right alley'], ylabel='peak \u0394 power (ratio)',
       ylim=[0, 5])
add_stat_annotation(ax, data=allDat[allDat['modality'] == 'MEG'].groupby(['subject', 'condition'], as_index=False).mean(),
                    x="condition", y=measure, use_fixed_offset=False, order=['left', 'right'],
                    box_pairs=[('right', 'left')], test='Wilcoxon',
                    text_format='star', loc='outside', verbose=2, comparisons_correction=None, linewidth=3)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.yaxis.set_tick_params(width=2, length=6)
ax.xaxis.set_tick_params(width=2, length=6)

fig.savefig(path + '/plots/figure2/rainplot_meg_power.pdf', bbox_inches='tight')
