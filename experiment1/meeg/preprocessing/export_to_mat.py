# EEG
import mne

# Data management
import scipy.io as sio
import numpy as np

# Create list of subject ids
subs = []
conditions = ['right', 'left']

# Loop over subjects
for sub in subs:

    # Read in epochs file
    epochsMEG = mne.read_epochs('file_directory/epochs/sub' + sub + '_tf-epo.fif', 
                                preload=True)
    epochsEEG = mne.read_epochs('file_directory/epochs/sub' + sub + '_tf_eeg64-epo.fif', 
                                preload=True)

    # Select the conditions and only select MEG sensors
    left = epochsMEG['reward_left', 'noreward_left'].copy().pick_types(meg=True, eeg=False, ref_meg=False).get_data()
    right = epochsMEG['reward_right', 'noreward_right'].copy().pick_types(meg=True, eeg=False, ref_meg=False).get_data()

    # Save the MEG data array as a mat file and re-arrange the dimensions, so that it is channels by samples by trials
    # For the matlab script from Baker et al. (2013) axes need to be re-ordered
    sio.savemat('file_directory/export/sub' + sub + 'left_meg.mat',
                mdict={'epochs': np.moveaxis(left, [0, 1, 2], [-1, 0, 1])},)
    sio.savemat('file_directory/export/sub' + sub + 'right_meg.mat',
                mdict={'epochs': np.moveaxis(right, [0, 1, 2], [-1, 0, 1])},)

    # Repeat for the 64 channel EEG data
    left = epochsEEG['reward_left', 'noreward_left'].pick_types(eeg=True, eog=False).get_data()
    right = epochsEEG['reward_right', 'noreward_right'].pick_types(eeg=True, eog=False).get_data()

    sio.savemat('file_directory/export/sub' + sub + 'left_eeg64.mat',
                mdict={'epochs': np.moveaxis(left, [0, 1, 2], [-1, 0, 1])},)
    sio.savemat('file_directory/export/sub' + sub + 'right_eeg64.mat',
                mdict={'epochs': np.moveaxis(right, [0, 1, 2], [-1, 0, 1])},)

# Lastly, create three channels lists, one for each data source
# MEG
names = epochsMEG.copy().pick_types(meg=True, eeg=False, ref_meg=False).info['ch_names']
with open('file_directory/channel_names_meg.txt', 'w') as f:
    for item in names:
        f.write("%s\n" % item)

# EEG (64 channels)
names = epochs64.pick_types(meg=False, eeg=True, ref_meg=False, eog=False).info['ch_names']
with open('file_directory/channel_names_eeg64.txt', 'w') as f:
    for item in names:
        f.write("%s\n" % item)
