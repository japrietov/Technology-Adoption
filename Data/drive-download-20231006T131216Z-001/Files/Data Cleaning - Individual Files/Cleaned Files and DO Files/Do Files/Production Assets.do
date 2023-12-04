
gen Total_Production_Asset_Value=0
replace Total_Production_Asset_Value=(G05b_Number*G06 _Value_Naira)
gen Male__Production_Value=0
replace Male__Production_Value=(G06_Value_Naira*G08_men_portn)
gen Women__Production_Value=0
replace Women__Production_Value=(G07_women_portn*G06_Value_Naira)

*spade*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Production_asset_All regions.dta"
drop ZoneID StateID LgaID LocalityID EnumerationID
keep if production_asset==7
drop production_asset

rename G05a_asset_ownership Shovel_Own
rename G05b_Number Shovel_Number_Own
rename G06_Value_Naira Shovel_Avg_Value
rename G08_men_portn Men_Shovel_Own
rename G07_women_portn Women_Shovel_Own
rename Total_Production_Asset_Value Shovel_Total_Value
rename Male__Production_Value Male_Shovel_Value
rename Women__Production_Value Women_Shovel_Value
label variable Shovel_Own "shovel/spade owned by household, yes/no"
label variable Shovel_Number_Own "number of shovel/spades owned"
label variable Shovel_Avg_Value "avg value of 1 shovel/spade"
label variable Women_Shovel_Own "number of shovel/spades women own"
label variable Men_Shovel_Own "number of shovel/spade men own"

*hoe*
use "/Users/Davis/Desktop/Methodology Paper/Methodology Paper Data Sets/Data Cleaning Files/Original Files - Not Cleaned/CMS (entire database)/Files/Production_asset_All regions.dta"
drop ZoneID StateID LgaID LocalityID EnumerationID
keep if production_asset==3
drop production_asset
rename G05a_asset_ownership Hoe_Own
rename G05b_Number Hoe_Number_Own
rename G06_Value_Naira Hoe_Avg_Value
rename G08_men_portn Men_Hoe_Own
rename G07_women_portn Women_SHoe_Own
rename Total_Production_Asset_Value Hoe_Total_Value
rename Male__Production_Value Male_Hoe_Value
rename Women__Production_Value Women_Hoe_Value
label variable Hoe_Own "Hoe owned by household, yes/no"
label variable Hoe_Number_Own "number of Hoe owned"
label variable Hoe_Avg_Value "avg value of 1 Hoe"
label variable Women_Hoe_Own "number of Hoe women own"
label variable Men_Hoe_Own "number of Hoe men own"

