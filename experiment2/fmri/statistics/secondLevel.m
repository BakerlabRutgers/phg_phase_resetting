%% Script for second level analysis of Maze study

% Load the config file
config

% Set the full path to the template batch script
jobFile = {[rootDir 'batch/secondLevel_job.m']};

% A list of contrasts to test. Each row should list the contrast
% file name and a descriptive name.
cons = {'con_0001', 'Maze-Nomaze';
        'con_0002', 'Maze_Reward-Noreward';
        'con_0003', 'Maze_NoReward-Reward';
        'con_0004', 'Maze_Right-Left';
        'con_0005', 'Maze_Left-Right';
        'con_0006', 'Nomaze_Reward-Noreward';
        'con_0007', 'Nomaze_NoReward-Reward';
        'con_0008', 'NoMaze_Right-Left';
        'con_0009', 'NoMaze_Left-Right';
        'con_0010', 'MazeRight-NomazeRight';
        'con_0011', 'MazeLeft-NomazeLeft';
        'con_0012', 'Reward-NoReward';
        'con_0013', 'NoReward-Reward'};

% Set the number of runs of the batch to be the number of subjects we are processing
nCons = size(cons, 1);

% Set the list of jobs to be our job repeated for each contrast
jobs = repmat(jobFile, 1, nCons);

% Create a 2D cell array to hold the job-specific values for each field
% There is one row for each field we need to fill in, and 1 column for each job
inputs = cell(5, nCons);

% For each subject, fill in our cell-array with the appropriate values for each field.
% List of open inputs
% Change Directory: Directory - cfg_files
% Factorial design specification: Directory - cfg_files
% Factorial design specification: Scans - cfg_files
% Contrast Manager: Name - cfg_entry
for iCon = 1:nCons
    % Set the paths for this particular contrast
    conDir = [rootDir 'results/contrastsTime/' cons{iCon, 2} '/'];
 
    % Create the directory if it doesn't exist
    [s,mess,messid] = mkdir(conDir);
    
    % Directory for contrast files
    inputs{1, iCon} = cellstr(conDir);
    inputs{2, iCon} = cellstr(conDir);

    % Contrast files for all subjects
    inputs{3, iCon} = cellstr(strcat(rootDir, 'subj/', subjs', '/results/modelTime/', cons{iCon, 1}, '.img'));

    % Name for upper tail contrast
    inputs{4, iCon} = cons{iCon, 2};   

    % Name for lower tail of contrast
    inputs{5, iCon} = ['-[' cons{iCon, 2} ']'];   

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
spm_jobman('serial', jobs, '', inputs{:});

% Set the current directory back to batch
cd([rootDir 'batch']);
