clear
import delimited "C:\Users\yi7\Dropbox\UW\Research\Cassava\AugCode25\Technology-Adoption-main\Technology-Adoption-main\Output\df_F_independent_tmp.csv",clear

save "C:\Users\yi7\Dropbox\UW\Research\Cassava\AugCode25\Technology-Adoption-main\Technology-Adoption-main\Output\df_F_independent_tmp.dta", replace

* Choose the 3 dummies; drop zone4 to make it the base
gen zoneid = .
replace zoneid = 1 if zone1 == 1
replace zoneid = 2 if zone2 == 1
replace zoneid = 3 if zone3 == 1
replace zoneid = 4 if zone4 ==1

label variable jointmanaged          "Joint Managed"
label variable jointcoop            "Joint Coop"
label variable jointcredit          "Joint Credit"
label variable jointprocessingaccess "Joint Processing Access"
label variable zone1                "Zone 1"
label variable zone2                "Zone 2"
label variable zone3                "Zone 3"
label variable age                 "Age"
label variable education           "Education"
label variable meninhouse          "Men in House"
label variable womeninhouse        "Women in House"
label variable kids                "Kids"
label variable contributiontofarmwork "Contribution to Farm Work"
	

probit  ynicv  jointmanaged jointcoop jointcredit jointprocessing zone1 zone2 zone3 ///
                age education meninhouse womeninhouse kids contributiontofarmwor, vce(cluster zoneid)
margins, dydx(*) post
esttab ., se star(* 0.10 ** 0.05 *** 0.01) label
esttab using "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\meffect_F.doc", se star(* 0.10 ** 0.05 *** 0.01) label replace

* Test differences between Zone 1 and Zone 2
test zone1 = zone2
* Test differences between Zone 1 and Zone 3
test zone1 = zone3
* Test differences between Zone 2 and Zone 3
test zone2 = zone3
			
// margins, dydx(*)   atmeans post // marginal effects for all covariates
// outreg2 using  "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\marginal_effects_F.doc", word replace ctitle(Marginal Effects) dec(3)

// margins, dydx(*)    atmeans post // marginal effects for all covariates
outreg2 using  "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\marginal_effects_F2.doc", word replace ctitle(Wives) dec(3)


nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster zoneid)

	
* Test difference between zone1 and zone2
test zone1 = zone2
* Test difference between zone1 and zone3
test zone1 = zone3
* Test difference between zone2 and zone3
test zone2 = zone3

outreg2 using  "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\NegB_F2.doc", word replace ctitle(Wives) dec(3)
//---------------------------------------------------------------------------------------//
import delimited "C:\Users\yi7\Dropbox\UW\Research\Cassava\AugCode25\Technology-Adoption-main\Technology-Adoption-main\Output\df_M_independent_tmp.csv",clear
save "C:\Users\yi7\Dropbox\UW\Research\Cassava\AugCode25\Technology-Adoption-main\Technology-Adoption-main\Output\df_M_independent_tmp.dta", replace

gen zoneid = .
replace zoneid = 1 if zone1 == 1
replace zoneid = 2 if zone2 == 1
replace zoneid = 3 if zone3 == 1
replace zoneid = 4 if zone4 ==1

label variable jointmanaged          "Joint Managed"
label variable jointcoop            "Joint Coop"
label variable jointcredit          "Joint Credit"
label variable jointprocessingaccess "Joint Processing Access"
label variable zone1                "Zone 1"
label variable zone2                "Zone 2"
label variable zone3                "Zone 3"
label variable age                 "Age"
label variable education           "Education"
label variable meninhouse          "Men in House"
label variable womeninhouse        "Women in House"
label variable kids                "Kids"
label variable contributiontofarmwork "Contribution to Farm Work"				

probit  ynicv  jointmanaged jointcoop jointcredit jointprocessing zone1 zone2 zone3 ///
                age education meninhouse womeninhouse kids contributiontofarmwor, vce(cluster zoneid)
margins, dydx(*) post   // marginal effects for all covariates
esttab ., se star(* 0.10 ** 0.05 *** 0.01) label
esttab using "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\meffect_M.doc", se star(* 0.10 ** 0.05 *** 0.01) label replace

test zone1 = zone2
* Test differences between Zone 1 and Zone 3
test zone1 = zone3
* Test differences between Zone 2 and Zone 3
test zone2 = zone3
// margins, dydx(*)   atmeans post // marginal effects for all covariates
outreg2 using  "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\marginal_effects_F2.doc", word append ctitle(Husbands) dec(3)

nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster zoneid)
test zone1 = zone2
* Test differences between Zone 1 and Zone 3
test zone1 = zone3
* Test differences between Zone 2 and Zone 3
test zone2 = zone3
outreg2 using  "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\NegB_F2.doc", word append ctitle(Husbands) dec(3)
//---------------------------------------------------------------------------------------//	

import delimited "C:\Users\yi7\Dropbox\UW\Research\Cassava\AugCode25\Technology-Adoption-main\Technology-Adoption-main\Output\df_H_independent_tmp.csv",clear
gen zoneid = .
replace zoneid = 1 if zone1 == 1
replace zoneid = 2 if zone2 == 1
replace zoneid = 3 if zone3 == 1
replace zoneid = 4 if zone4 ==1

label variable jointmanaged          "Joint Managed"
label variable jointcoop            "Joint Coop"
label variable jointcredit          "Joint Credit"
label variable jointprocessingaccess "Joint Processing Access"
label variable zone1                "Zone 1"
label variable zone2                "Zone 2"
label variable zone3                "Zone 3"
label variable age                 "Age"
label variable education           "Education"
label variable meninhouse          "Men in House"
label variable womeninhouse        "Women in House"
label variable kids                "Kids"
label variable contributiontofarmwork "Contribution to Farm Work"
probit  ynicv  jointmanaged jointcoop jointcredit jointprocessing zone1 zone2 zone3 ///
                age education meninhouse womeninhouse kids contributiontofarmwor, vce(cluster zoneid)			
esttab ., se star(* 0.10 ** 0.05 *** 0.01) label
esttab using "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\meffect_HH.doc", se star(* 0.10 ** 0.05 *** 0.01) label replace

// margins, dydx(*)   atmeans post // marginal effects for all covariates
outreg2 using  "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\hh_probit.doc", word replace ctitle(Household) dec(3)
test zone1 = zone2
* Test differences between Zone 1 and Zone 3
test zone1 = zone3
* Test differences between Zone 2 and Zone 3
test zone2 = zone3


nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster zoneid)
outreg2 using  "C:\Users\yi7\Dropbox\UW\Research\Cassava\Aug2025\NegB_F2.doc", word append ctitle(HH) dec(3)
	
test zone1 = zone2
* Test differences between Zone 1 and Zone 3
test zone1 = zone3
* Test differences between Zone 2 and Zone 3
test zone2 = zone3

	
