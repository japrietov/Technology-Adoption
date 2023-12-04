*Moto*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Household_assets_All regions.dta"
keep if Household_assets==18
rename G05a_hhd_asset_own Moto_Owned
rename G05b_TNumber Number_Motos_Owned
rename G06_UnitValue_Naira Moto_Avg_value
rename G07_women_portion Moto_Own_Women
rename G08_men_protion Moto_Own_Men
rename Total_Household_Asset_Value Moto_Asset_Value
rename Women_Owned_HHAsset_Value Moto_Women_Value
rename Male_Owned_HHAsset_Value Moto_Men_Value
label variable Moto_Owned "motorcycle owned, yes/no"
label variable Number_Motos_Owned "number of motos in household"
label variable Moto_Avg_value "value in Naira, 1 moto"
label variable Moto_Own_Women "number of motos owned by men"
label variable Moto_Own_Men "number of motos owned by men"
label variable Moto_Own_Women "number of motos owned by women"
label variable Moto_Asset_Value "total Naira value of all motos in house"
label variable Moto_Women_Value "Naira value of motos owned by women"
label variable Moto_Men_Value "Naira value of motos owned by men"


*Radio*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Household_assets_All regions.dta"
keep if Household_assets==12
rename G05a_hhd_asset_own Radio_Owned
rename G05b_TNumber Number_Radios_Owned
rename G06_UnitValue_Naira Radio_Avg_value
rename G07_women_portion Radio_Own_Women
rename G08_men_protion Radio_Own_Men
rename Total_Household_Asset_Value Radio_Asset_Value
rename Women_Owned_HHAsset_Value Radio_Women_Value
rename Male_Owned_HHAsset_Value Radio_Men_Value
label variable Radio_Owned "radios owned, yes/no"
label variable Number_Radios_Owned "number of radios in household"
label variable Radio_Avg_value "value in Naira, 1 radio"
label variable Radio_Own_Women "number of radios owned by men"
label variable Radio_Own_Men "number of radios owned by men"
label variable Radio_Own_Women "number of radios owned by women"
label variable Radio_Asset_Value "total Naira value of all radios in house"
label variable Radio_Women_Value "Naira value of radios owned by women"
label variable Radio_Men_Value "Naira value of radios owned by men"


*Bike*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Household_assets_All regions.dta"
keep if Household_assets==17
rename G05a_hhd_asset_own Bike_Owned
rename G05b_TNumber Number_Bikes_Owned
rename G06_UnitValue_Naira Bike_Avg_value
rename G07_women_portion Bike_Own_Women
rename G08_men_protion Bike_Own_Men
rename Total_Household_Asset_Value Bike_Asset_Value
rename Women_Owned_HHAsset_Value Bike_Women_Value
rename Male_Owned_HHAsset_Value Bike_Men_Value
label variable Bike_Owned "bikess owned, yes/no"
label variable Number_Bikes_Owned "number of bikes in household"
label variable Bike_Avg_value "value in Naira, 1 bike"
label variable Bike_Own_Women "number of bikes owned by men"
label variable Bike_Own_Men "number of bikes owned by men"
label variable Bike_Own_Women "number of bikes owned by women"
label variable Bike_Asset_Value "total Naira value of all bikes in house"
label variable Bike_Women_Value "Naira value of bikes owned by women"
label variable Bike_Men_Value "Naira value of bikes owned by men"


*Dish*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Household_assets_All regions.dta"
keep if Household_assets==22
rename G05a_hhd_asset_own Dishes_Owned
rename G05b_TNumber Number_Dishes_Owned
rename G06_UnitValue_Naira Dishes_Avg_value
rename G07_women_portion Dishes_Own_Women
rename G08_men_protion Dishes_Own_Men
rename Total_Household_Asset_Value Dishes_Asset_Value
rename Women_Owned_HHAsset_Value Dishes_Women_Value
rename Male_Owned_HHAsset_Value Dishes_Men_Value
label variable Dishes_Owned "Dishes owned, yes/no"
label variable Number_Dishes_Owned "number of Dishes in household"
label variable Dishes_Avg_value "value in Naira, 1 Dishes"
label variable Dishes_Own_Women "number of Dishes owned by men"
label variable Dishes_Own_Men "number of Dishes owned by men"
label variable Dishes_Own_Women "number of Dishes owned by women"
label variable Dishes_Asset_Value "total Naira value of all Dishes in house"
label variable Dishes_Women_Value "Naira value of Dishes owned by women"
label variable Dishes_Men_Value "Naira value of Dishes owned by men"


*Jewellery*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Household_assets_All regions.dta"
keep if Household_assets==20
rename G05a_hhd_asset_own Jewel_Owned
rename G05b_TNumber Number_Jewel_Owned
rename G06_UnitValue_Naira Jewel_Avg_value
rename G07_women_portion Jewel_Own_Women
rename G08_men_protion Jewel_Own_Men
rename Total_Household_Asset_Value Jewel_Asset_Value
rename Women_Owned_HHAsset_Value Jewel_Women_Value
rename Male_Owned_HHAsset_Value Jewel_Men_Value
label variable Jewel_Owned "jewellery owned, yes/no"
label variable Number_Jewel_Owned "number of jewellery in household"
label variable Jewel_Avg_value "value in Naira, 1 jewellery"
label variable Jewel_Own_Women "number of jewellery owned by men"
label variable Jewel_Own_Men "number of jewellery owned by men"
label variable Jewel_Own_Women "number of jewellery owned by women"
label variable Jewel_Asset_Value "total Naira value of all jewellery in house"
label variable Jewel_Women_Value "Naira value of jewellery owned by women"
label variable Jewel_Men_Value "Naira value of jewellery owned by men"


*Cell*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Household_assets_All regions.dta"
keep if Household_assets==15
rename G05a_hhd_asset_own Cell_Owned
rename G05b_TNumber Number_Cell_Owned
rename G06_UnitValue_Naira Cell_Avg_value
rename G07_women_portion Cell_Own_Women
rename G08_men_protion Cell_Own_Men
rename Total_Household_Asset_Value Cell_Asset_Value
rename Women_Owned_HHAsset_Value Cell_Women_Value
rename Male_Owned_HHAsset_Value Cell_Men_Value
label variable Cell_Owned "cellphone owned, yes/no"
label variable Number_Cell_Owned "number of cellphone in household"
label variable Cell_Avg_value "value in Naira, 1 cellphone"
label variable Cell_Own_Women "number of cellphone owned by men"
label variable Cell_Own_Men "number of cellphone owned by men"
label variable Cell_Own_Women "number of cellphone owned by women"
label variable Cell_Asset_Value "total Naira value of all cellphone in house"
label variable Cell_Women_Value "Naira value of cellphone owned by women"
label variable Cell_Men_Value "Naira value of cellphone owned by men"

