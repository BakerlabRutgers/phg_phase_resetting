import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)

chan = 'E160'
path = 'file_directory'
subs = [3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30]
bands = [[1, 4], [5, 6], [7, 8], [9, 10], [11, 12]]

##################

cond = 'right_maze'
allDat2 = pd.read_csv(path + '/EEG/tf/dataAlleys_samples_long_freqs_' + cond + '_evoked_rightHemi.csv')
allDat2 = allDat2[allDat2['time'] < 601]
allDat2 = allDat2[allDat2['channel'] == chan]

pal1 = sns.cubehelix_palette(6, start=0, rot=-.15, light=.7)
pal2 = sns.cubehelix_palette(6, start=.4, rot=.15, light=.7)
pal3 = sns.cubehelix_palette(6, start=.1, rot=-.1, light=.7)
pal4 = sns.cubehelix_palette(6, start=.7, rot=.1, light=.7)

ylim = [-0.04, 0.16]

allDat = pd.DataFrame(np.zeros((0, 6)))
allDat.columns = allDat2.columns
allDat = allDat.astype(allDat2.dtypes)

for band in bands:
    data = allDat2[(allDat2['frequency'] >= band[0]) & (allDat2['frequency'] <= band[1])]
    data = data.groupby(['subject', 'condition', 'time'], as_index=False).mean()
    data['channel'] = chan
    data['frequency'] = band[1]
    allDat = pd.concat([allDat, data])

g = sns.FacetGrid(allDat,
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal1)

g.map(sns.lineplot, "time", "power", alpha=1, errorbar=None, clip_on=False, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, errorbar=None, color=None, lw=4)
axes = g.axes

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax, 0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim(ylim)

g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=170, linewidth=2, linestyle="--", color=None, clip_on=False)

def label(x, color, label):
    ax = plt.gca()
    ax.text(0.02, .5, label + ' Hz', fontweight="normal", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "time")

g.figure.subplots_adjust(hspace=-.12)

g.set_titles("")
g.set(yticks=[], ylabel="", xticks=[], xlabel="")
g.despine(bottom=True, left=True)

ax = g.axes[4,0]
ax.set(xlabel='time (ms)', xticks=[-100, 0, 100, 200, 300, 400, 500, 600], ylim=ylim)
ax.tick_params(axis='both', which='both', length=0)
ax = g.axes[2,0]
ax.set_ylabel('')

for ax in g.axes.ravel():
    if ax.get_subplotspec().is_first_row():
        g.despine(bottom=True, left=True, right=False, top=True, offset=5)
        ax.yaxis.tick_right()
        ax.yaxis.set_ticks([0, 0.15])
        ax.yaxis.set_ticklabels(['0', '0.15'])
        ax.spines['right'].set_linewidth(1)
        ax.set_ylabel("")
    else:
        ax.spines['right'].set_visible(False)
        ax.tick_params(right=False, left=False)
        [l.set_visible(False) for l in ax.get_yticklabels()]

g.savefig(path + '/plots/figure6/ridgeplot_' + cond + '_rightHemi.pdf', bbox_inches='tight')

####################

cond = 'left_maze'
allDat2 = pd.read_csv(path + '/EEG/tf/dataAlleys_samples_long_freqs_' + cond + '_evoked_rightHemi.csv')
allDat2 = allDat2[allDat2['time'] < 601]
allDat2 = allDat2[allDat2['channel'] == chan]

allDat = pd.DataFrame(np.zeros((0, 6)))
allDat.columns = allDat2.columns
allDat = allDat.astype(allDat2.dtypes)

for band in bands:
    data = allDat2[(allDat2['frequency'] >= band[0]) & (allDat2['frequency'] <= band[1])]
    data = data.groupby(['subject', 'condition', 'time'], as_index=False).mean()
    data['channel'] = chan
    data['frequency'] = band[1]
    allDat = pd.concat([allDat, data])

g = sns.FacetGrid(allDat,
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal2)

g.map(sns.lineplot, "time", "power", alpha=1, errorbar=None, clip_on=False, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, errorbar=None, color=None, lw=4)
axes = g.axes

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax, 0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim(ylim)

g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=220, linewidth=2, linestyle="--", color=None, clip_on=False)

g.map(label, "time")

g.figure.subplots_adjust(hspace=-.12)

g.set_titles("")
g.set(yticks=[], ylabel="", xticks=[], xlabel="")
g.despine(bottom=True, left=True)

ax = g.axes[4,0]
ax.set(xlabel='time (ms)', xticks=[-100, 0, 100, 200, 300, 400, 500, 600], ylim=ylim)
ax.tick_params(axis='both', which='both', length=0)
ax = g.axes[2,0]
ax.set_ylabel('')

g.savefig(path + '/plots/figure6/ridgeplot_' + cond + '_rightHemi.pdf', bbox_inches='tight')

###################

cond = 'right_nomaze'
allDat2 = pd.read_csv(path + '/EEG/tf/dataAlleys_samples_long_freqs_' + cond + '_evoked_rightHemi.csv')
allDat2 = allDat2[allDat2['time'] < 601]
allDat2 = allDat2[allDat2['channel'] == chan]

allDat = pd.DataFrame(np.zeros((0, 6)))
allDat.columns = allDat2.columns
allDat = allDat.astype(allDat2.dtypes)

for band in bands:
    data = allDat2[(allDat2['frequency'] >= band[0]) & (allDat2['frequency'] <= band[1])]
    data = data.groupby(['subject', 'condition', 'time'], as_index=False).mean()
    data['channel'] = chan
    data['frequency'] = band[1]
    allDat = pd.concat([allDat, data])

g = sns.FacetGrid(allDat,
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal3)

g.map(sns.lineplot, "time", "power", alpha=1, errorbar=None, clip_on=False, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, errorbar=None, color=None, lw=4)
axes = g.axes

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax, 0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim(ylim)

g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=210, linewidth=2, linestyle="--", color=None, clip_on=False)

g.map(label, "time")

g.figure.subplots_adjust(hspace=-.12)

g.set_titles("")
g.set(yticks=[], ylabel="", xticks=[], xlabel="")
g.despine(bottom=True, left=True)

ax = g.axes[4,0]
ax.set(xlabel='time (ms)', xticks=[-100, 0, 100, 200, 300, 400, 500, 600], ylim=ylim)
ax.tick_params(axis='both', which='both', length=0)
ax = g.axes[2,0]
ax.set_ylabel('')

for ax in g.axes.ravel():
    if ax.get_subplotspec().is_first_row():
        g.despine(bottom=True, left=True, right=False, top=True, offset=5)
        ax.yaxis.tick_right()
        ax.yaxis.set_ticks([0, 0.15])
        ax.yaxis.set_ticklabels(['0', '0.15'])
        ax.spines['right'].set_linewidth(1)
        ax.set_ylabel("")
    else:
        ax.spines['right'].set_visible(False)
        ax.tick_params(right=False, left=False)
        [l.set_visible(False) for l in ax.get_yticklabels()]

g.savefig(path + '/plots/figure6/ridgeplot_' + cond + '_rightHemi.pdf', bbox_inches='tight')

######################

cond = 'left_nomaze'
allDat2 = pd.read_csv(path + '/EEG/tf/dataAlleys_samples_long_freqs_' + cond + '_evoked_rightHemi.csv')
allDat2 = allDat2[allDat2['time'] < 601]
allDat2 = allDat2[allDat2['channel'] == chan]

allDat = pd.DataFrame(np.zeros((0, 6)))
allDat.columns = allDat2.columns
allDat = allDat.astype(allDat2.dtypes)

for band in bands:
    data = allDat2[(allDat2['frequency'] >= band[0]) & (allDat2['frequency'] <= band[1])]
    data = data.groupby(['subject', 'condition', 'time'], as_index=False).mean()
    data['channel'] = chan
    data['frequency'] = band[1]
    allDat = pd.concat([allDat, data])

g = sns.FacetGrid(allDat,
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal4)

g.map(sns.lineplot, "time", "power", alpha=1, errorbar=None, clip_on=False, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, errorbar=None, color=None, lw=4)
axes = g.axes

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax, 0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim(ylim)

g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=181, linewidth=2, linestyle="--", color=None, clip_on=False)

g.map(label, "time")

g.figure.subplots_adjust(hspace=-.12)

g.set_titles("")
g.set(yticks=[], ylabel="", xticks=[], xlabel="")
g.despine(bottom=True, left=True)

ax = g.axes[4,0]
ax.set(xlabel='time (ms)', xticks=[-100, 0, 100, 200, 300, 400, 500, 600], ylim=ylim)
ax.tick_params(axis='both', which='both', length=0)
ax = g.axes[2,0]
ax.set_ylabel('')

g.savefig(path + '/plots/figure6/ridgeplot_' + cond + '_rightHemi.pdf', bbox_inches='tight')
