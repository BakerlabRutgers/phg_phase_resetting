# Data management
import pandas as pd
import numpy as np

# Statistics
from scipy.stats import wilcoxon, friedmanchisquare, ttest_rel
from statistics import mean, stdev
from math import sqrt
from statsmodels.stats.multitest import multipletests

##### Reaction times (RT)
# Create pandas dataframe with column names

measure = 'rt'
modality = 'meg'
columns = ['alley', 'subject', 'sum', 'rt', 'sd', 'se', 'ci']

# Path to data from EEG experiment
path = 'file_directory'
# Read EEG behavioral data
eegRT = pd.read_csv(path + 'rtR.csv', sep=',', names=columns, skiprows=1)
# Create new method/modality column with value 'eeg'
eegRT['method'] = 'eeg'

# Path to data from MEG experiment
path = 'file_directory'
# Read MEG behavioral data
megRT = pd.read_csv(path + 'rt.csv', sep=',', names=columns, skiprows=1)
# Create new method/modality column with value 'meg'
megRT['method'] = 'meg'

# Combine the two data frames
rt = pd.concat([eegRT, megRT])
# Recode the integer alley value to string
rt['alley'][rt['alley'] == 1] = 'left'
rt['alley'][rt['alley'] == 2] = 'right'
# Create a combined alley and method column for ease of plotting
rt['condition'] = rt['alley'] + '_' + rt['method']

# Extract two vectors with the values for each alley
x = rt[rt['condition']=='right_' + modality][measure].to_numpy()
y = rt[rt['condition']=='left_' + modality][measure].to_numpy()

# Run a Wilcoxon signed rank test to get the test statistic and p-value
w, p = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")

##### Shift behavior

measure = 'sum'

columns = ['shift', 'subject', 'sum', 'percent']

path = 'file_directory'
eegShifts = pd.read_csv(path + 'shifts.csv', sep=',', names=columns, skiprows=1)
eegShifts['method'] = 'eeg'

path = 'H:\\MEGEEG_project\\MEG\\behavior_meg\\shiftsR.csv'
megShifts = pd.read_csv(path, sep=',', names=columns, skiprows=1)
megShifts['method'] = 'meg'

# Recode the exisiting values to string labels
megShifts['shift'][megShifts['shift'] == 0] = 'win_stay'
megShifts['shift'][megShifts['shift'] == 1] = 'win_shift'
megShifts['shift'][megShifts['shift'] == 2] = 'lose_stay'
megShifts['shift'][megShifts['shift'] == 3] = 'lose_shift'

eegShifts['shift'][eegShifts['shift'] == 0] = 'win_stay'
eegShifts['shift'][eegShifts['shift'] == 1] = 'win_shift'
eegShifts['shift'][eegShifts['shift'] == 2] = 'lose_stay'
eegShifts['shift'][eegShifts['shift'] == 3] = 'lose_shift'

# Calculcate a Friedmann Chi Square test for the sum of choices for each behavior
friedmanchisquare(eegShifts[eegShifts['shift'] == 'win_stay'][measure],
                  eegShifts[eegShifts['shift'] == 'win_shift'][measure],
                  eegShifts[eegShifts['shift'] == 'lose_stay'][measure],
                  eegShifts[eegShifts['shift'] == 'lose_shift'][measure])

# Run post-hoc comparisons by running individual tests and then correcting the p-values for multiple comparisons
anovaDF = eegShifts.groupby(['subject', 'shift'], as_index=False).mean()
x = anovaDF[(anovaDF['shift'].isin(['win_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['win_shift']))][measure].to_numpy()
w, p = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")

x = anovaDF[(anovaDF['shift'].isin(['win_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['win_shift']))][measure].to_numpy()
p1 = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_shift']))][measure].to_numpy()
p2 = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_stay']))][measure].to_numpy()
p3 = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_shift']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_shift']))][measure].to_numpy()
p4 = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['win_shift']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_stay']))][measure].to_numpy()
p5 = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")[1]

x = anovaDF[(anovaDF['shift'].isin(['lose_stay']))][measure].to_numpy()
y = anovaDF[(anovaDF['shift'].isin(['lose_shift']))][measure].to_numpy()
p6 = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")[1]

# Use a Bonferroni-Holm correction for the obtained p-values
multipletests([p1, p6, p3, p4, p5, p2], alpha=0.05, method='holm', is_sorted=False, returnsorted=False)
