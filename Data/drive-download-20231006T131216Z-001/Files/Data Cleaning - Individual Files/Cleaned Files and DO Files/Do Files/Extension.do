*USE INSTITUION FILE*


 destring H03_3_MaleContact_No, replace
 replace H03_3_MaleContact_No=0 if H03_3_MaleContact_No==.
 replace H03_0_Ecntact=0 if H03_0_Ecntact==.
 replace H03_2_FemaleContact_No=0 if H03_2_FemaleContact_No==.
 
 gen Extension_Access=0
 replace Extension_Access=1 if H03_0_Ecntact>0
 gen Male_Ext_Access=0
replace Male_Ext_Access=1 if H03_3_MaleContact_No>0
gen Female_Ext_Access=0
replace Female_Ext_Access=1 if H03_2_FemaleContact_No>0
collapse (mean)Extension_Access Male_Ext_Access Female_Ext_Access, by(HouseID)

replace Extension_Access=1 if Extension_Access>0
replace Male_Ext_Access=1 if Male_Ext_Access>0
replace Female_Ext_Access=1 if Female_Ext_Access>0
gen Male_Ext_Only=0
replace Male_Ext_Only=1 if (Female_Ext_Access-Male_Ext_Access)==-1
 gen Female_Ext_Only=0
replace Female_Ext_Only=1 if (Male_Ext_Access-Female_Ext_Access)==-1
 gen Joint_Ext_Access=0
replace Joint_Ext_Access=1 if (Male_Ext_Access+ Female_Ext_Access)>1
drop Male_Ext_Access Female_Ext_Access

label variable Male_Ext_Only "only men have access to extension"
label variable Female_Ext_Only "only women have access to extension"
label variable Joint_Ext_Access "both men/women have access to extension"
label variable Extension_Access "general household extension access"
