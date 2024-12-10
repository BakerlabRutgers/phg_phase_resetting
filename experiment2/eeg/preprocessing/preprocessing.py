# Data management
import numpy as np

# EEG
import mne
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs, corrmap

# Set the directory and file name
path = 'file_directory'
sub = 'subject_ID'

# Load in the raw data corrected for gradient artifacts and with a first pass of ballistocardiac artifacts done
raw = mne.io.read_raw_edf(path + '/raw/bva/exp/sub' + sub + '_cbCorr.edf', preload=True)
# Drop the online reference
raw = raw.drop_channels(['E257'])

# Collect information to create a new raw info with all the necessary details
# Set the sampling rate
s_freq = 1000
# Get the EEG channel names
labels = raw.info['ch_names']
# Create a list of channel types
ch_types = ['eeg']*256 + ['ecg']
# Read the digital montage
montage = mne.channels.make_standard_montage(kind='GSN-HydroCel-256')
# Combine the information
info = mne.create_info(labels, s_freq, ch_types)
info['meas_date'] = raw.info['meas_date']
info['buffer_size_sec'] = 1
# Set the raw info
raw.info = info
raw.set_montage(montage=montage, on_missing='ignore')

# Bandpass filter data between 0.1 Hz and 60 Hz
filter_raw = raw.filter(l_freq=.1, h_freq=60, fir_window='hamming', method='fir')

# Create an event id dictionary
event_id = {'mazeleftapple': 101, 'mazerightapple': 102,
            'mazeleftorange': 103, 'mazerightorange': 104,
            'nomazeleftapple': 201, 'nomazerightapple': 202,
            'nomazeleftorange': 203, 'nomazerightorange': 204,
            'miss': 999}
# Read the custom made event array
events = mne.read_events('D:\\EEG_fMRI_tmaze\\events\\export_eeglab\\fullSample\\events' + sub + '_TR-eve.fif')

# Average the data around all events and plot to check for channels that need to be interpolated
raw2 = filter_raw.copy()
epochs = mne.Epochs(filter_raw, events=events, event_id=event_id, on_missing='ignore').average().plot()

# Interpolate channels if necessary
filter_raw.info['bads'] = []
filter_raw = filter_raw.interpolate_bads(reset_bads=True)

# For the ocular and other artifacts, employ an ICA correction approach
# Set parameters for ICA
n_components = 60
method='infomax'

# Create ICA object
ica = ICA(n_components=n_components, method=method)

# Apply stricter high-pass filter at 1 Hz to copy of raw data to be fed into ICA
# to reduce influence of slow drifts and other high amplitude low frequency artifacts.
# Also, exclude the EKG channels from the selection of channels.
ica.fit(filter_raw.copy().filter(l_freq=1, h_freq=60), picks=info['ch_names'][0:-1])

# Plot all ica components as topomaps and their respective time course contributions
ica.plot_components()
ica.plot_sources(filter_raw, start=100);
# To be sure, we can look at exact properties of these components
ica.plot_properties(filter_raw, picks=[])

# Create EKG epochs around likely artifact events and average them
ecg_average = create_ecg_epochs(raw, reject=None).average()

# Create EKG epochs around likely artifact events and correlate them
# to all ICA component source signal time course.
# Build artifact scores via the correlation anaylsis.
ecg_epochs = create_ecg_epochs(filter_raw, reject=None)
ecg_inds, scores = ica.find_bads_ecg(ecg_epochs)

# Plot the component artifact scores along with component properties 
# and averaged raw data around EKG events with the best matching component excluded
ica.plot_sources(ecg_average)
ica.plot_sources(filter_raw, start=100);
ica.plot_scores(scores)

# Save ICA
ica.save('file_directory/ica/sub' + sub + '_CBcorr-ica.fif', overwrite=True)

# Now we can remove these components before back-projecting the components to continuous data
bads = []
ica.exclude = bads

# Look at the raw data again after ICA
reconst_raw = filter_raw.copy()
ica.apply(reconst_raw)

raw.plot(events=events, start=100, duration=20, color='gray', event_id=event_id, scalings=dict(eeg=20e-6))
reconst_raw.plot(events=events, start=100, duration=20, color='gray', event_id=event_id, scalings=dict(eeg=20e-6))

# Rereference to the average of all EEG channels on top of the head,
# excluding sensors on the cheeks and the neck
idx = list(np.arange(0, 66)) + list(np.arange(67, 72)) + list(np.arange(73, 81)) + list(np.arange(82, 90)) + list(
    np.arange(91, 215)) + list(np.arange(219, 224))  # Get numeric indices
names = [reconst_raw.ch_names[i] for i in idx]  # Get the names (i.e., 'E128')
reconst_raw.set_eeg_reference(ref_channels=names)

# Segment the data after minimizing the number of events to make segments from
epochs = mne.Epochs(reconst_raw, events, event_id, tmin=-2.5, tmax=2.5, baseline=None, preload=True, on_missing='ignore')

# Reject artifact epochs and set ampltiude criteria
reject = dict(eeg=200e-6) # 200 microV
rejected = epochs.copy().apply_baseline(baseline=(-.2, -.1)).drop_bad(reject=reject)

# Save the indices of dropped segments for later when comparing to single fMRI trials
drop_log = np.array(rejected.drop_log)
artifact_epochs = np.array([i for i, x in enumerate(drop_log) if x])
epochs.drop(artifact_epochs)

# If needed show distribution of dropped segments across channels 
epochs.plot_drop_log()

# Save data
reconst_raw.save('file_directory/raw/sub' + sub + '_prepro-raw.fif', overwrite=True)
epochs.save('file_directory/raw/sub' + sub + '_tf-epo.fif', overwrite=True)
