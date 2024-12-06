# Data management
import pandas as pd
import numpy as np

# Statistics
from math import sqrt
from scipy.stats import wilcoxon
from statistics import mean, stdev

# Read the data
path = 'file_directory'
pdDat = pd.read_csv(path + 'tf/dataAlleysEvoked_eegmeg_peaksLat.csv')

# Pick the modality, channel and measure
modality = 'EEG'
measure = 'peak'
channel = 'PO8'

# Select the data (vector of values for selected measure) from the data frame
x = pdDat[pdDat['modality']==modality][pdDat['condition']=='right'][pdDat['channel']==channel][measure].to_numpy()
y = pdDat[pdDat['modality']==modality][pdDat['condition']=='left'][pdDat['channel']==channel][measure].to_numpy()
#x = pdDat[pdDat['modality']==modality][pdDat['condition']=='right'][measure].to_numpy()
#y = pdDat[pdDat['modality']==modality][pdDat['condition']=='left'][measure].to_numpy()

# Run Wilcoxon signed-rank test
w, p = wilcoxon(x=x, y=y, alternative='two-sided', mode="approx")
