# Data management
import pandas as pd
import numpy as np

# Statistics
from scipy import stats

# Read EEG and MEG statistics data frame
path = 'file_directory'
pdDat = pd.read_csv(path + 'tf/dataAlleysEvoked_eegmeg_peaksLat.csv')

# Pick measures and EEG electrode
measure = 'peak'
channel = 'PO8'
condition = ['right']

# Select data from data frame
eeg_data = pdDat[(pdDat['modality']=='EEG') & (pdDat['channel']==channel) & (pdDat['condition'].isin(condition))][measure].to_numpy()
meg_data = pdDat[(pdDat['modality']=='MEG') & (pdDat['condition'].isin(condition))][measure].to_numpy()

# Calculcate spearman correlation
stats.spearmanr(eeg_data, meg_data)
