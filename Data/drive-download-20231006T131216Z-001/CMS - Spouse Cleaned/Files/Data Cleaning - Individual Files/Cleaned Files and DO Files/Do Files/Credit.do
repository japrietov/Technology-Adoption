keep HouseID Institution_Id H03_4_credit_access H03_5_credit_source1 H03_5_credit_source2 H03_6_ever_gtn_loan

gen House_Credit=0

gen Male_Credit=0

gen Female_Credit=0

replace House_Credit=1 if (H03_4_credit_access*Institution_Id)==1
replace Male_Credit=1 if (Institution_Id*H03_4_credit_access)==3
replace Female_Credit=1 if (Institution_Id*H03_4_credit_access)==2

collapse (sum)House_Credit Male_Credit Female_Credit, by(HouseID)

gen Male_Credit_Only=0
gen Female_Credit_Only=0
gen Joint_Credit=0

replace Male_Credit_Only=1 if (Female_Credit-Male_Credit)==-1
replace Female_Credit_Only=1 if (Male_Credit-Female_Credit)==-1
replace Joint_Credit=1 if (Male_Credit+Female_Credit)==2

drop House_Credit Male_Credit Female_Credit

label variable Male_Credit_Only "only male access to credit"
label variable Female_Credit_Only "only female access to credit"
label variable Joint_Credit "joint male/female access to credit"

gen Credit_Access=0
replace Credit_Access=1 if (Male_Credit_Only+ Female_Credit_Only+ Joint_Credit)>0
label variable Credit_Access "general household credit access"


