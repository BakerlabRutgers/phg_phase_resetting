import mne
import numpy as np

path = 'file_directory'

event_id = {'mazeleftapple': 101, 'mazerightapple': 102,
            'mazeleftorange': 103, 'mazerightorange': 104,
            'nomazeleftapple': 201, 'nomazerightapple': 202,
            'nomazeleftorange': 203, 'nomazerightorange': 204}

reject = dict(eeg=200e-6) # 100 microV

subs = [str(x) for x in np.append(3, np.arange(5,31))]

for sub in subs:

    raw = mne.io.read_raw(path + '/raw/sub' + sub + '_prepro-raw.fif', preload=True)
    events = mne.read_events(path + '/events/events' + sub + '-eve.fif')
    events[:,0] = events[:,0]+100 # account for event code pre-release

    # Segment the data after minimizing the number of events to make segments from
    epochs = mne.Epochs(raw, events, event_id, tmin=-.2, tmax=.8, baseline=None, preload=True,
                        on_missing='ignore')

    # Remove epochs exceeding threshold
    epochs = epochs.drop_bad(reject=reject)

    epochs.save('D:/EEG_fMRI_tmaze/EEG/epochs/sub' + sub + '_ERP-epo.fif', overwrite=True)

    # Create epochs with a larger time window and without the stricter filtering or baseline correction
    epochs = mne.Epochs(raw, events, event_id, tmin=-2.5, tmax=2.5, baseline=None, preload=True,
                        on_missing='ignore')

    # Remove epochs exceeding threshold
    epochs = epochs.drop_bad(reject=reject)
    epochs.save('D:/EEG_fMRI_tmaze/EEG/epochs/sub' + sub + '_tf-epo.fif', overwrite=True)
