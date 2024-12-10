clc
clear
close all

pathdata = 'file_directory/export/';
pathout='file_directory/tf/';
mkdir(pathout);

SRate = 1000;    % Sampling Rate
Freq = 1:60;  % Frequency range for the analysis

conlist={'_left_maze'; '_right_maze'; '_left_nomaze'; '_right_nomaze'};%%
chanList=textread(strcat(pathdata,'../channel_names_egi.txt'),'%s');
chanNum=256;
TIME=5001;

subs = [3 5 6 7 8 9 10 11 12 13 15 16 17 18 19 20 21 22 23 24 26 27 28 29 30];
channels = [160];

lim2 = [50 250];

bands = {'delta','delta','delta','delta','theta1','theta1','theta2','theta2',...
    'theta3','theta3','alpha','alpha','beta','beta','beta','beta','beta','beta',...
    'beta','beta','beta','beta','beta','beta','beta','beta','beta','beta','beta',...
    'beta','beta','beta','gamma','gamma','gamma','gamma','gamma','gamma','gamma',...
    'gamma','gamma','gamma','gamma','gamma','gamma','gamma','gamma','gamma','gamma','gamma'}';

headers = {'power50250' 'peak' 'peakSample' 'trial' 'frequency' 'band' 'condition' 'channel' 'block' 'subject'};
allDatEvoked = cell2table(cell(0,10));
allDatEvoked.Properties.VariableNames = headers;

allDatInduced = cell2table(cell(0,10));
allDatInduced.Properties.VariableNames = headers;

allDatTotal = cell2table(cell(0,10));
allDatTotal.Properties.VariableNames = headers;

for s = 1:length(subs)

    sub = int2str(subs(s));

    for ai=1:numel(conlist) 

         conName=conlist{ai};
         conName=['sub' sub conName];
         files=dir(strcat(pathdata,conName,'.mat'));

         if strcmp(conlist{ai}, '_left_maze')
             cond = 'left';
             block = 'maze';
         elseif strcmp(conlist{ai}, '_left_nomaze')
             cond = 'left';
             block = 'nomaze';
         elseif strcmp(conlist{ai}, '_right_maze')
             cond = 'right';
             block = 'maze';
         elseif strcmp(conlist{ai}, '_right_nomaze')
             cond = 'right';
             block = 'nomaze';
         end

         for ci=1:length(channels)

             chanNr = channels(ci);
             chanVariable=['E' int2str(chanNr)];
             disp(strcat('Start processing for Channel:',chanVariable));
             fName = files.name;
             tmp=load ([pathdata, files.name]);
             chanData=tmp.epochs;
             tmpchan=reshape(chanData(chanNr,:,:),[TIME,size(chanData,3)])';
             POW = zeros(60,TIME);
             POW_subj = zeros(size(tmpchan,1),60,TIME); 
             POW_BASE_subj = zeros(size(tmpchan,1),60,TIME);
             
             for k=1:size(tmpchan,1)
                  COEFS = cwt (tmpchan(k,:),SRate*1.5./Freq,'cmor1-1.5');
                  POW = abs (COEFS(:,1:TIME)).^2; 
                  POW_subj(k,:,:)=POW;
             end
             
             BASE = squeeze(mean(mean(POW_subj(:,:,2300:2500),1),3));
             BASE = repmat(BASE',1,TIME);

             disp(strcat('done for subject ',fName));
             
             for trial = 1:size(POW_BASE_subj,1)
                
                POW_BASE_subj(trial,:,:)=(squeeze(POW_subj(trial,:,:))-BASE)./BASE;
                POW_BASE_subj_trial=squeeze(POW_BASE_subj(trial,1:50,2500:3100));

                data = mean(POW_BASE_subj_trial(:,lim(1):lim(2)),2);
                data2 = mean(POW_BASE_subj_trial(:,lim2(1):lim2(2)),2);
                data3 = mean(POW_BASE_subj_trial(:,lim3(1):lim3(2)),2);
                data4 = mean(POW_BASE_subj_trial(:,lim4(1):lim4(2)),2);

                [peak, peakSample] = max(POW_BASE_subj_trial(:,1:600),[],2);
               
                tr = repmat(trial,length(data),1);
                fr = [1:50]';
                co = repmat({cond},length(data),1);
                chan = repmat(chanNr,length(data),1);
                bl = repmat({block},length(data),1); 
                subject = repmat(str2double(sub),length(data),1);
                
                t = table(data, data2, data3, data4, peak, peakSample, tr, fr, bands, co, chan, bl, subject);
                t.Properties.VariableNames = headers;

                allDatTotal = [allDatTotal; t];
             end

             POWtot = POW_BASE_subj;
             
             %%%%induced 
             disp(strcat('Start induced for Channel:',chanVariable));
             fName = files.name;
             tmp=load ([pathdata, files.name]);
             chanData=tmp.epochs;
             tmpchan=reshape(chanData(ci,:,:),[TIME,size(chanData,3)])';
             theMean = mean(tmpchan, 1);
             POW = zeros(60,TIME);
             POW_subj=zeros(size(tmpchan,1),60,TIME); 
             POW_BASE_subj = zeros(size(tmpchan,1),60,TIME);

             for trial = 1:size(tmpchan,1)
                 % Subtract the mean from the data to remove evoked
                 % activity and get the continuous wavelet transform for
                 % each trial
                 inducedC3(trial,:) = tmpchan(trial,:) - theMean; 
                 COEFS = cwt(inducedC3(trial,:), SRate*1.5./Freq, 'cmor1-1.5');
                 % Collect the transforms in POW_subj
                 POW = abs(COEFS(:,1:TIME)).^2; 
                 POW_subj(trial,:,:)=POW;
             end
             
             BASE=squeeze(mean(mean(POW_subj(:,:,2300:2500),1),3)); 
             BASE=repmat(BASE',1,TIME);
             
             disp(strcat('done for suject',fName));

             for trial = 1:size(POW_BASE_subj,1)
                
                POW_BASE_subj(trial,:,:)=(squeeze(POW_subj(trial,:,:))-BASE)./BASE;
                POW_BASE_subj_trial=squeeze(POW_BASE_subj(trial,1:50,2500:3100));

                data = mean(POW_BASE_subj_trial(:,lim(1):lim(2)),2);
                data2 = mean(POW_BASE_subj_trial(:,lim2(1):lim2(2)),2);
                data3 = mean(POW_BASE_subj_trial(:,lim3(1):lim3(2)),2);
                data4 = mean(POW_BASE_subj_trial(:,lim4(1):lim4(2)),2);

                [peak, peakSample] = max(POW_BASE_subj_trial(:,1:600),[],2);
               
                tr = repmat(trial,length(data),1);
                fr = [1:50]';
                co = repmat({cond},length(data),1);
                chan = repmat(ci,length(data),1);
                bl = repmat({block},length(data),1); 
                subject = repmat(str2double(sub),length(data),1);
                
                t = table(data, data2, data3, data4, peak, peakSample, tr, fr, bands, co, chan, bl, subject);
                t.Properties.VariableNames = headers;

                allDatInduced = [allDatInduced; t];
             end 
             
             POWind = POW_BASE_subj;
             POW_evoked = POWtot-POWind;
             
             for trial = 1:size(POW_evoked,1)
                
                POW_evoked_trial=squeeze(POW_evoked(trial,1:50,2500:3100));

                data = mean(POW_evoked_trial(:,lim(1):lim(2)),2);
                data2 = mean(POW_evoked_trial(:,lim2(1):lim2(2)),2);
                data3 = mean(POW_evoked_trial(:,lim3(1):lim3(2)),2);
                data4 = mean(POW_evoked_trial(:,lim4(1):lim4(2)),2);

                [peak, peakSample] = max(POW_evoked_trial(:,1:600),[],2);
                
                tr = repmat(trial,length(data),1);
                fr = [1:50]';
                co = repmat({cond},length(data),1);
                chan = repmat(chanNr,length(data),1);
                bl = repmat({block},length(data),1); 
                subject = repmat(str2double(sub),length(data),1);
                
                t = table(data, data2, data3, data4, peak, peakSample, tr, fr, bands, co, chan, bl, subject);
                t.Properties.VariableNames = headers;

             end
         end
    end
end  

writetable(allDatEvoked, [pathout 'tf_singleTrials_evoked.txt'], 'Delimiter', 'tab')
writetable(allDatInduced, [pathout 'tf_singleTrials_induced.txt'], 'Delimiter', 'tab')
writetable(allDatTotal, [pathout 'tf_singleTrials_total.txt'], 'Delimiter', 'tab')
