%% Script for replicating phase analysis from Baker et al. (2013)
clear all
clc
close all

nb_subjects = 11;
nb_conditions = 2; % left is 1, right is 2
file_prefix = 'sub';
file_path = 'file_directory/export/';
All_Subject_Left_Right_Data8Hz = zeros(0,6);
allITC = zeros(0,200);
allAngleData = zeros(0,5); % first two set dimensions and rows, this will give you freq by row, time by columns
wins = {'pre', 'post'};
tlim = [-500, 1000];

file_suffix1 = '_left_tmaze_eeg64.mat'; % EEG
file_suffix2 = '_right_tmaze_eeg64.mat'; % EEG
%file_suffix1 = '_left_tmaze_meg.mat'; % MEG
%file_suffix2 = '_right_tmaze_meg.mat'; % MEG
method = 'EEG' %  Enter EEG or MEG

pnts = 1251; % EEG
%pnts = 3001; % MEG
srate = 250; % EEG
%srate = 600; % MEG
peakTime = 188; % EEG
%peakTime = 196; % MEG

montage = 'eeglab_directory/plugins/dipfit/standard_BESA/standard-10-5-cap385.elp'; % EEG
%montage = 'eeglab_directory/plugins/dipfit/standard_BESA/ctf_151.elp'; % MEG
montageLoadfile = {'file_directory/chan_loc_eeg64.ced' 'filetype' 'autodetect'}; % EEG
%montageLoadfile = {montage 'filetype' 'autodetect'}; % MEG
chan = {'PO8'}; % EEG

for win = 1:2

    for freq = [4, 6, 8, 10, 12]
        
        for subject=1:nb_subjects
            
            
            if method == 'MEG'
                if subject == 1 || subject == 8 || subject == 11
                    chan = {'MRO21-2511'};
                elseif subject == 2 || subject == 10
                    chan = {'MRO33-2511'};
                elseif subject == 3
                    chan = {'MRO22-2511'};
                elseif subject == 4 || subject ==5 || subject == 9
                    chan = {'MRO32-2511'};
                elseif subject == 6
                    chan = {'MZO01-2511'};  
                elseif subject == 7
                    chan = {'MLO21-2511'}; 
                end
            end
           
            %convolvedTime = [round(((393.3 - peakTime)/1286.6)*200), round(((393.3 + peakTime)/1286.6)*200)]; % MEG
            convolvedTime = [round(((372.3 - peakTime)/1244.6)*200), round(((372.3 + peakTime)/1244.6)*200)]; % EEG
            
            time = convolvedTime(win);

            subject_file = [file_prefix, int2str(subject)];
            subject_file_name_Seg1sleft = strcat(file_path, subject_file, file_suffix1);
            subject_file_name_Seg1sright = strcat(file_path, subject_file, file_suffix2);

            EEG = pop_importdata('dataformat','matlab','nbchan',0,'data',subject_file_name_Seg1sleft,'srate',srate,'pnts',pnts,'xmin',-2.5);
            EEG = pop_chanedit(EEG, 'lookup',montage,'load',montageLoadfile);
            EEG = pop_select( EEG,'channel',chan);
            EEG.data(1,:,:) = mean(EEG.data,1);
            figure; [all_ersp, all_itc, powbase, times, freqs, erspboot, itcboot, all_tfdata] = pop_newtimef(EEG, 1, 1, [tlim(1) tlim(2)], [0] ,'type', 'phasecoher', 'maxfreq', 40, 'nfreqs', 40, 'freqs', [1 40], 'elocs', EEG.chanlocs, 'chaninfo', EEG.chaninfo, 'padratio',2, 'plotersp','on','plotitc','on','plotphase','on','baseline',[NaN]);

            thetaphaseleft=squeeze(circ_mean(angle(all_tfdata(freq-1:freq,time,:)))); %6 = frequency, 121 time point, find this in freq and times
            thetaangleleft=thetaphaseleft*(180/pi);
            thetaangleleft(thetaangleleft<0)=thetaangleleft(thetaangleleft<0)+360;
            figure; rose(thetaphaseleft);
            title('left')
            sub6left=all_tfdata;
            
            allAngleData = vertcat(allAngleData, [repelem(subject, length(thetaphaseleft))', repelem(1, length(thetaphaseleft))', repelem(freq, length(thetaphaseleft))', repelem(win, length(thetaphaseleft))', thetaphaseleft]);

            if win == 2 && freq == 4
                allITC = vertcat(allITC, [all_itc, repelem(subject, size(all_itc,1))', repelem(1, size(all_itc,1))', [1:1:size(all_itc,1)]']);
            end
            
            EEG = pop_importdata('dataformat','matlab','nbchan',0,'data',subject_file_name_Seg1sright,'srate',srate,'pnts',pnts,'xmin',-2.5);
            EEG = pop_chanedit(EEG, 'lookup',montage,'load',montageLoadfile);
            EEG = pop_select( EEG,'channel',chan);
            EEG.data(1,:,:) = mean(EEG.data,1);
            figure; [all_ersp, all_itc, powbase, times, freqs, erspboot, itcboot, all_tfdata] = pop_newtimef(EEG ,1,1, [tlim(1) tlim(2)], [0] ,'type', 'phasecoher', 'maxfreq', 40, 'nfreqs', 40, 'freqs', [1 40], 'elocs', EEG.chanlocs, 'chaninfo', EEG.chaninfo, 'padratio',2, 'plotersp','on','plotitc','on','plotphase','on','baseline',[NaN]);

            thetaphaseright=squeeze(mean(angle(all_tfdata(freq-1:freq,time,:)),1));
            thetaangleright=thetaphaseright*(180/pi);
            thetaangleright(thetaangleright<0)=thetaangleright(thetaangleright<0)+360;
            figure; rose(thetaphaseright);
            title('right')
            sub6right=all_tfdata;
            
            allAngleData = vertcat(allAngleData, [repelem(subject, length(thetaphaseright))', repelem(2, length(thetaphaseright))', repelem(freq, length(thetaphaseright))', repelem(win, length(thetaphaseright))', thetaphaseright]);

            if win == 2 && freq == 4
                allITC = vertcat(allITC, [all_itc, repelem(subject, size(all_itc,1))', repelem(2, size(all_itc,1))', [1:size(all_itc,1)]']);
            end
            
            [uu, vv] = circle_mean(thetaangleleft);
            [ww, xx] = circle_mean(thetaangleright);

            % subject, alley, freq, pre vs. post, measure, value
            All_Subject_Left_Right_Data8Hz = vertcat(All_Subject_Left_Right_Data8Hz, [subject, 1, freq, win, 1, uu]);
            All_Subject_Left_Right_Data8Hz = vertcat(All_Subject_Left_Right_Data8Hz, [subject, 1, freq, win, 2, vv]);
            All_Subject_Left_Right_Data8Hz = vertcat(All_Subject_Left_Right_Data8Hz, [subject, 2, freq, win, 1, ww]);
            All_Subject_Left_Right_Data8Hz = vertcat(All_Subject_Left_Right_Data8Hz, [subject, 2, freq, win, 2, xx]);
            close all  
        end
    end
    end
    
if method == 'MEG'
    chan = {'poc'};
end

save(['circularMean_', method, '_', chan{:}, '.mat'], 'All_Subject_Left_Right_Data8Hz')
save(['phaseResults_', method, '_', chan{:}, '.mat'], 'allAngleData')
save(['itc_', method, '_', chan{:}, '.mat'], 'allITC')

%% circular ANOVA

All_Subject_Left_Right_Data8Hz = load('circularMean_MEG_poc.mat');
All_Subject_Left_Right_Data8Hz = All_Subject_Left_Right_Data8Hz.All_Subject_Left_Right_Data8Hz;
cond = All_Subject_Left_Right_Data8Hz(:,4) == 2 & All_Subject_Left_Right_Data8Hz(:,5) == 1 & (All_Subject_Left_Right_Data8Hz(:,3) <= 10 & All_Subject_Left_Right_Data8Hz(:,3) >= 8);
testData = All_Subject_Left_Right_Data8Hz(cond,:);

[anova, anovaTable] = circ_hktest(testData(:,6), testData(:,3), testData(:,2), 1, {'frequency', 'alley'});

%%

allITC = load('itc_MEG_poc.mat');
allITC = allITC.allITC;

cond = allITC(:,203) >= 7 & allITC(:,203) <= 10;
testData = allITC(cond,:);
condData = testData(:,[201, 202]);
left = zeros(11,200);
right = zeros(11,200);

for sub = 1:11
    left(sub,:) = mean(abs(testData(condData(:,2)==1 & abs(condData(:,1))==sub,1:200)));
    right(sub,:) = mean(abs(testData(condData(:,2)==2 & abs(condData(:,1))==sub,1:200)));
end

[maxValueLeft, maxIndLeft] = max(round(left(:,75:105),2),[],2);
[maxValueRight, maxIndRight] = max(round(right(:,75:105),2),[],2);

%maxIndLeft = ((maxIndLeft + 75)/200)*1244-372;
%maxIndRight = ((maxIndRight + 75)/200)*1244-372;

maxIndLeft = ((maxIndLeft + 75)/200)*1286.6-393.3;
maxIndRight = ((maxIndRight + 75)/200)*1286.6-393.3;

mean(maxIndLeft)
mean(maxIndRight)

std(maxIndLeft)
std(maxIndRight)

mean(maxValueLeft)
mean(maxValueRight)

std(maxValueLeft)
std(maxValueRight)

[P1,H,STATS1] = signrank(maxValueRight, maxValueLeft, 'tail', 'right', 'method', 'exact');
[P2,H,STATS2] = signrank(maxIndLeft, maxIndRight, 'tail', 'right', 'method', 'exact');
computeCohen_d(maxValueLeft, maxValueRight, 'paired')
computeCohen_d(maxIndLeft, maxIndRight, 'paired')

T = table([1:11, 1:11]', [maxValueLeft; maxValueRight], [maxIndLeft; maxIndRight], [repelem(1, 11), repelem(2, 11)]');
T.Properties.VariableNames = {'subject' 'itc_peak' 'itc_peakLatency' 'condition'};
writetable(T, 'itc_peakLat_meg.txt', 'Delimiter', 'tab');

[h,p,ci,stats] = ttest(maxValueRight, maxValueLeft);

anovaT = table(testData(:,1), testData(:,2), testData(:,3), testData(:,4));
anovaT.Properties.VariableNames = {'itc' 'subject' 'alley' 'frequency'};
anovaT.itc = abs(anovaT.itc);
writetable(anovaT, 'itc_anovaTable.txt', 'Delimiter', 'tab');
