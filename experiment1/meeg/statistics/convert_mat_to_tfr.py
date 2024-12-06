import os
import numpy as np
import pandas as pd
import mne
from mne.preprocessing import ICA
from itertools import chain
import csv
import numpy as np

import mne
from mne.time_frequency import tfr_morlet

from scipy.io import loadmat

# Import the mat files from time-frequency analysis to Python
# And convert into MNE-python tfr object

# Set montage file
montage = mne.channels.make_standard_montage(kind='standard_1005')

# Set some lists and variables for the loop
conditions = ['left_tmaze_eeg64', 'right_tmaze_eeg64', 'reward_tmaze_eeg64', 'noreward_tmaze_eeg64']
pType = ['evoked', 'total', 'induced']
subs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
path = 'file_directory'

samples = 1251
chNr = 60
sfreq = 250
subNr = len(subs)

# Create dummy of tf object
rdata = np.random.randn(subNr, chNr, samples)

epochs=mne.read_epochs(path + '/epochs/sub01_tf64-epo.fif')
info=epochs.pick_types(meg=False, eeg=True, ref_meg=False).info

# Create events for dummy epochs
events = np.array([
    [0, 1, 1],
    [1, 1, 1],
    [2, 1, 1],
    [3, 1, 1],
    [4, 1, 1],
    [5, 1, 1],
    [6, 1, 1],
    [7, 1, 1],
    [8, 1, 1],
    [9, 1, 1],
    [10, 1, 1]
])

event_id = dict(subjects=1)

# Trials were cut from -2.5 to 2.5 seconds
tmin = -2.5
tmax = 2.5
custom_epochs = mne.EpochsArray(rdata, info=info, events=events, tmin=tmin, event_id=event_id)

# Transform the dummy epochs to a tfr object
decim = 1
freqs = np.arange(1, 51, 1)
n_cycles = 0.5

tfr_epochs = tfr_morlet(custom_epochs, freqs,
                        n_cycles=n_cycles, decim=decim,
                        return_itc=False, average=False)

tfr_ave = tfr_epochs.average()

my_array=np.zeros(shape=(chNr, 50, samples))
ch_names = info['ch_names']

s = 0
c = 0
my_subs_array=np.zeros(shape=(subNr, chNr, 50, samples))

# Load every time frequency result exported from matlab and transform it into an mne tfr object
for condName in conditions:

    for powtype in pType:

        s = 0
        if powtype == 'evoked':
            key = 'POW_evoked'
        else:
            key = 'POW_BASE_subj'

        for sub in subs:

            c = 0

            for cl in ch_names:

                file = path + 'POW' + powtype + '_' + 'sub' + sub + '_' + condName + '_' + cl + '.mat'
                data = np.squeeze(loadmat(file)[key])[0:50,:]

                my_array[c, :, :] = data
                c = c + 1

            tfr_ave.data = my_array
            tfr_ave.save(path + '/tf/sub' + sub + '_' + condName + '_' + powtype + '-tfr.h5', overwrite=True)

            my_subs_array[s, :, :, :] = my_array
            my_array = np.zeros(shape=(chNr, 50, samples))

            s = s + 1

        tfr_ave.data = np.mean(my_subs_array, axis=0)
        tfr_ave.save(path + '/tf/' + condName + '_' + powtype + '-tfr.h5', overwrite=True)
