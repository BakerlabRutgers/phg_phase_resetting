import numpy as np
import pandas as pd
from itertools import chain
import csv
from scipy.io import loadmat
from scipy.signal import find_peaks

subs = [str(x) for x in np.arange(3,31)]
subs.remove('4')
subs.remove('14')
subs.remove('25')

path = 'file_directory'

conditions = ['left_maze', 'right_maze', 'left_nomaze', 'right_nomaze']
pType = ['evoked']

chanNames = path + 'channel_names_egi.txt'
with open(chanNames, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    chans = list(chain.from_iterable((list(reader))))

sfreq = 1000

timeRange = [2549, 2850] # 50 ms to 350 ms
freqRange = [3, 12]

chanNo = len(chans)
subNo = len(subs)
condNo = len(conditions)
freqs = 50
samples = 5001
all_data = np.zeros(shape=(0, 10))

for condName in conditions:

    if condName == 'left_maze':
        condition = 'left'
        block = 'maze'
    elif condName == 'right_maze':
        condition = 'right'
        block = 'maze'
    elif condName == 'left_nomaze':
        condition = 'left'
        block = 'nomaze'
    elif condName == 'right_nomaze':
        condition = 'right'
        block = 'nomaze'

    for powtype in pType:

        s = 0
        if powtype == 'evoked':
            key = 'POW_evoked'
        else:
            key = 'POW_BASE_subj'

        for sub in subs:

            c = 0

            for chan in chans:

                file = path + '/tf/POW' + powtype + '_' + 'sub' + sub + '_' + condName + '_' + chan + '.mat'
                TFdata = np.squeeze(loadmat(file)[key])[0:freqs, :]

                maxFreq = np.unravel_index(TFdata[freqRange[0]:freqRange[1], time_range[0]:time_range[1]].argmax(),
                                           TFdata[freqRange[0]:freqRange[1], time_range[0]:time_range[1]].shape)[0] + lim[0]

                data = TFdata[freqRange[0]:freqRange[1], :]
                data = np.hstack((data, np.array([data[:, time_range[0]:time_range[1]].mean(axis=1)]).T))

                peakData = data[:, time_range[0]:time_range[1]]
                peakVal = np.zeros(shape=(0))
                peakSample = np.zeros(shape=(0))

                for freq in np.arange(0, 9, 1):

                    peakVal1 = np.max(peakData[freq, :])
                    peakSample1 = np.argmax(peakData[freq, :])

                    peakVal = np.hstack([peakVal, peakVal1])
                    peakSample = np.hstack([peakSample, peakSample1])

                data = np.hstack((data, np.array([peakVal]).T))
                data = np.hstack((data, np.array([peakSample + 51]).T)) # account for 50 ms start of the search window

                data = np.delete(data, range(0, samples), axis=1)

                data = np.hstack((data, np.squeeze(np.array(([np.repeat(condition, data.shape[0])],
                                                  [np.repeat(block, data.shape[0])],
                                                  [np.repeat(powtype, data.shape[0])],
                                                  [np.repeat(int(sub), data.shape[0])],
                                                  [np.arange(4, 13, 1)],
                                                  [np.repeat(chan, data.shape[0])],
                                                  [np.repeat(maxFreq+1, data.shape[0])]))).T))
                all_data = np.vstack((all_data, data))

allDat = pd.DataFrame(data=all_data,
                      index=np.array(range(1, len(all_data)+1)),
                      columns=np.array(['mean', 'peak', 'peakLatency', 'alley', 'block',
                                        'powerType', 'subject', 'frequency', 'channel', 'peakFreq']),
                      )

allDat = allDat.astype({'mean': float, 'peak': float, 'peakLatency': float, 'alley': str, 'block': str,
                        'powerType': str, 'subject': int, 'frequency': str, 'channel': str, 'peakFreq': int})

allDat.to_csv(path + '/tf/tfr_stats_alleys_evoked.csv', index=False)
