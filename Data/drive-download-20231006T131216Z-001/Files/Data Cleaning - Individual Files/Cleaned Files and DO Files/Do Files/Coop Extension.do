use "/Users/Davis/Desktop/Methodology Cleaning 2/Original Files - Not Cleaned copy/Spouse (wife)/Association_Spouse_All regions.dta"

keep if Association==5
drop EnumerationID LocalityID LgaID StateID ZoneID
rename H01_Ass_member Credit_Group_Member
rename H02_female_member_ass Women_Credit_Group
rename H02_male_member_hhd Men_Credit_Group
label variable Credit_Group_Member "household member in credit group"
label variable Women_Credit_Group "women in credit group"
label variable Men_Credit_Group "men in credit group"
gen Male_CreditGroup_Only=0
replace Male_CreditGroup_Only=1 if (Women_Credit_Group-Men_Credit_Group)==-1
gen Women_CreditGroup_Only=0
replace Women_CreditGroup_Only=1 if (Men_Credit_Group-Women_Credit_Group)==-1
gen Joint_CreditGroup=0
replace Joint_CreditGroup=1 if (Women_Credit_Group+ Men_Credit_Group)==2
label variable Male_CreditGroup_Only "male only membership to credit group"
label variable Women_CreditGroup_Only "women only membership to credit group"
label variable Joint_CreditGroup "joint men/women membership to credit group"
drop Men_Credit_Group Women_Credit_Group Association


use "/Users/Davis/Desktop/Methodology Cleaning 2/Original Files - Not Cleaned copy/Spouse (wife)/Association_Spouse_All regions.dta"

keep if Association==6
drop EnumerationID LocalityID LgaID StateID ZoneID
rename H01_Ass_member Coop_Group_Member
rename H02_female_member_ass Women_Coop_Group
rename H02_male_member_hhd Men_Coop_Group
label variable Coop_Group_Member "household member in coop group"
label variable Women_Coop_Group "women in coop group"
label variable Men_Coop_Group "men in coop group"
gen Men_Only_Coop=0
replace Men_Only_Coop=1 if (Women_Coop_Group-Men_Coop_Group)==-1
gen Women_Only_Coop=0
replace Women_Only_Coop=1 if (Men_Coop_Group-Women_Coop_Group)==-1
gen Joint_Coop=0
replace Joint_Coop=1 if (Women_Coop_Group+ Men_Coop_Group)==2
label variable Men_Only_Coop "men only membership of a coop"
label variable Women_Only_Coop "women only membership of a coop"
label variable Joint_Coop "both men/women members of a coop"
drop Men_Coop_Group Women_Coop_Group Association
