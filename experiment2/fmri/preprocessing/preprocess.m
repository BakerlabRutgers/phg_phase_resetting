%% Script for automating preprocessing of multiple subjects using a template batch job.

% Load the config file
config

% Set the full path to the template batch script
jobFile = {[rootDir 'batch/preprocess_job.m']};

% Set the number of runs of the batch to be the number of subjects we are processing
nSubjs = length(subjs);

% Set the list of jobs to be our single subject job repeated for each subject
jobs = repmat(jobFile, 1, nSubjs);

% Create a 2D cell array to hold the subject-specific values for each field
% There is one row for each field we need to fill in, and 1 column for each subject
inputs = cell(7, nSubjs);

% For each subject, fill in our cell-array with the appropriate values for each field.
% List of open inputs
% Change Directory: Directory - cfg_files
% Slice Timing: Session - cfg_files
% Slice Timing: Session - cfg_files
% Slice Timing: Session - cfg_files
% Coreg: Estimate: Reference Image - cfg_files
% Segment: Data - cfg_files
% Segment: Tissue probability maps - cfg_files
% Check Registration: Images to Display - cfg_files
% Check Registration: Images to Display - cfg_files

for iSubj = 1:nSubjs
    % Set the path for this particular subject
    subjDir = [rootDir 'subj/' subjs{iSubj} '/data/nifti/all/'];
    
    % Directory with NIfTI files 
    inputs{1, iSubj} = cellstr(subjDir);

    % Due to timing issues, some subjects had different amounts of total volumes
    if subjs{iSubj}=='102'
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
    
    % Cell array holding the full paths of each raw functional image
    inputs{2, iSubj} = cellstr(strcat(subjDir, 'ep2d_bold_TMaze_0000', strtrim(cellstr(num2str((1:9)'))), '.nii'));
    inputs{2, iSubj} = vertcat(inputs{2, iSubj}, cellstr(strcat(subjDir, 'ep2d_bold_TMaze_000', strtrim(cellstr(num2str((10:99)'))), '.nii')));
    inputs{2, iSubj} = vertcat(inputs{2, iSubj}, cellstr(strcat(subjDir, 'ep2d_bold_TMaze_00', strtrim(cellstr(num2str((100:nUsedVols)'))), '.nii')));

    % Subject 12 did not have a T1, so the mean of all functional images was chosen as a replacement
    % and subjects 105, 111, and 119 had faulty alignments with the T1 that worked better with the mean functional image
    if any(strcmp(subjs{iSubj}, {'105', '111', '112', '119'}))
        inputs{3, iSubj} = cellstr([rootDir 'subj\' subjs{iSubj} '\data\nifti\all\meanaep2d_bold_TMaze_00001.nii']);
        inputs{4, iSubj} = cellstr([rootDir 'subj\' subjs{iSubj} '\data\nifti\all\meanaep2d_bold_TMaze_00001.nii']);
    else
        % The hi-res structural
        inputs{3, iSubj} = cellstr([rootDir 'subj\' subjs{iSubj} '\data\nifti\all\s_HiRes.nii']);
        % The hi-res structural
        inputs{4, iSubj} = cellstr([rootDir 'subj\' subjs{iSubj} '\data\nifti\all\s_HiRes.nii']);
    end

    % Cell array holding tissue probability maps
    inputs{5, iSubj} = cellstr(strcat(spmDir, {'tpm\grey.nii'; 'tpm\white.nii'; 'tpm\csf.nii'}));
    
	% Cell array holding the full paths of segmentation results
    inputs{6, iSubj} = cellstr(strcat(subjDir, {'s_HiRes.nii'; 'c1s_HiRes.nii'; 'c2s_HiRes.nii'; 'c3s_HiRes.nii'}));

    % Cell array holding the full paths of normalized images and template for comparison
    inputs{7, iSubj} = cellstr([strcat(subjDir, {'wms_HiRes.nii'; 'wmeanaf_bold_TMaze_00001.nii'}); [spmDir 'templates\T1.nii']]);
end

% Tell spm to configure itself for running in batch mode
spm('defaults', 'FMRI');

% Open the spm windows so that it will display and save the realignment and
% normalisation summaries.
spm('FMRI');

% Run our batch jobs!
% We do this by giving the job manager (jobman) our list of jobs (one for
% each subject) and our cell array of subject-specific values that are
% missing from the job template.
for sub = 1:nSubjs  
    spm_jobman('serial', jobs{:,sub}, '', inputs{:,sub});
end

% Set the current directory back to batch
cd([rootDir 'batch']);
