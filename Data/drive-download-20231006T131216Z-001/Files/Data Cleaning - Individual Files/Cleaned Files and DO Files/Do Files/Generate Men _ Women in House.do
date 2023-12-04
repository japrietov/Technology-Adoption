use "/Users/Davis/Desktop/Methodology Cleaning 2/Original Files - Not Cleaned copy/CMS (entire database)/Files/Household_composition_All regions.dta"

*change file for wife responses*

gen Women_In_House=0
replace Women_In_House=1 if A02_Sex==0
gen Men_In_House=0
replace Men_In_House=1 if A02_Sex==1

collapse (sum) Men_In_House Women_In_House, by(HouseID)
label variable Men_In_House "men in house greater than 12 yearsold"
label variable Women_In_House "women in house greater than 12 years old"

