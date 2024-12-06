import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)


path = 'file_directory'

allDat = pd.read_csv(path + '/tf/dataAlleys_samples_long_evoked_eeg.csv')
allDat = allDat[allDat['time'] <= 600]
allDat = allDat[(allDat['frequency'] >= 1) & (allDat['frequency'] <= 12)]
allDat = allDat[allDat['channel'] == 'PO8']

bands = [[1, 4], [5, 6], [7, 8], [9, 10], [11, 12]]

allDat2 = pd.DataFrame(np.zeros((0, 6)))
allDat2.columns = allDat.columns
allDat2 = allDat2.astype(allDat.dtypes)

for band in bands:
    data = allDat[(allDat['frequency'] >= band[0]) & (allDat['frequency'] <= band[1])]
    data = data.groupby(['subject', 'condition', 'time'], as_index=False).mean()
    data['frequency'] = band[1]
    allDat2 = pd.concat([allDat2, data])

# Initialize the FacetGrid object
pal1 = sns.cubehelix_palette(6, start=0, rot=-.15, light=.7)
pal2 = sns.cubehelix_palette(6, start=.4, rot=.15, light=.7)

ylim = [-.1, 1]

g = sns.FacetGrid(allDat2[allDat2['condition'].isin(['right'])],
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal1)

# Draw the densities in a few steps
g.map(sns.lineplot, "time", "power", alpha=1, clip_on=False, errorbar=None, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, color=None, errorbar=None, lw=4)
axes = g.axes

#g.map(plt.axhline, y=0, lw=4, clip_on=False)

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax,0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim([-.1, 1])

# passing color=None to refline() uses the hue mapping
g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=180, linewidth=2, linestyle="--", color=None, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0.05, .5, label + ' Hz', fontweight="normal", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "time")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.12)

# Remove axes details that don't play well with overlap
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
        ax.yaxis.set_ticks([0, 1])
        ax.spines['right'].set_linewidth(1)
        ax.set_ylabel("")
    else:
        ax.spines['right'].set_visible(False)
        ax.tick_params(right=False, left=False)
        [l.set_visible(False) for l in ax.get_yticklabels()]

g.savefig(path + '/plots/figure2/ridgeplot_right_eeg.pdf', bbox_inches='tight')


g = sns.FacetGrid(allDat2[allDat2['condition'].isin(['left'])],
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal2)

# Draw the densities in a few steps
g.map(sns.lineplot, "time", "power", alpha=1, errorbar=None, clip_on=False, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, errorbar=None, color=None, lw=4)
axes = g.axes

#g.map(plt.axhline, y=0, lw=4, clip_on=False)

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax,0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim([-.1, 1])

# passing color=None to refline() uses the hue mapping
g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=196, linewidth=2, linestyle="--", color=None, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0.05, .5, label + ' Hz', fontweight="normal", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "time")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.12)

# Remove axes details that don't play well with overlap
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
        ax.yaxis.set_ticks([0, 1])
        ax.spines['right'].set_linewidth(1)
        ax.set_ylabel("")
    else:
        ax.spines['right'].set_visible(False)
        ax.tick_params(right=False, left=False)
        [l.set_visible(False) for l in ax.get_yticklabels()]

g.savefig(path + '/plots/figure2/ridgeplot_left_eeg.pdf', bbox_inches='tight')

###################

allDat = pd.read_csv(path + '/tf/dataAlleys_samples_long_evoked_meg.csv')
allDat = allDat[allDat['time'] <= 600]
allDat = allDat[(allDat['frequency'] >= 1) & (allDat['frequency'] <= 12)]

allDat3 = pd.DataFrame(np.zeros((0, 6)))
allDat3.columns = allDat.columns
allDat3 = allDat3.astype(allDat.dtypes)

subs = np.arange(1,12)
chanKey = {1: 'MRO21-2511', 2: 'MRO33-2511', 3: 'MRO22-2511', 4: 'MRO32-2511', 5: 'MRO32-2511', 6: 'MZO01-2511',
           7: 'MLO21-2511', 8: 'MRO21-2511', 9: 'MRO32-2511', 10: 'MRO33-2511', 11: 'MRO21-2511'}

for sub in subs:
    data = allDat[(allDat['subject'] == sub) & (allDat['channel'] == chanKey[sub])]
    data['channel'] = chanKey[sub]
    allDat3 = pd.concat([allDat3, data])

allDat2 = pd.DataFrame(np.zeros((0, 6)))
allDat2.columns = allDat.columns
allDat2 = allDat2.astype(allDat.dtypes)

for band in bands:
    data = allDat3[(allDat3['frequency'] >= band[0]) & (allDat3['frequency'] <= band[1])]
    data = data.groupby(['subject', 'condition', 'time'], as_index=False).mean()
    data['frequency'] = band[1]
    allDat2 = pd.concat([allDat2, data])

# Initialize the FacetGrid object
pal1 = sns.cubehelix_palette(6, rot=-.15, light=.6)
pal2 = sns.cubehelix_palette(6, start=.4, rot=.15, light=.6)

g = sns.FacetGrid(allDat2[allDat2['condition'].isin(['right'])].groupby(['time', 'frequency'], as_index=False).mean(),
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal1)

# Draw the densities in a few steps
g.map(sns.lineplot, "time", "power", alpha=1, errorbar=None, clip_on=False, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, errorbar=None, color=None, lw=4)
axes = g.axes

#g.map(plt.axhline, y=0, lw=4, clip_on=False)

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax,0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim([-.1, 1])

# passing color=None to refline() uses the hue mapping
g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=184, linewidth=2, linestyle="--", color=None, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0.05, .5, label + ' Hz', fontweight="normal", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "time")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.12)

# Remove axes details that don't play well with overlap
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
        ax.yaxis.set_ticks([0, 1])
        ax.spines['right'].set_linewidth(1)
        ax.set_ylabel("")
    else:
        ax.spines['right'].set_visible(False)
        ax.tick_params(right=False, left=False)
        [l.set_visible(False) for l in ax.get_yticklabels()]

g.savefig(path + '/plots/figure2/ridgeplot_right_meg.pdf', bbox_inches='tight')


g = sns.FacetGrid(allDat2[allDat2['condition'].isin(['left'])],
                  row="frequency", hue="frequency", aspect=7,
                  height=1, palette=pal2)

# Draw the densities in a few steps
g.map(sns.lineplot, "time", "power", alpha=1, errorbar=None, clip_on=False, lw=4)
g.map(sns.lineplot, "time", "power", clip_on=False, errorbar=None, color=None, lw=4)
axes = g.axes

#g.map(plt.axhline, y=0, lw=4, clip_on=False)

for ax in np.arange(0,len(axes)):

    l1 = axes[ax,0].lines[0]
    color = l1.get_color()

    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    axes[ax,0].fill_between(x1, y1, color=color, alpha=.9)
    axes[ax, 0].set_ylim([-.1, 1])

# passing color=None to refline() uses the hue mapping
g.refline(x=0, linewidth=2, linestyle="--", color='black', clip_on=False, alpha=.7)
g.refline(x=211, linewidth=2, linestyle="--", color=None, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0.05, .5, label + ' Hz', fontweight="normal", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "time")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.12)

# Remove axes details that don't play well with overlap
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
        ax.yaxis.set_ticks([0, 1])
        ax.spines['right'].set_linewidth(1)
        ax.set_ylabel("")
    else:
        ax.spines['right'].set_visible(False)
        ax.tick_params(right=False, left=False)
        [l.set_visible(False) for l in ax.get_yticklabels()]

g.savefig(path + '/plots/figure2/ridgeplot_left_meg.pdf', bbox_inches='tight')

#######
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)

fig, ax = plt.subplots(figsize=(10,1))
ax.set(ylim=ylim, xticks=[], yticks=[-.1, 1], yticklabels=['-0.1', '1'])
sns.despine(right=False, left=True, top=True, bottom=True, offset=5, trim=True)
fig.savefig(path + '/plots/figure2/y_scale_ridge_plots.pdf', bbox_inches='tight')
