import pingouin as pg
from scipy.stats import wilcoxon
from statistics import mean, stdev
from math import sqrt
from scipy.io import loadmat
import numpy as np

method = 'MEG'
chan = 'poc'
measure = 2
freqs = [8, 10]

circMean = loadmat(path + '/phase_ITC_analysis/circularMean_' + method + '_' + chan + '.mat')['All_Subject_Left_Right_Data8Hz']
circMean = pd.DataFrame(circMean, columns=['subject', 'condition', 'frequency', 'window', 'measure', 'value'])
circMean = circMean.astype({'subject': int, 'condition': int, 'frequency': int, 'window': int, 'measure': int, 'value': float})

gcm_stats = circMean[circMean['frequency'].isin(freqs)].groupby(
    ['measure', 'subject', 'window', 'condition'], as_index=False).mean()

x = gcm_stats[gcm_stats['window'] == 2][gcm_stats['condition'] == 1][gcm_stats['measure'] == measure]['value']
y = gcm_stats[gcm_stats['window'] == 2][gcm_stats['condition'] == 2][gcm_stats['measure'] == measure]['value']

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

(mean(x) - mean(y)) / (sqrt((stdev(x) ** 2 + stdev(y) ** 2) / 2))

####

gcm_stats = circMean[circMean['frequency'].isin(freqs)].groupby(
    ['measure', 'subject', 'frequency', 'window', 'condition'], as_index=False).mean()
gcm_stats = gcm_stats[gcm_stats['window'] == 2][gcm_stats['measure'] == measure]

x = gcm_stats[gcm_stats['frequency'] == 8]['value']
y = gcm_stats[gcm_stats['frequency'] == 10]['value']

w, p = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")

anovaTable = pg.rm_anova(dv='value', within=['condition', 'frequency'],
                         subject='subject', data=gcm_stats, detailed=True,
                         effsize="np2")
