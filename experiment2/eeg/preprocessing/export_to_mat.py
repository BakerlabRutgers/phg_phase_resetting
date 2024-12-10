import mne
import scipy.io as sio
import numpy as np

# Create a list of strings with all subject IDs
subs = [str(x) for x in np.arange(3,31)]

# Set path and other variables
path = 'file_directory'
chanNum = 256
samples = 5001
drops = ['ECG']

# Loop across all subjects
for sub in subs:

    # Read EEG data
    epochs = mne.read_epochs(path + 'epochs/sub' + sub + '_tf-epo.fif', preload=True)

    # Extract numpy arrays with the time series data for each condition
    left_maze = epochs['mazeleftapple', 'mazeleftorange'].copy().drop_channels(drops).to_data_frame().drop(
        ['time', 'condition', 'epoch'], axis=1).to_numpy()
    left_maze = left_maze.reshape((int(left_maze.shape[0]/samples)), samples, chanNum)
    right_maze = epochs['mazerightapple', 'mazerightorange'].copy().drop_channels(drops).to_data_frame().drop(
        ['time', 'condition', 'epoch'], axis=1).to_numpy()
    right_maze = right_maze.reshape((int(right_maze.shape[0]/samples)), samples, chanNum)
    
    left_nomaze = epochs['nomazeleftapple', 'nomazeleftorange'].copy().drop_channels(drops).to_data_frame().drop(
        ['time', 'condition', 'epoch'], axis=1).to_numpy()
    left_nomaze = left_nomaze.reshape((int(left_nomaze.shape[0]/samples)), samples, chanNum)
    right_nomaze = epochs['nomazerightapple', 'nomazerightorange'].copy().drop_channels(drops).to_data_frame().drop(
        ['time', 'condition', 'epoch'], axis=1).to_numpy()
    right_nomaze = right_nomaze.reshape((int(right_nomaze.shape[0]/samples)), samples, chanNum)

    # Save the data array as a mat file and re-arrange the dimensions, so that it is channels by samples by trials
    sio.savemat(path + 'export/sub' + sub + '_left_maze.mat',
                mdict={'epochs': np.moveaxis(left_maze, [0, 1, 2], [-1, 1, 0])},)

    sio.savemat(path + 'export/sub' + sub + '_right_maze.mat',
                mdict={'epochs': np.moveaxis(right_maze, [0, 1, 2], [-1, 1, 0])},)

    sio.savemat(path + 'export/sub' + sub + '_left_nomaze.mat',
                mdict={'epochs': np.moveaxis(left_nomaze, [0, 1, 2], [-1, 1, 0])},)

    sio.savemat(path + 'export/sub' + sub + '_right_nomaze.mat',
                mdict={'epochs': np.moveaxis(right_nomaze, [0, 1, 2], [-1, 1, 0])},)

# Lastly, create the channels list
names = epochs.copy().drop_channels(drops).info['ch_names']
with open(path + 'export/channel_names_egi.txt', 'w') as f:
    for item in names:
        f.write("%s\n" % item)
