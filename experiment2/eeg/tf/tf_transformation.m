%% Time-Frequency Analaysis for t-maze experiments

clc
clear
close all

pathdata = 'file_directory/export/';
pathout='file_directory/tf/';
mkdir(pathout);

SRate = 1000;    % Sampling Rate
Freq = 1:60;  % Frequency range for the analysis

chanList = textread('D:\EEG_fMRI_tmaze\EEG\channel_names_egi.txt','%s');
chanNum=256; 
TIME = 5001;

conlist = {'_left_maze'; '_right_maze'; '_left_nomaze'; '_right_nomaze'};
subs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30];

for s = 1:length(subs)

    sub = int2str(subs(s));
    
    for ai=1:numel(conlist)
    
        conName=conlist{ai};
        conName=['sub' sub '_' conName];
        files=dir(strcat(pathdata,conName,'.mat'));
        
        for ci=1:chanNum
                      
        		chanVariable=chanList{ci}; % change channel names when switching between EEG and MEG
        		POW_subj=zeros(1,60,TIME); %subject, frequency, data points
        		POW_BASE_subj = zeros(1,60,TIME);
        	  
        		disp(strcat('Start processing for Channel:',chanVariable));
        		  
        		fName = files(1).name;
        		tmp=load ([pathdata, files(fi).name]);
        		chanData=tmp.epochs;
        		chanVariable=chanListeeg64{ci};
        		tmpchan=reshape(chanData(ci,:,:),[TIME,size(chanData,3)])';
        		POW = zeros(60,TIME);% freq, data points
        	  
        		for k=1:size(tmpchan,1)
          			COEFS = cwt (tmpchan(k,:),SRate*1.5./Freq,'cmor1-1.5');
          			POW = POW + abs (COEFS(:,1:TIME)).^2; 
        		end
        	  
        		POW_subj(1,:,:)=POW;          
        	  
        		BASE=squeeze(mean(POW_subj(1,:,2300:2400),3)); %size of baseline -200--100 
        		BASE=repmat(BASE',1,TIME);
        		POW_BASE_subj(1,:,:)=(squeeze(POW_subj(1,:,:))-BASE)./BASE;  
        		
        		disp(strcat('done for suject',fName));
        		
        		save([pathout 'POWtotal_', conName, '_',chanVariable,'.mat'], 'POW_BASE_subj') % save complex data
        		POWtot = POW_BASE_subj;
        		
        		%%%%induced 
        		disp(strcat('Start induced for Channel:',chanVariable));
        		POW_subj=zeros(1,60,TIME); % subject, frequency, data points
        		POW_BASE_subj = zeros(1,60,TIME);

          
          	fName = files(1).name;
          	tmp=load ([pathdata, files(1).name]);
          	chanData=tmp.epochs;
          	tmpchan=reshape(chanData(ci,:,:),[TIME,size(chanData,3)])';
          
          	theMean = mean(tmpchan, 1);
          	POW = zeros(60,TIME); % freq, data points-same as above
          	
          	for k = 1:size(tmpchan,1)
            		inducedC3(k,:) = tmpchan(k,:) - theMean; 
            		COEFS = cwt(inducedC3(k,:), SRate*1.5./Freq, 'cmor1-1.5');
            		POW = POW + abs(COEFS(:,1:TIME)).^2; 
          	end
	
          	POW_subj(1,:,:)=POW;
          
          	BASE=squeeze(mean(POW_subj(1,:,2300:2400),3)); %size of baseline -200--100
          	BASE=repmat(BASE',1,TIME);
          	POW_BASE_subj(1,:,:)=(squeeze(POW_subj(1,:,:))-BASE)./BASE;
          
          	disp(strcat('done for suject',fName));
    
            save([pathout 'POWinduced_', conName, '_',chanVariable,'.mat'], 'POW_BASE_subj') % save complex data
            
            POWind = POW_BASE_subj;
            POW_evoked = POWtot-POWind;
            
            save([pathout 'POWevoked_', conName, '_',chanVariable,'.mat'], 'POW_evoked'); % save complex data

        end  %%%for each channel

    end %%for each list
    
end  %%for each subject
