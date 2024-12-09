import pandas as pd
from statistics import mean, stdev
from statsmodels.stats.anova import AnovaRM
from math import sqrt
import numpy as np
from scipy import stats
from scipy.stats import levene
from statsmodels.stats.multitest import multipletests
import pingouin as pg

path = 'file_directory'

pdDat = pd.read_csv(path + 'tf/dataAlleysEvoked_long_peakTheta_50350_max.csv')
pdDat['peakLatency'] = pdDat['peakLatency'] + 50
pdDat['condition'] = pdDat['alley'] + '_' + pdDat['block']
subs = [3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30]

measure = 'peak'
chans = ['E160']

pdDat_short = pdDat[(pdDat['channel'].isin(chans))]

anovaDF = np.zeros(shape=(0, 11))
anovaDF = pd.DataFrame(data=anovaDF,
                      index=np.array(range(1, len(anovaDF)+1)),
                      columns=np.array(['mean', 'peak', 'peakLatency', 'alley', 'block',
                                        'powerType', 'subject', 'frequency', 'channel', 'peakFreq', 'condition']))

anovaDF = anovaDF.astype({'mean': float, 'peak': float, 'peakLatency': float, 'alley': str, 'block': str,
                          'powerType': str, 'subject': int, 'frequency': str, 'channel': str, 'peakFreq': str,
                          'condition': str})
conditions = ['left_maze', 'right_maze', 'left_nomaze', 'right_nomaze']

for sub in subs:

    currentData = pdDat_short[pdDat['subject']==sub].groupby(['subject', 'channel'], as_index=False).mean()
    peakChan = currentData.iloc[currentData['peak'].argmax(), 1]

    for condName in conditions:

        currentData = pdDat_short[(pdDat['subject'] == sub) &
                                  (pdDat['channel'] == peakChan) &
                                  (pdDat['condition'] == condName)].groupby(['subject', 'frequency'],
                                                                            as_index=False).mean()
        peakFreq = currentData.iloc[currentData['peak'].argmax(), 1]

        currentData = pdDat_short[(pdDat['subject']==sub) & (pdDat['channel'] == peakChan)
                                  & (pdDat['condition'] == condName) & (pdDat['frequency'] == peakFreq)]
        anovaDF = pd.concat([anovaDF, currentData])

anovaDFOverview = anovaDF.groupby(['alley', 'block'], as_index=False).mean()

stat1 = anovaDF.groupby(['alley', 'block'], as_index=False).mean()
stat1['sd'] = anovaDF.groupby(['alley', 'block'], as_index=False).std()['peakLatency']

result = pg.rm_anova(dv=measure, within=['alley', 'block'],
                     subject='subject', data=anovaDF, detailed=True,
                     effsize="np2")

anovaDF.to_csv(path + 'tf/peakTheta_peakChan_stats.csv', index=False)

levene(anovaDF[anovaDF['condition']=='right_maze'][measure[0]],
               anovaDF[anovaDF['condition']=='left_maze'][measure[0]],
               anovaDF[anovaDF['condition']=='right_nomaze'][measure[0]],
               anovaDF[anovaDF['condition']=='left_nomaze'][measure[0]])

stats.shapiro(pd.concat([anovaDF[anovaDF['condition']=='right_maze'][measure[0]],
               anovaDF[anovaDF['condition']=='left_maze'][measure[0]],
               anovaDF[anovaDF['condition']=='right_nomaze'][measure[0]],
               anovaDF[anovaDF['condition']=='left_nomaze'][measure[0]]]))

anovaRMlat = AnovaRM(anovaDF, measure[0], 'subject', within=['alley', 'block'])
anovaRMresLat = anovaRMlat.fit()
anovaRMpeak = AnovaRM(anovaDF, measure[1], 'subject', within=['alley', 'block'])
anovaRMresPeak = anovaRMpeak.fit()


x = anovaDF[(anovaDF['condition'].isin(['right_maze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure].to_numpy()
y = anovaDF[(anovaDF['condition'].isin(['left_maze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure].to_numpy()
p1 = stats.ttest_rel(x, y, alternative='two-sided')[1]

x = anovaDF[(anovaDF['condition'].isin(['right_nomaze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure].to_numpy()
y = anovaDF[(anovaDF['condition'].isin(['left_nomaze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure].to_numpy()
p2 = stats.ttest_rel(x, y, alternative='two-sided')[1]

x = anovaDF[(anovaDF['condition'].isin(['right_nomaze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
y = anovaDF[(anovaDF['condition'].isin(['left_maze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
p3 = stats.ttest_rel(x, y, alternative='two-sided')[1]

x = anovaDF[(anovaDF['condition'].isin(['right_maze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
y = anovaDF[(anovaDF['condition'].isin(['left_nomaze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
p4 = stats.ttest_rel(x, y, alternative='two-sided')[1]

x = anovaDF[(anovaDF['condition'].isin(['right_maze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
y = anovaDF[(anovaDF['condition'].isin(['right_nomaze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
p5 = stats.ttest_rel(x, y, alternative='two-sided')[1]

x = anovaDF[(anovaDF['condition'].isin(['left_maze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
y = anovaDF[(anovaDF['condition'].isin(['left_nomaze'])) & (anovaDF['channel'].isin(chans))].groupby(
    ['subject', 'condition'], as_index=False).mean()[measure[0]].to_numpy()
p6 = stats.ttest_rel(x, y, alternative='two-sided')[1]

multipletests([p1, p2, p3, p4, p6], alpha=0.05, method='holm', is_sorted=False, returnsorted=False)


# Descriptive stats

z = mean([x,y], axis=0)
mean(z)
stdev(z)

mean(x)
stdev(x)

mean(y)
stdev(y)

mean(x-y)
stdev(x-y)

cohens_d = (mean(x) - mean(y)) / (sqrt(
    (stdev(x) ** 2 + stdev(y) ** 2) / 2))
