import os
import pandas as pd

import mne

from itertools import chain
import csv
import numpy as np

# Set some lists and variables for the loop
conditions1 = ['left_tmaze_meg', 'right_tmaze_meg']
conditions2 = ['reward_tmaze_meg', 'noreward_tmaze_meg']
pType = ['evoked', 'total']
subs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
path = 'file_directory'

megNames = path + '/channel_names_meg.txt'

with open(megNames, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    MEGchans = list(chain.from_iterable((list(reader))))

chanNo = len(MEGchans)
subNo = len(subs)
condNo = 2
freqs = 50

bandDict = {"delta": [0, 3], "theta1": [4, 5], "theta2": [6, 7], "theta3": [8, 9], 'theta': [3, 7], 'alpha': [10, 11],
           'beta': [12, 19], "gamma": [20, 49]}
bands = ["delta", "theta1", "theta2", "theta3", "theta", "alpha", "beta", "gamma"]

all_data = np.zeros(shape=(0, 8))

for cond in conditions1:

    for powtype in pType:

        for sub in subs:

            file = path + '/tf/sub' + sub + '_' + cond + '_' + powtype + '-tfr.h5'
            tfr_file = mne.time_frequency.read_tfrs(file)[0]

            for chan in MEGchans:

                for band in bands:

                    lim = bandDict[band]

                    data = tfr_file.copy().pick_channels([chan]).data.squeeze()

                    data = data[lim[0]:lim[1], :].mean(axis=0) # 100 ms to 250 ms

                    data = np.concatenate((data, np.array([data[1529:1649].mean()]).T)) # 50 ms to 250 ms

                    data = np.concatenate((data, np.array([data[1499:1859].max()]).T)) # 0 to 600 ms
                    data = np.concatenate((data, np.array([data[1499:1859].argmax()]).T)) # 0 to 600 ms

                    data = np.delete(data, range(0, samples), axis=0)

                    if cond == 'left_tmaze_meg':
                        condition = 'left'
                    elif cond == 'right_tmaze_meg':
                        condition = 'right'
                    elif cond == 'reward_tmaze_meg':
                        condition = 'reward'
                    elif cond == 'noreward_tmaze_meg':
                        condition = 'noreward'

                    data = np.append(data, np.array([condition, powtype, int(sub), band, chan]))
                    all_data = np.vstack((all_data, data))

            del tfr_file

allDat = pd.DataFrame(data=all_data,
                      index=np.array(range(1, len(all_data)+1)),
                      columns=np.array(['mean', 'peak', 'peakSample', 'condition',
                                        'powerType', 'subject', 'band', 'channel']),
                      )

allDat = allDat.astype({'mean': float, 'peak': float, 'peakSample': float,
                        'condition': str, 'powerType': str, 'subject': int, 'band': str, 'channel': str})

allDat['peakSample'] = ((allDat['peakSample']*1/sfreq)*1000)

allDat.to_csv(path + '/tf/dataAlleysEvokedTotal_long_meg.csv', index=False)


############### dataframe maintaining time points

conditions1 = ['left_tmaze_meg', 'right_tmaze_meg']
conditions2 = ['reward_tmaze_meg', 'noreward_tmaze_meg']

pType = ['evoked']

eegNames = path + '/channel_names_eeg64.txt'

with open(megNames, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    chans = list(chain.from_iterable((list(reader))))

chanNo = len(chans)
samples = 661

all_data = np.zeros(shape=(0, 13))

for cond in conditions1:

    for powtype in pType:

        for sub in subs:

            file = path + 'sub' + sub + '_' + cond + '_' + powtype + '-tfr.h5'
            tfr_file = mne.time_frequency.read_tfrs(file)[0].pick_channels(chans)

            animalTheta = tfr_file.data[:, 4:11, 1440:2101].mean(axis=1).reshape(samples*chanNo,-1)
            delta = tfr_file.data[:, 0:3, 1440:2101].mean(axis=1).reshape(samples*chanNo,-1)
            alpha = tfr_file.data[:, 10:11, 1440:2101].mean(axis=1).reshape(samples*chanNo,-1)
            theta1 = tfr_file.data[:, 4:5, 1440:2101].mean(axis=1).reshape(samples*chanNo,-1)
            theta2 = tfr_file.data[:, 6:7, 1440:2101].mean(axis=1).reshape(samples*chanNo,-1)
            theta3 = tfr_file.data[:, 8:9, 1440:2101].mean(axis=1).reshape(samples*chanNo,-1)
            theta48 = tfr_file.data[:, 3:7, 1440:2101].mean(axis=1).reshape(samples * chanNo, -1)
            gamma = tfr_file.data[:, 31:49, 1440:2101].mean(axis=1).reshape(samples*chanNo,-1)

            data = np.concatenate((delta, theta1, theta2, theta3, theta48, animalTheta, alpha, gamma),1)

            del tfr_file

            if cond == 'left_tmaze_meg':
                condition = 'left'
            elif cond == 'right_tmaze_meg':
                condition = 'right'
            elif cond == 'reward_tmaze_meg':
                condition = 'reward'
            elif cond == 'noreward_tmaze_meg':
                condition = 'noreward'

            data = np.append(data, np.array([[condition]*len(data)]).T, 1)
            data = np.append(data, np.array([[int(sub)]*len(data)]).T, 1)
            data = np.append(data, np.array([[powtype]*len(data)]).T, 1)
            data = np.append(data, np.array([[[ele for ele in chans for i in range(1,samples+1)],]]).reshape(len(data), -1), 1)
            data = np.append(data, np.array([[[range(1,samples+1)],]*chanNo]).reshape(len(data),-1),1)

            all_data = np.vstack((all_data, data))

allDat = pd.DataFrame(data=all_data,
                      index=np.array(range(1, len(all_data)+1)),
                      columns=np.array(['delta', 'theta1', 'theta2', 'theta3', 'theta', 'animalTheta', 'alpha', 'gamma', 'condition',
                                        'subject', 'powerType', 'channel', 'sample'])
                      )

allDat = allDat.astype({'delta': float, 'theta1': float, 'theta2': float, 'theta3': float, 'theta': float, 'animalTheta': float, 'alpha': float, 'gamma': float,
                        'condition': str, 'subject': int, 'powerType': str, 'channel': str, 'sample': int})

allDat.to_csv(path + '/tf/dataAlleysEvokedTotal_samples_long_meg.csv', index=False)
