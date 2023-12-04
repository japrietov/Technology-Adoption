gen Animal_Unit=0
replace Animal_Unit=1 if Livestock_owned==1
replace Animal_Unit=1.25 if Livestock_owned==2
replace Animal_Unit=2 if Livestock_owned==3
replace Animal_Unit=.1 if Livestock_owned==4
replace Animal_Unit=.1 if Livestock_owned==5
replace Animal_Unit=.02 if Livestock_owned==6
replace Animal_Unit=.02 if Livestock_owned==7
replace Animal_Unit=.01 if Livestock_owned==8
replace Animal_Unit=.35 if Livestock_owned==9

*these numbers are derived from US Federal Guidelines and Illinois Extension*

drop if Livestock_owned==10

replace G01b_TNumber_owned=0 if G01b_TNumber_owned==.
replace G02_Num_own_male=0 if G02_Num_own_male==.
replace G03_Num_own_female=0 if G03_Num_own_female==.

gen HouseHold_AnimalUnits=0
replace HouseHold_AnimalUnits=(Animal_Unit*G01b_TNumber_owned)

gen Male_Owned_Livestock=0
replace Male_Owned_Livestock=(G02_Num_own_male*Animal_Unit)

gen Female_Owned_Livestock=0
replace Female_Owned_Livestock=(Animal_Unit*G03_Num_own_female)

collapse (sum) HouseHold_AnimalUnits Male_Owned_Livestock Female_Owned_Livestock, by(HouseID)
label variable HouseHold_AnimalUnits "total animal units owned by household"
label variable Male_Owned_Livestock "total animal units owned by male"
label variable Female_Owned_Livestock "total animal units owned by female"
