library(kableExtra)
library(plyr)

setwd('file_directory')

table <- ldply('/glasser_results_maze_mc.txt', read.table, header = T, sep ='\t')
sig_regions <- table[(table$theta1.p < 0.05) | (table$theta2.p < 0.05), 'roi']

table <- table[(table$roi %in% sig_regions),]
table <- table[-c(12, 13, 14, 15),]
sig_regions <- sig_regions[-c(12, 13, 14, 15)]

estimates <- data.frame(t(table[c('delta', 'theta1', 'theta2', 'theta3', 'alpha')]))
colnames(estimates) <- 'Esimtaes'
pvals <- data.frame(t(table[c('delta.p', 'theta1.p', 'theta2.p', 'theta3.p', 'alpha.p')]))
colnames(pvals) <- 'p'
tvals <- data.frame(t(table[c('delta.t', 'theta1.t', 'theta2.t', 'theta3.t', 'alpha.t')]))
colnames(tvals) <- 't'
cilow <- data.frame(t(table[c('delta.cilow', 'theta1.cilow', 'theta2.cilow', 'theta3.cilow', 'alpha.cilow')]))
colnames(cilow) <- sig_regions
cihigh <- data.frame(t(table[c('delta.cihigh', 'theta1.cihigh', 'theta2.cihigh', 'theta3.cihigh', 'alpha.cihigh')]))
colnames(cihigh) <- sig_regions
ci <- cihigh
for (region in c(1:length(sig_regions))){
  ci[region] <- data.frame(paste(cilow[region], '-', cihigh[region]))
}

table <- cbind(estimates, ci, pvals)
table <- table[, c(1, 12, 23, 2, 13, 24, 3, 14, 25, 4, 15, 26, 5, 16, 27, 6, 17, 28, 7, 18, 29, 8, 19, 30, 9, 20, 31, 10, 21, 32, 11, 22, 33)]

table2 <- data.frame(t(table))
colnames(table2) <- c('1-4 Hz', '5-6 Hz', '7-8 Hz', '9-10 Hz', '11-12 Hz')

options(knitr.kable.NA = '')
mri_table <- kable(table2, booktabs = F,  linesep = "\\addlinespace") %>%
                  kable_styling(latex_options = "striped", font_size = 20, stripe_color = "white") %>% 
                  pack_rows(index = c("T-maze" = 6, "No-Maze" = 1), background = '#EEEEEE', color = 'black') %>%
                  column_spec(column = 1:6, background = 'white', color = 'black') %>%
                  row_spec(0, bold = T, color = "black", background = "white")

save_kable(
  mri_table,
  '/tables/glasser_lmeTable.pdf'
)
