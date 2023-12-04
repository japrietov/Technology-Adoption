# This script is developed for the measurement error study
# Copyright: Jing Yi, Email: jy348@cornell.edu
import random
import numpy as np
import statsmodels.api as sm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
import scipy.stats as stats
from scipy.stats import fisher_exact
from scipy.stats import ttest_ind
from scipy.stats.stats import pearsonr

import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_row', 10)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


WorkingDir = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Gender\MeasureError"

import pyreadstat
TempDir = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Gender\ExistingCode"
df_hh, meta = pyreadstat.read_sav(TempDir + "/MethodsPaperDataSet_HH.sav")
df_hh.head()
df_hh.shape

df_hh.to_excel(WorkingDir + "//Data//HH.xlsx")

df_ind, meta = pyreadstat.read_sav(TempDir + "/MethodsPaperDataSet_Indivs.sav")
df_ind.head()
df_ind.shape
df_ind.to_excel(WorkingDir + "//Data//Ind.xlsx")

df_all = pd.merge(df_hh, df_ind, on='HouseID')
df_all['HH_Ind'] = df_all.groupby(['HouseID']).ngroup()
first_col = df_all.pop('HH_Ind')
df_all.insert(0, 'HH_Ind',first_col)
print(df_all.head(1))
df_all.to_excel(WorkingDir +"//Data//All.xlsx")

# ----------------------------New section starts from here-------------------------------#
# ----------------------------New section starts from here-------------------------------#
WorkingDir = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Gender\MeasureError"
df_all = pd.read_excel(WorkingDir + "//Data//HH.xlsx")

df_all['HH_Ind'] = df_all.groupby(['HouseID']).ngroup()
first_col = df_all.pop('HH_Ind')
df_all.insert(0, 'HH_Ind',first_col)
df_all = df_all.drop("Unnamed: 0",axis=1)
df_all = df_all.sort_values("HH_Ind")
df_all.head()

df_all.HH_Ind.unique()
# icv_cols = [col for col in df_all.columns if 'ICV' in col]
# df_ICV = pd.DataFrame(icv_cols, columns=["ICV_cols"])

df_all["Dif_m"] = df_all["M_ICV_Managed_Male"] - df_all["F_ICV_Managed_Male"]
df_all["Dif_m_mean"] = (df_all["M_ICV_Managed_Male"] + df_all["F_ICV_Managed_Male"])/2
df_all["Dif_m_mean_diff"] =  df_all["M_ICV_Managed_Male"] - df_all["Dif_m_mean"]
df_all["Dif_f_mean_diff"] =  df_all["F_ICV_Managed_Male"] - df_all["Dif_m_mean"]
df_all["Dif_m_mean_diff_pct"] = df_all["Dif_m_mean_diff"]/df_all["Dif_m_mean"]
df_all["Dif_f_mean_diff_pct"] = df_all["Dif_f_mean_diff"]/df_all["Dif_m_mean"]


df_all['Dif_m_pct'] = df_all["Dif_m"] /df_all["Dif_m_mean"]
df_all["Dif_f"] = df_all["M_ICV_Managed_Female"] - df_all["F_ICV_Managed_Female"]
df_all["Dif_f_mean"] = (df_all["M_ICV_Managed_Female"] + df_all["F_ICV_Managed_Female"])/2
df_all['Dif_f_pct'] = df_all["Dif_f"] /df_all["Dif_f_mean"]
df_all["Dif_j"] = df_all["M_ICV_Managed_Joint"] - df_all["F_ICV_Managed_Joint"]
df_all["m_tot"] =  df_all["M_ICV_Managed_Male"] +df_all["M_ICV_Managed_Female"] +df_all["M_ICV_Managed_Joint"]
df_all["f_tot"] =  df_all["F_ICV_Managed_Male"] +df_all["F_ICV_Managed_Female"] +df_all["F_ICV_Managed_Joint"]
df_all["Dif_tot"] = df_all["m_tot"] - df_all["f_tot"]

sns.kdeplot(df_all['m_tot'], shade=True, color="b", label ="Male")
sns.kdeplot(df_all['f_tot'], shade=True, color="r", label ="Female")
plt.legend()
plt.title("Household total ICV")
plt.show()


d1_m =df_all['M_ICV_HH_yn'].sum()/df_all.shape[0]
d1_f = df_all['F_ICV_HH_yn'].sum()/df_all.shape[0]
scipy.stats.ttest_ind(df_all['M_ICV_HH_yn'], df_all['F_ICV_HH_yn'])
# different: they came from two distributions

df_all.shape[0]*0.1
df_sample_fe = df_all.sample(73)
df_sample_fe.shape
df_sample_ma = df_all.drop(df_sample_fe.index)
df_sample_ma.shape
df_sample_1 = df_sample_fe['F_ICV_HH_yn'].append(df_sample_ma['M_ICV_HH_yn'])
df_sample_1 = pd.DataFrame(df_sample_1,columns=['ICV_HH_yn'])
df_sample_1.sum()/df_all.shape[0]
rate = 0.2
random.seed(42)
def sudo_share(rate):
    num = int(df_all.shape[0]*rate)
    df_sample_fe =  df_all.sample(num)
    df_sample_ma = df_all.drop(df_sample_fe.index)
    df_sample_i = df_sample_fe['F_ICV_HH_yn'].append(df_sample_ma['M_ICV_HH_yn'])
    df_sample_i = pd.DataFrame(df_sample_i, columns=['ICV_HH_yn'])
    Adop_rate = df_sample_i.sum() / df_all.shape[0]
    return [df_sample_i,Adop_rate]

df_sample_0,Adop_rate_0 = sudo_share(0)
df_sample_1,Adop_rate_1 = sudo_share(0.1)
df_sample_2,Adop_rate_2 = sudo_share(0.2)
df_sample_3,Adop_rate_3 = sudo_share(0.3)
df_sample_4,Adop_rate_4 = sudo_share(0.4)
df_sample_5,Adop_rate_5 = sudo_share(0.5)
df_sample_6,Adop_rate_6 = sudo_share(0.6)
df_sample_7,Adop_rate_7 = sudo_share(0.7)
df_sample_8,Adop_rate_8 = sudo_share(0.8)
df_sample_9,Adop_rate_9 = sudo_share(0.9)
df_sample_10,Adop_rate_10 = sudo_share(1)

df_sudo = pd.concat([df_sample_0,df_sample_1,df_sample_2,df_sample_3,df_sample_4,df_sample_5,df_sample_6,df_sample_7,df_sample_8,df_sample_9,df_sample_10], axis=1)
df_sudo.columns = [['0','1','2','3','4','5','6','7','8','9','10']]
dct = {x: {y: ttest_ind(df_sudo[x], df_sudo[y]).pvalue for y in df_sudo} for x in df_sudo}
mat = pd.DataFrame(dct)
print(mat)
mat.to_csv(WorkingDir+"\\MeasurementError\\adoption.csv", sep='|', index=False)
df_rate = pd.concat([Adop_rate_0,Adop_rate_1,Adop_rate_2,Adop_rate_3, Adop_rate_4, Adop_rate_5, Adop_rate_6, Adop_rate_7, Adop_rate_8, Adop_rate_9, Adop_rate_10])
df_rate.to_csv(WorkingDir+"\\MeasurementError\\adoptionRate.csv", sep='|', index=False)

df_rate = pd.read_csv(WorkingDir+"\\MeasurementError\\rate.csv")
df_rate = pd.read_clipboard()
# fractional logiit model:
Y = df_rate['AdoptionRate']
X = sm.add_constant(df_rate['Female'])
X =  df_rate['Female']
mod = sm.Logit(Y,X)
mod = sm.OLS(Y,X)
res = mod.fit()
print(res.summary())

pearsonr(Y,X)
# df_diff = df_all[["Dif_m","Dif_f","Dif_j","Dif_tot","Dif_m_mean",'Dif_m_mean_diff','Dif_f_mean_diff','Dif_m_mean_diff_pct','Dif_f_mean_diff_pct']]
# df_diff.describe()
# df_all['Ever'] = df_all['M_ICV_HH_yn']
df_all.to_csv(WorkingDir+"\\MeasurementError\\hh.csv", sep='|', index=False)
df_all['M_ICV_Managed_Male'].describe()
df_all = pd.read_csv(WorkingDir+"\\MeasurementError\\hh.csv",sep='|')
# df_all = df_all[["Name1", "HouseID","M_ICV_Managed_Male","F_ICV_Managed_Male","M_ICV_Managed_Female", "F_ICV_Managed_Female", "M_ICV_Managed_Joint", "F_ICV_Managed_Joint"]]
df_all["Dif_m"] = df_all["M_ICV_Managed_Male"] - df_all["F_ICV_Managed_Male"]
df_all["Dif_f"] = df_all["M_ICV_Managed_Female"] - df_all["F_ICV_Managed_Female"]
df_all["Dif_j"] = df_all["M_ICV_Managed_Joint"] - df_all["F_ICV_Managed_Joint"]
df_all["M_tot"] =  df_all["M_ICV_Managed_Male"] +df_all["M_ICV_Managed_Female"] +df_all["M_ICV_Managed_Joint"]
df_all["F_tot"] =  df_all["F_ICV_Managed_Male"] +df_all["F_ICV_Managed_Female"] +df_all["F_ICV_Managed_Joint"]
df_all["Dif_tot"] = df_all["M_tot"] - df_all["F_tot"]
df_all.to_csv(WorkingDir+"\\MeasurementError\\hh.csv", sep='|', index=False)

# df_all.describe()

# Compbdt: an R program to compare two binary diagnostic tests subject to a paired design
# Download PDF

sns.kdeplot(df_all['M_ICV_HH_yn'], shade=True, color="b", label ="Male")
sns.kdeplot(df_all['F_ICV_HH_yn'], shade=True, color="r", label ="Female")
plt.legend()
plt.title("ICV_HH_yn")
plt.show()

#  paired samples T-Test:
stats.ttest_rel(df_all['m_icv_hh_yn'], df_all['f_icv_hh_yn'])
stats.ttest_rel(df_all['m_icv_managed_male'], df_all['f_icv_managed_male'])
stats.ttest_rel(df_all['m_icv_managed_female'], df_all['f_icv_managed_female'])
stats.ttest_rel(df_all['m_icv_managed_joint'], df_all['f_icv_managed_joint'])
stats.ttest_rel(df_all['m_tot'], df_all['f_tot'])

stats.fisher_exact(df_all['m_icv_hh_yn'], df_all['f_icv_hh_yn'])
boxplot = df_all.boxplot(column=['m_icv_hh_yn','f_icv_hh_yn'])
plt.show()

df_all[['m_icv_hh_yn','f_icv_hh_yn']].describe()


df_all.M_Household_assets.head()



sns.kdeplot(df_all['M_ICV_Managed_Male'], shade=True, color="b", label ="Male")
sns.kdeplot(df_all['F_ICV_Managed_Male'], shade=True, color="r", label ="Female")
plt.legend()
plt.show()

sns.ecdfplot(df_all['M_ICV_Managed_Male'],  label ="Male")
sns.ecdfplot(df_all['F_ICV_Managed_Male'],  label ="Female")
plt.legend()
plt.show()

sns.ecdfplot(df_all['m_tot'],  label ="Male")
sns.ecdfplot(df_all['f_tot'],  label ="Female")
plt.legend()
plt.show()


sns.ecdfplot(df_all['M_ICV_HH_yn'],  label ="Male")
sns.ecdfplot(df_all['F_ICV_HH_yn'],  label ="Female")
plt.legend()
plt.show()

sns.ecdfplot(df_all['M_ICV_HH_yn'],  label ="Male")
sns.ecdfplot(df_all['F_ICV_HH_yn'],  label ="Female")
sns.ecdfplot(df_all['Household_ICV'],  label ="HH")
plt.legend()
plt.show()
df_all['Male_Ext_Only'].head()
sns.ecdfplot(df_all['Extension_Access'],  label ="HH")
sns.ecdfplot(df_all['Male_Ext_Only'],  label ="Male")
sns.ecdfplot(df_all['Female_Ext_Only'],  label ="Female")
plt.legend()
plt.show()


df_all['Male_Ext_Only'].value_counts().plot(kind='bar')
plt.title('Male_Ext_Only')
plt.tight_layout()
plt.show()
df_all['Female_Ext_Only'].value_counts().plot(kind='bar')
plt.title('Female_Ext_Only')
plt.tight_layout()
plt.show()

# Create the figure and subplots
fig, ax = plt.subplots(figsize=(12, 10))

# Create the heatmap
sns.heatmap(sorted_correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Top 20 Important Features Heatmap with Targets (Sorted by Diff_ICV_HH_yn)')

# Adjust the position of the heatmap to the right
plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)

plt.show()



sns.ecdfplot(df_all['M_Age'],  label ="Male")
sns.ecdfplot(df_all['F_Age'],  label ="Female")
plt.legend()
plt.show()


sns.ecdfplot(df_all['M_Edu'],  label ="Male")
sns.ecdfplot(df_all['F_Edu'],  label ="Female")
plt.legend()
plt.show()
df_all['M_Edu'].describe()
df_all['F_Edu'].describe()

from scipy.stats import ks_2samp
import numpy as np
# olmogorov–Smirnov test
ks_2samp(df_all['M_ICV_HH_yn'], df_all['F_ICV_HH_yn'])
# the distributions are different
ks_2samp(df_all['m_tot'], df_all['f_tot'])
# the distributions are different

from scipy.stats.stats import pearsonr
pearsonr(df_all['m_tot'], df_all['f_tot'])
import scipy.stats
scipy.stats.spearmanr(df_all['M_ICV_HH_yn'], df_all['F_ICV_HH_yn'])
scipy.stats.kendalltau(df_all['M_ICV_HH_yn'], df_all['F_ICV_HH_yn'])

import statsmodels.api as sm
result = sm.OLS(df_all['M_ICV_HH_yn'], x).fit()
# gps data:
df_gps = pd.read_csv(WorkingDir+"//Data//gps_data_offset.csv")
print(df_gps.head(10))

df_all.columns= df_all.columns.str.lower()
df_all.head()
asset_cols = [col for col in df_all.columns.str.strip().str.lower() if 'asset' in col]
asset_cols = [col for col in df_all.columns if 'Asset' in col]

df_asset_cols = pd.DataFrame(asset_cols, columns=["asset_cols"])

df_asset = df_all[np.intersect1d(df_all.columns,asset_cols)]
df_asset.describe()
df_all.f_total_processing_asset_hh.head()

c = ["M_HHAsset_Value_Male","F_HHAsset_Value_Male"]
c = ['M_HHAsset_Value_Female','F_HHAsset_Value_Female']
c = ["M_HHAsset_Production_Value","F_HHAsset_Production_Value"]
c = ['M_HHAsset_Production_Value','F_HHAsset_Production_Value']
df_ass_1 = df_all[c]
df_ass_1_m = pd.melt(df_ass_1)
df_ass_1_m.head()
import matplotlib.pyplot as plt
import seaborn as sns
sns.boxplot(x='variable', y='value', data=df_ass_1_m, showfliers=False)
plt.show()

sns.ecdfplot(df_all['M_HHAsset_Value_Male'],  label ="Male")
sns.ecdfplot(df_all['F_HHAsset_Value_Male'],  label ="Female")
plt.legend()
plt.show()


# Temp = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\Research\GlobalFoodDollar\fao2022\fao2022Github\GlobalFoodValueShare\ConferenceMay_2023_ICAS"
# df_temp = pd.read_csv(Temp+'/FAOSTAT_data_en_2-13-2023FAH.csv')
# df_temp.head()
# import matplotlib.pyplot as plt
# plt.scatter(df_temp.Area, df_temp.Value)
# plt.show()
#
# from statsmodels.stats.contingency_tables import mcnemar
# data1 = df_all[["M_ICV_Managed_Female","F_ICV_Managed_Female" ]]
# print(mcnemar(data1, exact=False))
# file = r"D:\Dropbox\BoxOld\FEDSshare\healthcare\Healthcare2023"
# df_health = pd.read_csv(file+'/Project Groups- Spring 2023.csv')
# df_health.to_csv(file+"/2023_1.csv",sep="|",index=False)
#
sns.ecdfplot(df_all['M_HHAsset_Value_Total'],  label ="Male")
sns.ecdfplot(df_all['F_HHAsset_Value_Total'],  label ="Female")
plt.legend()
plt.show()
df_temp = df_all[["HouseID","M_HHAsset_Value_Total","F_HHAsset_Value_Total"]]
df_temp = df_all[["M_HHAsset_Value_Total","F_HHAsset_Value_Total"]]
df_all['diff_value_total'] = df_all["M_HHAsset_Value_Total"] -  df_all["F_HHAsset_Value_Total"]
df_temp.plot(style=['o','rx'])
plt.show()

sns.distplot(df_all["diff_value_total"], hist=False, kde=True, label='diff_value_total',
                  kde_kws={'linestyle': '--'})
plt.show()

sns.ecdfplot(df_all['diff_value_total'],  label ="diff_value_total")
plt.show()

from scipy.stats import ks_2samp
import numpy as np
# kolmogorov–Smirnov test
ks_2samp(df_all['M_HHAsset_Value_Total'], df_all['F_HHAsset_Value_Total'])

plt.scatter(df_all['F_HHAsset_Value_Total'],df_all['M_HHAsset_Value_Total'], color='red')
plt.xlabel('F_HHAsset_Value_Total')
plt.ylabel('M_HHAsset_Value_Total')
plt.show()

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

data = pd.read_excel(r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Gender\MeasureError\MeasurementError\MeasureError" +'/hh_r.xlsx')
data = data.dropna()
# Select columns with prefix 'M_'
M_columns = [col for col in data.columns if col.startswith('M_')]
# Select columns with prefix 'F_'
F_columns = [col for col in data.columns if col.startswith('F_')]
# Create a new column 'Diff_'
data['Diff_'] = data[F_columns].sum(axis=1) - data[M_columns].sum(axis=1)

# 'M_ICV_HH_yn', 'F_ICV_HH_yn'
# Separate features and targets
features = data.drop(['Diff_ICV_HH_yn'], axis=1)
targets = data[['Diff_ICV_HH_yn' ]]

# Create a Random Forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf.fit(features, targets)

# Get feature importances
importances = rf.feature_importances_

# Get feature names
feature_names = features.columns

# Sort feature importances in descending order
indices = importances.argsort()[::-1]

# Print feature importance ranking
print("Feature importance ranking:")
# for i in range(len(feature_names)):
for i in range(30):

    print(f"{i + 1}. {feature_names[indices[i]]}: {importances[indices[i]]}")

# Plot feature importances
plt.figure()
plt.title("Feature Importance")
plt.bar(range(len(feature_names)), importances[indices])
plt.xticks(range(len(feature_names)), feature_names[indices], rotation='vertical')
plt.show()


# Create a DataFrame for feature importances
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
# Sort feature importances in descending order
importance_df = importance_df.sort_values('Importance', ascending=False)
# Export feature importances to an Excel file
importance_df.to_excel(r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Gender\MeasureError\MeasurementError\MeasureError" +'/feature_importances_diff.xlsx', index=False)


top_features = importance_df.head(20)['Feature'].tolist()

top_features.insert(0, 'Diff_ICV_HH_yn')

correlation_matrix = data[top_features ].corr()
sorted_correlation_matrix = correlation_matrix.sort_values('Diff_ICV_HH_yn', ascending=False)

plt.figure(figsize=(12, 10))
sns.heatmap(sorted_correlation_matrix, annot=True, cmap='coolwarm', xticklabels=True)
plt.title('Top 20 Important Features Heatmap with Targets (Sorted by Diff_ICV_HH_yn)')
plt.xticks(rotation=90)
plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.3)

plt.show()

# drop variables from the datasets, such as bike, etc.
# M_ICV_Managed_Male/Female/joint
# find min(diff)
# RUN THIS BY REGION
# ADJUST "MORE CO-orporative household" use some weights
# use plantedd as the dependant variable
