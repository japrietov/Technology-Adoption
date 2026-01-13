

import delimited "/.../folder/Technology-Adoption-main/Technology-Adoption-main/Output/df_F_independent_tmp.csv",clear
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
                age education meninhouse womeninhouse kids contributiontofarmwor, vce(cluster cluster)
margins, dydx(*) post
		
nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)


//	Husbands
import delimited ".../folder/Technology-Adoption-main/Technology-Adoption-main/Output/df_M_independent_tmp.csv",clear
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
label variable kids                "Number of Children"
label variable contributiontofarmwork "Contribution to Farm Work"



probit  ynicv  jointmanaged jointcoop jointcredit jointprocessing zone1 zone2 zone3 ///
                age education meninhouse womeninhouse kids contributiontofarmwor, vce(cluster cluster)
margins, dydx(*) post
		
nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)

//Household
import delimited ".../folder/Technology-Adoption-main/Technology-Adoption-main/Output/df_H_independent_tmp.csv",clear	
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
label variable kids                "Number of Children"
label variable contributiontofarmwork "Contribution to Farm Work"



probit  ynicv  jointmanaged jointcoop jointcredit jointprocessing zone1 zone2 zone3 ///
                age education meninhouse womeninhouse kids contributiontofarmwor, vce(cluster cluster)
margins, dydx(*) post
		
nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)
