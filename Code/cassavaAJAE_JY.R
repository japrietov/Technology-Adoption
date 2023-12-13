# install.packages('oaxaca')
rm(list = ls())
dir <- getwd()

OutputDir <- paste(dir, '/Output', sep = '')
requiredPackages = c('gee','PropCIs','RVAideMemoire','ggpubr', 'broom', 'modelsummary','dplyr','oaxaca')
for(p in requiredPackages){
  if(!require(p,character.only = TRUE)) install.packages(p)
  library(p,character.only = TRUE)
}
options(modelsummary_format_numeric_latex = "plain")




df <- read.csv(paste0(OutputDir,'/df_FM_Update.csv'))

formula_1 = planted ~ J02_per_hh_inc_cassav + Joint_Coop + Credit_Access + log_Total_Household_Asset_Value + log_Total_Production_Asset_Value + ZoneID_1 + ZoneID_3 + ZoneID_4 + A03_Age + A05_Edu + Household_Size + A07_1_Main_occupatn_Farming + A07_1_Main_occupatn_Self_employed_off_farm + A07_1_Main_occupatn_Other + A08_fam_lab_contributn | A02_Sex  | ZoneID_1 + ZoneID_3 + ZoneID_4


formula_dna = DNA_planted ~ J02_per_hh_inc_cassav + Joint_Coop + Credit_Access + log_Total_Household_Asset_Value + log_Total_Production_Asset_Value + ZoneID_1 + ZoneID_3 + ZoneID_4 + A03_Age + A05_Edu + Household_Size + A07_1_Main_occupatn_Farming + A07_1_Main_occupatn_Self_employed_off_farm + A07_1_Main_occupatn_Other + A08_fam_lab_contributn | A02_Sex  | ZoneID_1 + ZoneID_3 + ZoneID_4

# result1 <- oaxaca(formula_1, data=df, R=100)
resultDNA <- oaxaca(formula_dna,data=df, reg.fun = glm, family = binomial(link = 'probit'),R=30)
resultDNA['threefold']
print(result1)
summary(result1)

extra = "reg.fun = glm, family = binomial(link = 'probit')"
library(oaxaca)
results <- oaxaca(formula = formula_1, data=df, {extra}, R=100)
results_dna <- oaxaca(formula = formula_dna, data=df, {extra}, R=100)


df <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/df_FM_Update.csv")

results <- oaxaca(formula = self_mag_icv ~ J02_per_hh_inc_cassav + Joint_Coop + Credit_Access + log_Total_Household_Asset_Value + log_Total_Production_Asset_Value + ZoneID_1 + ZoneID_3 + ZoneID_4 + A03_Age + A05_Edu + Household_Size + A07_1_Main_occupatn_Farming + A07_1_Main_occupatn_Self_employed_off_farm + A07_1_Main_occupatn_Other + A08_fam_lab_contributn | A02_Sex  | ZoneID_1 + ZoneID_3 + ZoneID_4, data=df, reg.fun = glm, family = binomial(link = "probit"), R=100)



results <- oaxaca(formula = self_mag_icv ~ J02_per_hh_inc_cassav + Joint_Coop + Credit_Access + log_Total_Household_Asset_Value + log_Total_Production_Asset_Value + ZoneID_1 + ZoneID_3 + ZoneID_4 + A03_Age + A05_Edu + Household_Size + A07_1_Main_occupatn_Farming + A07_1_Main_occupatn_Self_employed_off_farm + A07_1_Main_occupatn_Other + A08_fam_lab_contributn | A02_Sex  | ZoneID_1 + ZoneID_3 + ZoneID_4, data=df, reg.fun = glm, family = binomial(link = "probit"), R=100)


results$y
plot(results, components = c('endowments','coefficients'))


dfSelfMag <- read.csv(paste0(OutputDir,'/dfSefMag.csv'))=

results <- oaxaca(
  formula = selfMagIcv ~ G_Coop + G_Credit + G_Ext_Only + G_CellValue + 
    Fertilizer + Consump.perc + Zone1 + Zone3 + 
    Zone4 + Age + Education + `Household.size` + 
    Main.occupation..Salaried.employment | A02_Sex | Zone1 + Zone3 + Zone4,
  data = dfSelfMag,
  reg.fun = glm,
  family = binomial(link = "probit"),
  R = 100
)





dfSelfMag <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/dfSefMag.csv")
results <- oaxaca(
  formula = selfMagIcv ~ G_Coop + G_Credit + G_Ext_Only + G_CellValue + 
    Fertilizer + Consump.perc + Zone1 + Zone3 + 
    Zone4 + Age + Education + `Household.size` + 
    Main.occupation..Salaried.employment | A02_Sex | Zone1 + Zone3 + Zone4,
  data = dfSelfMag,
  reg.fun = glm,
  family = binomial(link = "probit"),
  R = 100
)


dfHead <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/head.csv")
results <- oaxaca(
  formula = DNA_planted  ~ Coop_Group_Member+Credit_Access+Extension_Access+CellAssValThd
  +J01_hhd_apply_fert+J05_consumption_perc+ ZoneID_1 + ZoneID_3 + 
    ZoneID_4 + A03_Age + A05_Edu + Household_Size + 
    A07_1_Main_occupatn_Salaried_employment | A02_Sex | ZoneID_1 + ZoneID_3 + 
    ZoneID_4,
  data = dfHead,
  reg.fun = glm,
  family = binomial(link = "probit"),
  R = 100
)

resultDNA['threefold']
print(results)
summary(result1)




df <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/df_FM_test.csv")

df <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/df_FM_Update.csv")

results <- oaxaca(formula = selfMagIcv ~ Coop_Group_Member + Credit_Access + Extension_Access + J05_consumption_perc + ZoneID_1 + ZoneID_3 + ZoneID_4 + A03_Age + A05_Edu + Household_Size + A07_1_Main_occupatn_Salaried_employment | A02_Sex  | ZoneID_1 + ZoneID_3 + ZoneID_4, data=df, reg.fun = glm, family = binomial(link = "probit"), R=100)

df_f_self <- subset(df,A02_Sex==0)
df_m_self <- subset(df,A02_Sex==1)
