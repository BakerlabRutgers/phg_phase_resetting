import mne
import numpy as np
import pandas as pd

path = 'file_directory'
subs = [str(x) for x in np.append(3, np.arange(5,31))]
all_artifacts = np.zeros(shape=(0, 2))

for sub in subs:
    epochs = mne.read_epochs(path + '/epochs/sub' + sub + '_tf-epo.fif', preload=True)
    drop_log = np.array(epochs.drop_log)
    artifact_epochs = np.array([i+1 for i, x in enumerate(drop_log) if (x != ('IGNORED',)) & (len(x) > 0)])
    artifact_epochs = np.vstack([artifact_epochs, np.repeat(int(sub),len(artifact_epochs))])
    all_artifacts = np.vstack([all_artifacts, artifact_epochs.T])

all_artifacts = pd.DataFrame(data=all_artifacts,
                             index=np.array(range(1, len(all_artifacts)+1)),
                             columns=np.array(['epoch', 'subject']))

all_artifacts = all_artifacts.astype({'epoch': int, 'subject': int})
all_artifacts.to_csv(path + '/epochs/artifact_epochs.csv', index=False)
