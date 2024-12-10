# Data management
library(plyr)
library(gdata)
library(dplyr)
library(tidyr)
library(reshape2)
library(xfun)
library(hash)

# Stats
library(car)
library(lme4)
library(effects)
library(psych)
library(GPArotation)
library(modelsummary)

eegfmri <- ldply("lme_df_glasser_evoked.txt", read.table, header = T, sep ='\t')

glasser_results <- data.frame(matrix(ncol = 15, nrow = 0))
colnames(glasser_results) <- c('roi', 'delta', 'theta1', 'theta2', 'theta3', 
                               'alpha', 'beta', 'gamma', 'delta.p', 'theta1.p', 
                              'theta2.p', 'theta3.p', 'alpha.p', 'beta.p', 'gamma.p')

rois <- c(5:364)
chans <- c(160)
blocks <- c('maze')

eegcols <- c(paste(numbers_to_words(c(1:50)), '50250', sep="_"), 'peakTheta_50250', 'peakThetaFrequ_50250')

for (roi in rois) {
  
  roi_label <- colnames(eegfmri)[roi]
  eegfmri_roi <- eegfmri[,c(1:4, roi, 365:417)]
  colnames(eegfmri_roi) <- c(c('trials', 'trial_type', 'block', 'subject', 'target_roi'), 'channel', eegcols)
  
  model_df <- ddply(eegfmri_roi[(eegfmri_roi$block %in% blocks)) 
                                & (eegfmri_roi$channel %in% chans) 
                                & (eegfmri_roi$trial_type %in% c('right','left')) ,], 
                    c('subject', 'trials'), summarise,
                    delta = mean(c(one_50250, two_50250, three_50250, four_50250)),
                    theta1 = mean(c(five_50250, six_50250)),
                    theta2 = mean(c(seven_50250, eight_50250)),
                    theta3 = mean(c(nine_50250, ten_50250)),
                    peakTheta = mean(peakTheta_50250),
                    theta = mean(c(four_50250, five_50250, six_50250, seven_50250, eight_50250)),
                    animalTheta = mean(c(four_50250, five_50250, six_50250, seven_50250, eight_50250, nine_50250, ten_50250, eleven_50250, twelve_50250)),
                    alpha = mean(c(eleven_50250, twelve_50250)),
                    beta = mean(thirteen_50250),
                    gamma = mean(thirty_50250),
                    target_roi = mean(target_roi)
  )
  
  model <- lmerTest::lmer(target_roi ~ delta + theta1 + theta2 + theta3 + alpha + beta + gamma + (1|subject),
                          data = model_df)
  weights <- coef(summary(model))[ , "Estimate"]
  weights <- weights[2:8]
  
  p.values <- coef(summary(model))[ , "Pr(>|t|)"]
  p.values <- p.values[2:8]
  
  glasser_results[nrow(glasser_results) + 1,] = c(roi_label, weights, p.values)
  
}

write.table(glasser_results, file = "glasser_results_maze.txt", sep = "\t", dec = ".", row.names = FALSE)
