% Configuration file for T-maze fMRI data analysis

% SPM directory
spmDir = 'spm_directory';

% Root directory
rootDir = 'file_directory';

% List of subjects
subjs = {'103','105','106','107','108','109','110','111','112', '113', ...
         '115','116','117','118','119','120','121','122','123','124', ...
         '126','127','128','129','130'}; 

% The TR for the functionals in seconds
TR = 2;

% Number of volumes in each run
nTotalVols = 450;

% Number of volumes to drop from start of each run
nDropVols = 0;

% Number of used volumes in each run
nUsedVols = nTotalVols - nDropVols;
