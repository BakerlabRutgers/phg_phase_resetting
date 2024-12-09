import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from scipy.stats import ttest_rel
from statsmodels.stats.anova import AnovaRM
import pingouin as pg
from statsmodels.stats.multitest import multipletests

measure = 'rt'
path = 'file_directory'

# Create pandas dataframe with column names

columns = ['block', 'outcome', 'subject', 'sum', 'rt', 'sd', 'se', 'ci']
rt = pd.read_csv(path + 'behavioral_data\\edat\\rt.csv', sep=',', names=columns, skiprows=1)
rt['alley'] = rt['outcome'].replace({'left_apple': 'left', 'left_orange': 'left',
                                          'right_apple': 'right', 'right_orange': 'right'})
rt['condition'] = rt['alley'] + '_' + rt['block']

columns = ['shift', 'subject', 'block', 'sum', 'percent']

shifts = pd.read_csv(path + '/behavioral_data/edat/shifts.csv', sep=',', names=columns, skiprows=1)
shifts['shift'][shifts['shift'] == 0] = 'win_stay'
shifts['shift'][shifts['shift'] == 1] = 'win_shift'
shifts['shift'][shifts['shift'] == 2] = 'lose_stay'
shifts['shift'][shifts['shift'] == 3] = 'lose_shift'
shifts = shifts[shifts['subject'].isin([3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18,
                                        19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30])]

rt = rt[rt['subject'].isin([3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18,
                           19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30])]

anovaRM = AnovaRM(rt.groupby(['subject', 'alley', 'block'], as_index=False).mean(),
                  measure, 'subject', within=['alley', 'block'])
anovaRMres = anovaRM.fit()

result = pg.rm_anova(dv=measure, within=['alley', 'block'], subject='subject',
            data=rt.groupby(['subject', 'alley', 'block'], as_index=False).mean(), detailed=True, effsize="np2")

########

measure = 'sum'

shifts = shifts[shifts['subject'].isin([3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18,
                                        19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30])]

pg.rm_anova(dv=measure, within=['shift', 'block'], subject='subject',
            data=shifts.groupby(['subject', 'shift', 'block'], as_index=False).mean(), detailed=True, effsize="np2")

anovaDF = shifts.groupby(['subject', 'shift'], as_index=False).mean()

x = anovaDF[(anovaDF['shift'].isin(['win_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['win_shift']))][measure].to_numpy()
p1 = ttest_rel(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_shift']))][measure].to_numpy()
p2 = ttest_rel(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_stay']))][measure].to_numpy()
p3 = ttest_rel(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_shift']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_shift']))][measure].to_numpy()
p4 = .ttest_rel(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_shift']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_stay']))][measure].to_numpy()
p5 = ttest_rel(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['lose_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_shift']))][measure].to_numpy()
p6 = ttest_rel(x=x, y=y, alternative='two-sided', mode="approx")[1]

# Use a Bonferroni-Holm correction for the obtained p-values
multipletests([p1, p6, p3, p4, p5, p2], alpha=0.05, method='holm', is_sorted=False, returnsorted=False)
