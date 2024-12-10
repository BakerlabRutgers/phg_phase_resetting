import pandas as pd
from scipy.io import loadmat
import seaborn as sns
import numpy as np
import matplotlib

matplotlib.use('Qt5Agg')

method = 'EEG'
chan = 'PO8'
measure = 2
win = 2
freq = 8

path = 'file_directory'

pal1 = sns.cubehelix_palette(10, rot=-.15, light=.7)
pal2 = sns.cubehelix_palette(10, start=.4, rot=.15, light=.7)

phaseStats = loadmat(path + '/phase_ITC_analysis/phaseResults_' + method + '_' + chan + '.mat')['allAngleData']
circMean = loadmat(path + '/phase_ITC_analysis/circularMean_' + method + '_' + chan + '.mat')['All_Subject_Left_Right_Data8Hz']

phaseStats = pd.DataFrame(phaseStats, columns=['subject', 'condition', 'frequency', 'window', 'angle'])
phaseStats['window'][phaseStats['window'] == 1] = 'pre-feedback'
phaseStats['window'][phaseStats['window'] == 2] = 'post-feedback'
phaseStats = phaseStats.astype({'subject': int, 'condition': int, 'frequency': int, 'window': str, 'angle': float})

circMean = pd.DataFrame(circMean, columns=['subject', 'condition', 'frequency', 'window', 'measure', 'angle'])
circMean = circMean.astype({'subject': int, 'condition': int, 'frequency': int, 'window': int, 'measure': int, 'angle': float})

######

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)


for sub in np.arange(10,11):
    # Set up a grid of axes with a polar projection
    g = sns.FacetGrid(phaseStats[phaseStats['subject']==sub][phaseStats['frequency']==freq], col="window",
                      hue="condition", subplot_kws=dict(projection='polar'), height=3.5,
                      sharex=False, sharey=False, despine=False, palette=[pal2[4], pal1[4]])
    g.map(sns.distplot, "angle", rug=False, hist=True, kde=False, norm_hist=False, bins=20,
          hist_kws={"histtype": "bar", "fill": True, "alpha": .3})
    ax = g.axes
    ax[0][0].set_xlabel('')
    ax[0][1].set_xlabel('')
    ax[0][0].set_ylim([0,14])
    ax[0][1].set_ylim([0,25])
    #ax[0][0].legend(handles=legend_elements, loc='upper right')
    g.set_titles(col_template="{col_name} (EEG)", size=15)

    g.savefig(path + '/plots/figure4/polarplot_angle_sub' + str(sub) + '_' + str(freq) + 'Hz_' + chan +
              '.pdf', bbox_inches='tight')

######

method = 'MEG'
chan = 'poc'
measure = 2
win = 2
freq = 8

phaseStats = loadmat('H:\\MEGEEG_project\\phase_ITC_analysis\\phaseResults_' + method + '_' + chan + '.mat')['allAngleData']
circMean = loadmat('H:\\MEGEEG_project\\phase_ITC_analysis\\circularMean_' + method + '_' + chan + '.mat')['All_Subject_Left_Right_Data8Hz']

phaseStats = pd.DataFrame(phaseStats, columns=['subject', 'condition', 'frequency', 'window', 'angle'])
phaseStats['window'][phaseStats['window'] == 1] = 'pre-feedback'
phaseStats['window'][phaseStats['window'] == 2] = 'post-feedback'
phaseStats = phaseStats.astype({'subject': int, 'condition': int, 'frequency': int, 'window': str, 'angle': float})

circMean = pd.DataFrame(circMean, columns=['subject', 'condition', 'frequency', 'window', 'measure', 'angle'])
circMean = circMean.astype({'subject': int, 'condition': int, 'frequency': int, 'window': int, 'measure': int, 'angle': float})

for sub in np.arange(10,11):
    # Set up a grid of axes with a polar projection
    g = sns.FacetGrid(phaseStats[phaseStats['subject']==sub][phaseStats['frequency']==freq], col="window",
                      hue="condition", subplot_kws=dict(projection='polar'), height=3.5,
                      sharex=False, sharey=False, despine=False, palette=[pal2[4], pal1[4]])
    g.map(sns.distplot, "angle", rug=False, hist=True, kde=False, norm_hist=False, bins=20,
          hist_kws={"histtype": "bar", "fill": True, "alpha": .3})
    ax = g.axes
    ax[0][0].set_xlabel('')
    ax[0][1].set_xlabel('')
    ax[0][0].set_ylim([0,14])
    ax[0][1].set_ylim([0,20])
    g.set_titles(col_template="{col_name} (MEG)", size=15)

    g.savefig(path + '/plots/figure4/polarplot_angle_sub' + str(sub) + '_' + str(freq) + 'Hz_' + chan +
              '.pdf', bbox_inches='tight')

####

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

legend_elements = [Line2D([0], [0], color=pal2[3], lw=7, label='left alley'),
                   Line2D([0], [0], color=pal1[3], lw=7, label='right alley')]

fig, ax = plt.subplots()
ax.legend(legend_elements, ['left alley', 'right alley'])
fig.savefig(path + '/plots/figure4/legend.pdf', bbox_inches='tight')
