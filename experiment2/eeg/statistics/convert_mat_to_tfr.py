import numpy as np

import mne
from mne.time_frequency import tfr_morlet

from scipy.io import loadmat

## Load the data and get an idea of the raw files

# Set the directory and file name
montage = mne.channels.make_standard_montage(kind='GSN-HydroCel-256')

# Import tf results
# Set some lists and variables for the loop
conditions = ['left_maze', 'right_maze', 'left_nomaze', 'right_nomaze']
pType = ['evoked']
subs = [str(x) for x in np.arange(3,31)]
subs.remove('4')
subs.remove('14')
subs.remove('25')
path = 'file_directory'

samples = 5001
chNr = 256
sfreq = 1000
subNr = len(subs)

# Create dummy of tf object
rdata = np.random.randn(subNr, chNr, samples)

epochs = mne.read_epochs('D:/EEG_fMRI_tmaze/EEG/epochs/sub3_tf-epo.fif')
info = epochs.drop_channels(['ECG']).info

events = np.array([np.arange(0, 25, 1), np.repeat(1, 25), np.repeat(1, 25)]).T

event_id = dict(subject=1)

# Trials were cut from -2.5 to 2.5 seconds
tmin = -2.5
tmax = 2.5
custom_epochs = mne.EpochsArray(rdata, info=info, events=events, tmin=tmin, event_id=event_id)

# Transform the dummy epochs to a tfr object
decim = 1
freqs = np.arange(1, 51, 1)
n_cycles = 0.5

tfr_epochs = tfr_morlet(custom_epochs, freqs, picks=info['ch_names'],
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
