%% Generate single subject event files from the aggregated E-Prime data

% Load the settings in the config.m file
config

% Read in raw E-Prime data
eprime = dataset('File',[rootDir 'behav/Tmaze_fMRI_allSubs.txt']);

% Iterate over the subjects
for subj = 1:size(subjs,2)
    
    sub = subjs{subj};
    
    % Create the destination directory if it doesn't exist
    eventDir = [rootDir 'subj/' sub '\data\events\'];
    [s,mess,messid] = mkdir(eventDir);
    
    if sub == '102'
        startTime = eprime.ScannerPulseWait_OffsetTime(eprime.Subject==subj);
        startTime = startTime(1);   
    elseif sub == '104'
        startTime = eprime.Trigger_RTTime(eprime.Subject==subj);
        startTime = startTime(2);   
    else
        % Iterate over the runs for each subject
        % First scan time, offset by the number of volumes dropped
        %startTime = eprime3.ScannerPulseWait_OffsetTime(eprime3.Subject==subj);
        startTime = eprime.Trigger_RTTime(eprime.Subject==subj);
        startTime = startTime(1);
    end
    
    % Define events
    names = cell(0);
    names{1} = 'mazeleftapple';
    names{2} = 'mazerightapple';
    names{3} = 'mazeleftorange';
    names{4} = 'mazerightorange';
    names{5} = 'nomazeleftapple';
    names{6} = 'nomazerightapple';
    names{7} = 'nomazeleftorange';
    names{8} = 'nomazerightorange';

    % Assign onset times for events
    onsets = cell(0);
    onsets{1} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('left_apple', eprime.outcomeImage) & strcmp('maze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;
    onsets{2} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('right_apple', eprime.outcomeImage) & strcmp('maze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;
    onsets{3} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('left_orange', eprime.outcomeImage) & strcmp('maze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;
    onsets{4} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('right_orange', eprime.outcomeImage) & strcmp('maze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;
    onsets{5} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('left_apple', eprime.outcomeImage) & strcmp('nomaze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;
    onsets{6} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('right_apple', eprime.outcomeImage) & strcmp('nomaze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;
    onsets{7} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('left_orange', eprime.outcomeImage) & strcmp('nomaze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;
    onsets{8} = (eprime.StartDisplay_OnsetTime(eprime.Subject==subj & strcmp('right_orange', eprime.outcomeImage) & strcmp('nomaze', eprime.blockType) & eprime.ChoiceDisplay_RT >= 100)-startTime) / 1000;

    % Set duration to 2 seconds
    durations = cell(0);
    durations{1} =2;
    durations{2} =2;
    durations{3} =2;
    durations{4} =2;
    durations{5} =2;
    durations{6} =2;
    durations{7} =2;
    durations{8} =2;

    % Save the event file in SPM8 format
    save([eventDir 'events_MazeRun_completeSample.mat'], 'names', 'onsets', 'durations');
end

%% Same for single trial BIDS format without artifact trials excluded from EEG

cd(rootDir)

config

artifacts = readmatrix('epochs/artifact_epochs.csv');

% Iterate over the subjects
for subj = 1:size(subjs,2)
    
    sub = string(subj);
    subST = subjs{subj};
    
    load(['/mri/subj/' subST '/data/events/events.mat'])
    
    events = zeros(0,2);
    for i = 1:8
        onset = onsets{:,i};
        name = repmat(i, length(onset), 1);
        events = vertcat(events, [onset, name]);
    end
    
    events = horzcat(events(:,1), repmat(2, size(events,1),1), repmat(0, size(events,1),1), events(:,2), repmat(0, size(events,1),1));
    
    eve = num2cell(events);
    eve(:,3) = {'Y'};

    for line = 1:size(eve,1)
        
        if eve{line,4} == 1
            eve{line,4} = 'mazeleft';
        elseif eve{line,4} == 2
            eve{line,4} = 'mazeright';
        elseif eve{line,4} == 3
            eve{line,4} = 'mazeleft';
        elseif eve{line,4} == 4
            eve{line,4} = 'mazeright';
        elseif eve{line,4} == 5
            eve{line,4} = 'nomazeleft';
        elseif eve{line,4} == 6
            eve{line,4} = 'nomazeright';
        elseif eve{line,4} == 7
            eve{line,4} = 'nomazeleft';
        elseif eve{line,4} == 8
            eve{line,4} = 'nomazeright';
        end
        
    end    
    
    T = cell2table(eve, 'VariableNames', {'onsets', 'duration', 'correct', 'trial_type', 'response_time'});
    T = sortrows(T, 'onsets');
    
    sub_artifacts = artifacts(artifacts(:,2)==str2double(sub));
    
    if length(sub_artifacts) > 0
        T(sub_artifacts,:) = [];
    end
    
    writetable(T, ['/sub-0' subST(2:end) '_task-tmaze_events.tsv'],'FileType', 'text', 'Delimiter', '\t')
end

%%

cd(rootDir)

config

% Iterate over the subjects
for subj = 1:size(subjs,2)
    
    subST = subjs{subj};
        
    file = strcat(['/mri/subj/' subST '/data/nifti/all/rp_aep2d_bold_TMaze_00001.txt']);
    events = readmatrix(file);
    
    T = array2table(events, 'VariableNames', {'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z'});
    writetable(T, ['/sub-0' subST(2:end) '_task-tmaze_desc-confounds_regressors.tsv'],'FileType', 'text', 'Delimiter', '\t')
end
