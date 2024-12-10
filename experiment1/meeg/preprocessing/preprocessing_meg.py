# Data management
import os

# EEG
import mne
from mne.preprocessing import ICA

# Set the directory and file name
data_folder = 'file_directory/raw/'
raw_file = os.path.join(data_folder, 'filename.ds')

# Load the digital montage file used for the simultaneously recorded reduced EEG montage
montage = mne.channels.make_standard_montage(kind='standard_1005')

# Read the file in
raw = mne.io.read_raw_ctf(raw_file, preload=True)

# For setting the EEG montage, first identify the eog channels which cannot be recognized from standard digital montage names
raw.set_channel_types({'Saccade': 'eog', 'EEG031': 'eog'})
# Set positions based on names (Fz, Cz, M1, M2) and ignore the two eog channels (missing montage positions allowed)
raw.set_montage(montage=montage, on_missing='ignore')

# For an overview of the sensor maps, plot topographies for EEG ...
raw.plot_sensors(kind='topomap', ch_type='eeg', show_names=True, title='EEG');
# ... and for MEG
raw.plot_sensors(kind='topomap', ch_type='mag', show_names=True, title='MEG');

# Next, build a dictionary of event ids
event_id = {'noreward_right': 589824, 'noreward_left': 524288, 'reward_right': 458752, 'reward_left': 393216,
            'response_right': 327680, 'response_left': 262144, 'arrows': 131072, 'maze': 65536}

# Read the events from the stimulus channel
events = mne.events_from_annotations(raw)[0]
# Plot all events across time
fig = mne.viz.plot_events(events, raw.info['sfreq'],
                          event_id=event_id, first_samp=raw.first_samp)

# Save event array
mne.write_events('file_directory/events/' + sub + '-eve.fif', events)

# Bandpass filter data between 0.1 Hz and 60 Hz
filter_raw = raw.filter(l_freq=.1, h_freq=60, fir_window='hamming', method='fir')

# Plot average across all events to check for faulty channels
raw2 = filter_raw.copy()
epochs = mne.Epochs(raw2, events=events, event_id=event_id).average().plot()

# Interpolate channels if necessary
filter_raw.info['bads'] = []
filter_raw = filter_raw.interpolate_bads(reset_bads=True)

# For the ocular and other artifacts, employ an ICA correction approach
# Set parameters for ICA
n_components = 60
method='infomax'
allow_ref_meg = False

# Create ICA object
ica = ICA(n_components=n_components, method=method, allow_ref_meg=allow_ref_meg)

# Apply stricter high-pass filter at 1 Hz to copy of raw data to be fed into ICA
# to reduce influence of slow drifts and other high amplitude low frequency artifacts
ica.fit(filter_raw.copy().filter(l_freq=1, h_freq=60))

# Save ICA
ica.save('file_directory/ica/sub' + sub + '-ica.fif', overwrite=True)

# Plot all ica components as topomaps and their respective time course contributions
ica.plot_components()
ica.plot_sources(filter_raw, start=100);
# To be sure, we can look at exact properties of these components
ica.plot_properties(filter_raw, picks=[])

# Select components to be excluded from back-projection to continuous data
bads = []
ica.exclude = bads

# Validate artifact component selection by running automatic ICA eog component identification
eog_indices, eog_scores = ica.find_bads_eog(raw)
ica.exclude = eog_indices

# Plot the component artifact scores along with component properties and averaged raw data around EOG events with the best matching component excluded
ica.plot_scores(eog_scores);
ica.plot_properties(raw, picks=eog_indices);
ica.plot_sources(raw, start=100);
ica.plot_sources(eog_epochs.average());

# Back-project to continous data without artifact components
reconst_raw = filter_raw.copy()
ica.apply(reconst_raw)

# The same procedure can be applied using an automatic detection ICA-approach
# Build an empty list for component indices to be excluded
ica.exclude = []

# Create an event id dictionary with only the events to be analyzed
event_id = {'noreward_right': 589824, 'noreward_left': 524288, 'reward_right': 458752, 'reward_left': 393216}

# Epoch cleaned data round events and extract -2.5 to 2.5 seconds for time frequency analysis
epochs = mne.Epochs(reconst_raw, events, event_id, tmin=-2.5, tmax=2.5, baseline=None, preload=True, on_missing='ignore')

# Reject artifact epochs by first setting ampltiude criteria
reject = dict(mag=2000e-15) # 2000 fT
# Drop epochs exceeding amplitude threshold
epochs = epochs.drop_bad(reject=reject)
# If needed show distribution of dropped segments across channels 
epochs.plot_drop_log()

# Save data
reconst_raw.save('file_directory/raw/sub' + sub + '-raw.fif', overwrite=True)
epochs.save('file_directory/epochs/sub' + sub + '_tf-epo.fif', overwrite=True)
