# ------------------------------------# ------------------------------------
    # planted: binary
    # DNA_Household_ICV: counts
    # householdICV: counts
    #
    # df_F_test = df_FM_test[df_FM_test['A02_Sex'] == 0].rename(columns=variables_dict)
    # df_M_test = df_FM_test[df_FM_test['A02_Sex'] == 1].rename(columns=variables_dict)
# ------------------------------------# ------------------------------------

# In[1]:
# py37lib = r"C:\Users\jingy\AppData\Local\Programs\Python\Python37\Scripts"
import sys
# sys.path.append(py37lib)
major, minor, micro = sys.version_info[:3]
print(f"Your Python version is {major}.{minor}.{micro}")
from matplotlib.ticker import FuncFormatter
from scipy.stats import ks_2samp

import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba
import matplotlib

matplotlib.use('TkAgg')

import numpy as np
from scipy.stats import t
from scipy.stats import norm
from scipy.stats import ttest_rel
from numpy.linalg import inv
import warnings
import roman
import random

sns.set_style('whitegrid')
warnings.filterwarnings('ignore')

import rpy2
from rpy2 import robjects
import rpy2.robjects as ro
from rpy2.robjects.packages import importr, data
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
import logging

rpy2_logger.setLevel(logging.ERROR)

import rpy2.rinterface as ri
ri.initr()

from statsmodels.stats.outliers_influence import variance_inflation_factor

utils = importr('utils')
base = importr('base')
oaxaca = importr('oaxaca')

pd.set_option('max_columns', 10)


WorkDir = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Code\DataSynthesis\MeasureError\Gender\MeasureError\AJAE_2023\Technology-Adoption"
DataDir = WorkDir + '/Data'
OutputDir = WorkDir + '/Output'


# # 1. Montecarlo Analysis

# In[208]:


#########################################################################
# Create pseudo-datasets with different percentage of Male/female answers
# input: Dataset and percentage of female answers
# output: pseudo-dataset with the ICV_HH_yn values and Adop_rate.
#########################################################################


def update_resultsOri(resulst_dict_threefold, ind, char, variables_dict, base=[], part='all'):
    columns_names = ['coef(endowments)', 'se(endowments)', 'coef(coefficients)', 'se(coefficients)',
        'coef(interaction)', 'se(interaction)']

    df_overall = pd.DataFrame(np.array([resulst_dict_threefold['overall']]), columns=columns_names)
    df_overall['endowments'] = df_overall[['coef(endowments)', 'se(endowments)']].apply(update_tab,
        axis=1)
    df_overall['coefficients'] = df_overall[['coef(coefficients)', 'se(coefficients)']].apply(
        update_tab, axis=1)
    df_overall['interaction'] = df_overall[['coef(interaction)', 'se(interaction)']].apply(
        update_tab, axis=1)
    df_overall = df_overall[['endowments', 'coefficients', 'interaction']]
    df_overall = pd.concat([df_overall[col].explode(ignore_index=True) for col in df_overall],
        axis="columns")
    df_overall.index = ['Agregate decomposition', '']

    df_overall_shared = df_overall.loc['Agregate decomposition'].to_frame().T.apply(
        lambda x: share_gap(x), axis=1)
    df_overall.loc[len(df_overall.index)] = df_overall_shared.values[0]
    df_overall.loc[len(df_overall.index)] = ['', '', '']
    df_overall.index = ['Agregate decomposition', '', 'Share of the gap', 'Detailed decomposition']

    df_variables = pd.DataFrame(np.array(resulst_dict_threefold['variables']),
        index=['constant'] + ind + char + base, columns=columns_names)
    df_variables = df_variables.rename(index=variables_dict)

    df_variables['endowments'] = df_variables[['coef(endowments)', 'se(endowments)']].apply(
        update_tab, axis=1)
    df_variables['coefficients'] = df_variables[['coef(coefficients)', 'se(coefficients)']].apply(
        update_tab, axis=1)
    df_variables['interaction'] = df_variables[['coef(interaction)', 'se(interaction)']].apply(
        update_tab, axis=1)
    df_variables = df_variables[['endowments', 'coefficients', 'interaction']]
    old_index = df_variables.index
    df_variables = pd.concat([df_variables[col].explode(ignore_index=True) for col in df_variables],
        axis="columns")
    new_index = [""] * (2 * len(old_index) - 1)

    df_variables.index = list(joinit(old_index, '')) + ['']

    df_results = pd.concat([df_overall, df_variables])
    if part == 'overall':
        return df_overall
    elif part == 'variables':
        return df_variables
    else:
        return df_results


def update_results(resulst_dict_threefold, ind, char, variables_dict, base=[], part='all'):
    columns_names = ['coef(endowments)', 'se(endowments)', 'coef(coefficients)', 'se(coefficients)',
        'coef(interaction)', 'se(interaction)']

    df_overall = pd.DataFrame(np.array([resulst_dict_threefold['overall']]), columns=columns_names)
    df_overall['endowments'] = df_overall[['coef(endowments)', 'se(endowments)']].apply(update_tab,
        axis=1)
    df_overall['coefficients'] = df_overall[['coef(coefficients)', 'se(coefficients)']].apply(
        update_tab, axis=1)
    df_overall['interaction'] = df_overall[['coef(interaction)', 'se(interaction)']].apply(
        update_tab, axis=1)
    df_overall = df_overall[['endowments', 'coefficients', 'interaction']]
    df_overall = pd.concat([df_overall[col].explode(ignore_index=True) for col in df_overall],
        axis="columns")
    df_overall.index = ['Aggregate decomposition', '']

    df_overall_shared = df_overall.loc['Aggregate decomposition'].to_frame().T.apply(
        lambda x: share_gap(x), axis=1)
    df_overall.loc[len(df_overall.index)] = df_overall_shared.values[0]
    df_overall.loc[len(df_overall.index)] = ['', '', '']
    df_overall.index = ['Aggregate decomposition', '', 'Share of the gap', 'Detailed decomposition']

    df_variables = pd.DataFrame(np.array(resulst_dict_threefold['variables']),
        index=['constant'] + ind + char + base, columns=columns_names)
    df_variables = df_variables.rename(index=variables_dictDeco)

    df_variables['endowments'] = df_variables[['coef(endowments)', 'se(endowments)']].apply(
        update_tab, axis=1)
    df_variables['coefficients'] = df_variables[['coef(coefficients)', 'se(coefficients)']].apply(
        update_tab, axis=1)
    df_variables['interaction'] = df_variables[['coef(interaction)', 'se(interaction)']].apply(
        update_tab, axis=1)
    df_variables = df_variables[['endowments', 'coefficients', 'interaction']]
    old_index = df_variables.index
    df_variables = pd.concat([df_variables[col].explode(ignore_index=True) for col in df_variables],
        axis="columns")
    new_index = [""] * (2 * len(old_index) - 1)

    df_variables.index = list(joinit(old_index, '')) + ['']

    df_results = pd.concat([df_overall, df_variables])
    if part == 'overall':
        return df_overall
    elif part == 'variables':
        return df_variables
    else:
        return df_results


def sudo_share(df_M, df_F, rate,variable):
    # print(df.shape)

    num_fe = int(df_F.shape[0]*rate)
    num_ma = int(df_M.shape[0]*(1-rate))
    df_sample_fe =  df_F.sample(num_fe)
    df_sample_ma = df_M.sample(num_ma)
    df_sample_fe = df_sample_fe[[variable, 'ZoneID']]
    df_sample_ma = df_sample_ma[[variable, 'ZoneID']]
    df_sample_i = pd.concat([df_sample_fe, df_sample_ma])
    df_sample_i['F_Rate'] = rate
    # df_sample_i = np.concatenate((df_sample_fe[variable, 'ZoneID'].values, df_sample_ma[variable,'ZoneID'].values))
    # df_sample_i = pd.DataFrame(df_sample_i, columns=[variable])
    # Adop_rate = df_sample_i.sum() / df_sample_i.shape[0]
    # Adop_rate_Zone = df_sample_i.groupby('ZoneID').sum() / df_sample_i.groupby('ZoneID').count()
    # Adop_rate_Zone.reset_index(inplace=True)
    # return [df_sample_i, Adop_rate,Adop_rate_Zone]
    return df_sample_i

# Weighted selection: p_i is the probability of selecting element i
def weighted(p):
    y = random.random()
    k=0
    while k<len(p) and y>=p[k]:
        y -= p[k]
        k+=1
    return k

df_FM_test = pd.read_csv(OutputDir + "/df_FM.csv")
# df_FM_test.to_csv(OutputDir +'/df_FM_test.csv',sep='|',index=False)
p = (df_FM_test['ZoneID'].value_counts()/df_FM_test['ZoneID'].value_counts().sum()).sort_index().values

dependent_self_reported = ['planted', 'Household_ICV']
dependent_DNA = ['DNA_planted', 'DNA_Household_ICV']

df_F_test = df_FM_test[df_FM_test['A02_Sex'] == 0].rename(columns=variables_dict)
df_M_test = df_FM_test[df_FM_test['A02_Sex'] == 1].rename(columns=variables_dict)
dep_self =  list(map(lambda x: variables_dict[x], dependent_self_reported))

experiment = {y:[] for y in dep_self}
y = 'Y/N ICV'
# for y in dep_self:

df_sudo = pd.DataFrame()
for i in range(5):
    # print(i)
    df_adop_rate = []
    adopt_rate_zone = []

    df_sudo_cluster = []
    df_adop_rate_cluster = []
    for percentage in np.arange(0, 1.1, 0.1):
        # print(percentage)
        # df_sample, adop_rate, adopt_rate_zone = sudo_share(df_M_test, df_F_test, round(percentage, 1), y)
        df_sample  = sudo_share(df_M_test, df_F_test, round(percentage, 1), y)
        df_sample['Iteration'] = int(i)
        df_sudo = df_sudo.append(df_sample)
df_sudo.to_csv(OutputDir +'/sudoRate_5.csv',sep='|',index=False)

df_sudo =pd.read_csv(OutputDir +'/sudoRate_500Ite.csv',sep='|')
df_sudo =pd.read_csv(OutputDir +'/sudoRate_5.csv',sep='|')

Adop_rate = df_sudo.groupby(['F_Rate','Iteration'])['Y/N ICV'].sum() / df_sudo.groupby(['F_Rate','Iteration'])['Y/N ICV'].count()
Adop_rate = pd.DataFrame({'Adop_rate': Adop_rate})
Adop_rate.reset_index(inplace=True)

Adop_rate_Zone = df_sudo.groupby(['ZoneID','F_Rate','Iteration'])['Y/N ICV'].sum() / df_sudo.groupby(['ZoneID','F_Rate','Iteration'])['Y/N ICV'].count()
Adop_rate_Zone = pd.DataFrame({'adop_rate_zone': Adop_rate_Zone})
Adop_rate_Zone.reset_index(inplace=True)

def percentage_formatter(x, pos):
    return f'{x * 100:.0f}%'

fig1, ax1 = plt.subplots(dpi=100)
sns.lineplot(ax=ax1, data=Adop_rate,x='F_Rate',y='Adop_rate',  markers=True,errorbar=("se", 2) )
ax1.yaxis.set_major_formatter(FuncFormatter(percentage_formatter))
ax1.set_title(y, fontweight='bold')
ax1.set_xlabel('Percentage of Female', fontweight='bold')
ax1.set_ylabel('Adoption rate' , fontweight='bold')
# plt.savefig(OutputDir+'/Figure/AdopRate_500.png',dpi = 2000)
plt.savefig(OutputDir+'/Figure/AdopRate_5.png',dpi = 2000)
plt.show()

fig1, ax1 = plt.subplots(dpi=100)
sns.lineplot(
    ax=ax1,    data=Adop_rate_Zone,    x='F_Rate',    y='adop_rate_zone',
    markers=True,    err_style='band',    hue='ZoneID',    style='ZoneID'
)
ax1.yaxis.set_major_formatter(FuncFormatter(percentage_formatter))
ax1.set_title(y, fontweight='bold')
ax1.set_xlabel('Percentage of Female', fontweight='bold')
ax1.set_ylabel('Adoption rate', fontweight='bold')
ax1.legend(loc='upper right', title='Zone',bbox_to_anchor=(0.95,0.5))
# plt.savefig(OutputDir + '/Figure/AdopRateZone_500.png', dpi=2000)
plt.savefig(OutputDir + '/Figure/AdopRateZone_5.png', dpi=2000)
plt.show()


# # 2. Regressions
# Run 4 regressions:
# - $Y_{husband} = X_{husband} \beta + C + \epsilon$
# - $Y_{wife} = X_{wife} \beta + C + \epsilon$
# - $Y_{DNA} = X_{husband} \beta + C + \epsilon$
# - $Y_{DNA} = X_{wife} \beta + C + \epsilon$


dependent_self_reported = ['planted']
dependent_DNA = ['DNA_planted']

characteristic = ['ZoneID_1', 'ZoneID_3', 'ZoneID_4', # ZoneID_2 is base
                  'A03_Age', 'A05_Edu', 'Household_Size',
                  'A07_1_Main_occupatn_Farming', 'A07_1_Main_occupatn_Self_employed_off_farm',
                  'A07_1_Main_occupatn_Other', # A07_1_Main_occupatn_Salaried_employment is base
                  'A08_fam_lab_contributn']

characteristic = ['ZoneID_1', 'ZoneID_3', 'ZoneID_4', # ZoneID_2 is base
                  'A03_Age', 'A05_Edu', 'Household_Size',
                  'A07_1_Main_occupatn_Farming',  # A07_1_Main_occupatn_Salaried_employment is base
                  'A08_fam_lab_contributn']
test =df_FM_test = pd.read_csv(OutputDir + "/df_FM.csv")
test = df_FM_test[['ZoneID_1', 'ZoneID_2','ZoneID_3', 'ZoneID_4']]
test.sum(axis=0)

y_self = 'Y/N ICV'
Y = df_F_test[y_self]
X = sm.add_constant(df_F_test[ind + char], prepend=False)
model_F = sm.Probit(Y, X)
results_F = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_F_test['ZoneID'].values}, maxiter=100, )
results_F.summary2()
results.append(results_F)

model_lg = sm.Logit(Y,X)
results_F_lg = model_lg.fit(cov_type='cluster', cov_kwds={'groups': df_F_test['ZoneID'].values}, maxiter=100, )

results_F_lg.summary2()

##############################################
# Self-reported regressions
##############################################
results = []

# Husband

y_self = ['Y/N ICV']
Y = df_M_test[y_self]
X = sm.add_constant(df_M_test[ind + char], prepend=False)
model_F = sm.Probit(Y, X) if y_self == 'Y/N ICV' else sm.OLS(Y, X)
results_H_self = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_M_test['ZoneID'].values}, maxiter=100, )
results.append(results_H_self)
print(results_H_self.summary2())
# Wife
Y = df_F_test[y_self]
X = sm.add_constant(df_F_test[ind + char], prepend=False)
model_F = sm.Probit(Y, X) if y_self == 'Y/N ICV' else sm.OLS(Y, X)
results_F_self = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_F_test['ZoneID'].values}, maxiter=100, )
results.append(results_F_self)

results = []
dep_self = ['Y/N ICV']
dep_dna = ['DNA Y/N ICV']
for y_self, y_DNA in zip(dep_self, dep_dna):
    ##############################################
    # Self-reported regressions
    ##############################################
    # Husband
    Y = df_M_test[y_self]
    X = sm.add_constant(df_M_test[ind + char], prepend=False)
    model_F = sm.Probit(Y, X) if y_self == 'Y/N ICV' else sm.OLS(Y, X)
    results_H_self = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_M_test['ZoneID'].values}, maxiter=100, )
    results.append(results_H_self)

    # Wife
    Y = df_F_test[y_self]
    X = sm.add_constant(df_F_test[ind + char], prepend=False)
    model_F = sm.Probit(Y, X) if y_self == 'Y/N ICV' else sm.OLS(Y, X)
    results_F_self = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_F_test['ZoneID'].values}, maxiter=100, )
    results.append(results_F_self)

    ##############################################
    # DNA-fingerprint regressions
    ##############################################
    # Husband
    Y = df_M_test[y_DNA]
    X = sm.add_constant(df_M_test[ind + char], prepend=False)
    model_M = sm.Probit(Y, X) if y_DNA == 'DNA Y/N ICV' else sm.OLS(Y, X)
    results_H_DNA = model_M.fit(cov_type='cluster', cov_kwds={'groups': df_M_test['ZoneID'].values}, maxiter=100, )
    results.append(results_H_DNA)

    # Wife
    Y = df_F_test[y_DNA]
    X = sm.add_constant(df_F_test[ind + char], prepend=False)
    model_F = sm.Probit(Y, X) if y_DNA == 'DNA Y/N ICV' else sm.OLS(Y, X)
    results_F_DNA = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_F_test['ZoneID'].values},
        maxiter=100, )
    results.append(results_F_DNA)

vif_data = pd.DataFrame()
X = df_M_test[ind + char]
vif_data["feature"] = X.columns

vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(len(X.columns))]
print(vif_data)

# Then, call summary_col with the renamed results
summary_str = summary_col(
    results,
    stars=True,
    model_names=[
        'Husband_self',
        'Wife_self',
        'Husband_DNA',
        'Wife_DNA'
    ],
    float_format='%.3f',
    info_dict={'N': lambda x: "{0:d}".format(int(x.nobs))},
    regressor_order=ind + char
)

columns_dataset_level_1 = {0: 'Y/N ICV' }

columns_dataset_level_2 = {0: 'Husband', 1: 'Husband', 2: 'Wife', 3: 'Wife',
                           }

columns_dataset_level_3 = {0: 'Self-reported', 1: "DNA"}
# [results_H_self, results_F_self, results_H_DNA, results_F_DNA]
summary_str = summary_col(results,
    stars=True,
    model_names=[
    'Husband (self)',
    'Wife (self)',
    'Husband (DNA)','Wife (self)'],
    float_format='%.3f',info_dict={'N': lambda x: "{0:d}".format(int(x.nobs))},
    regressor_order=ind + char, multiCol=False)

df_results = summary_str.tables[0]

print(df_results.to_latex())


latex_hL = r""" \documentclass{article}
\usepackage{booktabs}
\usepackage{lscape}
\begin{document}
\begin{landscape}
\begin{table}
\caption{Regression}
\footnotesize
"""

latex_h = r""" \documentclass{article}
\usepackage{booktabs}
\usepackage{lscape}
\begin{document}
\begin{table}
 \footnotesize
"""

latex_endL = r""" \end{table}
\end{landscape}
\end{document}
"""


latex_end = r""" \end{table}
\end{document}
"""



with open('mytable1.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ df_results.to_latex()+'\n' +latex_end)

## Select the group A and B
groupA = 'F' # Female
groupB = 'M' # Male
dataset = f'{groupA}{groupB}'


dependent_self_reported = ['planted', 'Household_ICV']
dependent_DNA = ['DNA_planted', 'DNA_Household_ICV']

characteristic = ['ZoneID_1', 'ZoneID_3', 'ZoneID_4', # ZoneID_2 is base
                  'A03_Age', 'A05_Edu', 'Household_Size',
                  'A07_1_Main_occupatn_Farming', 'A07_1_Main_occupatn_Self_employed_off_farm',
                  'A07_1_Main_occupatn_Other', # A07_1_Main_occupatn_Salaried_employment is base
                  'A08_fam_lab_contributn']

# J02_ percentage of household income comes from cassava? (%)
independent_income = ['J02_per_hh_inc_cassav']

# household member in coop group (0, 1)
independent_coop_member = ['Joint_Coop']

# general household credit access (0, 1)
independent_credit =  ['Credit_Access'] # Also check ['Joint_Credit']

# total household value of household assets
independent_household_asset = ['log_Total_Household_Asset_Value']

# total production asset value owned by house
independent_production_asset = ['log_Total_Production_Asset_Value']

independent = independent_income + independent_coop_member + independent_credit  + independent_household_asset + independent_production_asset

y = 'planted'
y = 'DNA_planted'

y = 'selfMagIcv'
group = 'A02_Sex'
formula = f'{y} ~ ' + ' + '.join(independent) + " + " + ' + '.join(
    characteristic) + f' | {group} ' + ' | ' + ' + '.join(characteristic[:3])
# formula = f'{dependent} ~ ' + ' + '.join(independent)  +  f' | {group}'
extra = 'reg.fun = glm, family = binomial(link = "probit")'

# print(formula)
robjects.r(f''' 
    df <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/df_FM_Update.csv")
    results <- oaxaca(formula = {formula}, data=df, {extra}, R=100)

''')

results = robjects.globalenv['results']
resulst_dict = dict(zip(results.names, results))
resulst_dict_threefold = dict(
    zip(resulst_dict['threefold'].names, list(resulst_dict['threefold'])))

results_dict_y = dict(zip(resulst_dict['y'].names, resulst_dict['y']))
print(y, '\t'
         'Group A = ', '{:.3f}'.format(results_dict_y['y.A'][0]), ', Group B = ',
    '{:.3f}'.format(results_dict_y['y.B'][0]), ', Mean gender gap=',
    '{:.3f}'.format(results_dict_y['y.diff'][0]))

df_tmp = update_results(resulst_dict_threefold, independent, characteristic, base=['(Base)'],
    variables_dict=variables_dict)
df_tmp.columns = pd.MultiIndex.from_product([[y], df_tmp.columns])
print(df_tmp.to_latex(escape=False))

with open('mytableDecom_SelfManage.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ df_tmp.to_latex(escape=False)+'\n' +latex_end)

with open('mytableDecom_Self.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ pd.concat(df_results, axis=1).to_latex(escape=False)+'\n' +latex_end)


with open(OutputDir+'/mytableDecom_Self.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ pd.concat(df_results, axis=1).to_latex(escape=False)+'\n' +latex_end)

with open('mytableDecom_DNA.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ df_tmp.to_latex(escape=False)+'\n' +latex_end)


df_F.to_excel(OutputDir+'/df_F_test.xlsx',index=False)
hh_g = pd.crosstab(df_FM_test['A02_Sex'],df_FM_test['A06_Relatn_hhd'])
print(hh_g)

# -------------------------------# -------------------------------# -------------------------------
# --------------------------------------Clean version# --------------------------------------
# -------------------------------# -------------------------------# -------------------------------
# Data processing:
df_FM_test = pd.read_csv(OutputDir + "/df_FM.csv")

df_FM_test = df_FM_test[(df_FM_test['Total_Production_Asset_Value']<1e6) & (df_FM_test[
              'Total_Production_Asset_Value']>0)]
df_FM_test['Total_Production_Asset_Value'].describe()
df_FM_test['TotProdAssetValueThd'] = df_FM_test['Total_Production_Asset_Value']/1000
df_FM_test['CellAssValThd'] = df_FM_test['Cell_Asset_Value']/1000
df_FM_test['Cell_Women_ValueTh'] = df_FM_test['Cell_Women_Value']/1000
df_FM_test['Cell_Men_ValueTh'] = df_FM_test['Cell_Men_Value']/1000

df_FM_test['Coop_Group_Member'] = df_FM_test['Coop_Group_Member'].replace({'Yes': 1, 'No': 0})
df_FM_test['J01_hhd_apply_fert'] = df_FM_test['J01_hhd_apply_fert'].replace({'Yes':1,'No':0})
df_FM_test['selfMagIcv'] = np.where((df_FM_test['A02_Sex'] == 1) & (df_FM_test['Male_ICV_Managed']
                                                                  > 0), 1,
                              np.where((df_FM_test['A02_Sex'] == 1) & (df_FM_test['Male_ICV_Managed'] == 0), 0,
                                       np.where((df_FM_test['A02_Sex'] == 0) & (df_FM_test['Female_ICV_Managed'] > 0), 1,
                                                np.where((df_FM_test['A02_Sex'] == 0) & (
                                                        df_FM_test['Female_ICV_Managed'] == 0),
                                                    0, None)))).astype(int)
# df_test = df_FM_test[['HouseID','A02_Sex', 'Male_ICV_Managed','Female_ICV_Managed','selfMagIcv']]
# df_test.to_csv(OutputDir +'/test.csv',sep='|',index=False)
df_FM_test= df_FM_test.dropna(subset=['Coop_Group_Member','J01_hhd_apply_fert'])
# df_FM_test['lgTotProdAss'] = np.log(df_FM_test['Total_Production_Asset_Value'])
# test = df_FM_test[['lgTotProdAss','log_Total_Production_Asset_Value']]
df_FM_test['AgeSq'] = df_FM_test['A03_Age']**2
# df_FM_test['selfMagIcv'].describe()
variables_dict = {'planted': 'Y/N ICV', 'Household_ICV': 'Total ICV',
                  'DNA_planted': 'DNA Y/N ICV', 'DNA_Household_ICV': 'DNA Total ICV',
                  'ZoneID_1': 'Zone1', 'ZoneID_2': 'Zone2', 'ZoneID_3': 'Zone3', 'ZoneID_4':
        'Zone4',         'A03_Age': 'Age', 'A05_Edu': 'Education',
                  'Men_In_House': 'Men in House', 'Women_In_House': 'Women in House', 'Kids': 'Children',
                  'Household_Size': 'Household size',
                  'A07_1_Main_occupatn_Farming': 'Main occupation: Farming',
                  'A07_1_Main_occupatn_Salaried_employment': 'Main occupation: Salaried employment',
                  'A07_1_Main_occupatn_Self_employed_off_farm': 'Main occupation: Self employed off farm',
                  'A07_1_Main_occupatn_Other': 'Main occupation: Other',
                  'A08_fam_lab_contributn': 'Contribution to farm work',
                  'Male_Managed': 'Male Managed', 'Female_Managed': 'Female Managed', 'Joint_Managed': 'Joint Managed',
                  'Household_Plots': 'Household Plots', 'J02_per_hh_inc_cassav': 'Income from Cassava (%)',
                  'Men_Only_Coop': 'G_Coop', 'Women_Only_Coop': 'G_Coop', 'Joint_Coop':
        'Joint Coop',
                  'Credit_Access': 'Household Credit', 'Male_Credit_Only': 'G_Credit',
    'Female_Credit_Only': 'G_Credit', 'Joint_Credit': 'Joint Credit',
                  'Male_Total_Processing_Access': 'Male Processing Access', 'Female_Total_Processing_Access': 'Female Processing Access', 'Joint_Total_Processing_Access': 'Joint Processing Access',
                  'Total_Household_Asset_Value': 'Household Asset', 'Women_Owned_HHAsset_Value': 'Women-owned HH Asset', 'Male_Owned_HHAsset_Value': 'Male-owned HH Asset',
                  'log_Total_Household_Asset_Value': 'Log Household Asset',
                  'Male__Production_Value': 'Male Production Asset', 'Women__Production_Value': 'Women Production Asset', 'Total_Production_Asset_Value': 'Total Production Asset',
                  'log_Total_Production_Asset_Value': 'Log Total Production Asset',
    'Total_Production_Asset_Value':'Total Production Asset',
    'Coop_Group_Member':'Coop Member', 'Extension_Access':'Extension Access',
    'Cell_Asset_Value':'Cell value HH','J05_consumption_perc':'Consump perc',
    'J05_sales_perc':'Sales perc','J01_hhd_apply_fert':'Fertilizer','AgeSq':'Age Square',
    'TotProdAssetValueThd':'Total Production Asset Value (1,000)','CellAssValThd':'Cell value HH '
    '(1,000)', 'Cell_Women_Value':'G_CellValue','Cell_Men_Value':'G_CellValue',
    'Male_Ext_Only':'G_Ext_Only', 'Female_Ext_Only':'G_Ext_Only'}
df_F_test = df_FM_test[df_FM_test['A02_Sex'] == 0].rename(columns=variables_dict)
df_M_test = df_FM_test[df_FM_test['A02_Sex'] == 1].rename(columns=variables_dict)
dep_self =  list(map(lambda x: variables_dict[x], dependent_self_reported))
df_FM_test.to_csv(OutputDir+'/df_FM_Update.csv',sep=',',index=False)

df_FM_test['DNA_planted'].sum()/df_FM_test['DNA_planted'].shape[0]
df_F['Y/N ICV'].sum()/df_F['DNA Y/N ICV'].shape[0]
df_M['Y/N ICV'].sum()/df_M['DNA Y/N ICV'].shape[0]


reversed_variables_dict = {v: k for k, v in variables_dict.items()}
char_ori = [reversed_variables_dict.get(char, char) for char in char]

FList = ['HouseID','A02_Sex','planted','DNA_planted', 'Cell_Women_Value','selfMagIcv',
    'Women_Only_Coop','Female_Credit_Only','Female_Ext_Only','J01_hhd_apply_fert',
            'J05_consumption_perc']+char_ori
MList = ['HouseID','A02_Sex','planted','DNA_planted','Cell_Men_Value','selfMagIcv',
    'Men_Only_Coop','Male_Credit_Only','Male_Ext_Only','J01_hhd_apply_fert',
            'J05_consumption_perc']+char_ori


df_F = df_FM_test[df_FM_test['A02_Sex'] == 0][FList].rename(columns=variables_dict)

df_M = df_FM_test[df_FM_test['A02_Sex'] == 1][MList].rename(columns=variables_dict)

df_selfMag = pd.concat([df_F, df_M],ignore_index=True)
df_selfMag.to_csv(OutputDir+'/dfSefMag.csv',sep=',',index=False)

MList_newName = [variables_dict.get(char,char) for char in MList]
# -------------------------------# -----Data Processing (ends)--------------------------#

# --------------------------------------------------------------------------------------
# -----------------------------Plot and Checking Data (# starts)-------------------------

sns.kdeplot(df_FM_test['selfMagIcv'], shade=True, label='KDE Plot')
plt.show()
df_FM_test['Household_Size'].describe()
sns.kdeplot(df_FM_test['Household_Size'])
plt.show()
sns.kdeplot(df_FM_test['Total_Production_Asset_Value'], shade=True, label='KDE Plot')
plt.show()

x_values = df_FM_test['Cell_Asset_Value']
y_values = df_FM_test['Total_Production_Asset_Value']

# Create the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(x_values, y_values, alpha=0.5)  # Adjust alpha for transparency
plt.title('Scatter Plot')
plt.xlabel('Independent Household Asset')
plt.ylabel('Total Production Asset Value')
plt.grid(True)  # Add grid lines (optional)
plt.show()
df_FM_test['Total_Production_Asset_Value'].describe()
8.796167e+05+3*2.655436e+07
data = df_FM_test['Total_Production_Asset_Value']
from scipy import stats
z_scores = stats.zscore(df_FM_test['Total_Production_Asset_Value'])
z_threshold = 3

upper = df_FM_test[df_FM_test['Total_Production_Asset_Value']>1e6]
Q1 = df_FM_test['Total_Production_Asset_Value'].quantile(0.25)
Q3 = df_FM_test['Total_Production_Asset_Value'].quantile(0.75)
IQR = Q3 - Q1

# Define lower and upper bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 2 * IQR
above_upper_bound = df_FM_test[df_FM_test['Total_Production_Asset_Value'] > upper_bound]
count_above_upper_bound = len(above_upper_bound)

below_bound = df_FM_test[df_FM_test['Total_Production_Asset_Value'] < lower_bound]
below_bound = df_FM_test[df_FM_test['Total_Production_Asset_Value'] ==0]
len(below_bound)

# Create a boxplot to visualize outliers
plt.figure(figsize=(8, 6))
plt.boxplot(data, vert=False)
plt.title('Boxplot of Total_Production_Asset_Value')
plt.xlabel('Total_Production_Asset_Value')
plt.show()

subset_1 = df_FM_test[df_FM_test['A02_Sex'] == 1]['selfMagIcv']
subset_0 = df_FM_test[df_FM_test['A02_Sex'] == 0]['selfMagIcv']
sns.kdeplot(subset_1, shade=True, label='Husband managed')
sns.kdeplot(subset_0, shade=True, label='Wife managed')

subset_1 = df_FM_test[df_FM_test['A02_Sex'] == 1]['A03_Age']
subset_0 = df_FM_test[df_FM_test['A02_Sex'] == 0]['A03_Age']
sns.kdeplot(subset_1, shade=True, label='Male age')
sns.kdeplot(subset_0, shade=True, label='Female age')
plt.xlabel('Age')
plt.ylabel('Density')
plt.savefig(OutputDir +'/Figure/age.png',dpi = 2000)
plt.legend()
plt.show()

df_FM_test[df_FM_test['A02_Sex'] == 1]['A03_Age'].describe()
df_FM_test[df_FM_test['A02_Sex'] == 0]['A03_Age'].describe()

sns.kdeplot(df_FM_test['log_Total_Household_Asset_Value'])
sns.kdeplot(df_FM_test['Total_Household_Asset_Value'])
# Create KDE plots for each subset

plt.xlabel('Independently Managed')
plt.ylabel('Density')
plt.savefig(OutputDir +'/Figure/SelfReptSelfMang.png',dpi = 2000)
plt.legend()


subset_1 = df_FM_test[df_FM_test['A02_Sex'] == 1]['A03_Age']
subset_0 = df_FM_test[df_FM_test['A02_Sex'] == 0]['A03_Age']
sns.kdeplot(subset_1, shade=True, label='Husband')
sns.kdeplot(subset_0, shade=True, label='Wife')
plt.xlabel('Age')
plt.ylabel('Density')
# plt.savefig(OutputDir +'/Figure/SelfReptSelfMang.png',dpi = 2000)
plt.legend()
ks_statistic, p_value = ks_2samp(subset_1, subset_0)
alpha = 0.05

# Check if the p-value is less than alpha
if p_value < alpha:
    print("Reject the null hypothesis: The two samples come from different distributions.")
else:
    print("Fail to reject the null hypothesis: The two samples may come from the same distribution.")

df_FM_test['Cell_Asset_Value'].describe()
# -----------------------------Plot and Checking Data (ends)-------------------------


# *************************************************************************************************#
# -------------------------------Variables-------------------------------------------------
# *************************************************************************************************#
dependent_self_reported = ['planted', 'Household_ICV']
dependent_DNA = ['DNA_planted', 'DNA_Household_ICV']
characteristic = ['ZoneID_1', 'ZoneID_3', 'ZoneID_4', # ZoneID_2 is base
                  'A03_Age', 'A05_Edu', 'Household_Size',
                  'A07_1_Main_occupatn_Salaried_employment',
# 'AgeSq',
    # 'A07_1_Main_occupatn_Self_employed_off_farm',
    #               'A07_1_Main_occupatn_Other',
    # A07_1_Main_occupatn_Salaried_employment is base
    #               'A08_fam_lab_contributn','A07_1_Main_occupatn_Farming'
]

# J02_ percentage of household income comes from cassava? (%)
independent_income = ['J02_per_hh_inc_cassav']
independent_fert = ['J01_hhd_apply_fert']
independent_consum = ['J05_consumption_perc']
independent_sale = ['J05_sales_perc']
independent_TotAssValThd = ['TotProdAssetValueThd']
# household member in coop group (0, 1)
# independent_coop_member = ['Joint_Coop']
independent_coop_member =['Coop_Group_Member']
independent_ext = ['Extension_Access']
# general household credit access (0, 1)
independent_credit =  ['Credit_Access'] # Also check ['Joint_Credit']
# total household value of household assets
independent_lghousehold_asset = ['log_Total_Household_Asset_Value']
# total production asset value owned by house
independent_lgProduction_asset = ['log_Total_Production_Asset_Value']
independent_production_assetNom = ['Total_Production_Asset_Value']
independent_cellValue = ['Cell_Asset_Value']
independent_cellValueThd = ['CellAssValThd']
independent_livestock = ['HouseHold_AnimalUnits']

independent =  independent_coop_member + independent_credit +\
              independent_ext +independent_fert +independent_consum
# +independent_cellValueThd
# +independent_TotAssValThd
    # independent_production_assetNom + independent_household_asset +independent_income+
# independent_production_asset +
# +independent_sale+independent_lgProduction_asset+independent_cellValue

ind = list(map(lambda x: variables_dict[x], independent))
char = list(map(lambda x: variables_dict[x], characteristic))


vif_data = pd.DataFrame()
for df_i, prefix in [(df_M_test, 'M_test'), (df_F_test, 'F_test')]:
    X = df_i[ind + char]

    # Calculate VIF for the current DataFrame
    vif = pd.DataFrame()
    vif["feature"] = X.columns
    vif["VIF_" + prefix] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

    # Concatenate the current results to the main vif_data DataFrame
    vif_data = pd.concat([vif_data, vif], axis=1)

# Print the combined vif_data DataFrame
print(vif_data)
#
# X_f = df_F_test[ind + char]
# print(X_f.corr())
# occu = ['Main occupation: Farming', 'Main occupation: Salaried employment',
# 'Main occupation: Self employed off farm', 'Main occupation: Other']
# print(df_F_test[occu].describe())
# pd.crosstab(df_F_test)
#
# OriWorkDir = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety" \
#              r"\Code\DataSynthesis\MeasureError\Gender\MeasureError"
# df_hh = pd.read_excel(OriWorkDir + "//Data//HH.xlsx")
# plt.plot(df_hh["M_ICV_Managed_Male"])
#
# fig, ax = plt.subplots()
# difference = df_hh['M_ICV_HH_yn'] - df_hh['F_ICV_HH_yn']
#
# # Create a bar chart to show the difference
# ax.scatter(df_hh['HouseID'], difference, color='b', label='Difference')
#
# # Set labels and legend
# ax.set_xlabel('HouseID')
# ax.set_ylabel('Difference')
# ax.legend()

# **********************************************************************************************
# --------------------------Regressions ( Begin)--------------------------------------------------
# **********************************************************************************************


def fn_reg_ind(y_self,ModelNames,ResName):

    results = []
    Y = df_M_test[y_self]
    X = sm.add_constant(df_M_test[ind + char], prepend=False)

    model_F = sm.Probit(Y, X)
    results_H_self = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_M_test['ZoneID'].values},
        maxiter=100, )
    results.append(results_H_self)

    # Wife
    Y = df_F_test[y_self]
    X = sm.add_constant(df_F_test[ind + char], prepend=False)
    model_F = sm.Probit(Y, X)

    results_F_self = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_F_test['ZoneID'].values},
        maxiter=100, )
    results.append(results_F_self)

    summary_str = summary_col(
        results,
        stars=True,
        model_names=ModelNames,
        float_format='%.3f',
        info_dict={'N': lambda x: "{0:d}".format(int(x.nobs))},
        regressor_order=ind + char
    )

    df_results = summary_str.tables[0]
    with open(OutputDir+f'/{ResName}.tex', 'w') as tf:
        tf.write(latex_h+'\n'+ df_results.to_latex()+'\n' +latex_end)

y_self = ['selfMagIcv']
ResName = ''
ModelNames = ['HusbandManage', 'WifeManage']

y_self = ['Y/N ICV']
y_DNA = ['DNA Y/N ICV' ]
ModelNames =['MaleReport','FemaleReport']
ResName = 'Self Reported'

fn_reg_ind(y_self='Y/N ICV',ModelNames=['MaleReport','FemaleReport'],ResName = 'Self Reported')
fn_reg_ind(y_self='DNA Y/N ICV',ModelNames=['MaleDNA','FemaleDNA'],ResName = 'DNA Test')

fn_reg_ind(y_self='Y/N ICV',ModelNames=['MaleReport','FemaleReport'],ResName = 'Self '
                                                                               'ReportedNoAsset')
fn_reg_ind(y_self='DNA Y/N ICV',ModelNames=['MaleDNA','FemaleDNA'],ResName = 'DNA TestNoAsset')
fn_reg_ind(y_self='DNA Y/N ICV',ModelNames=['MaleDNA','FemaleDNA'],ResName = 'DNATest2')



y = 'selfMagIcv'
group = 'A02_Sex'
formula = f'{y} ~ ' + ' + '.join(independent) + " + " + ' + '.join(
    characteristic) + f' | {group} ' + ' | ' + ' + '.join(characteristic[:3])
# formula = f'{dependent} ~ ' + ' + '.join(independent)  +  f' | {group}'
extra = 'reg.fun = glm, family = binomial(link = "probit")'

# print(formula)
robjects.r(f''' 
    df <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/df_FM_Update.csv")
    results <- oaxaca(formula = {formula}, data=df, {extra}, R=100)

''')
rcode = f''' 
    df <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/df_FM_Update.csv")
    results <- oaxaca(formula = {formula}, data=df, {extra}, R=100)

'''

rcodeSelf = """dfSelfMag <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/dfSefMag.csv")
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
"""
robjects.r(rcodeSelf)
results = robjects.globalenv['results']
resulst_dict = dict(zip(results.names, results))
resulst_dict_threefold = dict(
    zip(resulst_dict['threefold'].names, list(resulst_dict['threefold'])))

results_dict_y = dict(zip(resulst_dict['y'].names, resulst_dict['y']))
print(y, '\t'
         'Group A = ', '{:.3f}'.format(results_dict_y['y.A'][0]), ', Group B = ',
    '{:.3f}'.format(results_dict_y['y.B'][0]), ', Mean gender gap=',
    '{:.3f}'.format(results_dict_y['y.diff'][0]))

independent_decom= ['G_Coop','G_Credit','G_Ext_Only','G_CellValue','Fertilizer','Consump.perc']
characteristic_decom = ['Zone1' , 'Zone3' ,  'Zone4' , 'Age' ,'Education' , 'Household.size' ,
    'Main.occupation..Salaried.employment']

variables_dictDeco = {'Zone1':'Zone 1','Zone2':'Zone 2','Zone3':'Zone 3','Zone4':'Zone 4',
'Main.occupation..Salaried.employment':'Main occupation: Salaried employment','G_Coop':'Coop Member (self)',
'G_Credit':'Credit (self)', 'G_Ext_Only':'Extension Access (self)','G_CellValue':'Cell value (self)',
    'Household.size':'Household size'}

df_tmp = update_results(resulst_dict_threefold, independent_decom, characteristic_decom,
    base=['(Base)'],
    variables_dict=variables_dict
)
df_tmp.columns = pd.MultiIndex.from_product([[y], df_tmp.columns])
print(df_tmp.to_latex(escape=False))

with open(OutputDir+'/resultSelfManageDeco.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ df_tmp.to_latex(escape=False)+'\n' +latex_end)

# *******************************************
# test household head:
df_FM_Head = df_FM_test[df_FM_test['A06_Relatn_hhd']=='Household head']
df_FM_Head.to_csv(OutputDir+'/head.csv',sep=',',index=False)


y = 'DNA_planted'

ax = sns.countplot(x=y, hue='A02_Sex', data=df_FM_Head, palette='Set1')
plt.xlabel('DNA test')
plt.legend(title='Gender', labels=['Husband', 'Wife'])

# Add labels to the bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='center', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')

plt.show()

rcodeHead = """dfHead <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/head.csv")
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
"""
robjects.r(rcodeHead)
results = robjects.globalenv['results']
resulst_dict = dict(zip(results.names, results))
resulst_dict_threefold = dict(
    zip(resulst_dict['threefold'].names, list(resulst_dict['threefold'])))

results_dict_y = dict(zip(resulst_dict['y'].names, resulst_dict['y']))
print(y, '\t'
         'Group A = ', '{:.3f}'.format(results_dict_y['y.A'][0]), ', Group B = ',
    '{:.3f}'.format(results_dict_y['y.B'][0]), ', Mean gender gap=',
    '{:.3f}'.format(results_dict_y['y.diff'][0]))


df_tmp = update_resultsOri(resulst_dict_threefold, independent, characteristic,
    base=['(Base)'],
    variables_dict=variables_dict
)
df_tmp.columns = pd.MultiIndex.from_product([[y], df_tmp.columns])
print(df_tmp.to_latex(escape=False))

with open(OutputDir+'/HeadDeco.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ df_tmp.to_latex(escape=False)+'\n' +latex_end)


# *******************************************************************
# Additional plot:]
# household head:
subset_1 = df_FM_Head[df_FM_Head['A02_Sex'] == 1]
subset_0 = df_FM_Head[df_FM_Head['A02_Sex'] == 0]

total_husbands = len(subset_1)
total_wives = len(subset_0)

adoption_rate_husbands =  subset_1[y].sum()  /  subset_1[y].count()
adoption_rate_wives =  subset_0[y].sum()  /  subset_0[y].count()

# Set a custom color palette
colors = ["#FF6F61", "#6B4226"]

# Create the bar plot
plt.figure(figsize=(8, 6))
ax = sns.countplot(x=y, hue='A02_Sex', data=df_FM_Head, palette='Set1')
plt.xlabel('DNA test')
plt.legend(title='Gender', labels=['Wife','Husband'])

# Add labels to the bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='center', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')
ax.annotate(f'Adoption rate: {int(adoption_rate_husbands*100)}%', (p.get_x(), p.get_height()/2),
    fontsize=10, color='black')
ax.annotate(f'Adoption rate: {int(adoption_rate_wives*100)}%', (p.get_x()-0.4, p.get_height(
)-400),
    fontsize=10, color='black')
plt.savefig(OutputDir+'/Figure/householdHead.png',dpi=2000)
plt.show()

y = 'planted'
subset_1 = df_FM_test[df_FM_test['A02_Sex'] == 1]
subset_0 = df_FM_test[df_FM_test['A02_Sex'] == 0]

total_husbands = len(subset_1)
total_wives = len(subset_0)

adoption_rate_husbands =  subset_1[y].sum()  /  subset_1[y].count()
adoption_rate_wives =  subset_0[y].sum()  /  subset_0[y].count()

# Set a custom color palette
colors = ["#FF6F61", "#6B4226"]

# Create the bar plot
plt.figure(figsize=(8, 6))
ax = sns.countplot(x=y, hue='A02_Sex', data=df_FM_test, palette='Set1')
plt.xlabel('Self reported')
plt.legend(title='Gender', labels=['Wife','Husband'])

# Add labels to the bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='center', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')
ax.annotate(f'Adoption rate: {int(adoption_rate_husbands*100)}%', (p.get_x(), p.get_height()/2),
    fontsize=10, color='black')
ax.annotate(f'Adoption rate: {int(adoption_rate_wives*100)}%', (p.get_x()-0.4, p.get_height(
)-400),
    fontsize=10, color='black')
plt.savefig(OutputDir+'/Figure/GenderSelfReport.png',dpi=2000)
plt.show()

# gender dummy:
df_FM_Head.to_csv(OutputDir+'/test_head.csv',sep='|',index=False)
df_selfMag.to_csv(OutputDir +'/test_selfMag.csv', sep='|',index=False)
y = 'DNA Y/N ICV'
Y = df_selfMag[y]
X = sm.add_constant(df_FM_Head[ind + char], prepend=False)

fn_reg_ind(y_self=y,ModelNames=['MaleDNA','FemaleDNA'],ResName = 'DNA Test')
model_F = sm.Probit(Y, X)
results_H_self = model_F.fit(cov_type='cluster', cov_kwds={'groups': df_M_test['ZoneID'].values},
    maxiter=100, )
results.append(results_H_self)



df_FHH =  df_FM_test[(df_FM_test['A02_Sex'] == 0) &(df_FM_test['A06_Relatn_hhd']=='Household head') ]
df_FHH.to_csv(OutputDir +'/test_fhh.csv',sep='|',index=False)
df_FHH_dif = df_FHH[['planted','DNA_planted']]
import numpy as np
from scipy import stats
t_statistic, pfh_value = stats.ttest_rel(df_FHH['planted'], df_FHH['DNA_planted'])
# no sig difference between the paired samples
t_statisticf, pf_value = stats.ttest_rel(df_F['Y/N ICV'], df_F['DNA Y/N ICV'])
t_statisticm, pm_value = stats.ttest_rel(df_M['Y/N ICV'], df_M['DNA Y/N ICV'])

columns = ['Variable', 'Female self-reported', 'DNA tests', 'T-Statistic', 'P-Value']
data = [['Female self-reported', pd.Series(df_F['Y/N ICV']).mean(), pd.Series(df_F['DNA Y/N ICV']).mean(), t_statistic, p_value]]
summary_tableF = pd.DataFrame(data, columns=columns)

columnsM = ['Variable', 'Male self-reported', 'DNA tests', 'T-Statistic', 'P-Value']
dataM = [['Male self-reported', pd.Series(df_M['Y/N ICV']).mean(), pd.Series(df_M['DNA Y/N '
                                                                                 'ICV']).mean(), t_statistic, p_value]]
summary_tableM = pd.DataFrame(dataM, columns=columnsM)

summary_tableBoth = pd.concat([summary_tableF, summary_tableM])

df_FHH
t_statisticfh, pfh_value = stats.ttest_rel(df_FHH['planted'], df_FHH['DNA_planted'])

 dataM = [['Male self-reported', pd.Series(df_FHH['planted']).mean(), pd.Series(df_FHH['DNA_planted'
                                                                                 'ICV']).mean(), t_statistic, p_value]]



 # plot
female_self_reported = df_FM_test[df_FM_test['A02_Sex'] == 0]['planted']
male_self_reported = df_FM_test[df_FM_test['A02_Sex'] == 1]['planted']
dna_tests = df_FM_test[df_FM_test['A02_Sex'] == 1]['DNA_planted']

# Create a figure and axis for the plots
plt.figure(figsize=(10, 6))

# Plot kernel density for female self-reported
sns.kdeplot(female_self_reported, label='Female Self-Reported', shade=True )

# Plot kernel density for male self-reported
sns.kdeplot(male_self_reported, label='Male Self-Reported', shade=True )

# Plot kernel density for DNA tests
sns.kdeplot(dna_tests, label='DNA Tests', shade=True )

# Customize the plot
plt.title('Kernel Density Plot of Planted Column')
plt.xlabel('Planted Values')
plt.ylabel('Density')
plt.legend(loc='upper left')
plt.savefig(OutputDir+'/Figure/fmdna.png',dpi=1000)
# Show the plot
plt.show()