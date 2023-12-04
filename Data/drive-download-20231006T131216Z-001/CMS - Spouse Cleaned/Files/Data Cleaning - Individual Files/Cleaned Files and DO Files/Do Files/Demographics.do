 use "/Users/Davis/Desktop/Methodology Cleaning 2/Spouse/Household_composition_Spouse_All Regions.dta"

 
 *this is to identify the person who is assumed to have taken the survey for the spouses.*
 keep if Individual_family_code<3
 keep if A02_Sex==0
 
 *save file* 
 
 collapse (count) A03_Age, by(HouseID)
 tab A03_Age
 bro if A03_Age==2
 *for observations where A03_Age==2 after collapsing the data we know there are two observations at that houshold of potential women who filled out the survey
 
 bro if A03_Age==2
 *write down HouseID of observations where A03_Age==2
 
 *reload original file*
  keep if Individual_family_code<3
 keep if A02_Sex==0
 
 *delete observations where  Individual_family_code==2 for households with multiple observations, this equals deleting 18 observations*
 
 *this will result in 795 total observations, one for each household surveyed*
 
 
