### Set working directory and load all the necessary libraries

# Data management
library(plyr)
library(gdata)
library(dplyr)
library(tidyr)
library(reshape2)
library(xfun)
library(hash)

setwd("file_directory")

#### Collect all the data arrays
############################################################################################

# Single rois for cingulate and PHC
df1 <- ldply('/mri/beta_glasser_mazeleft.csv', read.table, header = T, sep =',')
df2 <- ldply('/mri/beta_glasser_mazeright.csv', read.table, header = T, sep =',')
df3 <- ldply('/mri/beta_glasser_nomazeleft.csv', read.table, header = T, sep =',')
df4 <- ldply('/mri/beta_glasser_nomazeright.csv', read.table, header = T, sep =',')
beta_glasser_st <- rbind(df1, df2, df3, df4)

## EEG time frequency measures, single trial and average values
############################################################################################

# Single evoked trials for a selection of channels
evoked_st <- ldply('/EEG/tf/tf_singleTrials_evoked_rpt.txt', read.table, header = T, sep ='\t')

## Now let's create multimodal data frames
############################################################################################

rois <- unique(beta_glasser_st$roi)
channels <- c(160)
frequs <- c(unique(evoked_st$frequency), c('peakTheta', 'peakThetaFrequ'))
bands <- levels(unique(evoked_st$band))
conditions <- c('left', 'right')
blocks <- c('maze', 'nomaze')
subs <- unique(evoked_st$subject)

eegcols <- c(paste(numbers_to_words(c(1:50)), '50250', sep="_"), 'peakTheta_50250', 'peakThetaFrequ_50250')

eegfmri <- data.frame(matrix(ncol = 417, nrow = 0))
colnames(eegfmri) <- c(c('trials', 'trial_type', 'block', 'subject'), rois, 'channel', eegcols)

for (chan in channels) {
  for (bl in blocks)
  {
    for (cond in conditions)
    {
      for (sub in subs)
      {
        
        df1 <- ddply(evoked_st[(evoked_st$block == bl) 
                        & (evoked_st$channel == chan) 
                        & (evoked_st$condition == cond)
                        & (evoked_st$subject == sub),], c('trial', 'channel', 'frequency'), summarise, 
                        P = mean(power50250))
       
        df1$P <- scale(df1$P)
        df1 <- spread(df1, frequency, P)
        dfTheta <- df1[,c(6:14)]
        peakFrequ <- which.max(colMeans(dfTheta))
        if (peakFrequ == 1){
          df1$peakTheta <- rowMeans(dfTheta[,c(peakFrequ,peakFrequ+1)])
        } else if (peakFrequ == 12) {
          df1$peakTheta <- rowMeans(dfTheta[,c(peakFrequ-1,peakFrequ)])
        } else {
          df1$peakTheta <- rowMeans(dfTheta[,peakFrequ-1:peakFrequ+1])
        }     
        df1$peakThetaFrequ <- rep(names(peakFrequ), length(df1$peakTheta))
        
        df2 <- beta_glasser_st[(beta_glasser_st$block==bl)
                              & (beta_glasser_st$trial_type==cond)
                              & (beta_glasser_st$subject == sub),]
        df2$beta <- scale(df2$beta)
        df2 <- spread(df2, roi, beta)
        
        rownames(df1) <- NULL
        rownames(df2) <- NULL
        
        df1 <- df1[-c(1)]
        df3 <- data.frame(cbind(df2, df1))
        eegfmri <- rbind(eegfmri, df3)
        
      }
    }
  }
}

colnames(eegfmri) <- c(c('trials', 'trial_type', 'block', 'subject'), rois, 'channel', eegcols)
write.table(eegfmri, file = "lme_df_glasser_evoked.txt", sep = "\t", dec = ".", row.names = FALSE)
