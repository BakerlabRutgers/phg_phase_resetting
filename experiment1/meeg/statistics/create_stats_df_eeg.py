import mne

import os
import numpy as np
from itertools import chain
import csv

# Set some lists and variables for the loop
conditions1 = ['left_tmaze_eeg64', 'right_tmaze_eeg64']
conditions2 = ['reward_tmaze_eeg64', 'noreward_tmaze_eeg64']
pType = ['evoked']
subs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
path = 'file_directory'

eegNames = path + 'channel_names_eeg64.txt'

with open(eegNames, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    EEGchans = list(chain.from_iterable((list(reader))))

bandDict = {"delta": [0, 2], "theta1": [4, 5], "theta2": [6, 7], "theta3": [8, 9], 'theta': [3, 7], 'alpha': [10, 11],
           'beta': [12, 19], "gamma": [20, 50], "animalTheta": [3, 11]}
bands = ["delta", "theta1", "theta2", "theta3", "theta", "alpha", "beta", "gamma", "animalTheta"]

all_data = np.zeros(shape=(0, 8))

for cond in conditions1:

    for powtype in pType:

        for sub in subs:

            file = path + '/tf/sub' + sub + '_' + cond + '_' + powtype + '-tfr.h5'
            tfr_file = mne.time_frequency.read_tfrs(file)[0]

            for chan in EEGchans:

                for band in bands:

                    lim = bandDict[band]

                    data = tfr_file.copy().pick_channels([chan]).data.squeeze()

                    data = data[lim[0]:lim[1], :].mean(axis=0)

                    data = np.concatenate((data, np.array([data[637:687].mean()]).T)) 

                    roundedData = np.round(np.array(data[624:774]),3) 
                    peakSample = np.array([roundedData.argmax()]).T

                    if len(peakSample) > 1:
                        peakSample = peakSample[0]
                        print('double')

                    peakVal = np.array(roundedData[peakSample]).T

                    data = np.concatenate((data, peakVal))
                    data = np.concatenate((data, peakSample+1))

                    data = np.delete(data, range(0, samples), axis=0)

                    if cond == 'left_tmaze_eeg64':
                        condition = 'left'
                    elif cond == 'right_tmaze_eeg64':
                        condition = 'right'
                    elif cond == 'reward_tmaze_eeg64':
                        condition = 'reward'
                    elif cond == 'noreward_tmaze_eeg64':
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

allDat.to_csv(path + '/tf/dataAlleysEvokedTotal_long_eeg.csv', index=False)


############### data frame maintaining time points

subs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

conditions1 = ['left_tmaze_eeg64', 'right_tmaze_eeg64']
conditions2 = ['reward_tmaze_eeg64', 'noreward_tmaze_eeg64']

pType = ['evoked', 'total']

megNames = path + 'channel_names_meg.txt'
eegNames = path + 'channel_names_eeg64.txt'

with open(eegNames, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    chans = list(chain.from_iterable((list(reader))))

samples=275

all_data = np.zeros(shape=(0, 14))

chans = ['PO8']

for cond in conditions1:

    for powtype in pType:

        for sub in subs:

            file = path + '/tf/sub' + sub + '_' + cond + '_' + powtype + '-tfr.h5'
            tfr_file = mne.time_frequency.read_tfrs(file)[0].pick_channels(chans)

            data = np.squeeze(tfr_file.data[:, :, 600:875]).T

            del tfr_file

            if cond == 'left_tmaze_eeg64':
                condition = 'left'
            elif cond == 'right_tmaze_eeg64':
                condition = 'right'
            elif cond == 'reward_tmaze_eeg64':
                condition = 'reward'
            elif cond == 'noreward_tmaze_eeg64':
                condition = 'noreward'

            for f in np.arange(0,50):

                dataTemp = np.hstack([data[:, f], np.array([[condition]*len(data)]).T])
                dataTemp = np.append(dataTemp, np.array([[int(sub)]*len(data)]).T, 1)
                dataTemp = np.append(dataTemp, np.array([[powtype]*len(data)]).T, 1)
                dataTemp = np.append(dataTemp, np.arange(1, len(dataTemp)+1).T, 1)
                dataTemp = np.append(dataTemp, np.repeat(f+1, len(dataTemp)), 1)
                all_data = np.vstack((all_data, data))

allDat = pd.DataFrame(data=all_data,
                      index=np.array(range(1, len(all_data)+1)),
                      columns=np.array(['delta', 'theta1', 'theta2', 'theta3', 'theta', 'animalTheta', 'diesdas', 'alpha', 'gamma', 'condition',
                                        'subject', 'powerType', 'channel', 'sample'])
                      )

allDat = allDat.astype({'delta': float, 'theta1': float, 'theta2': float, 'theta3': float, 'theta': float, 'animalTheta': float, 'diesdas': float,
                        'alpha': float, 'gamma': float,'condition': str, 'subject': int, 'powerType': str, 'channel': str, 'sample': int})

allDat.to_csv(path + '/tf/dataAlleysEvokedTotal_samples_long_eeg64.csv', index=False)
