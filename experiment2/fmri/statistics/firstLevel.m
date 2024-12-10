%% Script for first level analysis of Maze study

% Load the config file
config

% Set the full path to the template batch script
jobFile = {[rootDir 'batch/firstLevel_job.m']};

% Set the number of runs of the batch to be the number of subjects we are processing
%nSubjs = length(subjs);
nSubjs = length(subjs);

% Set the list of jobs to be our single subject job repeated for each subject
jobs = repmat(jobFile, 1, nSubjs);

% Create a 2D cell array to hold the subject-specific values for each field
% There is one row for each field we need to fill in, and 1 column for each subject
inputs = cell(5, nSubjs);

% For each subject, fill in our cell-array with the appropriate values for each field.
% List of open inputs
% Change Directory: Directory - cfg_files
% fMRI model specification: Directory - cfg_files
% fMRI model specification: Scans - cfg_files
% fMRI model specification: Multiple conditions - cfg_files
% fMRI model specification: Multiple regressors - cfg_files
% fMRI model specification: Scans - cfg_files
% fMRI model specification: Multiple conditions - cfg_files
% fMRI model specification: Multiple regressors - cfg_files
% fMRI model specification: Scans - cfg_files
% fMRI model specification: Multiple conditions - cfg_files
% fMRI model specification: Multiple regressors - cfg_files
for iSubj = 1:nSubjs
    
    % Set the paths for this particular subject
    subjDir = [rootDir 'subj/' subjs{iSubj} '/'];
    niftiDir = [subjDir 'data/nifti/all/'];
    eventsDir = [subjDir 'data/events/'];   
    modelDir = [rootDir 'subj/' subjs{iSubj} '/results/modelFiltered/'];
    
    % Create the model directory if it doesn't exist
    [s,mess,messid] = mkdir(modelDir);
    
    % Directory for model files
    inputs{1, iSubj} = cellstr(modelDir);
    inputs{2, iSubj} = cellstr(modelDir);
   
    if subjs{iSubj}=='101'
        nUsedVols=420;
    elseif subjs{iSubj}=='102'
        nUsedVols=274;
    elseif subjs{iSubj}=='101'
        nUsedVols=420;
    elseif subjs{iSubj}=='103'
        nUsedVols=480;
    elseif subjs{iSubj}=='104'
        nUsedVols=480;
    elseif subjs{iSubj}=='105'
        nUsedVols=447;
    else
        nUsedVols=450;
    end

    inputs{3, iSubj} = cellstr(strcat(niftiDir, 'swraep2d_bold_TMaze_0000', strtrim(cellstr(num2str((1:9)'))), '.nii'));
    inputs{3, iSubj} = vertcat(inputs{3, iSubj}, cellstr(strcat(niftiDir, 'swraep2d_bold_TMaze_000', strtrim(cellstr(num2str((10:99)'))), '.nii')));
    inputs{3, iSubj} = vertcat(inputs{3, iSubj}, cellstr(strcat(niftiDir, 'swraep2d_bold_TMaze_00', strtrim(cellstr(num2str((100:nUsedVols)'))), '.nii')));
    inputs{4, iSubj} = cellstr([eventsDir 'events_MazeRun_completeSample.mat']);
    inputs{5, iSubj} = cellstr([[subjDir 'data/nifti/all/'], 'rp_aep2d_bold_TMaze_00001.txt']);

end

% Tell spm to configure itself for running in batch mode
spm('defaults', 'FMRI');

% Open the spm windows so that it will display and save the realignment and
% normalisation summaries.
spm('FMRI');

% Run our batch jobs!jobs
% We do this by giving the job manager (jobman) our list of jobs (one for
% each subject) and our cell array of subject-specific values that are
% missing from the job template.
spm_jobman('serial', jobs, '', inputs{:});

% Set the current directory back to batch
cd([rootDir 'batch']);
