# Author: Jing Yi, 2022

# Terminal: py  -m spacy download en_core_web_sm

import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re
from re import match
import io
import csv
import os
import urllib
import seaborn as sns
import warnings
import numpy as np
from scipy.stats import chisquare
from scipy.stats import kstest
import scipy.stats as stats

pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_row', 1000)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

warnings.filterwarnings('ignore')
import en_core_web_sm
import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_sm")

WorkingDir = r'D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Code\DataSynthesis\Code_Data'
DataDir = WorkingDir + "\\CMSC"
ProcDataDir = WorkingDir + "\\ProcessedData"
PaperDir = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Manuscript"

def fn_plt(df, col1, col2, col3):
    spacing = 0.5
    spacing_up = 0.1
    plt.subplot(3, 1, 1)
    df[col1].value_counts().plot(kind='barh').invert_yaxis()
    # plt.hist(sorted(df_Variety_All_Region_stop_allHH.prodtn_trait1_x), orientation='horizontal' )
    plt.tick_params(labelsize=8)
    plt.title(col1, fontsize=8)
    plt.subplots_adjust(left=spacing)

    plt.subplot(3, 1, 2)
    df[col2].value_counts().plot(kind='barh').invert_yaxis()
    plt.tick_params(labelsize=8)
    plt.title(col2, fontsize=8)
    plt.subplots_adjust(left=spacing)

    plt.subplot(3, 1, 3)
    df[col3].value_counts().plot(kind='barh').invert_yaxis()
    plt.tick_params(labelsize=8)
    plt.subplots_adjust(left=spacing)
    plt.title(col3, fontsize=8)
    plt.subplots_adjust(left=spacing)
    # plt.xticks(fontsize=10, rotation=90)
    # plt.title('prodtn_trait1_x')
    plt.tight_layout(pad=1.0)
    plt.show()

# with "Cassava prefernece" as keywords, i have the folloiwng list:
url_pref = "https://data.iita.org/dataset?q=cassava+preference&tags=Cassava&sort=score+desc%2C+metadata_modified+desc"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

page = requests.get(url_pref, headers=headers)
print(page.text)
# soup = BeautifulSoup(page.text, "html.parser")
df_url = []
soup = BeautifulSoup(page.text)
for a in soup.find_all('a', href=True):
    df_url.append(a['href'])
    # print("Found the URL:", a['href'])

# re.findall('^/dataset/')
new_url = list(filter(lambda v: match('^/dataset/',v), df_url))
new_url = pd.DataFrame(new_url)
new_url = new_url.drop_duplicates(keep='first',inplace=False)
dataset_header = "https://data.iita.org"
new_url['url'] = dataset_header + new_url

new_url.shape

def get_urls(i):
    # get url for downlaoding the csv files
    url_i = new_url["url"].iloc[i]
    page_i = requests.get(url_i,headers=headers)
    df_url_i = []
    soup_i = BeautifulSoup(page_i.text)
    for a in soup_i.find_all('a', href=True):
        df_url_i.append(a['href'])
    new_url_i = list(filter(lambda  v: match('^https:', v), df_url_i))
    new_url_i = list(filter(lambda  v: v.endswith('csv'), new_url_i))
    return new_url_i

def get_meta_url(new_url_i, meta_string):

    new_url_i_meta = list(filter(lambda v: v.endswith(str(meta_string)), new_url_i))
    new_url_i_data = list(set(new_url_i).difference(new_url_i_meta))
    return new_url_i_meta, new_url_i_data
# new_url_i = pd.DataFrame(new_url_i)

def get_csv(new_url_i):
    req = requests.get(new_url_i[0],headers=headers).content
    try:
        df_i = pd.read_csv(io.StringIO(req.decode('utf-8')))
    except:
        df_i = pd.read_csv(io.StringIO(req.decode('ISO-8859-1')))
    return df_i


    req = requests.get(new_url_i[1],headers=headers).content
    df_Cameroon_meta = pd.read_csv(io.StringIO(req.decode('utf-8')))
    df_Cameroon_meta["Dataset"] = "Cameroon"


def proc_meta(df_i):

    df_i = df_i[["Column","description_abstract"]]
    df_i = df_i.dropna(axis='rows')
    df_i = df_i.rename(columns={"description_abstract":"Col_Desc"})
    return df_i

def Add_ds(ds, Dataset_Name):
    ds["Dataset"] = Dataset_Name
    cols = ds.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Dataset')))
    ds = ds.reindex(columns=cols)
    return ds

def df_dic(df):
    df_dict = dict(zip([i for i in df.columns],
                       [pd.DataFrame(df[i].unique(), columns=[i]) for i in
                        df.columns]))
    return df_dict


meta_df = pd.DataFrame(columns=["Dataset","Column","Col_Desc"])
i = 0
urls= get_urls(i)
meta_df_Cameroon, df_Cameroon = get_meta_url(urls, 'metadata.csv')
meta_df_Cameroon = get_csv(meta_df_Cameroon)
meta_df_Cameroon = proc_meta(meta_df_Cameroon)
meta_df_Cameroon["Dataset"] = "Cameroon"
meta_df_Cameroon = meta_df_Cameroon[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_Cameroon])

i = 3
urls = get_urls(i)
meta_df_gender_url, df_gender_url = get_meta_url(urls, 'data_dictionary.csv')
meta_df_gender = get_csv(meta_df_gender_url)
meta_df_gender = proc_meta(meta_df_gender)
meta_df_gender["Dataset"] = "Beyond women’s traits"
meta_df_gender = meta_df_gender[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_gender])

df_gender = get_csv(df_gender_url)
df_gender["Dataset"] = "Beyond women’s traits"
cols = df_gender.columns.tolist()
cols.insert(0, cols.pop(cols.index('Dataset')))
df_gender = df_gender.reindex(columns = cols)
df_gender["Gender"].unique()

df_gender["Gender"].value_counts().plot(kind='bar')
plt.title('High market demand')
plt.tight_layout()
plt.show()

df_gender.groupby('Gender')['farmsize_acre'].plot(legend=True)
plt.show()

i = 4
urls = get_urls(i)
meta_df_association_url, df_left_url = get_meta_url(urls, 'metadata_association_all_region.csv')
meta_df_association_url = get_csv(meta_df_association_url)
meta_df_association_url = proc_meta(meta_df_association_url)
meta_df_association_url["Dataset"] = "CMSNHPL_Association"
meta_df_association_url = meta_df_gender[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_association_url])

meta_df_ppi, df_left_url = get_meta_url(df_left_url,'metadata_cass_ppi_all_region.csv')
meta_df_url = get_csv(meta_df_ppi)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_PPI"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_Trait_All, df_left_url = get_meta_url(df_left_url,'metadata_cass_trait_prefernc_all_region.csv')
meta_df_url = get_csv(meta_df_Trait_All)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Trait_All_Region"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

url1, url2 = get_meta_url(df_left_url, "cassava_traits-preference_all-regions.csv")
df_CMSNHPL_Trait_All = get_csv(url1)
df_CMSNHPL_Trait_All["Dataset"] = "CMSNHPL_Trait_All_Region"
cols = df_CMSNHPL_Trait_All.columns.tolist()
cols.insert(0, cols.pop(cols.index('Dataset')))
df_CMSNHPL_Trait_All = df_CMSNHPL_Trait_All.reindex(columns = cols)
df_CMSNHPL_Trait_All.to_excel(WorkingDir +"\\ProcessedData\\CMSNHPL_Trait_All_Region.xlsx")

meta_df_Variety_All, df_left_url = get_meta_url(df_left_url,'metadata_cass_variety_all_region.csv')
meta_df_url = get_csv(meta_df_Variety_All)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Variety_All_Region"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])


meta_df_i, df_left_url = get_meta_url(urls,'cassava_variety_all-regions.csv')
df_url = get_csv(meta_df_i)
df_Variety_All_Region = Add_ds(df_url,"CMSNHPL_Variety_All_Region")
df_Variety_All_Region.columns
# unique values in each column:
df_dict = dict(zip([i for i in df_Variety_All_Region.columns] , [pd.DataFrame(df_Variety_All_Region[i].unique(), columns=[i]) for i in df_Variety_All_Region.columns]))
df_Variety_All_Region.to_excel(WorkingDir + "\\\ProcessedData\\CMSNHPL_Variety_All_Region.xlsx" )

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_cassava_dna.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_DNA"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_cassava_plot.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Plot"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_cassava_plot_all-regions-_dr-tunji_nike_var_coded.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Plot_AllRegions"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_cassava_productn_all_region.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Production_AllRegions"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(urls,'metadata_farmer_preference1.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Farmer_Pref1"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(urls,'farmer_preference1_all-regions.csv')
df_url = get_csv(meta_df_i)
df_url_1 = Add_ds(df_url,"CMSNHPL_Farmer_Pref1")

meta_df_i, df_left_url = get_meta_url(urls,'farmer_preference1_all-regions.csv')
df_url = get_csv(meta_df_i)
df_url_2 = Add_ds(df_url,"CMSNHPL_Farmer_Pref2")

meta_df_i, df_left_url = get_meta_url(urls,'farmer_preference1_all-regions.csv')
df_url = get_csv(meta_df_i)
df_url_3 = Add_ds(df_url,"CMSNHPL_Farmer_Pref3")

meta_df_i, df_left_url = get_meta_url(urls,'farmer_preference1_all-regions.csv')
df_url = get_csv(meta_df_i)
df_url_4 = Add_ds(df_url,"CMSNHPL_Farmer_Pref4")

df_pre1_4 = pd.concat([df_url_1, df_url_2, df_url_3, df_url_4])
df_pre1_4.info()
df_pre1_4.head()
meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_farmer_preference2.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Farmer_Pref2"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_farmer_preference3.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Farmer_Pref3"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_farmer_preference4.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Farmer_Pref4"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_gps_data_offset.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_GPD"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_hhcomposition_all_region.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_HHComposition"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_house_asset_all-region.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_House_Asset"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_input_use.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Input_Use"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_institution_variable_all-regions.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Institution"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_land_category_all_region.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Land_Cate"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_livestockowned_allregion.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Livestock"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_processing_machine_allregion.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Proce_Machine"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

meta_df_i, df_left_url = get_meta_url(df_left_url,'metadata_production_asset_all-regions.csv')
meta_df_url = get_csv(meta_df_i)
meta_df_url = proc_meta(meta_df_url)
meta_df_url["Dataset"] = "CMSNHPL_Production_Asset"
meta_df_url = meta_df_url[["Dataset","Column","Col_Desc"]]
meta_df = pd.concat([meta_df, meta_df_url])

df_gender
dict_df_gender = df_dic(df_gender)
dict_CMSNHPL_Trait_All = df_dic(df_CMSNHPL_Trait_All)
dict_df_pre_1_4 = df_dic(df_pre1_4)
dict_df_Variety_All_Region = df_dic(df_Variety_All_Region)
filter(dict_df_gender.has_key, dict_CMSNHPL_Trait_All.keys())
df_Variety_All_Region.info()
df_Variety_All_Region.head()
df_Variety_All_Region.shape

# fig, axs = plt.subplots(2,2)
from pylab import rcParams
rcParams['figure.figsize'] = 20, 20
plt.subplot(221)
df_Variety_All_Region['prodtn_trait1'].value_counts().plot(kind='bar')
plt.title("prodtn_trait1")
plt.xticks(fontsize=10, rotation=60)
spacing = 0.4
plt.subplots_adjust(bottom=spacing)

plt.subplot(222)
df_Variety_All_Region['prodtn_trait2'].value_counts().plot(kind='bar')
plt.title("prodtn_trait2")
plt.xticks(fontsize=10, rotation=60)
spacing = 0.4
plt.subplots_adjust(bottom=spacing)

plt.subplot(223)
df_Variety_All_Region['prodtn_trait3'].value_counts().plot(kind='bar')
plt.title("prodtn_trait3")
plt.xticks(fontsize=10, rotation=60)
spacing = 0.2
plt.subplots_adjust(bottom=spacing)
plt.suptitle('df_Variety_All_Region',size=18)
plt.tight_layout
plt.savefig(PaperDir + "\\Fig\\prodtn_trait.png")
plt.show()

df_pre1_4.head(10)
df_pre1_4['Rank_Score'] = df_pre1_4['B01_Rank']
df_pre1_4['Trait_Id'].unique()
df_pre1_4['Rank_Score'].unique()
df_pre1_4['Rank_Score'] = df_pre1_4['Rank_Score'].replace(['Not important','Moderately Important','Important','Very Important'], [1,2,3,4])
df_pre1_4_agg = df_pre1_4.groupby('Trait_Id')['Rank_Score'].sum().reset_index()

rcParams['figure.figsize'] = 10,10
# plt.figure(figsize=(20, 5))

plt.bar(df_pre1_4_agg['Trait_Id'], df_pre1_4_agg['Rank_Score'])
plt.xticks(fontsize=14, rotation=90)
plt.tight_layout
spacing = 0.3
plt.subplots_adjust(bottom=spacing)
plt.savefig(PaperDir + "\\Fig\\df_pre1_4.png")
plt.show()

df_uniq = df_dic(df_Variety_All_Region[['prodtn_trait1', 'prodtn_trait2', 'prodtn_trait3']])
from itertools import chain
res = list(set(chain.from_iterable(sub.string() for sub in df_uniq)))

res = list(set(val for dic in df_uniq for val in dic.values()))

df_gender_subset = [[ 'Gender',
       'main_activity', 'main_farmer', 'Farmer_all', 'other_farmer',
       'other_processor', 'other_gariseller', 'other_other', 'ownership',
       'farmsize_acre', 'yearly_production', 'home_consumption',
       'where_obtain_stems_new', 'gari_colour_preference',
       'gari_texture_preference', 'gari_taste_preference',
       'root_colour_preference', 'root_size_preference', 'root_yield',
       'fresh_root_yield', 'price', 'maturity_time', 'ground_storage',
       'root_colour', 'root_size', 'dry_matter', 'disease_resistance',
       'gari_taste', 'gari_texture', 'gari_colour', 'gari_swelling',
       'HHsizeMAE', 'HouseholdType', 'Head_EducationLevel_2', 'LandOwned',
       'LandCultivated', 'PPI_Likelihood', 'total_income', 'offfarm_income',
       'farm_income', 'valuefarmproduce', 'cropsales', 'valuecropproduce',
       'livestockprodsales', 'valuelivestockproduction', 'Gender_MaleControl',
       'Gender_FemaleControl', 'Gender_MaleYouthControl',
       'Gender_FemaleYouthControl', 'CropDiv', 'LivestockDiv', 'resp_age',
       'improved', 'HDDS', 'HFIAS', 'clusterPCA', 'clusterPCA_1',
       'clusterPCA_2', 'clusterPCA_3', 'FoodInsecure_yn', 'PPI_Below10',
       'PPI_10to30', 'PPI_over30', 'Region_North', 'Region_SouthEast',
       'Region_SouthSouth', 'Region_SouthWest', 'own_YN', 'rent_YN',
       'obtainstem_simple', 'obtainstem_self', 'obtainstem_neighbor',
       'obtainstem_other', 'household_couple', 'household_femalesingle',
       'main_processor', 'main_gariseller', 'main_other', 'adult_education',
       'no_school', 'postsecondary']]

df_gender['gari_colour_preference'].unique()
df_gender['gari_texture_preference'].unique()
df_gender['ground_storage'].unique()

df_Variety_All_Region['prodtn_trait1'].unique()
df_Variety_All_Region['Serialnumber'].unique()
df_Variety_All_Region['reasn_stopn'].unique()
df_Variety_All_Region['prodtn_trait1'].unique()
df_Variety_All_Region['prodtn_trait2'].unique()
df_Variety_All_Region['prodtn_trait3'].unique()

corr_matrix = df_Variety_All_Region.corr(methods='spearman')

# https://stackoverflow.com/questions/17340922/how-to-search-if-dictionary-value-contains-certain-string-with-python
# https://stats.stackexchange.com/questions/479446/can-i-apply-machine-learning-classifier-to-survey-data-in-order-to-describe

# *********************************************** Integrate metadata ************************************************
# meta_df.to_excel(WorkingDir + "\\Inte_Meta.xlsx")
meta_df = pd.read_excel(WorkingDir + "\\Inte_Meta.xlsx")
meta_df["Dataset"].nunique()
meta_df_trait_col = meta_df[meta_df['Column'].str.contains('trait')]
meta_df_trait_desc = meta_df[meta_df['Col_Desc'].str.contains('trait')]

meta_df_trait = meta_df[(meta_df['Column'].str.contains('preference')) | (meta_df['Column'].str.contains('trait'))
                            | (meta_df['Col_Desc'].str.contains('trait') )|(meta_df['Col_Desc'].str.contains('preference')) |(meta_df['Col_Desc'].str.contains('like'))  ]
# meta_df_trait.to_excel(WorkingDir + "\\Meta_pref.xlsx")
meta_df_trait = pd.read_excel(WorkingDir + "\\Meta_pref.xlsx")

print(df_gender.columns)
print(df_CMSNHPL_Trait_All.columns)

df_gender.info()

df_spouse = pd.read_stata(WorkingDir + "\\Spouse\\Stata\\Cassava_Traits_Spouse_All Regions.dta")
df_spouse.info()
# df_spouse.I01_Trait1.unique()
# df_spouse.I01_2_Trait2.unique()
# df_spouse.I01_Trait1
Rem_list = ['like','cassava' ]
# doc = nlp(df_spouse.I01_Trait1.iloc[0])
# t = [chunk.text for chunk in doc.noun_chunks]

# filtered_sent=[]
# for word in doc:
#     if word.is_stop==False and word.is_punct ==False and word.text not in Rem_list:
#         filtered_sent.append(word)
# print(filtered_sent)
#
# def keyword_keep(words):
#     return  [stopwords for stopwords in nlp(words) if not stopwords.is_stop]
#     # filtered_sent = []
#     # for word in doc:
#     #     if word.is_stop == False and word.is_punct == False and word.text not in Rem_list:
#     #         filtered_sent.append(word)
#
#
# df_spouse['Clean_I01_Trait1'] = df_spouse['I01_Trait1'].apply(keyword_keep())

def stopwords_remover(words):
    return [ stopwords for stopwords in nlp(words)
            if not stopwords.is_stop and not stopwords.is_punct and not stopwords.text in Rem_list ]

df_spouse['Clean_Trait1']  = df_spouse['I01_Trait1'].apply(stopwords_remover)
df_spouse['Clean_Trait2']  = df_spouse['I01_2_Trait2'].apply(stopwords_remover)
df_spouse['Clean_Trait3']  = df_spouse['I01_3_Trait3'].apply(stopwords_remover)


def CateFunc(s):
    if "yield" in s:
        return 'yield'
    elif  ("root" in s):
        if ("big" in s) or ('many' in s) or ('money' in s) or ('plenty' in s) or ('feed' in s) or ('yield' in s) or ('profit' in s) or ('yeild' in s):
            return 'root for high yield or more income'
        elif ('different' in s) or ('various' in s):
            return 'root for different types of food'
        elif ('early' in s):
            return 'root for early mature'
        elif ('white' in s ) and ('gari'):
            return 'root white for gari'
        elif ('yellow' in s):
            return 'root yellow for quality'
        elif ('white' in s):
            return 'root white for high market value'
        elif ('fertilizer' in s):
            return 'root no need for fertilizer'
        elif ('income' in s) or ('value' in s):
            return 'root for money'
        else:
            return 'root in general'
    elif ("low" in s) and ("water" in s):
        return "low water"
    elif  'alubo' in s:
        return 'alubo'
    elif ('garri' in s) or ('gari' in s):
        return 'garri'
    elif 'akpu' in s:
        return 'akpu'
    elif 'lafun' in s:
        return 'lafun'
    # production for next season:
    elif (('high' in s) or ('long' in s)) and ('stem' in s):
        if ('money' in s):
            return 'high/long stem for money'
        elif ('sell' in s) or ('momney' in s):
            return 'high/long stem for money'
        elif  (('plant' in s) or ("multiplication" in s)):
            return 'high/long stem for reproduction'
        elif (('next session' in s) or ("next season")):
            return 'high/long stem for reproduction'
        elif  (('tuber' in s) or ("yeild" in s)):
            return 'high/long stem for yield'
        else:
            return 'high/long stem in general'
    elif  ('garri' in s):
            return 'high/long stem for garri'

    elif  ('matur' in s ) or ('early mturity'):
        return 'early mature'
    elif  'swell' in s:
        return 'swell'
    # marketable:
    elif ('big' in s) and ('tuber' in s):
        return 'big tuber'
    elif ('different variety of food' in s) or ('diffirent types of food' in s) or ('different types of food' in s):
        return 'different types of food'
    elif ('high markt value' in s) or ('high maket demand' in s):
        return 'high market value'
    elif ('raw' in s):
        return 'eat it raw'
    elif ('black leaf' in s):
        return "black leaf for high market value"
    elif ('income' in s):
        return 'income in general'
df_spouse['Cat_Trait1'] = df_spouse['Clean_Trait1'].astype(str).str.lower().apply(CateFunc)
df_spouse['Cat_Trait2'] = df_spouse['Clean_Trait2'].astype(str).str.lower().apply(CateFunc)
df_spouse['Cat_Trait3'] = df_spouse['Clean_Trait3'].astype(str).str.lower().apply(CateFunc)
# df_spouse.head()
df_spouse.to_excel(WorkingDir +"\\Teeken_spouse_proce.xlsx")
df_spouse = pd.read_excel(WorkingDir +"\\Teeken_spouse_proce.xlsx")
# df_spournce_Trait1 = pd.DataFrame(df_spouse['Cat_Trait1'].str.split(expand=True).stack().value_counts())
df_spournce_Trait1 = df_spouse['Cat_Trait1'].value_counts()
df_spournce_Trait1.columns = ["Trait1"]
# df_spournce_Trait2 = pd.DataFrame(df_spouse['Cat_Trait2'].str.split(expand=True).stack().value_counts())
df_spournce_Trait2 = df_spouse['Cat_Trait2'].value_counts()
df_spournce_Trait2.columns = ["Trait2"]
# df_spournce_Trait3 = pd.DataFrame(df_spouse['Cat_Trait3'].str.split(expand=True).stack().value_counts())
df_spournce_Trait3 = df_spouse['Cat_Trait3'].value_counts()
df_spournce_Trait3.columns = ["Trait3"]

df_spournce_Trait1_3 = pd.concat([df_spournce_Trait1, df_spournce_Trait2, df_spournce_Trait3], axis=1)
# df_spournce_Trait1_3_Top10 = df_spournce_Trait1_3[:10]
from pylab import rcParams
rcParams['figure.figsize'] = 10, 10
plt.subplot(221)
df_spournce_Trait1_3['Cat_Trait1'].plot(kind='bar')
plt.title("Cat_Trait1")
plt.xticks(fontsize=10, rotation=90)
spacing = 0.4
plt.subplots_adjust(bottom=spacing)

plt.subplot(222)
df_spournce_Trait1_3['Cat_Trait2'].plot(kind='bar')
plt.title("Cat_Trait2")
plt.xticks(fontsize=10, rotation=90)
spacing = 0.4
plt.subplots_adjust(bottom=spacing)

plt.subplot(223)
df_spournce_Trait1_3['Cat_Trait3'].plot(kind='bar')
plt.title("Cat_Trait3")
plt.xticks(fontsize=10, rotation=90)
spacing = 0.4
plt.subplots_adjust(bottom=spacing)
plt.suptitle('Teeken_Stata_Dataset',size=18)
plt.tight_layout(pad=3.0)
plt.savefig(PaperDir + "\\Fig\\Teeken_Stata.png")
plt.show()


df_CMSNHPL_Trait_All.head()
df_CMSNHPL_Trait_All.info()
df_CMSNHPL_Trait_All.columns
df_CMSNHPL_Trait_All["perc_hhd_food_cass"]
df_CMSNHPL_Trait_All.ZoneID.unique()
df_CMSNHPL_Trait_All.to_excel(WorkingDir+"\\ProcessedData\\CMSNHPL_Trait_All_Region_1.xlsx")
# 4 zones

df_CMSNHPL_Trait_All.StateID.nunique()
# 16 states
fig, ax = plt.subplots()
df_CMSNHPL_Trait_All['perc_hhd_food_cass'].groupby('ZoneID').value_counts().plot(ax=ax, kind='bar')
# df_CMSNHPL_Trait_All['perc_hhd_food_cass'].plot(kind='bar')
plt.show()
# dft = df.groupby(['no_employees']).treatment.value_counts().reset_index(name='Count')
p_df_CMSNHPL_Trait_All = df_CMSNHPL_Trait_All.groupby(["ZoneID"]).perc_hhd_food_cass.

p = sns.barplot(x='Zone',y='perc_hhd_food_cass', data=df_CMSNHPL_Trait_All, hue= 'ZoneID')
df_CMSNHPL_Trait_All['perc_hhd_food_cass'].hist(by=df_CMSNHPL_Trait_All['ZoneID'])
plt.show()

sns.displot(df_CMSNHPL_Trait_All['perc_hhd_food_cass'], col = df_CMSNHPL_Trait_All['ZoneID']  )
plt.show()

df_CMSNHPL_Trait_All_Zone1 = df_CMSNHPL_Trait_All[df_CMSNHPL_Trait_All["ZoneID"]==1]
df_CMSNHPL_Trait_All_Zone2 = df_CMSNHPL_Trait_All[df_CMSNHPL_Trait_All["ZoneID"]==2]
df_CMSNHPL_Trait_All_Zone3 = df_CMSNHPL_Trait_All[df_CMSNHPL_Trait_All["ZoneID"]==3]
df_CMSNHPL_Trait_All_Zone4 = df_CMSNHPL_Trait_All[df_CMSNHPL_Trait_All["ZoneID"]==4]
fig, axs = plt.subplots(ncols=4)
sns.displot(df_CMSNHPL_Trait_All_Zone1["perc_hhd_food_cass"],ax=axs[0])

sns.displot(df_CMSNHPL_Trait_All_Zone2["perc_hhd_food_cass"],ax=axs[1])

sns.displot(df_CMSNHPL_Trait_All_Zone3["perc_hhd_food_cass"], ax=axs[2])

sns.displot(df_CMSNHPL_Trait_All_Zone4["perc_hhd_food_cass"], ax=axs[3])

plt.show()


df_CMSNHPL_Trait_All = pd.read_excel(WorkingDir +"\\ProcessedData\\CMSNHPL_Trait_All_Region.xlsx")
df_CMSNHPL_Trait_All.head()

df_CMSNHPL_Trait_All_Trait1= pd.DataFrame(df_CMSNHPL_Trait_All['Trait1'].astype(str).apply(stopwords_remover))
df_CMSNHPL_Trait_All_Trait1.head()
df_CMSNHPL_Trait_All_Trait1 = df_CMSNHPL_Trait_All_Trait1.rename(columns={'Trait1': 'Clean_Trait1'})

df_CMSNHPL_Trait_All_Trait2  = pd.DataFrame(df_CMSNHPL_Trait_All['Trait2'].astype(str).apply(stopwords_remover))
df_CMSNHPL_Trait_All_Trait2 = df_CMSNHPL_Trait_All_Trait2.rename(columns={'Trait2': 'Clean_Trait2'})

df_CMSNHPL_Trait_All_Trait3  = pd.DataFrame(df_CMSNHPL_Trait_All['Trait3'].astype(str).apply(stopwords_remover))
df_CMSNHPL_Trait_All_Trait3 = df_CMSNHPL_Trait_All_Trait3.rename(columns={'Trait3': 'Clean_Trait3'})

df_CMSNHPL_Trait_All = pd.concat([df_CMSNHPL_Trait_All,df_CMSNHPL_Trait_All_Trait1, df_CMSNHPL_Trait_All_Trait2, df_CMSNHPL_Trait_All_Trait3], axis=1)
df_CMSNHPL_Trait_All.head()

df_CMSNHPL_Trait_All['Cat_Trait1'] = df_CMSNHPL_Trait_All['Clean_Trait1'].astype(str).str.lower().apply(CateFunc)
df_CMSNHPL_Trait_All['Cat_Trait2'] = df_CMSNHPL_Trait_All['Clean_Trait2'].astype(str).str.lower().apply(CateFunc)
df_CMSNHPL_Trait_All['Cat_Trait3'] = df_CMSNHPL_Trait_All['Clean_Trait3'].astype(str).str.lower().apply(CateFunc)
df_CMSNHPL_Trait_All.to_excel(WorkingDir +"\\ProcessedData\\df_CMSNHPL_Trait_All_proce.xlsx")
df_CMSNHPL_Trait_All.HouseID.nunique()
df_CMSNHPL_Trait_All.shape
df_Variety_All_Region = pd.read_excel(WorkingDir + "\\ProcessedData\\CMSNHPL_Variety_All_Region.xlsx" )
df_Variety_All_Region.head
df_Variety_All_Region.shape
df_Variety_All_Region.Imp_cassv_var_name.nunique()

df_Variety_All_Region.HouseID.nunique()
df_Variety_All_Region.Serialnumber.nunique()
df_Variety_All_Region["Imp_cassv_var_name"].nunique()
df_Variety_All_Region = df_Variety_All_Region.dropna(subset = ['Imp_cassv_var_name'])
df_Variety_All_Region_vt = pd.DataFrame(df_Variety_All_Region["Imp_cassv_var_name"].value_counts()).reset_index()
df_Variety_All_Region_vt_pct = pd.DataFrame(df_Variety_All_Region["Imp_cassv_var_name"].value_counts(normalize = True)).reset_index()
df_Variety_All_Region_vt = df_Variety_All_Region_vt.merge(df_Variety_All_Region_vt_pct, on="index")
df_Variety_All_Region_vt.head()
df_Variety_All_Region_vt = df_Variety_All_Region_vt.rename(columns={"Imp_cassv_var_name_x":"Vt_Count", "Imp_cassv_var_name_y":"Vt_freq"})
# del df_count
df_count = pd.DataFrame()
df_count["Count"]  = pd.DataFrame(np.arange(len(df_Variety_All_Region_vt)+1))+1

df_Variety_All_Region_vt = pd.concat([df_Variety_All_Region_vt,df_count], axis = 1, ignore_index=True)
print(df_Variety_All_Region_vt.head())
df_Variety_All_Region_vt.columns = ["Variety","Count","Freq","Rank"]
df_Variety_All_Region.Imp_cassv_var_name.isnull().sum()
df_Variety_All_Region_vt.to_excel(WorkingDir + "\\ProcessedData\\CMSNHPL_Variety_All_Region_Vt.xlsx", sheet_name='Vt_freq' )

df_Variety_All_Region_vt_st = df_Variety_All_Region_vt[df_Variety_All_Region_vt["Number"]<=16]
plt.bar(df_Variety_All_Region_vt_st["Variety"], df_Variety_All_Region_vt_st["Count"])
plt.xticks(fontsize=10, rotation=75)
spacing = 0.5
plt.subplots_adjust(bottom=spacing)
plt.show()

def Find_agric(s):
    if "agric" in s:
        return 1
    else:
        return 0

df_Variety_All_Region_vt_agric = df_Variety_All_Region_vt["Variety"].astype(str).str.lower().apply(Find_agric)
df_Variety_All_Region_vt_agric = pd.concat([df_Variety_All_Region_vt, df_Variety_All_Region_vt_agric], axis=1, ignore_index=True)
df_Variety_All_Region_vt_agric.columns = ["Variety","Count","Freq","Rank", "AGRIC_related"]
df_Variety_All_Region_vt_agric = df_Variety_All_Region_vt_agric[df_Variety_All_Region_vt_agric["AGRIC_related"] ==1]
df_Variety_All_Region_vt_agric.shape
df_Variety_All_Region["Imp_cassv_var_name"].value_counts().plot(kind='bar')

df_Variety_All_Region["Serialnumber"].value_counts().plot(kind='bar')
plt.title('Variety counts')
plt.tight_layout()
plt.show()

df_trait_vat = pd.merge(df_CMSNHPL_Trait_All, df_Variety_All_Region, on='HouseID', how='left')
print(df_trait_vat.head())
df_trait_vat["Variety_cat"] = df_trait_vat["Serialnumber"].astype("category")
df_trait_vat.Cassv_prodt_used1.nunique()

freq_var_use = df_trait_vat.groupby(['ZoneID_x','Variety_cat'])['Variety_cat'].agg({'count'}).reset_index()
freq_var_use = freq_var_use.sort_values(by=[ 'ZoneID_x','count'], ascending=[True,False])

rcParams['figure.figsize'] = 10, 5
freq_var_use.pivot("ZoneID_x","Variety_cat","count").plot(kind='bar')
plt.title("Variety by Zone")
plt.xticks(fontsize=10, rotation=0)
plt.show()

# df_trait_vat.to_excel(WorkingDir + "\\ProcessedData\\CMSNHPL_Trait_Variety.xlsx", sheet_name='Intg')
df_trait_vat.to_excel(WorkingDir + "\\ProcessedData\\CMSNHPL_Trait_Variety.xlsx", sheet_name='left')
df_trait_vat_dup = df_trait_vat[df_trait_vat.duplicated(subset = 'HouseID', keep = False)]
df_trait_vat_dup.head()

writer = pd.ExcelWriter(WorkingDir + "\\ProcessedData\\CMSNHPL_Trait_Variety_proc.xlsx", engine='xlsxwriter')
df_trait_vat_dup.to_excel(writer, sheet_name ="dup")

df_trait_vat_uniqueHH = df_trait_vat.drop_duplicates(subset = ["HouseID"])
df_trait_vat_uniqueHH.to_excel(writer, sheet_name="unique")
writer.save()
writer.close()

freq_zone_hh_vt = df_trait_vat.groupby(['ZoneID_x','HouseID'])['HouseID'].agg({'count'}).reset_index()
freq_zone_hh_vt = freq_zone_hh_vt.sort_values(by=[ 'ZoneID_x','count'], ascending=[True,False])

df_trait_vat_dup.shape
df_trait_vat_sum = pd.DataFrame()
cat1= pd.DataFrame(df_trait_vat["Cat_Trait1"].value_counts()).reset_index()
cat2= pd.DataFrame(df_trait_vat["Cat_Trait2"].value_counts()).reset_index()
cat3= pd.DataFrame(df_trait_vat["Cat_Trait3"].value_counts()).reset_index()
df_trait_vat_sum = cat1.merge( cat2 , on='index')
df_trait_vat_sum = df_trait_vat_sum.merge(cat3, on = 'index')
# df_trait_vat = df_trait_vat.dropna(subset = ['Imp_cassv_var_name'])
df_trait_vat.shape
df_CMSNHPL_Trait_All.shape
df_vat_use1= pd.DataFrame(df_Variety_All_Region["Cassv_prodt_used1"].value_counts()).reset_index()
df_vat_use2= pd.DataFrame(df_Variety_All_Region["Cassav_prodt_used2"].value_counts()).reset_index()
df_vat_use3= pd.DataFrame(df_Variety_All_Region["Cassav_prodt_used3"].value_counts()).reset_index()

freq_var_use = df_Variety_All_Region.groupby(['Imp_cassv_var_name','Cassv_prodt_used1'])['Cassv_prodt_used1'].agg({'count'})
freq_var_use.to_excel(WorkingDir + "\\ProcessedData\\freq_var_use.xlsx")
df_test = df_trait_vat[['Imp_cassv_var_name','Cassv_prodt_used1']]

df_trait_vat_uniqueHH
sns.distplot(df_trait_vat_uniqueHH[["sales_perc"]].astype(float), hist=False, rug=True)
sns.distplot(df_trait_vat_uniqueHH["per_hh_inc_cassav"].str.rstrip('%').astype('float'), hist=False, rug=True)
plt.legend(labels = ['sales','income'])
spacing = 0.2
plt.subplots_adjust(bottom=spacing)
plt.show()

df_trait_vat_uniqueHH[["sales_perc"]].astype(float).plot.kde()
plt.show()

df_trait_vat_uniqueHH["per_hh_inc_cassav"].str.rstrip('%').astype('float').plot.kde()
plt.show()

df_test = df_trait_vat_uniqueHH[["sales_perc","per_hh_inc_cassav"]]
print(df_test.corr())

df_trait_vat_uniqueHH.ZoneID_x.nunique()
df_trait_vat_uniqueHH.StateID_x.nunique()
df_trait_vat_uniqueHH["sales_perc"] = df_trait_vat_uniqueHH["sales_perc"].astype(float)
sns.displot(data =df_trait_vat_uniqueHH , x ="sales_perc", hue='ZoneID_x', kind='kde')
plt.show()

freq_zone_use = df_trait_vat_uniqueHH.groupby(['ZoneID_x','Cassv_prodt_used1'])['Cassv_prodt_used1'].agg({'count'}).reset_index()
freq_zone_use = freq_zone_use.sort_values(by=[ 'ZoneID_x','count'], ascending=[True,False])
from pylab import rcParams
rcParams['figure.figsize'] = 10, 5
freq_zone_use.pivot("ZoneID_x","Cassv_prodt_used1","count").plot(kind='bar')
plt.show()




df_Variety_All_Region_vt_st
df_trait_vat_16Vt = df_Variety_All_Region_vt_st.merge(df_trait_vat, left_on='Variety', right_on='Imp_cassv_var_name', how='left')
df_trait_vat_16Vt.shape

freq_zone_vat = df_Variety_All_Region.groupby(['ZoneID','Serialnumber'])['Serialnumber'].agg({'count'}).reset_index()
freq_zone_vat = freq_zone_vat.sort_values(by=[ 'ZoneID','count'], ascending=[True,False])
rcParams['figure.figsize'] = 10, 5
freq_zone_vat.pivot("ZoneID","Serialnumber","count").plot(kind='bar')
plt.title("Varieties by zone")
plt.show()

# output
writer = pd.ExcelWriter(WorkingDir + "\\ProcessedData\\CMSNHPL_Trait_Variety_proc.xlsx", engine='xlsxwriter')
df_trait_vat_dup.to_excel(writer, sheet_name ="dup")
df_trait_vat_uniqueHH = df_trait_vat.drop_duplicates(subset = ["HouseID"])
df_trait_vat_uniqueHH.to_excel(writer, sheet_name="unique")

freq_zone_use.to_excel(writer, sheet_name ="use")
freq_zone_vat.to_excel(writer, sheet_name='zoneVSvat')

freq_zone_hh_vt.to_excel(writer, sheet_name='zoneVShh')
writer.save()
writer.close()
# sns.color_palette("tab10")
rcParams['figure.figsize'] = 10, 5
sns.displot(data =freq_zone_hh_vt , x ="count", hue='ZoneID_x', kind='kde')
plt.title("Number of varieties by household")
plt.tight_layout()
plt.show()
###############################################################################################
########################             Analysis           #######################################
###############################################################################################
# variety survey
df_Variety_All_Region = pd.read_excel(WorkingDir + "\\ProcessedData\\CMSNHPL_Variety_All_Region.xlsx" )
df_Variety_All_Region['HH_Count'] = df_Variety_All_Region.groupby('HouseID')['HouseID'].transform('count')
df_Variety_All_Region_plt = df_Variety_All_Region[df_Variety_All_Region['Ever_planted']=='Yes']

print(df_Variety_All_Region['HH_Count'].unique() )
df_Variety_All_Region.head()
df_Variety_All_Region.shape
df_Variety_All_Region.reasn_stopn.unique()
df_Variety_All_Region.Year_first_planted.unique()

# plt.hist(df_Variety_All_Region_plt.Year_first_planted, bins=np.arange(1950, 2016, 1))
plt.hist(df_Variety_All_Region_plt.Year_first_planted, bins=np.arange(1950, 2016, 1))

# plt.xticks(np.arange(1950, 2016, 5),fontsize=10, rotation=90)
plt.title("Year_first_planted")
plt.grid()
plt.show()
df_Variety_All_Region_plt.Year_first_planted.max()
df_Variety_All_Region_plt.Year_first_planted.min()
ls_year = pd.DataFrame(df_Variety_All_Region_plt.Year_first_planted.value_counts())
ls_year.reset_index(inplace=True)
ls_year.columns = ['Year','count']
df_Variety_All_Region_plt['Year_first_planted'] =df_Variety_All_Region_plt['Year_first_planted'].astype(int)
df_Variety_All_Region_plt.Year_first_planted.value_counts().sort_index().plot(kind='bar')
plt.xticks(fontsize=8)
plt.title("Planted Varieties: Year_first_planted")
plt.show()

fn_plt(df, col1, col2, col3)

#  acres/size:
df_Variety_All_Region.Unit_Area_cass_pltd.unique()
cvt_dic = {'Hectare': 2.47,'Football field':1.32,'Plot':1/6,'Meter square': 0.000247105  }
df_Variety_All_Region['Cvt_Unit'] = df_Variety_All_Region['Unit_Area_cass_pltd'].map(cvt_dic)

df_Variety_All_Region_stop = df_Variety_All_Region[~df_Variety_All_Region.reasn_stopn.isnull()]
df_Variety_All_Region_stop.shape
df_Variety_All_Region_stop.reasn_stopn.unique()
# plt.hist(df_Variety_All_Region_stop.reasn_stopn, orientation='horizontal')
df_Variety_All_Region_stop.reasn_stopn.value_counts().plot(kind='barh').invert_yaxis()
spacing = 0.5
plt.subplots_adjust(left=spacing)
plt.xticks(fontsize=8, rotation=90)
plt.title('reasn_stopn')
plt.show()
ls_Rea_stop = pd.DataFrame(df_Variety_All_Region_stop.reasn_stopn.value_counts())
ls_Rea_stop.reset_index(inplace=True)
ls_Rea_stop.columns = ['Year','count']
df_Variety_All_Region_stop['ZoneID'] = df_Variety_All_Region_stop['ZoneID'].astype(int)
ls_Rea_stop_zone = pd.DataFrame(df_Variety_All_Region_stop.groupby('ZoneID').reasn_stopn.value_counts())
ls_Rea_stop_zone = ls_Rea_stop_zone.rename(columns={'reasn_stopn':'Count'})
ls_Rea_stop_zone.reset_index(inplace=True)
ls_Rea_stop_zone = ls_Rea_stop_zone.sort_values(by = ['ZoneID', 'Count'], ascending=[True,False])
# ls_Rea_stop.columns = ['Year','count']
sns.displot(data =ls_Rea_stop_zone , x ="Count", hue='ZoneID', kind='kde')
plt.show()
spacing = 0.4
pd.pivot(ls_Rea_stop_zone.reset_index(), index = 'reasn_stopn', columns='ZoneID',values='Count').plot(kind='bar',subplots=True)
plt.subplots_adjust(bottom=spacing)

plt.show()


# (251, 52)
df_Variety_All_Region_stop.prodtntraits_num.unique()
df_Variety_All_Region_stop.processn_trait_no.unique()
df_Variety_All_Region_stop.consumptn_no.unique()
fig,axs =plt.subplots(2,2)
axs[0,0].plt.hist(df_Variety_All_Region_stop.prodtntraits_num)
df_Variety_All_Region_stop_allHH = pd.merge(df_Variety_All_Region, df_Variety_All_Region_stop, how='right',on = ['HouseID'])
df_Variety_All_Region_stop_allHH.shape
df_Variety_All_Region_stop_allHH = df_Variety_All_Region_stop_allHH[(df_Variety_All_Region_stop_allHH.HH_Count_y>1) &
                                    (df_Variety_All_Region_stop_allHH.Ever_planted_x=='Yes')]
df_Variety_All_Region_stop_allHH= df_Variety_All_Region_stop_allHH[df_Variety_All_Region_stop_allHH['reasn_stopn_x'].isnull()]
df_Variety_All_Region_stop_allHH = df_Variety_All_Region_stop_allHH.dropna(subset=['prodtn_trait1_x', 'processing_trait1_x','consumptn_trait1_x'])


df = df_Variety_All_Region_stop_allHH
col1 = "prodtn_trait1_x"
col2 = "processing_trait1_x"
col3 = "consumptn_trait1_x"
fn_plt(df, col1, col2, col3)



df_Variety_All_Region_stop_allHH.to_csv(ProcDataDir+'/stopped.csv',sep='|',index=False)

df_Variety_All_Region.Imp_cassv_var_name.nunique()
df_Variety_All_Region.mnths_var_ready_harv.unique()
df_Variety_All_Region.HouseID.nunique()
df_Variety_All_Region.first_stem_cuttn_source.unique()
# df_Variety_All_Region['prodtn_trait1_count'] = df_Variety_All_Region.groupby('prodtn_trait1')['prodtn_trait1'].transform('count')
df_Variety_All_Region
df_Variety_All_Region_Ge2 = df_Variety_All_Region[df_Variety_All_Region['HH_Count']>1]
df_Variety_All_Region_Ge2.HouseID.nunique()

df_Variety_All_Region_Ge2['Change_prodtn_trait1'] = df_Variety_All_Region_Ge2.groupby('HouseID').prodtn_trait1.transform('nunique').ne(1).map({True:'Y',False:'N'})
df_Variety_All_Region_Ge2 = df_Variety_All_Region_Ge2.drop_duplicates(subset=['HH_Count','HouseID']).reset_index()
df_Variety_All_Region_Ge2.shape
# df_Variety_All_Region_Ge2['HH_ID'] = df_Variety_All_Region_Ge2['HouseID']
# df_Variety_All_Region_Ge2['prodtn_trait1_cp'] = df_Variety_All_Region_Ge2['prodtn_trait1']
# df_Variety_All_Region_Ge2.to_csv(ProcDataDir+'/test.csv',sep='|',index=False)
df_Variety_All_Region_Ge2['HH_Tot_ByNum'] = df_Variety_All_Region_Ge2.groupby('HH_Count')['HH_Count'].transform('count')
df_Variety_All_Region_Ge2['HH_Tot_ByNum_Zone'] = df_Variety_All_Region_Ge2.groupby(['HH_Count', 'ZoneID'])['HH_Count'].transform('count')

df_Variety_All_Region_Ge2_HH_ZoneCount = df_Variety_All_Region_Ge2.drop_duplicates(subset=['HH_Count','ZoneID']).reset_index()
df_Variety_All_Region_Ge2_HH_ZoneCount = df_Variety_All_Region_Ge2_HH_ZoneCount[['ZoneID','HH_Count','HH_Tot_ByNum_Zone']]
df_Variety_All_Region_Ge2_HH_ZoneCount['HH_Tot'] = sum(df_Variety_All_Region_Ge2_HH_ZoneCount['HH_Tot_ByNum_Zone'].astype(int))
df_Variety_All_Region_Ge2_HH_ZoneCount['HH_Tot_Pct_Zone'] = df_Variety_All_Region_Ge2_HH_ZoneCount['HH_Tot_ByNum_Zone']/df_Variety_All_Region_Ge2_HH_ZoneCount['HH_Tot']
df_Variety_All_Region_Ge2_HH_ZoneCount['HH_Count'] = df_Variety_All_Region_Ge2_HH_ZoneCount['HH_Count'].astype(int)
sns.barplot(x='HH_Count', y='HH_Tot_Pct_Zone', hue ='ZoneID',data=df_Variety_All_Region_Ge2_HH_ZoneCount )
plt.show()

pd.pivot_table(df_Variety_All_Region_Ge2_HH_ZoneCount.reset_index(),index = 'HH_Count', columns = 'ZoneID',
               values ='HH_Tot_Pct_Zone' ).plot(subplots=True)
plt.show()

sns.kdeplot(x='HH_Count',data=df_Variety_All_Region_Ge2_HH_ZoneCount, hue='ZoneID', common_norm = False)
spacing = 0.2
plt.subplots_adjust(bottom=spacing)
plt.title('Number of varieties by households by region')
plt.xlabel('Number of Varieties per households')
plt.show()
# variety numbers

df_var = df_Variety_All_Region[['HH_Count', 'ZoneID']]
df_var['HH_Tot_ByNum_Zone'] = df_var.groupby(['HH_Count', 'ZoneID'])['HH_Count'].transform('count')
df_var = df_var.drop_duplicates(subset=['HH_Count', 'ZoneID']).reset_index()
df_var = df_var.dropna()

df_var_p = df_var.pivot(index = 'HH_Count',    columns = 'ZoneID',  values = 'HH_Tot_ByNum_Zone' )
df_var_p.columns =  ['Zone_1','Zone_2','Zone_3','Zone_4']
stat,p_value = kstest(df_var_p['Zone_1'],df_var_p['Zone_2'],df_var_p['Zone_3'],df_var_p['Zone_4'] )
print(p_value)
df_var_p = df_var_p.dropna()
u_statistic, p_value = stats.mannwhitneyu(df_var_p['Zone_4'],df_var_p['Zone_3'] )
print(p_value)
# Mann-Whitney U Test: zone 3 is different from others

df_Variety_All_Region_Ge2_HHCount = df_Variety_All_Region_Ge2.drop_duplicates(subset=['HH_Count']).reset_index()
df_Variety_All_Region_Ge2_HHCount = df_Variety_All_Region_Ge2_HHCount[['HH_Count','HH_Tot_ByNum']]
df_Variety_All_Region_Ge2_HHCount = df_Variety_All_Region_Ge2_HHCount.sort_values(by=['HH_Count'], ascending=True)
df_Variety_All_Region_Ge2_HHCount['HH_Tot'] = sum(df_Variety_All_Region_Ge2_HHCount['HH_Tot_ByNum'].astype(int))
df_Variety_All_Region_Ge2_HHCount['HH_Tot_Pct'] = df_Variety_All_Region_Ge2_HHCount['HH_Tot_ByNum']/df_Variety_All_Region_Ge2_HHCount['HH_Tot']
df_Variety_All_Region_Ge2_HHCount['HH_Count'] = df_Variety_All_Region_Ge2_HHCount['HH_Count'].astype(int)

plt.bar(df_Variety_All_Region_Ge2_HHCount['HH_Count'], df_Variety_All_Region_Ge2_HHCount['HH_Tot_Pct'] )
plt.title('Varieties by households')
plt.show()


df_Variety_All_Region_Ge2['Change_prodtn_trait1_count'] = df_Variety_All_Region_Ge2.groupby('Change_prodtn_trait1')['Change_prodtn_trait1'].transform('count')/df_Variety_All_Region_Ge2.shape[0]
df_Variety_All_Region_Ge2 = df_Variety_All_Region_Ge2.drop_duplicates(subset=['Change_prodtn_trait1'])
df_Variety_All_Region_Ge2['Change_prodtn_trait1_count'].hist()
sns.barplot(x='Change_prodtn_trait1', y = 'Change_prodtn_trait1_count', hue = 'Change_prodtn_trait1', data=df_Variety_All_Region_Ge2)
spacing = 0.15
plt.subplots_adjust(bottom=spacing)
plt.title('Do we need to repeat the question by variety?')
plt.show()





df_Variety_All_Region_plt['Early'] = np.where((df_Variety_All_Region_plt['prodtn_trait1'].str.contains('Early maturity')) |
                                              (df_Variety_All_Region_plt['prodtn_trait2'].str.contains('Early maturity')) |
                                          (df_Variety_All_Region_plt['prodtn_trait3'].str.contains('Early maturity')), "Early Maturity Variety","Non-Early Maturity Variety")
df_Variety_All_Region_plt['Maturity'] = df_Variety_All_Region_plt.groupby(['ZoneID','Early'])['mnths_var_ready_harv'].transform('mean')

df_Variety_All_Region_Early = df_Variety_All_Region_plt[['ZoneID','Early','Maturity']]
df_Variety_All_Region_Early = df_Variety_All_Region_plt.drop_duplicates().reset_index().sort_values(by=['ZoneID','Early'],ascending=[True,True])
df_Variety_All_Region_Early = df_Variety_All_Region_plt[['ZoneID','Early','Maturity' ]]
df_Variety_All_Region_Early = df_Variety_All_Region_Early.drop_duplicates()
sns.barplot(x='ZoneID', y ='Maturity', hue = 'Early', data =df_Variety_All_Region_Early  )
# plt.legend([],[], frameon=False)
plt.xticks(rotation=0)
spacing = 0.3
plt.subplots_adjust(bottom=spacing)
plt.title('How Early is Early')
plt.legend(loc='lower center')
plt.show()


from pingouin import ttest
df_early = df_Variety_All_Region_plt[['ZoneID','Early','mnths_var_ready_harv' ]]
df_early['ZoneID'] = df_early['ZoneID'].astype(int)
df_early_zone1_Yes = df_early[(df_early.ZoneID==1) & (df_early.Early=='Early Maturity Variety')]
df_early_zone1_No = df_early[(df_early.ZoneID==1) & (df_early.Early=='Non-Early Maturity Variety')]

df_early_zone2_Yes = df_early[(df_early.ZoneID==2) & (df_early.Early=='Early Maturity Variety')]
df_early_zone2_No = df_early[(df_early.ZoneID==2) & (df_early.Early=='Non-Early Maturity Variety')]

df_early_zone3_Yes = df_early[(df_early.ZoneID==3) & (df_early.Early=='Early Maturity Variety')]
df_early_zone3_No = df_early[(df_early.ZoneID==3) & (df_early.Early=='Non-Early Maturity Variety')]

df_early_zone4_Yes = df_early[(df_early.ZoneID==4) & (df_early.Early=='Early Maturity Variety')]
df_early_zone4_No = df_early[(df_early.ZoneID==4) & (df_early.Early=='Non-Early Maturity Variety')]


df_early = pd.pivot(df_early,columns='ZoneID',index = 'Early', values='mnths_var_ready_harv')
df_early.reset_index(inplace=True)
df_early.columns = ['Type','Zone1','Zone2','Zone3','Zone4']
ttest(df_early_zone1_Yes['mnths_var_ready_harv'],df_early_zone2_Yes['mnths_var_ready_harv'], correction = False)
ttest(df_early_zone1_Yes['mnths_var_ready_harv'],df_early_zone3_Yes['mnths_var_ready_harv'], correction = False)
ttest(df_early_zone1_Yes['mnths_var_ready_harv'],df_early_zone4_Yes['mnths_var_ready_harv'], correction = False)
ttest(df_early_zone2_Yes['mnths_var_ready_harv'],df_early_zone3_Yes['mnths_var_ready_harv'], correction = False)
ttest(df_early_zone2_Yes['mnths_var_ready_harv'],df_early_zone4_Yes['mnths_var_ready_harv'], correction = False)
ttest(df_early_zone3_Yes['mnths_var_ready_harv'],df_early_zone4_Yes['mnths_var_ready_harv'], correction = False)

from scipy import stats
stats.ttest_ind(df_early_zone1_Yes['mnths_var_ready_harv'],df_early_zone2_Yes['mnths_var_ready_harv'])
# 1155
df_Variety_All_Region.HouseID.nunique()
df_Variety_All_Region.Serialnumber.nunique()
# 10
# 1880
df_count["Cassv_prodt_used1"].unique()
df_Variety_All_Region.shape
# (3600, 50)
df_var_imp = df_Variety_All_Region[['Serialnumber','Imp_cassv_var_name']]
df_var_imp_unique = df_var_imp.drop_duplicates()
df_var_imp_unique = df_var_imp_unique.sort_values(by = ['Serialnumber','Imp_cassv_var_name']).reset_index()
# (1530, 2)
df_var_imp_unique['Check'] = df_var_imp_unique.groupby('Imp_cassv_var_name')['Imp_cassv_var_name'].transform('count')


df_Variety_All_Region['Use_Count'] = df_Variety_All_Region.groupby('Cassv_prodt_used1')['Cassv_prodt_used1'].transform('count')
df_Variety_All_Region['Use_Reg_Count'] = df_Variety_All_Region.groupby(['Cassv_prodt_used1','ZoneID'] )['Cassv_prodt_used1'].transform('count')

df_count_all = df_Variety_All_Region[["Cassv_prodt_used1", 'Use_Count']].dropna().drop_duplicates().reset_index().sort_values(by=['Use_Count'],ascending=False)
df_count_reg = df_Variety_All_Region[['ZoneID', "Cassv_prodt_used1",'Use_Reg_Count']].dropna().drop_duplicates().reset_index().sort_values(by=['Use_Reg_Count'],ascending=False)

plt.bar(x = df_count_all["Cassv_prodt_used1"], height= df_count_all["Use_Count"])
plt.xticks(fontsize=14, rotation=45)
plt.rcParams["figure.figsize"] = [7.50, 3.50]
spacing = 0.5
plt.subplots_adjust(bottom=spacing)
plt.show()

pd.pivot_table(df_count_reg.reset_index(),index='Cassv_prodt_used1',columns='ZoneID', values = 'Use_Reg_Count').plot(subplots = True)
plt.show()

df_count_reg['Tot_reg'] = df_Variety_All_Region.groupby(['ZoneID'] )['Cassv_prodt_used1'].transform('count')
df_count_reg['Freq_reg_pct'] = df_count_reg['Use_Reg_Count']/ df_count_reg['Tot_reg']

sns.barplot(x='Cassv_prodt_used1', y ='Freq_reg_pct', hue = 'ZoneID', data =df_count_reg )
plt.legend(loc='upper right')
# plt.legend([],[], frameon=False)
plt.xticks(rotation=25)
spacing = 0.3
plt.subplots_adjust(bottom=spacing)
plt.show()


df_Variety_All_Region.reasn_stopn.unique()

df_Variety_All_Region_hh = df_Variety_All_Region[['HouseID','HH_Count']]
df_Variety_All_Region.consumptn_trait3.nunique()
df_Variety_All_Region.Cassv_prodt_used1.unique()
df_Variety_All_Region.prodtntraits_num.unique()

def Get_Trait_list(Trait_Name):
    df_1 = df_Variety_All_Region[[Trait_Name]].drop_duplicates().reset_index()
    df_1=df_1.drop(['index'], axis=1)
    df_1['Type'] = Trait_Name
    df_1.columns = ["Trait", "Type"]
    return df_1

df_traits_lt1 = Get_Trait_list('prodtn_trait1')
df_traits_lt2 = Get_Trait_list('prodtn_trait2')
df_traits_lt3 = Get_Trait_list('prodtn_trait3')
df_traits_lt = pd.concat([df_traits_lt1,df_traits_lt2, df_traits_lt3], axis=0, ignore_index=True)
df_traits_lt_prod = df_traits_lt['Trait'].drop_duplicates().reset_index()
df_traits_lt_prod['Type'] = 'Production'
df_traits_lt1 = Get_Trait_list('processing_trait1')
df_traits_lt2 = Get_Trait_list('processing_trait2')
df_traits_lt3 = Get_Trait_list('processing_trait3')
df_traits_lt_proce = pd.concat([df_traits_lt1,df_traits_lt2, df_traits_lt3], axis=0, ignore_index=True)
df_traits_lt_proce = df_traits_lt_proce['Trait'].drop_duplicates().reset_index()
df_traits_lt_proce['Type'] = 'Process'

df_traits_lt1 = Get_Trait_list('consumptn_trait1')
df_traits_lt2 = Get_Trait_list('consumptn_trait2')
df_traits_lt3 = Get_Trait_list('consumptn_trait3')
df_traits_lt_consump = pd.concat([df_traits_lt1,df_traits_lt2, df_traits_lt3], axis=0, ignore_index=True)
df_traits_lt_consump = df_traits_lt_consump['Trait'].drop_duplicates().reset_index()
df_traits_lt_consump['Type'] = 'Consumption'

df_traits_lt = pd.concat([df_traits_lt_prod,df_traits_lt_proce, df_traits_lt_consump ] , axis=0, ignore_index=True)
df_traits_lt = df_traits_lt[['Trait','Type']].drop_duplicates().reset_index()
df_traits_lt['Count'] = df_traits_lt.groupby('Trait')['Trait'].transform('count')

df_traits_lt = pd.concat([df_traits_lt1,df_traits_lt2, df_traits_lt3], axis=0, ignore_index=True)
df_traits_lt_uni =  df_traits_lt['Trait'].drop_duplicates().reset_index()

freq_var = df_Variety_All_Region.groupby(['ZoneID_x','Variety_cat'])['Serialnumber'].agg({'count'}).reset_index()

writer = pd.ExcelWriter(ProcDataDir+"/proc_data_JY.xlsx", engine='xlsxwriter')
df_Variety_All_Region.to_excel(writer,sheet_name='Variety_All')
df_var_imp_unique.to_excel(writer,sheet_name='Ser_Imp')
df_traits_lt.to_excel(writer, sheet_name='Trait_List')
df_traits_lt_uni.to_excel(writer, sheet_name = 'Trait_unic')
df_count_reg.to_excel(writer,sheet_name = 'Use')
df_Variety_All_Region_Early.to_excel(writer,sheet_name='Early')
df_Variety_All_Region_Ge2_HHCount.to_excel(writer,sheet_name='HH_Count')
df_Variety_All_Region_stop.to_excel(writer,sheet_name = 'stopped')
ls_year.to_excel(writer,sheet_name = 'YearAdopted')
writer.save()
writer.close()



df_CMSNHPL_Trait_All= pd.read_excel(WorkingDir +"\\ProcessedData\\CMSNHPL_Trait_All_Region.xlsx")
df_out= df_CMSNHPL_Trait_All.Trait1.unique()
# pd.DataFrame(df_CMSNHPL_Trait_All.Trait1.unique()).to_csv(ProcDataDir+"/Traits.csv")

Rem_list = ['like','cassava' ]

def stopwords_remover(words):
    return [ stopwords for stopwords in nlp(words)
            # if not stopwords.is_stop and not stopwords.is_punct and not stopwords.text in Rem_list ]
            if not stopwords.is_stop and not stopwords.is_punct]

# combine domain knowledge and NLP:
def CateFunc2(s):
    if ('early' in s):
        return 'Early maturity'
    elif ('garri' in s) or ('gari' in s) or ('akpu' in s):
        return 'garri'
    elif ('white' in s):
            return 'White cassava roots'
    elif ('spoil' in s) or ('underground' in s):
            return 'Store well under ground'
    elif ('big' in s) or ('many' in s) or ('high' in s) or ('more' in s):
            return 'High yielding(roots)'

df_CMSNHPL_Trait_All_Trait1= pd.DataFrame(df_CMSNHPL_Trait_All['Trait1'].astype(str).apply(stopwords_remover))
df_CMSNHPL_Trait_All_Trait1.head()
df_CMSNHPL_Trait_All_Trait1 = df_CMSNHPL_Trait_All_Trait1.rename(columns={'Trait1': 'Clean_Trait1'})

df_CMSNHPL_Trait_All_Trait2  = pd.DataFrame(df_CMSNHPL_Trait_All['Trait2'].astype(str).apply(stopwords_remover))
df_CMSNHPL_Trait_All_Trait2 = df_CMSNHPL_Trait_All_Trait2.rename(columns={'Trait2': 'Clean_Trait2'})

df_CMSNHPL_Trait_All_Trait3  = pd.DataFrame(df_CMSNHPL_Trait_All['Trait3'].astype(str).apply(stopwords_remover))
df_CMSNHPL_Trait_All_Trait3 = df_CMSNHPL_Trait_All_Trait3.rename(columns={'Trait3': 'Clean_Trait3'})

df_CMSNHPL_Trait_All = pd.concat([df_CMSNHPL_Trait_All,df_CMSNHPL_Trait_All_Trait1, df_CMSNHPL_Trait_All_Trait2, df_CMSNHPL_Trait_All_Trait3], axis=1)
df_CMSNHPL_Trait_All.head()

df_CMSNHPL_Trait_All['Cat_Trait1'] = df_CMSNHPL_Trait_All['Clean_Trait1'].astype(str).str.lower().apply(CateFunc2)
df_CMSNHPL_Trait_All['Cat_Trait2'] = df_CMSNHPL_Trait_All['Clean_Trait2'].astype(str).str.lower().apply(CateFunc2)
df_CMSNHPL_Trait_All['Cat_Trait3'] = df_CMSNHPL_Trait_All['Clean_Trait3'].astype(str).str.lower().apply(CateFunc2)
df_CMSNHPL_Trait_All['Cat_Trait1_check'] = df_CMSNHPL_Trait_All['Trait1']
df_CMSNHPL_Trait_All.to_excel(WorkingDir +"\\ProcessedData\\test_rootData.xlsx")

df_CMSNHPL_Trait_All['Clean_Trait1'].str[0]

print(df_CMSNHPL_Trait_All['Clean_Trait1'].head())


df_lists = df_CMSNHPL_Trait_All['Clean_Trait1'].tolist()
df_flatten = [val for sublist in df_lists for val in sublist]



df_Erin2 = df_Erin.replace(r"\[",'')
df_Erin2 = df_Erin.str.strep()
df_Erin2 = df_CMSNHPL_Trait_All['Clean_Trait1'].to_numpy()
df_CMSNHPL_Trait_All['Clean_Trait1'].str.replace(r"\[",'')
str(df_CMSNHPL_Trait_All['Clean_Trait1'])[1:-1]
df_pref1 = pd.read_csv(DataDir + "\\farmer_preference1_all-regions.csv")
df_pref1 = df_pref1.rename(columns={"B01_Rank": "Rank"})
df_pref1 = df_pref1.iloc[:,:10]
df_pref1 = df_pref1.drop(['Trait_Id_remark'], axis = 1)
df_pref2 = pd.read_csv(DataDir + "\\farmer_preference2_all-regions.csv")
df_pref2 = df_pref2.iloc[:,:9]
df_pref2 = df_pref2.rename(columns ={'Traits_id':'Trait_Id'})
df_pref3 = pd.read_csv(DataDir + "\\farmer_preference3_all-regions.csv")
df_pref3 = df_pref3.iloc[:,:9]
df_pref3 = df_pref1.rename(columns={"B01_3_Ranking": "Rank", 'trait':'Trait_Id'})

df_pref4 = pd.read_csv(DataDir + "\\farmer_preference4_all-regions.csv")
df_pref4 = df_pref4.iloc[:,:9]
df_pref4 = df_pref4.rename(columns={'Varietal_traits':'Trait_Id', 'Rank_traits':  "Rank"})
df_pref1.Trait_Id_remark.unique()

df_pref_all = pd.concat([df_pref1,df_pref2, df_pref3, df_pref4])
dic_rank = {"Very Important": 4, 'Important':3,'Moderately Important':2, 'Not important':1
            }
df_pref_all['Rank_score'] = df_pref_all['Rank'].map(dic_rank)
df_pref_all_score = df_pref_all.groupby(['Trait_Id'])['Rank_score'].sum().reset_index()


meta_df_url["Dataset"] = "CMSNHPL_Input_Use"

df_beyond = pd.read_csv(WorkingDir +"\\Beyond_womens_traits.csv")
df_beyond.head()
df_beyond.shape
df_beyond.where_obtain_stems_new.unique()
df_beyond.main_activity.unique()
df_beyond.obtainstem_simple.unique()
df_beyond_farmer = df_beyond[df_beyond.main_activity =='Farmer (root producer)']
df_beyond_farmer.shape
df_beyond_farmer.Regions.unique()
df_beyond_farmer.where_obtain_stems_new.value_counts().plot(kind='barh').invert_yaxis()
spacing = 0.5
plt.subplots_adjust(left=spacing)
plt.show()

df_beyond_farmer['Count_StemSource'] = df_beyond_farmer.groupby(['Regions','where_obtain_stems_new'])['where_obtain_stems_new'].transform('count')
df_beyond_farmer_unic = df_beyond_farmer[['Regions','where_obtain_stems_new', 'Count_StemSource']]
df_beyond_farmer_unic = df_beyond_farmer_unic.drop_duplicates().reset_index().sort_values(by=['Regions','where_obtain_stems_new'], ascending=[True, True])
df_beyond_farmer_unic = df_beyond_farmer_unic.dropna(subset=['Count_StemSource'])
spacing = 0.4
spacing_low = 0.5
sns.barplot(data = df_beyond_farmer_unic, hue='where_obtain_stems_new', x='Regions',y='Count_StemSource').plot(subplots =True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.subplots_adjust(right=spacing, bottom=spacing_low)
plt.show()

df_beyond_farmer.improved.unique()
df_beyond_farmer.improved.value_counts().plot(kind='barh').invert_yaxis()
plt.title('Beyond Women')
plt.subplots_adjust(left = 0.3)
plt.show()

df_beyond_farmer['Count_Var_StemSource'] = df_beyond_farmer.groupby(['Regions','where_obtain_stems_new','improved'])['where_obtain_stems_new'].transform('count')
df_beyond_farmer_imp = df_beyond_farmer[['Regions','where_obtain_stems_new', 'improved','Count_Var_StemSource']]
df_beyond_farmer_imp = df_beyond_farmer_imp.drop_duplicates().reset_index().sort_values(by=['Regions','where_obtain_stems_new','improved'], ascending=[True, True,True])
df_beyond_farmer_imp = df_beyond_farmer_imp.dropna(subset=['Count_Var_StemSource'])

plt.subplot(2,1,1)
sns.barplot(data = df_beyond_farmer_imp[df_beyond_farmer_imp.improved=='yes.improved'].reset_index().sort_values(by=['Regions','Count_Var_StemSource'], ascending=[True, True]), hue='where_obtain_stems_new', x='Regions',y='Count_Var_StemSource').plot(subplots =True)
plt.subplots_adjust(right=0.45, hspace=1)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',fontsize=8)
plt.xticks(fontsize=7, rotation=45)
plt.title('Yes.improved')

plt.subplot(2,1,2)
sns.barplot(data = df_beyond_farmer_imp[df_beyond_farmer_imp.improved=='no.improved '].reset_index().sort_values(by=['Regions','Count_Var_StemSource'], ascending=[True, True]), hue='where_obtain_stems_new', x='Regions',y='Count_Var_StemSource').plot(subplots =True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',fontsize=8)
plt.xticks(fontsize=7, rotation=45)
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.subplots_adjust(bottom=0.15 )
plt.title('No.improved')

plt.show()

df_beyond_farmer_imp = df_beyond_farmer_imp.reset_index().sort_values(by=['improved', 'Regions','Count_Var_StemSource'], ascending=[True, True, False])
df_beyond_farmer['Gov_NGO'] = np.where((df_beyond_farmer['where_obtain_stems_new'] =='From NGOs, extension workers or projects') | (df_beyond_farmer['where_obtain_stems_new'] =='From NGOs, extension workers or projects'), 1, 0)
df_beyond_farmer_ngo = df_beyond_farmer[df_beyond_farmer['Gov_NGO'] ==1]
df_beyond_farmer_ngo.shape
# 5% of farms received from government & NGO
df_beyond_farmer.shape
df_beyond_farmer_imp_check = df_beyond_farmer[df_beyond_farmer.improved=='yes.improved']
df_beyond_farmer_imp_check.shape
# (327, 88)

df_beyond_farmer_imp.to_csv(ProcDataDir+"/ImpVSNo.csv", sep='|',index=False)

df_beyond_farmer_ngo.Gender_MaleControl.unique()

df_beyond_farmer_ngo.Gender_MaleControl.value_counts().plot(kind='barh').invert_yaxis()
plt.title('Total value of activities (TVA) which is controlled by a male',fontsize=10)
plt.subplots_adjust(left=.4)
plt.show()


df_beyond_farmer_ngo.adult_education.value_counts().plot(kind='barh').invert_yaxis()
plt.show()

root_yield
dry_matter
PPI_Likelihood
total_income
offfarm_income
farm_income

df_beyond_farmer['Count_Var_StemSourceAllReg'] = df_beyond_farmer.groupby(['where_obtain_stems_new','improved'])['where_obtain_stems_new'].transform('count')
df_beyond_farmer_imp_Allregs = df_beyond_farmer[['improved','where_obtain_stems_new','Count_Var_StemSourceAllReg']]
df_beyond_farmer_imp_Allregs = df_beyond_farmer_imp_Allregs.drop_duplicates(subset =['improved','where_obtain_stems_new'])
df_beyond_farmer_imp_Allregs = df_beyond_farmer_imp_Allregs.reset_index().sort_values(by=['improved', 'Count_Var_StemSourceAllReg'], ascending=[True,  False])
df_beyond_farmer_imp_Allregs.to_csv(ProcDataDir+"/ImpVSNo_Allregions.csv", sep='|',index=False)

df_beyond_farmer.FoodInsecure_yn.unique()
df_beyond_farmer['Count_Var_StemSourceAllReg_FI'] = df_beyond_farmer.groupby(['FoodInsecure_yn','where_obtain_stems_new','improved'])['where_obtain_stems_new'].transform('count')
df_beyond_farmer_imp_Allregs_FI = df_beyond_farmer[['improved','where_obtain_stems_new','FoodInsecure_yn','Count_Var_StemSourceAllReg_FI']]
df_beyond_farmer_imp_Allregs_FI = df_beyond_farmer_imp_Allregs_FI.drop_duplicates(subset =['improved','where_obtain_stems_new','FoodInsecure_yn']).sort_values(by=['improved', 'Count_Var_StemSourceAllReg_FI'], ascending=[True,  False])
df_beyond_farmer_imp_Allregs_FI.to_csv(ProcDataDir+"/df_beyond_farmer_imp_Allregs_FI.csv", sep='|',index=False)

df_beyond_farmer['Count_Imp_FI'] = df_beyond_farmer.groupby(['FoodInsecure_yn', 'improved'])['FoodInsecure_yn'].transform('count')
df_beyond_farmer_imp_FI = df_beyond_farmer[['improved','FoodInsecure_yn','Count_Imp_FI']]
df_beyond_farmer_imp_FI = df_beyond_farmer_imp_FI.drop_duplicates(subset =['improved','FoodInsecure_yn']).sort_values(by=['improved', 'Count_Imp_FI'], ascending=[True,  False])
df_beyond_farmer_imp_FI.to_csv(ProcDataDir+"/df_beyond_farmer_imp_FI.csv", sep='|',index=False)


df_beyond_farmer['Count_Var_StemSourceAllReg_FI'].value_counts().plot(kind='barh').invert_yaxis()
plt.title('Beyond Women')
plt.subplots_adjust(left = 0.3)
plt.show()

household_femalesingle
df_beyond_farmer['Count_Imp_Gen'] = df_beyond_farmer.groupby(['household_femalesingle', 'improved'])['improved'].transform('count')
df_beyond_farmer_imp_gen = df_beyond_farmer[['improved','household_femalesingle','Count_Imp_Gen']]
df_beyond_farmer_imp_gen = df_beyond_farmer_imp_gen.drop_duplicates(subset =['improved','household_femalesingle']).sort_values(by=['improved', 'Count_Imp_Gen'], ascending=[True,  False])
df_beyond_farmer_imp_gen.to_csv(ProcDataDir+"/df_beyond_farmer_imp_gen.csv", sep='|',index=False)


import pyreadstat
TempDir = r"D:\Dropbox\BoxOld\FEDSshare\MasterGithub\CornellGitHub\DataSynthesisForCropVariety\Gender\ExistingCode"
df, meta = pyreadstat.read_sav(TempDir + "/MethodsPaperDataSet_HH.sav")
df.head()
df.shape
df.to_excel()
