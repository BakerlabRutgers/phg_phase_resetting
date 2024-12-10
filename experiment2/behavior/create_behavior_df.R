library(plyr)
library(gdata)
library(dplyr)
library(tidyr)
library(reshape2)

setwd("/file_directory/behavioral_data/")

rt <- ldply('allSub_rt.csv', read.table, header = T, sep =',')

rt <- rt[!(is.na(rt$outcomeImage) | rt$outcomeImage==""), ]
rt <- rt[!(is.na(rt$outcomeImage) | rt$outcomeImage=="start"), ]
rt$Subject <- revalue(as.factor(rt$Subject), c('42' = '4',
                                               '118' = '18'))
rt$outcomeImage <- as.factor(rt$outcomeImage)

for (sub in seq(1, 30, by=1)) {
  
  data <- rt
  data <- data[ which(data$Subject == sub),]
  
  # Build the new data frame for each subject
  data <- rename(data, 
                 RT = ChoiceDisplay.RT, 
                 block = trialType, 
                 Type = outcomeImage)
  
  data$Type <- revalue(data$Type, c('left_apple' = 0, 'right_apple' = 1, 'left_orange' = 2, 'right_orange' = 3))
  
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

# Delete the first trials
data_all <- filter(data_all, Shift != 999)

# Recode shift to a factor and create counters to summarize shifting behavior
shifts <- data_all
shifts$Shift <- as.factor(shifts$Shift)
shifts$counter <- rep(1,length(shifts$Shift))

# Count the occurances of each shifting behavior
shifts$Win_stay <- revalue(shifts$Shift, c('0' = 1, '1' = 0, '2' = 0,'3' = 0))
shifts$Win_shift <- revalue(shifts$Shift, c('0' = 0, '1' = 1, '2' = 0, '3' = 0))
shifts$Lose_stay <- revalue(shifts$Shift, c('0' = 0, '1' = 0, '2' = 1, '3' = 0))
shifts$Lose_shift <- revalue(shifts$Shift, c('0' = 0, '1' = 0, '2' = 0, '3'= 1))


rt_subs <- ddply(rt, c('trialType', 'outcomeImage', 'Subject'), summarise,
                Sum    = sum(!is.na(ChoiceDisplay.RT)),
                Mean_RT = mean(ChoiceDisplay.RT),
                sd   = sd(ChoiceDisplay.RT),
                se   = sd / sqrt(Sum),
                ci   = se * qt(.95/2 + .5, Sum-1))

rt_shifts <- ddply(shifts, c('Shift'), summarise,
                   Sum    = sum(!is.na(RT)),
                   Mean_RT = mean(RT),
                   sd   = sd(RT),
                   se   = sd / sqrt(Sum),
                   ci   = se * qt(.95/2 + .5, Sum-1))

shifts_average_subs <- ddply(shifts, c('Shift','Subject','block'), summarise,
                             Sum    = sum(!is.na(counter)),
                             Percent = Sum/sum(shifts$counter)*10000
)

write.table(rt_subs, file = "rt.csv", sep = ",", dec = ".", row.names = FALSE)
write.table(shifts_average_subs, file = "shifts.csv", sep = ",", dec = ".", row.names = FALSE)
