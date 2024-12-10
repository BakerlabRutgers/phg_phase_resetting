library(plyr)
library(gdata)
library(dplyr)
library(tidyr)
library(reshape2)

setwd('file_directory')

rt_eeg <- ldply('/behavior_eeg/allSubs_rt.txt', read.table, header = T, sep ='\t')
rt_eeg$feedback <- substr(rt_eeg$feedback, 48, 59)

rt_eeg$alley <- revalue(rt_eeg$feedback, c('ltapple.bmp' = '1', 
                                           'rtapple.bmp' = '2',
                                           'ltorange.bmp' = '1', 
                                           'rtorange.bmp' = '2'))
rt_eeg$Subject <- as.factor(rt_eeg$Subject)

for (sub in seq(1, 11, by=1)) {
  
  data <- rt_eeg
  data <- data[ which(data$Subject == sub),]
  
  # Build the new data frame for each subject
  data <- rename(data, 
                 RT = imagedisplay2.RT, 
                 alley = alley, 
                 Type = feedback)
  
  data$Type <- revalue(data$Type, c('ltapple.bmp' = 0, 'rtapple.bmp' = 1, 'ltorange.bmp' = 2, 'rtorange.bmp' = 3))
  
  data$Shift <- rep(4,length(data$Subject))
  data$Subject <- as.numeric(data$Subject)
  
  # Create a transitional variable that will code the previous trial's decision
  temp_resp <- 0
  
  # Start a second loop to go through each line of the reaction data
  for (line in seq(1, length(data$Type), by=1)) {
    
    if (line == 1) {
      # Code the previous response
      if(temp_resp == 0 & data$Type[line] == 0){
        temp_resp <- 1 # Win left
      } else if(temp_resp == 0 & data$Type[line] == 1){
        temp_resp <- 2 # Win right
      } else if(temp_resp == 0 & data$Type[line] == 2){
        temp_resp <- 3 # Lose left
      } else if(temp_resp == 0 & data$Type[line] == 3){
        temp_resp <- 4 # Lose right
      }
      
      data$Shift[line] <- 999
      
    } else {
      
      # Determine the shift behavior
      if(temp_resp == 1 & data$Type[line] == 0){
        data$Shift[line] <- 0 # Win stay (stay left win)
        temp_resp <- 1
      } else if(temp_resp == 1 & data$Type[line] == 2){
        data$Shift[line] <- 0 # Win stay (stay left lose)
        temp_resp <- 3
      } else if(temp_resp == 2 & data$Type[line] == 1){
        data$Shift[line] <- 0 # Win stay (stay right win)
        temp_resp <- 2
      } else if(temp_resp == 2 & data$Type[line] == 3){
        data$Shift[line] <- 0 # Win stay (stay right lose)
        temp_resp <- 4
      } else if(temp_resp == 1 & data$Type[line] == 1){
        data$Shift[line] <- 1 # Win shift (left to right win)
        temp_resp <- 2
      } else if(temp_resp == 1 & data$Type[line] == 3){
        data$Shift[line] <- 1 # Win shift (left to right lose)
        temp_resp <- 4
      } else if(temp_resp == 2 & data$Type[line] == 0){
        data$Shift[line] <- 1 # Win shift (right to left win)
        temp_resp <- 1
      } else if(temp_resp == 2 & data$Type[line] == 2){
        data$Shift[line] <- 1 # Win shift (right to left lose)
        temp_resp <- 3
      } else if(temp_resp == 3 & data$Type[line] == 0){
        data$Shift[line] <- 2 # Lose stay (stay left win)
        temp_resp <- 1
      } else if(temp_resp == 3 & data$Type[line] == 2){
        data$Shift[line] <- 2 # Lose stay (stay left lose)
        temp_resp <- 3
      } else if(temp_resp == 4 & data$Type[line] == 1){
        data$Shift[line] <- 2 # Lose stay (stay right win)
        temp_resp <- 2
      } else if(temp_resp == 4 & data$Type[line] == 3){
        data$Shift[line] <- 2 # Lose stay (stay right lose)
        temp_resp <- 4
      } else if(temp_resp == 3 & data$Type[line] == 1){
        data$Shift[line] <- 3 # Lose shift (left to right win)
        temp_resp <- 2
      } else if(temp_resp == 3 & data$Type[line] == 3){
        data$Shift[line] <- 3 # Lose shift (left to right lose)
        temp_resp <- 4
      } else if(temp_resp == 4 & data$Type[line] == 0){
        data$Shift[line] <- 3 # Lose shift (right to left win)  
        temp_resp <- 1
      } else if(temp_resp == 4 & data$Type[line] == 2){
        data$Shift[line] <- 3 # Lose shift (right to left lose)  
        temp_resp <- 3
      }
      
    }
    
  }
  # Save each subject's results in a combined data frame
  if(sub==1){
    data_all <- data
  }
  else {
    data_all <- rbind(data_all, data)
  }
}

# Delete the first trials and trials with invalid reaction times
data_all <- filter(data_all, Shift != 999)
rt_eeg <- filter(rt_eeg, imagedisplay2.RT >= 100)
rt_eeg <- filter(rt_eeg, imagedisplay2.RT <= 1200)

# Recode shift to a factor and create counters to summarize shifting behavior
shifts <- data_all
shifts$Shift <- as.factor(shifts$Shift)
shifts$counter <- rep(1,length(shifts$Shift))

# Count the occurances of each shifting behavior
shifts$Win_stay <- revalue(shifts$Shift, c('0' = 1, '1' = 0, '2' = 0,'3' = 0))
shifts$Win_shift <- revalue(shifts$Shift, c('0' = 0, '1' = 1, '2' = 0, '3' = 0))
shifts$Lose_stay <- revalue(shifts$Shift, c('0' = 0, '1' = 0, '2' = 1, '3' = 0))
shifts$Lose_shift <- revalue(shifts$Shift, c('0' = 0, '1' = 0, '2' = 0, '3'= 1))


rt_eeg_subs <- ddply(rt_eeg, c('alley', 'Subject'), summarise,
                Sum    = sum(!is.na(imagedisplay2.RT)),
                Mean_RT = mean(imagedisplay2.RT),
                sd   = sd(imagedisplay2.RT),
                se   = sd / sqrt(Sum),
                ci   = se * qt(.95/2 + .5, Sum-1))

rt_eeg <- ddply(rt_eeg, c('alley'), summarise,
                     Sum    = sum(!is.na(imagedisplay2.RT)),
                     Mean_RT = mean(imagedisplay2.RT),
                     sd   = sd(imagedisplay2.RT),
                     se   = sd / sqrt(Sum),
                     ci   = se * qt(.95/2 + .5, Sum-1))

rt_shifts <- ddply(shifts, c('Shift'), summarise,
                   Sum    = sum(!is.na(RT)),
                   Mean_RT = mean(RT),
                   sd   = sd(RT),
                   se   = sd / sqrt(Sum),
                   ci   = se * qt(.95/2 + .5, Sum-1))

# Summarize the percentage of decisions per block and shift behavior
shifts_average <- ddply(shifts, c('Shift'), summarise,
                        Sum    = sum(!is.na(counter)),
                        Percent = Sum/sum(shifts$counter)*100
)

# Start a second loop to go through each line of the reaction data
for (sub in c(1,2,3,4,5,6,7,8,10,11)) {
  for (shift in c(0,1,2,3)) {
    shifts_average_subs[(shifts_average_subs$Subject==sub & shifts_average_subs$Shift==shift),]$Percent <- sum(shifts[(shifts$Subject==sub & shifts$Shift==shift),]$counter)/sum(shifts[(shifts$Subject==sub),]$counter)*100
}
}

write.table(rt_eeg_subs, file = "/behavior_eeg/rt.csv", sep = ",", dec = ".", row.names = FALSE)
write.table(shifts_average_subs, file = "/behavior_eeg/shifts.csv", sep = ",", dec = ".", row.names = FALSE)

##### Same for MEG behavioral data

rt_meg <- ldply('/behavior_meg/allSubs_rt.txt', read.table, header = T, sep ='\t')

# Fix some issues with subject IDs in the original files
rt_meg$Subject[rt_meg$Subject == 111] <- 1
rt_meg$Subject[rt_meg$Subject == 22] <- 2
rt_meg$Subject[rt_meg$Subject == 33] <- 3
rt_meg$Subject[rt_meg$Subject == 44] <- 4
rt_meg$Subject[rt_meg$Subject == 55] <- 5
rt_meg$Subject[rt_meg$Subject == 66] <- 6

rt_meg$feedback <- str_sub(rt_meg$feedback,-12)
rt_meg$feedback <- str_replace(rt_meg$feedback, fixed("/"), "")
rt_meg$alley <- revalue(rt_meg$feedback, c('ltapple.bmp' = '1', 'rtapple.bmp' = '2', 
                                        'ltorange.bmp' = '1', 'rtorange.bmp' = '2'))


for (sub in seq(1, 11, by=1)) {
  
  data <- rt_meg
  data <- data[ which(data$Subject == sub),]
  
  # Build the new data frame for each subject
  data <- rename(data, 
                 RT = imagedisplay2.RT, 
                 alley = alley, 
                 Type = feedback)
  
  data$Type <- revalue(data$Type, c('ltapple.bmp' = 0, 'rtapple.bmp' = 1, 'ltorange.bmp' = 2, 'rtorange.bmp' = 3))
  
  data$Shift <- rep(4,length(data$Subject))
  data$Subject <- as.numeric(data$Subject)
  
  # Create a transitional variable that will code the previous trial's decision
  temp_resp <- 0

  # Start a second loop to go through each line of the reaction data
  for (line in seq(1, length(data$Type), by=1)) {
    
    if (line == 1) {
      # Code the previous response
      if(temp_resp == 0 & data$Type[line] == 0){
        temp_resp <- 1 # Win left
      } else if(temp_resp == 0 & data$Type[line] == 1){
        temp_resp <- 2 # Win right
      } else if(temp_resp == 0 & data$Type[line] == 2){
        temp_resp <- 3 # Lose left
      } else if(temp_resp == 0 & data$Type[line] == 3){
        temp_resp <- 4 # Lose right
      }
      
      data$Shift[line] <- 999

    } else {

      # Determine the shift behavior
      if(temp_resp == 1 & data$Type[line] == 0){
        data$Shift[line] <- 0 # Win stay (stay left win)
        temp_resp <- 1
      } else if(temp_resp == 1 & data$Type[line] == 2){
        data$Shift[line] <- 0 # Win stay (stay left lose)
        temp_resp <- 3
      } else if(temp_resp == 2 & data$Type[line] == 1){
        data$Shift[line] <- 0 # Win stay (stay right win)
        temp_resp <- 2
      } else if(temp_resp == 2 & data$Type[line] == 3){
        data$Shift[line] <- 0 # Win stay (stay right lose)
        temp_resp <- 4
      } else if(temp_resp == 1 & data$Type[line] == 1){
        data$Shift[line] <- 1 # Win shift (left to right win)
        temp_resp <- 2
      } else if(temp_resp == 1 & data$Type[line] == 3){
        data$Shift[line] <- 1 # Win shift (left to right lose)
        temp_resp <- 4
      } else if(temp_resp == 2 & data$Type[line] == 0){
        data$Shift[line] <- 1 # Win shift (right to left win)
        temp_resp <- 1
      } else if(temp_resp == 2 & data$Type[line] == 2){
        data$Shift[line] <- 1 # Win shift (right to left lose)
        temp_resp <- 3
      } else if(temp_resp == 3 & data$Type[line] == 0){
        data$Shift[line] <- 2 # Lose stay (stay left win)
        temp_resp <- 1
      } else if(temp_resp == 3 & data$Type[line] == 2){
        data$Shift[line] <- 2 # Lose stay (stay left lose)
        temp_resp <- 3
      } else if(temp_resp == 4 & data$Type[line] == 1){
        data$Shift[line] <- 2 # Lose stay (stay right win)
        temp_resp <- 2
      } else if(temp_resp == 4 & data$Type[line] == 3){
        data$Shift[line] <- 2 # Lose stay (stay right lose)
        temp_resp <- 4
      } else if(temp_resp == 3 & data$Type[line] == 1){
        data$Shift[line] <- 3 # Lose shift (left to right win)
        temp_resp <- 2
      } else if(temp_resp == 3 & data$Type[line] == 3){
        data$Shift[line] <- 3 # Lose shift (left to right lose)
        temp_resp <- 4
      } else if(temp_resp == 4 & data$Type[line] == 0){
        data$Shift[line] <- 3 # Lose shift (right to left win)  
        temp_resp <- 1
      } else if(temp_resp == 4 & data$Type[line] == 2){
        data$Shift[line] <- 3 # Lose shift (right to left lose)  
        temp_resp <- 3
      }
      
    }
    
  }
  # Save each subject's results in a combined data frame
  if(sub==1){
    data_all <- data
  }
  else {
    data_all <- rbind(data_all, data)
  }
}

# Delete the first trials and trials with invalid reaction times
data_all <- filter(data_all, Shift != 999)
rt_meg <- filter(rt_meg, imagedisplay2.RT <= 1200)
rt_meg <- filter(rt_meg, imagedisplay2.RT >= 100)

# Recode shift to a factor and create counters to summarize shifting behavior
shifts <- data_all
shifts$Shift <- as.factor(shifts$Shift)
shifts$counter <- rep(1,length(shifts$Shift))

# Count the occurances of each shifting behavior
shifts$Win_stay <- revalue(shifts$Shift, c('0' = 1, '1' = 0, '2' = 0,'3' = 0))
shifts$Win_shift <- revalue(shifts$Shift, c('0' = 0, '1' = 1, '2' = 0, '3' = 0))
shifts$Lose_stay <- revalue(shifts$Shift, c('0' = 0, '1' = 0, '2' = 1, '3' = 0))
shifts$Lose_shift <- revalue(shifts$Shift, c('0' = 0, '1' = 0, '2' = 0, '3'= 1))


rt_meg_subs <- ddply(rt_meg, c('alley', 'Subject'), summarise,
                Sum    = sum(!is.na(imagedisplay2.RT)),
                Mean_RT = mean(imagedisplay2.RT),
                sd   = sd(imagedisplay2.RT),
                se   = sd / sqrt(Sum),
                ci   = se * qt(.95/2 + .5, Sum-1))

rt_shifts <- ddply(shifts, c('Shift'), summarise,
                   Sum    = sum(!is.na(RT)),
                   Mean_RT = mean(RT),
                   sd   = sd(RT),
                   se   = sd / sqrt(Sum),
                   ci   = se * qt(.95/2 + .5, Sum-1))

# As before, create a second data frame where we keep single subject values
shifts_average_subs <- ddply(shifts, c('Shift','Subject'), summarise,
                             Sum    = sum(!is.na(counter)),
                             Percent = Sum/sum(shifts$counter)*100
)

# Start a second loop to go through each line of the reaction data
for (sub in c(1,2,3,4,5,6,7,8,9,10,11)) {
  for (shift in c(0,1,2,3)) {
    shifts_average_subs[(shifts_average_subs$Subject==sub & shifts_average_subs$Shift==shift),]$Percent <- sum(shifts[(shifts$Subject==sub & shifts$Shift==shift),]$counter)/sum(shifts[(shifts$Subject==sub),]$counter)*100
}
}

write.table(rt_meg_subs, file = "/behavior_meg/rt.csv", sep = ",", dec = ".", row.names = FALSE)
write.table(shifts_average_subs, file = "/behavior_meg/shifts.csv", sep = ",", dec = ".", row.names = FALSE)
