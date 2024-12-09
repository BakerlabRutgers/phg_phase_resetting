## Script for extracting time series values from ROIs and atlases
################ Glasser with left and right split

import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker
from nilearn.input_data import NiftiMasker

import numpy as np
import pandas as pd

from itertools import chain
import csv

glasser = '/glasser_directory/HCP-MMP1_on_MNI152_ICBM2009a_nlin.nii.gz'
Glasserlabels = '/glasser_directory/HCP-MMP1_on_MNI152_ICBM2009a_nlin.txt'

with open(Glasserlabels, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    labelsList = list(chain.from_iterable((list(reader))))

GlasserMasker = NiftiLabelsMasker(labels_img=glasser, standardize=False,
                                    memory='nilearn_cache', verbose=0)

path = 'file_directory'
subs = [str(x) for x in np.arange(3,31)]
subs.remove('4')
subs.remove('14')
subs.remove('25')
conditions = ['mazeleft', 'mazeright', 'nomazeleft', 'nomazeright']

for cond in conditions:

    ts_allsubs = np.zeros(shape=(0, 6))

    for sub in subs:

        functional = path + 'nibetaseries/sub-0' + sub + '/func/sub-0' + sub + '_task-tmaze_space-MNI152NLin2009cAsym_desc-' + cond + '_betaseries.nii.gz'
        img = nib.load(functional)

        data = GlasserMasker.fit_transform(img)

        trials = data.shape[0]

        if cond == 'mazeleft':
            alley = 'left'
            block = 'maze'
        elif cond == 'mazeright':
            alley = 'right'
            block = 'maze'
        elif cond == 'nomazeleft':
            alley = 'left'
            block = 'nomaze'
        elif cond == 'nomazeright':
            alley = 'right'
            block = 'nomaze'

        for roi in range(0,len(labelsList)):

            label = labelsList[roi]
            region = data[:,roi]

            for trial in range(0, trials):

                epoch = region[trial]
                line = np.array([epoch, trial+1, alley, label, block, sub])
                ts_allsubs = np.vstack((ts_allsubs, line))

    allDat = pd.DataFrame(data=ts_allsubs,
                          index=np.array(range(1, len(ts_allsubs)+1)),
                          columns=np.array(['beta', 'trials', 'trial_type', 'roi', 'block', 'subject'])
                          )

    allDat = allDat.astype({'beta': float, 'trials': float, 'trial_type': str, 'roi': str, 'block': str, 'subject': int})
    allDat.to_csv(path + '/beta_glasser_alleys_' + cond + '.csv', index=False)
