import mne
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use('Qt5Agg')

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 28}
matplotlib.rc('font', **font)

path = 'file_directory'

sub = '8'

sub8 = pd.read_csv(path + '/EEG/tf/tf_singleTrials_evoked_sub8_samples.txt', sep='\t')
sub8 = sub8[sub8['condition'] == 'right']
sub8 = sub8[(sub8['frequency'] >= 7) & (sub8['frequency'] <= 8)]
sub8 = sub8.groupby(['subject', 'sample', 'trial'], as_index=False).mean()[['subject', 'sample', 'trial', 'power']]

good_trials = sub8.groupby(['trial'], as_index=False).max()[['trial', 'power']].sort_values(by='power', ascending=False).iloc[[0, 2, 3, 4, 5, 7, 9, 10],:]
plotData = sub8[sub8['trial'].isin(good_trials['trial'].tolist())]
average = sub8[sub8['trial'].isin(good_trials['trial'].tolist())].groupby(['sample'], as_index=False).mean()[['power', 'sample']]

fig, ax = plt.subplots()
sns.lineplot(x="sample", y="power", hue='trial', data=plotData,
             palette='Greys', linewidth=1.5,
             legend=None, ax=ax)
plt.setp(ax.lines, alpha=.8)
sns.lineplot(x="sample", y="power", data=average,
             color='black', linewidth=2.5,
             legend=None, ax=ax)
ax.axvspan(50, 250, color='cornflowerblue', alpha=.3)
ax.set(ylim=(-1, 2.35), ylabel='\u0394 power (ratio)', xlabel='time (ms)', xticks=[0, 200, 400, 600, 800])

sns.despine(right=True, top=True, trim=True, offset=5)

fig.savefig(path + '/plots/figure9/theta8_STave_sub8.pdf', bbox_inches='tight')
