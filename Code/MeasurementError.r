# This R script is created for the measurement error study
# Copyright: Jing Yi, email: jy348@cornell.edu

# bootstramping to generate adoption rate
# 
rm(list = ls())
dir <- getwd()
dir_result <- paste(dir, '/Output', sep = '')
requiredPackages = c('gee','PropCIs','RVAideMemoire','ggpubr', 'broom', 'modelsummary','dplyr')
for(p in requiredPackages){
  if(!require(p,character.only = TRUE)) install.packages(p)
  library(p,character.only = TRUE)
}
options(modelsummary_format_numeric_latex = "plain")

# my_packages <- c('gee','PropCIs')                                        # Specify your packages
# not_installed <- my_packages[!(my_packages %in% installed.packages()[ , "Package"])]    # Extract not installed packages
# if(length(not_installed)) install.packages(not_installed)      

# data(Paired1) # Hypothetical study data 
hh <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Gender/MeasureError/MeasurementError/hh.csv" , header=TRUE, sep = '|')
hh<- subset(hh,F_HHAsset_Value_Total!=0 )
hh$M_HHAsset_Value_Total_lg <- log(hh$M_HHAsset_Value_Total)
hh$F_HHAsset_Value_Total_lg <- log(hh$F_HHAsset_Value_Total)

summary(hh$F_Total_Processing_Access_HH)
summary(hh$M_planted)

hh$Diff_ICV_HH_yn <- hh$M_ICV_HH_yn - hh$F_ICV_HH_yn

hh$Diff_HHAsset_Value_Total <- hh$M_HHAsset_Value_Total - hh$F_HHAsset_Value_Total
hh$Diff_Age <- hh$M_Age - hh$F_Age
hh$Diff_HHSize <- hh$M_HHSize - hh$F_HHSize
# Don't use the following:
hh$Diff_HHAsset_ByGender <- hh$M_Household_assets-hh$F_Household_assets
summary(hh$Diff_ICV_HH_yn)

hh$Cell_Value_MF <- hh$M_Cell_Value_Male - hh$F_Cell_Value_Female
hh$Cell_Value_M <- hh$M_Cell_Value_Male - hh$F_Cell_Value_Male
hh$Cell_Value_F <- hh$M_Cell_Value_Female- hh$F_Cell_Value_Female


hh$M_ZoneID_ft <- as.factor(hh$M_ZoneID)
hh$F_ZoneID_ft <- as.factor(hh$F_ZoneID)
summary(hh$M_ZoneID_ft)
hh$M_ZoneID_ft <- relevel(hh$M_ZoneID_ft , ref = 3)

library("writexl")
write_xlsx(hh,"hh_r.xlsx")


# hh_yn <- hh[c("M_ICV_HH_yn", "F_ICV_HH_yn")]
# df_test2 <- hh[c('f_tot')]
# test3 <-  ecdf(df_test2$f_tot)
# test4 <- test3(df_test2$f_tot)
# Paired t-test: the null hypothesis assumes that the true mean difference between the paired samples is zero. 
mtcars <- hh[c('Diff_ICV_HH_yn','Diff_HHAsset_Value_Total','Diff_Age','Diff_HHSize','M_ZoneID','Cell_Value_MF','Cell_Value_M','Cell_Value_F')]
# if (!require(heatmaply)) install.packages('heatmaply')
# if (!require(corrplot)) install.packages('corrplot')

# Load the package
library(corrplot)
library(heatmaply)
cor_mat <- cor(mtcars)
print(cor_mat)
# dev.off()
heatmaply(cor_mat)

 


rg_logit_m <- glm(M_ICV_HH_yn ~ M_Age+M_Edu+M_HHAsset_Value_Total_lg+M_ZoneID_ft+M_HHSize+M_Coop_HH,data = hh)

# pair_test_m2 <- mcnemar.test(hh$M_ICV_HH_yn, hh$F_ICV_HH_yn) 

# pair_test_yn <- t.test(hh$M_ICV_HH_yn, hh$F_ICV_HH_yn, paired =TRUE) 
pair_test_m <- t.test(hh$M_ICV_Managed_Male, hh$F_ICV_Managed_Male, paired =TRUE) 
pair_test_f <- t.test(hh$M_ICV_Managed_Female, hh$F_ICV_Managed_Female, paired =TRUE) 
pair_test_j <- t.test(hh$M_ICV_Managed_Joint, hh$F_ICV_Managed_Joint, paired =TRUE) 
pair_test_Tot <- t.test(hh$m_tot, hh$f_tot, paired =TRUE) 
test <- as.data.frame(hh$M_HHAsset_Value_Total)
test <- as.data.frame(hh$M_Household_assets)

out1 <- broom::tidy(pair_test_Tot)
write.table(out1, "out1.csv", sep = '|')

summary(hh$M_planted)
pair_test_yn <- t.test(hh$M_ICV_HH_yn, hh$F_ICV_HH_yn, paired =TRUE) 
out <- broom::tidy(pair_test_yn)

pair_test_ever <- t.test(hh$M_planted, hh$F_planted, paired =TRUE) 

# write.table(out, "out.csv", sep = '|')

sum(is.na(hh$F_ZoneID))
pair_zone <- t.test(hh$M_ZoneID, hh$F_ZoneID, paired =TRUE) 
pair_zone <- broom::tidy(pair_zone)


pair_size <- t.test(hh$M_HHAsset_Value_Total, hh$F_HHAsset_Value_Total, paired =TRUE) 
pair_zone <- broom::tidy(pair_zone)

summary(hh$M_ICV_HH_yn)
summary(hh$F_ICV_HH_yn)
summary(hh$M_HHAsset_Value_Total)
summary(hh$M_HHSize)
summary(hh$F_HHSize)
summary(hh$M_HHAsset_Value_Total)



sum(is.na(hh$F_HHAsset_Value_Total))
sum(hh$F_HHAsset_Value_Total==0)

df_test <- subset(hh,F_HHAsset_Value_Total==0 ,select=c(F_HHAsset_Value_Total, M_HHAsset_Value_Total))
sum(df_test$F_HHAsset_Value_Total)
summary(df_test$M_ZoneID_ft)

# ------------------------------------------------------------------------------------------------------------
# logistic regressions:

rg_logit_m <- glm(M_ICV_HH_yn ~ M_Age+M_Edu+M_HHAsset_Value_Total_lg+M_ZoneID_ft+M_HHSize+M_Coop_HH,data = hh)
summary(rg_logit_m)

rg_logit_m_manage <- glm(M_tot ~ M_Age+M_Edu+M_HHAsset_Value_Total_lg+M_ZoneID_ft+M_HHSize+M_Coop_HH,data = hh)
summary(rg_logit_m_manage)

# GENDER:
rg_logit_m <- glm(M_ICV_HH_yn ~ M_Age+M_Edu+M_HHAsset_Value_Total_lg+M_ZoneID_ft+M_HHSize+M_Credit_HH + M_Cell_Own_yn+M_Coop_HH+F_Production_Value_Female+F_Dishes_Own_yn,data = hh)
summary(rg_logit_m)

rg_logit_f <- glm(F_ICV_HH_yn ~ F_Age+F_Edu+F_HHAsset_Value_Total_lg+M_ZoneID_ft+F_HHSize+F_Credit_HH + F_Cell_Own_yn+F_Coop_HH,data = hh)
summary(rg_logit_f)


rg_logit_f <- glm(F_planted ~ F_Age+F_Edu+F_HHAsset_Value_Total_lg+M_ZoneID_ft+F_HHSize+F_Credit_HH + F_Cell_Own_yn+F_Coop_HH,data = hh)
summary(rg_logit_f)


summary(hh$M_Age)
model_gender <- list('Male'=rg_logit_m, 'Female'=rg_logit_f)
modelsummary(model_gender, stars = TRUE,coef_rename =TRUE, output = paste(dir_result,'/reg_yn_3.tex', sep=""))

install.packages("randomForest")
library(randomForest)
target <- "M_ICV_HH_yn"
data <- hh


# Create a random forest model
model <- randomForest(as.formula(paste(target, "~ .")), data = data)

# Calculate feature importance
importance <- importance(model, type = 1)

# Sort the importance values in descending order
importance <- importance[order(importance[, 3], decreasing = TRUE), ]

# Plot feature importance
ggplot(importance, aes(x = reorder(rownames(importance), -MeanDecreaseGini), y = MeanDecreaseGini)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  xlab("Features") +
  ylab("Mean Decrease Gini") +
  ggtitle("Feature Importance") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# --------------------------Create a fake dataset--------------------------

df_sudo$age_gender <- df_sudo$Age * df_sudo$gender

base_model <- glm(ICV_HH_yn ~ gender+Age+Edu+ZoneID_ft, family=binomial(link='probit'),data = df_sudo)
summary(base_model)
candidate_vars <- c("HHAsset_Value_Total_lg", "HHSize", "Credit_HH","Coop_HH" )  # replace with your actual variables
for (var in candidate_vars) {
  model <- glm(as.formula(paste("ICV_HH_yn ~ gender+Age+Edu+ZoneID_ft+", var)), family=binomial(link='probit'), data = df_sudo)
  print(summary(model))
}

model_list <- list()
# f_rate = 0.95
n_values <- seq(0.05, 0.5, by=0.05)
# n_values <- seq(0.5, 0.95, by=0.05)

wb <- createWorkbook()
for (i in 1:length(n_values)) {
  

  n <- n_values[i]
  f_rate <- n
  
  set.seed(123)
  df_f <- sample_frac(hh,f_rate)
  df_f$F_gender <- 0
  # names(df_m)
  df_m <- anti_join(hh, df_f)
  df_m$M_gender <- 1
  
  df_f <- df_f %>% select(starts_with(("F_")))
  names(df_f) <- sub("^F_","",names(df_f))
  names(df_m) <- sub("^M_","",names(df_m))
  df_sudo <- bind_rows(df_f, df_m)
  # names(df_sudo)
  summary(df_sudo$gender)
  summary(df_sudo$ICV_HH_yn)
  df_sudo$tot_bi <- ifelse(df_sudo$tot > 0, 1, 0)
  df_sudo$test <- df_sudo$tot_bi - df_sudo$ICV_HH_yn 
  summary(df_sudo$test)
  df_test <-  data.frame(df_sudo$test)
  # hh$M_ZoneID_ft <- relevel(hh$M_ZoneID_ft , ref = 3)
  df_sudo$ZoneID_gender <-df_sudo$ZoneID *df_sudo$gender
  df_sudo$edu_gender <-df_sudo$Edu *df_sudo$gender
  df_sudo$age_gender <-df_sudo$Age *df_sudo$gender
  
  df_sudo$ZoneID_ft <- relevel(df_sudo$ZoneID_ft , ref = 3)

  summary(df_sudo$ZoneID_ft)
  # strange:
  # model <- glm(ICV_HH_yn ~ Age+Edu+ZoneID_ft+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender ,data = df_sudo,family = binomial(link = 'probit'))
  # model <- glm(tot_bi ~ Age+Edu+ZoneID_ft+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender+ZoneID_gender ,data = df_sudo,family = binomial(link = 'probit'))
  df_sudo <- subset(df_sudo, ZoneID_ft == 3)
  
  # model <- glm(tot_bi ~ Age+Edu+ZoneID_ft+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender+edu_gender+age_gender ,data = df_sudo,family = binomial(link = 'probit'))
  model <- glm(tot_bi ~ Age+Edu+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender+edu_gender+age_gender ,data = df_sudo,family = binomial(link = 'probit'))
  # model <- lm(tot ~ Age+Edu+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender  ,data = df_sudo)
  # model <- lm(tot ~ Age+Edu+ZoneID_ft+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender ,data = df_sudo )

  summary(model)
  model_list[[i]] <- model
  
  summary <- modelsummary(model, column_names = c(f_rate))
  
 
}
print(model_list)
  
modelsummary(model_list, stars = TRUE, coef_rename = TRUE,output = paste(dir_result,'/reg_yn_2.tex', sep=""))

 
# Add the results_table as a worksheet to the workbook
addWorksheet(wb, "Regression Results")
writeData(wb, "Regression Results", results_table)

# Save the workbook as an Excel file
saveWorkbook(wb, "regression_results.xlsx", overwrite = TRUE)
print(results_table)

rg_logit_sudo <- glm(ICV_HH_yn ~ Age+Edu+HHAsset_Value_Total_lg+ZoneID_ft +gender ,data = df_sudo)
summary(rg_logit_sudo)

# full:
rg_logit_sudo <- glm(ICV_HH_yn ~ Age+Edu+HHAsset_Value_Total_lg+ZoneID_ft+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender ,data = df_sudo)
summary(rg_logit_sudo)

rg_logit_sudo_short <- glm(ICV_HH_yn ~ Age+Edu+HHAsset_Value_Total_lg+ZoneID_ft+gender ,data = df_sudo)
summary(rg_logit_sudo_short)

df_sudo$ZoneID_ft <- as.factor(df_sudo$ZoneID_ft)
summary(df_sudo$ZoneID_ft)
df_sudo$ZoneID_ft <- relevel(df_sudo$ZoneID_ft , ref = "1")


# --------------------------Create a "full" dataset--------------------------
df_f_full <- dplyr::select(hh, dplyr::starts_with("F_"))
df_f_full$F_gender <- 0
 
df_m_full <-  dplyr::select(hh, dplyr::starts_with("M_"))
df_m_full$M_gender <- 1

names(df_f_full) <- sub("^F_","",names(df_f_full))
names(df_m_full) <- sub("^M_","",names(df_m_full))
df_full <- bind_rows(df_f_full, df_m_full)

library(MASS)
full_model <- glm(ICV_HH_yn ~Age+Edu+HHAsset_Value_Total_lg+ZoneID_ft+HHSize+Credit_HH + Cell_Own_yn+Coop_HH+gender,data = df_full)
summary(full_model)

full_model

# Apply stepwise regression with both directions (forward and backward)
step_model <- stepAIC(full_model, direction = "both")
print(step_model$finalModel)

# short:
rg_logit_sudo_short <- glm(ICV_HH_yn ~ Age+Edu+HHAsset_Value_Total_lg+ZoneID_ft +gender ,data = df_sudo)
summary(rg_logit_sudo_short)

# temp
rg_logit_sudo_temp <- glm(ICV_HH_yn ~ Age+Edu+HHAsset_Value_Total_lg+ZoneID_ft+HHSize+Credit_HH + Cell_Own_yn+HouseHold_AnimalUnits+Coop_HH+gender ,data = df_sudo)
summary(rg_logit_sudo_temp)

shh$ICV_HH_yn_diff <- hh$M_ICV_HH_yn - hh$F_ICV_HH_yn
hh$ICV_HH_yn_avg <- 0.5*( hh$M_ICV_HH_yn + hh$F_ICV_HH_yn)
hh$ICV_TotValue_avg <- 0.5*( hh$M_HHAsset_Value_Total + hh$F_HHAsset_Value_Total)
hh$ICV_TotValue_avg_k <- hh$ICV_TotValue_avg/1000
hh$Zone1 <- 0 
hh$Zone1[hh$M_ZoneID==1] <-1
hh$Zone2 <- 0 
hh$Zone2[hh$M_ZoneID==2] <-1
hh$Zone3 <- 0 
hh$Zone3[hh$M_ZoneID==3] <-1
hh$Zone4 <- 0 
hh$Zone4[hh$M_ZoneID==4] <-1

hh$age_diff <- hh$M_Age - hh$F_Age
hh$edu_diff <- hh$M_Edu - hh$F_Edu


hh$ICV_HH_yn_diff_abs <- hh$ICV_HH_yn_diff
hh$ICV_HH_yn_diff_abs[hh$ICV_HH_yn_diff_abs!=0] = 1

attr(hh$F_ICV_HH_yn, "label") <- "F_Ever planted ICV"
attr(hh$M_ICV_HH_yn, "label") <- "M_Ever planted ICV"


test <- hh[,c('ICV_HH_yn_diff','ICV_HH_yn_diff_abs')]
summary(hh$ICV_HH_yn_diff)



reg_log <- glm(as.factor(ICV_HH_yn_diff) ~ 0 + age_diff + edu_diff+  ICV_TotValue_avg_k + Zone1 +Zone2 +Zone3 , family = binomial, data = hh)
summary(reg_log)

Out_List <- list('Diff_Icv'=reg_log)

modelsummary(Out_List, stars = TRUE,coef_rename =TRUE, output = paste(dir_result,'/reg_yn_diff.tex', sep=""))


# install.packages('epiDisplay')
library(epiDisplay)
tab1(hh$M_ZoneID, sort.group = "decreasing", cum.percent = TRUE)
test <- hh[,c('M_ZoneID','F_ZoneID')]
test$diff <- test$M_ZoneID-test$F_ZoneID
summary(test$diff )


install.packages('epiDisplay')
library(epiDisplay)
tab1(hh$ICV_HH_yn_diff, sort.group = "decreasing", cum.percent = TRUE)

summary(hh$ICV_HH_yn_diff)
hist(hh$ICV_HH_yn_diff)





library(EnvStats) 
par(mfrow=c(1,2)) 
epdfPlot(hh$M_ICV_HH_yn)
epdfPlot(hh$F_ICV_HH_yn)

par(mfrow=c(1,2)) 
plot(ecdf(hh$M_ICV_HH_yn))
plot(ecdf(hh$F_ICV_HH_yn))


plot(hh$M_ICV_HH_yn, hh$F_ICV_HH_yn)

par(mfrow=c(1,2)) 

reg_yn <- lm(M_ICV_HH_yn ~0+F_ICV_HH_yn, data=hh)
summary(reg_yn)
AIC(reg_yn)

with(hh,plot(F_ICV_HH_yn,M_ICV_HH_yn))
abline(reg_yn)
title("OLS")

probit_yn <- glm(M_ICV_HH_yn ~ 0 + F_ICV_HH_yn, family = binomial(link = "probit"), 
                data = hh)
summary(probit_yn)
AIC(probit_yn)

with(hh,plot(F_ICV_HH_yn,M_ICV_HH_yn))
abline(probit_yn)
title("Probit")

probit_yn2 <- glm(F_ICV_HH_yn ~ 0 + M_ICV_HH_yn, family = binomial(link = "probit"), 
                 data = hh)
summary(probit_yn2)



Out_List <- list('Male'=probit_yn, 'Female'=probit_yn2)

modelsummary(Out_List, stars = TRUE,coef_rename =TRUE, output = paste(dir_result,'/reg_yn.tex', sep=""))

# Comparison of the accuracy of two binary diagnostic tests in a “paired” study design, i.e. when each test is applied to each subject in the study.

# It is required that results from a binary gold-standard test are also available.


install.packages("DTComPair")
library(DTComPair)
data(Paired1) # Hypothetical study data 
hsd <- tab.paired(d=d, y1=y1, y2=y2, data=Paired1)
acc.paired(hsd)
sesp.mcnemar(hsd)
pv.rpv(hsd)
dlr.regtest(hsd)


rbind(tidy(pair_test_m),tidy(pair_test_f),tidy(pair_test_j),tidy(pair_test_Tot),tidy(pair_test_yn))
pair_test_m$p.value
pair_test_m$estimate

col1 <- rbind(pair_test_m$p.value,pair_test_f$p.value,pair_test_j$p.value, pair_test_Tot$p.value )
col2<- rbind(pair_test_m$estimate,pair_test_f$estimate,pair_test_j$estimate, pair_test_Tot$estimate )


reg_ICV_Managed_Male <- lm(M_ICV_Managed_Male ~0+F_ICV_Managed_Male, data=hh)
summary(reg_ICV_Managed_Male)
with(hh,plot(F_ICV_Managed_Male,M_ICV_Managed_Male))
abline(reg_ICV_Managed_Male)

plot(M_ICV_Managed_Male~F_ICV_Managed_Male,data=hh)
plot(M_ICV_Managed_Male~M_ICV_Managed_Female,data=hh)

hh$Avg_ICV_Managed_Male = (hh$M_ICV_Managed_Male+hh$F_ICV_Managed_Male)*0.5
reg_Avg_ICV_Managed_Male <- lm(Avg_ICV_Managed_Male ~0+M_ICV_Managed_Male+F_ICV_Managed_Male, data=hh)
summary(reg_Avg_ICV_Managed_Male)

reg_ICV_Managed_Female <- lm(M_ICV_Managed_Female ~0+F_ICV_Managed_Female, data=hh)
summary(reg_ICV_Managed_Female)
with(hh,plot(F_ICV_Managed_Female,M_ICV_Managed_Female))
abline(reg_ICV_Managed_Female)

reg_ICV_Managed_Joint <- lm(M_ICV_Managed_Joint ~0+F_ICV_Managed_Joint, data=hh)
summary(reg_ICV_Managed_Joint)
with(hh,plot(F_ICV_Managed_Joint,M_ICV_Managed_Joint))
abline(reg_ICV_Managed_Joint)

reg_ICV_Managed_Joint2 <- lm(F_ICV_Managed_Joint ~0+M_ICV_Managed_Joint , data=hh)
summary(reg_ICV_Managed_Joint2)

reg_ICV_m_tot<- lm(m_tot ~0+f_tot, data=hh)
summary(reg_ICV_m_tot)
with(hh,plot(f_tot,m_tot))
abline(reg_ICV_m_tot)



Out_List <- list('Managed_Male'=reg_ICV_Managed_Male, 'Managed_Female'=reg_ICV_Managed_Female,'Joint'=reg_ICV_Managed_Joint,'Total'=reg_ICV_m_tot)
library(modelsummary)
modelsummary(Out_List,stars=TRUE, coef_rename = TRUE , output = 'D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Gender/MeasureError/MeasurementError/Results/regression.tex')

# McNemar's test to see the effect of some treatment, training, or advertisement which brings about the changes in the attitude of individuals. It is similar to the paired samples t-test but for dichotomous nominal instead of interval variables.
# pair_test_yn2 <- mcnemar.test(hh$M_ICV_HH_yn, hh$F_ICV_HH_yn) 
test <- cbind(hh$M_ICV_Managed_Male,hh$F_ICV_Managed_Male )

pair_test_m2 <- mcnemar.test(test )
pair_test_f2 <- mcnemar.test(hh$M_ICV_Managed_Female, hh$F_ICV_Managed_Female ) 
pair_test_j2 <- mcnemar.test(hh$M_ICV_Managed_Joint, hh$F_ICV_Managed_Joint ) 
pair_test_Tot2 <- mcnemar.test(hh$m_tot, hh$f_tot) 
pair_test_yn2 <- mcnemar.test(hh$M_ICV_HH_yn, hh$F_ICV_HH_yn, paired =TRUE) 
rbind(tidy(pair_test_m),tidy(pair_test_f),tidy(pair_test_j),tidy(pair_test_Tot),tidy(pair_test_yn))

# Compbdt
# fisher.bintest: pairwise comparisons by using Fisher’s exact tests.
# If the response is a 0/1 variable, the probability of the ’1’ group is tested. In any other cases, the response is transformed into a factor and the probability of the second level is tested.
fisher <- fisher.bintest(hh$M_ICV_HH_yn~hh$F_ICV_HH_yn)

df_test <- hh[c("M_ICV_Managed_Male", "M_ICV_Managed_Male")]
df_test <- as.matrix(df_test)

# Fisher's exact test:
# Null hypothesis: The two categorical variables are independent (no association between the two variables)
test1 <- fisher.test(df_test,simulate.p.value = TRUE, B = 1e5)
test1$p.value
# The two series are independence.
# 
# https://www.jmp.com/en_us/statistics-knowledge-portal/t-test/paired-t-test.html

# Dif_m
# 
# M_Household_assets
pair_test_Aset_Tot <- t.test(hh$M_HHAsset_Value_Total, hh$F_HHAsset_Value_Total, paired =TRUE) 
pair_test_Aset_M <- t.test(hh$M_HHAsset_Value_Male, hh$F_HHAsset_Value_Male, paired =TRUE) 
pair_test_Aset_F <- t.test(hh$M_HHAsset_Value_Female, hh$F_HHAsset_Value_Female, paired =TRUE) 

reg_HHAsset_Value_Total <- lm(M_HHAsset_Value_Total ~0+F_HHAsset_Value_Total, data=hh)
summary(reg_HHAsset_Value_Total)
mean(hh$M_HHAsset_Value_Total)
mean(hh$F_HHAsset_Value_Total)

reg_HHAsset_Value_Male <- lm(M_HHAsset_Value_Male ~0+F_HHAsset_Value_Male, data=hh)
summary(reg_HHAsset_Value_Male)
plot(M_HHAsset_Value_Male ~F_HHAsset_Value_Male, data=hh)

reg_HHAsset_Value_Male2 <- lm(F_HHAsset_Value_Male ~0+M_HHAsset_Value_Male, data=hh)


reg_HHAsset_Value_Female <- lm(M_HHAsset_Value_Female ~0+F_HHAsset_Value_Female, data=hh)
summary(reg_HHAsset_Value_Female)
plot(M_HHAsset_Value_Female~F_HHAsset_Value_Female, data=hh)
hh$M_HHAsset_Value_Female
# remove outliers
# 
reg_M_HHAsset_Value_Male <- lm(M_HHAsset_Value_Male ~0+F_HHAsset_Value_Male, data=hh)
summary(reg_M_HHAsset_Value_Male)



pair_test_Aset <- t.test(hh$M_Household_assets, hh$F_Household_assets, paired =TRUE) 
hh$M_Household_assets.mean()

asset_1 <- t.test(hh$M_HHAsset_Value_Female,hh$F_HHAsset_Value_Female, paired =TRUE) 
asset_2 <- t.test(hh$M_HHAsset_Value_Male,hh$F_HHAsset_Value_Male, paired =TRUE) 
asset_3 <- t.test(hh$M_HHAsset_Production_Value,hh$F_HHAsset_Production_Value, paired =TRUE) 
asset_4 <- t.test(hh$M_Total_Processing_Asset_HH,, paired =TRUE) 
rbind(tidy(asset_1),tidy(asset_2),tidy(asset_3))

# remove outliers
# put 45-degree lines & other lines together
install.packages("clipr")
library("clipr")
rate_data <- read_clip_tbl()
library(foreign)
install.packages("frm")
library(frm)
library(sandwich)
library(lmtest)
# write.csv(rate_data, "D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Gender/MeasureError/MeasurementError/rate.csv", row.names=FALSE)
model <- lm(AdoptionRate ~Female,data = rate_data)
