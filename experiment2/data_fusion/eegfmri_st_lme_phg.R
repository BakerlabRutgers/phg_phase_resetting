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

setwd("D:\\EEG_fMRI_tmaze\\")
eegfmri <- ldply("lme_df_phg_evoked.txt", read.table, header = T, sep ='\t')

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
                       beta = mean(c(thirteen_50250, fourteen_50250, fifteen_50250, 
                                     sixteen_50250, seventeen_50250, eighteen_50250, 
                                     nineteen_50250, twenty_50250, twenty.one_50250,
                                     twenty.two_50250, twenty.three_50250, twenty.four_50250,
                                     twenty.five_50250, twenty.six_50250, twenty.seven_50250,
                                     twenty.eight_50250, twenty.nine_50250)),
                       gamma = mean(c(thirty_50250, thirty.one_50250, thirty.two_50250, 
                                      thirty.three_50250, thirty.four_50250, thirty.five_50250,
                                      thirty.six_50250, thirty.seven_50250, thirty.eight_50250,
                                      thirty.nine_50250, forty_50250, forty.one_50250,
                                      thirty.two_50250, forty.three_50250, forty.four_50250,
                                      thirty.five_50250, forty.six_50250, forty.seven_50250,
                                      thirty.eight_50250, forty.nine_50250, fifty_50250)),
                       pphg1_r = mean(pphg1_r),
                       pphg1_l = mean(pphg1_l),
                       pphg2_r = mean(pphg2_r),
                       pphg2_l = mean(pphg2_l),
                       aphg1_r = mean(aphg1_r),
                       aphg1_l = mean(aphg1_l),
                       aphg2_r = mean(aphg2_r),
                       aphg2_l = mean(aphg2_l),
                       aphg3_r = mean(aphg3_r),
                       aphg3_l = mean(aphg3_l),
                       aphg4_r = mean(aphg4_r),
                       aphg4_l = mean(aphg4_l),                         
                       antPHG_r = mean(c(aphg1_r, aphg2_r, aphg3_r, aphg4_r)),
                       postPHG_r = mean(c(pphg1_r, pphg2_r))
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
                         beta = mean(c(thirteen_50250, fourteen_50250, fifteen_50250, 
                                       sixteen_50250, seventeen_50250, eighteen_50250, 
                                       nineteen_50250, twenty_50250, twenty.one_50250,
                                       twenty.two_50250, twenty.three_50250, twenty.four_50250,
                                       twenty.five_50250, twenty.six_50250, twenty.seven_50250,
                                       twenty.eight_50250, twenty.nine_50250)),
                         gamma = mean(c(thirty_50250, thirty.one_50250, thirty.two_50250, 
                                        thirty.three_50250, thirty.four_50250, thirty.five_50250,
                                        thirty.six_50250, thirty.seven_50250, thirty.eight_50250,
                                        thirty.nine_50250, forty_50250, forty.one_50250,
                                        thirty.two_50250, forty.three_50250, forty.four_50250,
                                        thirty.five_50250, forty.six_50250, forty.seven_50250,
                                        thirty.eight_50250, forty.nine_50250, fifty_50250)),
                         pphg1_r = mean(pphg1_r),
                         pphg1_l = mean(pphg1_l),
                         pphg2_r = mean(pphg2_r),
                         pphg2_l = mean(pphg2_l),
                         aphg1_r = mean(aphg1_r),
                         aphg1_l = mean(aphg1_l),
                         aphg2_r = mean(aphg2_r),
                         aphg2_l = mean(aphg2_l),
                         aphg3_r = mean(aphg3_r),
                         aphg3_l = mean(aphg3_l),
                         aphg4_r = mean(aphg4_r),
                         aphg4_l = mean(aphg4_l),
                         antPHG_r = mean(c(aphg1_r, aphg2_r, aphg3_r, aphg4_r)),
                         postPHG_r = mean(c(pphg1_r, pphg2_r))
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

maphg1_r <-  lmer(aphg1_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmaphg1_r <-  lmer(aphg1_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                   data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
maphg2_r <-  lmer(aphg2_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmaphg2_r <-  lmer(aphg2_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                   data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
maphg3_r <-  lmer(aphg3_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmaphg3_r <-  lmer(aphg3_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                   data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
maphg4_r <-  lmer(aphg4_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmaphg4_r <-  lmer(aphg4_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                   data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
mpphg1_r <-  lmer(pphg1_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmpphg1_r <-  lmer(pphg1_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                   data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
mpphg2_r <-  lmer(pphg2_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmpphg2_r <-  lmer(pphg2_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                   data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
mant_r <-  lmer(antPHG_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmant_r <-  lmer(antPHG_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                 data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))
mpost_r <-  lmer(postPHG_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                 data = model_df_maze, control = lmerControl(optimizer = "nmkbw"))
nmpost_r <-  lmer(postPHG_r~ delta + theta1 + theta2 + theta3 + alpha + (1|subject),
                  data = model_df_nomaze, control = lmerControl(optimizer = "nmkbw"))

p <- plot_models(maphg1_r, maphg2_r, maphg3_r, maphg4_r, mpphg1_r, mpphg2_r,
            show.p = T, p.threshold = 0.05, dot.size = 7, 
            line.size = 2, p.adjust = 'fdr',
            legend.title = NULL, show.values = F, p.shape = T, ci.lvl = .95, spacing = .7, std.est = TRUE,
            colors = c('#0696BA', '#D6D302', '#0618BA', '#9306BA', '#06BA08', '#BA0606'),
            legend.pval.title = 'p-value < 0.05', value.size = 6,
            axis.labels=c('11-12 Hz', '9-10 Hz',
                          '7-8 Hz','5-6 Hz', '1-4 Hz'),
            m.labels = c('APHG1', 'APHG2', 'APHG3', 'APHG4', 'PPHG1', 
                         'PPHG2', 'ns', '*p < .05')
            ) + 
  theme_classic(base_size = 40) +
  geom_hline(yintercept = 0, size=2) +
  geom_vline(xintercept = 1.5, size=1, linetype='dotted') +
  geom_vline(xintercept = 2.5, size=1, linetype='dotted') +
  geom_vline(xintercept = 3.5, size=1, linetype='dotted') +
  geom_vline(xintercept = 4.5, size=1, linetype='dotted') +
  ylim(c(-0.3, 0.3)) +
  theme( strip.background  = element_blank(),
         panel.grid.minor = element_blank(),
         panel.grid.major = element_blank(),
         axis.ticks = element_line(colour = "black"),
         axis.text = element_text(colour = "black"),
         strip.text = element_text(colour = "black"),
         panel.grid.minor.x=element_blank(),
         panel.grid.major.x=element_blank(),
         axis.ticks.y=element_blank(),
         axis.line.y=element_blank(),
         axis.title.y = element_text('beta weights'))

plot_models(nmaphg1_r, nmaphg2_r, nmaphg3_r, nmaphg4_r, nmpphg1_r, nmpphg2_r, show.p = T, p.threshold = 0.05, dot.size = 7, 
            line.size = 2, p.adjust = 'fdr',
            legend.title = NULL, show.values = F, p.shape = T, ci.lvl = .95, spacing = .7, std.est = TRUE,
            colors = c('#0696BA', '#D6D302', '#0618BA', '#9306BA', '#06BA08', '#BA0606'), 
            legend.pval.title = 'p-value < .05', value.size = 6,
            axis.labels=c('11-12 Hz', '9-10 Hz',
                          '7-8 Hz','5-6 Hz', '1-4 Hz'),
            m.labels = c('APHG1', 'APHG2', 'APHG3', 'APHG4', 'PPHG1', 
                         'PPHG2', 'ns', '*p < .05')) + 
  theme_classic(base_size = 40) +
  geom_hline(yintercept = 0, size=2) +
  geom_vline(xintercept = 1.5, size=1, linetype='dotted') +
  geom_vline(xintercept = 2.5, size=1, linetype='dotted') +
  geom_vline(xintercept = 3.5, size=1, linetype='dotted') +
  geom_vline(xintercept = 4.5, size=1, linetype='dotted') +
  ylim(c(-0.3,0.3)) +
  theme( strip.background  = element_blank(),
         panel.grid.minor = element_blank(),
         panel.grid.major = element_blank(),
         axis.ticks = element_line(colour = "black"),
         axis.text = element_text(colour = "black"),
         strip.text = element_text(colour = "black"),
         panel.grid.minor.x=element_blank(),
         panel.grid.major.x=element_blank(),
         axis.ticks.y=element_blank(),
         axis.line.y=element_blank(),
         axis.title.y = element_text('beta weights')
  )

tab_model(maphg1_r, maphg2_r, maphg3_r, maphg4_r, mpphg1_r, mpphg2_r, 
          p.adjust = 'fdr',
          title = 'Right PHG, T-maze condition',
          digits = 3,
          digits.p = 3,
          show.est = FALSE,
          show.intercept = FALSE,
          show.re.var = FALSE,
          show.r2 = FALSE,
          show.icc = FALSE,
          show.obs = FALSE,
          collapse.ci = TRUE,
          show.ngroups = FALSE,
          show.stat = TRUE,
          string.stat = 't',
          string.std = "Beta",
          show.std = TRUE,
          pred.labels = c('1-4 Hz','5-6 Hz', '7-8 Hz', '9-10 Hz', '11-12 Hz'),
          dv.labels = c('aPHG1', 'aPHG2', 'aPHG3', 'aPHG4', 'pPHG1', 'pPHG2')
)

tab_model(nmaphg1_r, nmaphg2_r, nmaphg3_r, nmaphg4_r, nmpphg1_r, nmpphg2_r, 
          p.adjust = 'fdr',
          title = 'Right PHG, No-maze condition',
          digits = 3,
          digits.p = 3,
          show.est = FALSE,
          show.intercept = FALSE,
          show.re.var = FALSE,
          show.r2 = FALSE,
          show.icc = FALSE,
          show.obs = FALSE,
          collapse.ci = TRUE,
          show.ngroups = FALSE,
          show.stat = TRUE,
          string.stat = 't',
          string.std = "Beta",
          show.std = TRUE,
          pred.labels = c('1-4 Hz','5-6 Hz', '7-8 Hz', '9-10 Hz', '11-12 Hz'),
          dv.labels = c('aPHG1', 'aPHG2', 'aPHG3', 'aPHG4', 'pPHG1', 'pPHG2')
)

plot_models(mant_r, mpost_r, show.p = T, p.threshold = 0.05, dot.size = 7, 
            line.size = 2, p.adjust = 'fdr',
            legend.title = NULL, show.values = F, p.shape = T, ci.lvl = .95, spacing = .7, std.est = NULL,
            colors = c('blue', 'purple'), 
            legend.pval.title = 'p-value < .05', value.size = 6,
            axis.labels=c('gamma (21-50 Hz)', 'beta (13-19 Hz)', 'theta (11-12 Hz)', 'theta (9-10 Hz)',
                          'theta (7-8 Hz)','theta (5-6 Hz)', 'delta (1-4 Hz)'),
            m.labels = c('APHG', 'PPHG','ns', '*p < .05')) + 
  theme_classic(base_size = 40) +
  geom_hline(yintercept = 0, size=2) +
  ylim(c(-0.3,0.3)) +
  theme( strip.background  = element_blank(),
         panel.grid.minor = element_blank(),
         panel.grid.major = element_blank(),
         axis.ticks = element_line(colour = "black"),
         axis.text = element_text(colour = "black"),
         strip.text = element_text(colour = "black"),
         panel.grid.minor.x=element_blank(),
         panel.grid.major.x=element_blank(),
         axis.title.y = element_text('beta weights')
  )

tab_model(mant_r, mpost_r, 
          p.adjust = 'fdr',
          title = 'Right PHG, Maze condition',
          pred.labels = c('intercept', 'delta (1-4 Hz)','theta (5-6 Hz)', 
                          'theta (7-8 Hz)', 'theta (9-10 Hz)', 
                          'theta (11-12 Hz)', 'beta (13-19 Hz)',
                          'gamma (21-50 Hz)')
)
