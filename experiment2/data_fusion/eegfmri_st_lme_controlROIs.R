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

# Plotting and summary tables
library(ggplot2)
library(viridis)
library(corrplot)
library(sjmisc)
library(sjPlot)
library(lavaan)
library(semPlot)
library(kableExtra)

setwd("file_directory")
eegfmri <- ldply("lme_df_controlROIs_evoked.txt", read.table, header = T, sep ='\t')

subs <- c(3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30)
alley <- c('right', 'left')

chans <- c(160)

model_df <- eegfmri

model_df_maze <- ddply(model_df[(model_df$block %in% c('maze')) 
                                & (model_df$channel %in% chans)
                                & (model_df$subject %in% subs)
                                & (model_df$trial_type %in% c(alley)) ,], 
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
                       precuneus = mean(precuneus)
)

model_df_nomaze <- ddply(model_df[(model_df$block %in% c('nomaze')) 
                                  & (model_df$channel %in% chans)
                                  & (model_df$subject %in% subs)
                                  & (model_df$trial_type %in% c(alley)) ,], 
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
                         precuneus = mean(precuneus)
)

model_df_maze$delta <- scale(model_df_maze$delta, center=TRUE, scale=FALSE)
model_df_maze$theta1 <- scale(model_df_maze$theta1, center=TRUE, scale=FALSE)
model_df_maze$theta2 <- scale(model_df_maze$theta2, center=TRUE, scale=FALSE)
model_df_maze$theta3 <- scale(model_df_maze$theta3, center=TRUE, scale=FALSE)
model_df_maze$alpha <- scale(model_df_maze$alpha, center=TRUE, scale=FALSE)

model_df_nomaze$delta <- scale(model_df_nomaze$delta, center=TRUE, scale=FALSE)
model_df_nomaze$theta1 <- scale(model_df_nomaze$theta1, center=TRUE, scale=FALSE)
model_df_nomaze$theta2 <- scale(model_df_nomaze$theta2, center=TRUE, scale=FALSE)
model_df_nomaze$theta3 <- scale(model_df_nomaze$theta3, center=TRUE, scale=FALSE)
model_df_nomaze$alpha <- scale(model_df_nomaze$alpha, center=TRUE, scale=FALSE)

m_precuneus <-  lmer(precuneus~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nm_precuneus <-  lmer(precuneus~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                   data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))

eegfmri <- ldply("final_hc.txt", read.table, header = T, sep ='\t')
model_df <- eegfmri

model_df_maze <- ddply(model_df[(model_df$block %in% c('maze')) 
                                & (model_df$channel %in% chans)
                                & (model_df$subject %in% subs)
                                & (model_df$trial_type %in% c(alley)) ,], 
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
                       heschl_r = mean(heschl_r),
                       heschl_l = mean(heschl_l)
)

model_df_nomaze <- ddply(model_df[(model_df$block %in% c('nomaze')) 
                                  & (model_df$channel %in% chans)
                                  & (model_df$subject %in% subs)
                                  & (model_df$trial_type %in% c(alley)) ,], 
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
                         heschl_r = mean(heschl_r),
                         heschl_l = mean(heschl_l)
)

model_df_maze$delta <- scale(model_df_maze$delta, center=TRUE, scale=FALSE)
model_df_maze$theta1 <- scale(model_df_maze$theta1, center=TRUE, scale=FALSE)
model_df_maze$theta2 <- scale(model_df_maze$theta2, center=TRUE, scale=FALSE)
model_df_maze$theta3 <- scale(model_df_maze$theta3, center=TRUE, scale=FALSE)
model_df_maze$alpha <- scale(model_df_maze$alpha, center=TRUE, scale=FALSE)

model_df_nomaze$delta <- scale(model_df_nomaze$delta, center=TRUE, scale=FALSE)
model_df_nomaze$theta1 <- scale(model_df_nomaze$theta1, center=TRUE, scale=FALSE)
model_df_nomaze$theta2 <- scale(model_df_nomaze$theta2, center=TRUE, scale=FALSE)
model_df_nomaze$theta3 <- scale(model_df_nomaze$theta3, center=TRUE, scale=FALSE)
model_df_nomaze$alpha <- scale(model_df_nomaze$alpha, center=TRUE, scale=FALSE)

m_heschl_r <-  lmer(heschl_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                    data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
m_heschl_l <-  lmer(heschl_l~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                    data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))

nm_heschl_r <-  lmer(heschl_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                     data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
nm_heschl_l <-  lmer(heschl_l~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                     data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))

tab_model(m_heschl_r, m_heschl_l, m_precuneus,
          p.adjust = 'fdr',
          title = 'Control ROIs, T-maze condition',
          digits = 3,
          digits.p = 3,
          show.intercept = FALSE,
          show.re.var = FALSE,
          show.r2 = FALSE,
          show.icc = FALSE,
          show.obs = FALSE,
          show.ngroups = FALSE,
          pred.labels = c('1-4 Hz','5-6 Hz', '7-8 Hz', '9-10 Hz', '11-12 Hz'),
          dv.labels = c('Left Heschl\'s Gyrus', 'Right Heschl\'s Gyrus', 'Precuneus')
)

tab_model(nm_heschl_r, nm_heschl_l, nm_precuneus,
          p.adjust = 'fdr',
          title = 'Control ROIs, No-maze condition',
          digits = 3,
          digits.p = 3,
          show.intercept = FALSE,
          show.re.var = FALSE,
          show.r2 = FALSE,
          show.icc = FALSE,
          show.obs = FALSE,
          show.ngroups = FALSE,
          pred.labels = c('1-4 Hz','5-6 Hz', '7-8 Hz', '9-10 Hz', '11-12 Hz'),
          dv.labels = c('Left Heschl\'s Gyrus', 'Right Heschl\'s Gyrus', 'Precuneus')
)
