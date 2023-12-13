# GenderInd_7Dec2023_JY.PY is the ancestor


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


df_FM_test = pd.read_csv(OutputDir + "/df_FM.csv")
unique_house_ids = df_FM_test['HouseID'].value_counts()
house_ids_appeared_once = unique_house_ids[unique_house_ids == 1].index.tolist()

mask = df_FM_test[['Coop_Group_Member', 'J01_hhd_apply_fert']].isna()
df_FM_test2 = df_FM_test[mask]

df_FM_test['J01_hhd_apply_fert'] = df_FM_test['J01_hhd_apply_fert'].replace({'Yes':1,'No':0})
df_FM_test['Coop_Group_Member'] = df_FM_test['Coop_Group_Member'].replace({'Yes': 1, 'No': 0})

df_FM_test= df_FM_test.dropna(subset=['Coop_Group_Member','J01_hhd_apply_fert'])
df_FM_test2= df_FM_test.isna(subset=['Coop_Group_Member','J01_hhd_apply_fert'])

df_F_test = df_FM_test[df_FM_test['A02_Sex'] == 0].rename(columns=variables_dict)
df_M_test = df_FM_test[df_FM_test['A02_Sex'] == 1].rename(columns=variables_dict)
dep_self =  list(map(lambda x: variables_dict[x], dependent_self_reported))
# *************************************************************************************************#
# -------------------------------Variables-------------------------------------------------
# *************************************************************************************************#
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
              independent_ext+independent_consum
# +independent_cellValueThd
# +independent_TotAssValThd
    # independent_production_assetNom + independent_household_asset +independent_income+
# independent_production_asset +
# +independent_sale+independent_lgProduction_asset+independent_cellValue
# +independent_fert

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


# **********************************************************************************************
# --------------------------Regressions ( Begin)--------------------------------------------------
# **********************************************************************************************


def fn_reg_ind(y_self,ModelNames,ResName,ind,char):

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

fn_reg_ind(y_self='Y/N ICV',ModelNames=['MaleReport','FemaleReport'],ResName = 'SelfReported',
    ind=ind,char=char)


fn_reg_ind(y_self='Y/N ICV',ModelNames=['MaleReport','FemaleReport'],ResName = 'test',
    ind=ind,char=char)

fn_reg_ind(y_self='DNA Y/N ICV',ModelNames=['MaleDNA','FemaleDNA'],ResName = 'DNATest',ind=ind,char=char)

df_selfMag =pd.read_csv(OutputDir+'/dfSefMag.csv',sep=',' )



y = 'selfMagIcv'
group = 'A02_Sex'
formula = f'{y} ~ ' + ' + '.join(independent) + " + " + ' + '.join(
    characteristic) + f' | {group} ' + ' | ' + ' + '.join(characteristic[:3])
# formula = f'{dependent} ~ ' + ' + '.join(independent)  +  f' | {group}'
extra = 'reg.fun = glm, family = binomial(link = "probit")'

robjects.r(f''' 
    df <- read.csv("D:/Dropbox/BoxOld/FEDSshare/MasterGithub/CornellGitHub/DataSynthesisForCropVariety/Code/DataSynthesis/MeasureError/Gender/MeasureError/AJAE_2023/Technology-Adoption/Output/df_FM_Update.csv")
    results <- oaxaca(formula = {formula}, data=df, {extra}, R=100)

''')

results = robjects.globalenv['results']
resulst_dict = dict(zip(results.names, results))
resulst_dict_threefold = dict(zip(resulst_dict['threefold'].names, list(resulst_dict['threefold'])))

results_dict_y = dict(zip(resulst_dict['y'].names, resulst_dict['y']))
print(y, '\t'
         'Group A = ', '{:.3f}'.format(results_dict_y['y.A'][0]), ', Group B = ',
    '{:.3f}'.format(results_dict_y['y.B'][0]), ', Mean gender gap=',
    '{:.3f}'.format(results_dict_y['y.diff'][0]))

df_tmp = update_results(resulst_dict_threefold, independent, characteristic, base=['(Base)'],
    variables_dict=variables_dict)
df_tmp.columns = pd.MultiIndex.from_product([[y], df_tmp.columns])



with open(OutputDir+'/mytableDecom_Self.tex', 'w') as tf:
    tf.write(latex_h+'\n'+ df_tmp.to_latex(escape=False)+'\n' +latex_end)

