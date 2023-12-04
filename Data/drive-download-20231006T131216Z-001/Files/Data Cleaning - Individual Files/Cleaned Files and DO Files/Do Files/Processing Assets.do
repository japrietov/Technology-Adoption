*sieve*
use "/Users/Davis/Desktop/Methodology Paper/Stata/Data Cleaning Files/Cleaned Files/Asset Information/Processing assets/Processing Asset Access.dta"

keep if Sex==1
keep if Processing_Id==4
drop F02_male_female
drop Processing_Id
rename F01_Access Sieve_Access
rename Male_Processing_Access Male_Sieve_Access
rename Female_Processing_Access Female_Sieve_Access
rename Joint_Processing_Access Joint_Sieve_Access
label variable Male_Sieve_Access "Male only sieve access"
label variable Female_Sieve_Access "Female only sieve access"
label variable Joint_Sieve_Access "joint sieve access"
label variable Sieve_Access "sieve household access, yes/no"

*fryer*
use "/Users/Davis/Desktop/Methodology Paper/Stata/Data Cleaning Files/Cleaned Files/Asset Information/Processing assets/Processing Asset Access.dta"

keep if Sex==1
keep if Processing_Id==3
drop F02_male_female
drop Processing_Id
rename F01_Access Fryer_Access
rename Male_Processing_Access Male_Fryer_Access
rename Female_Processing_Access Female_Fryer_Access
rename Joint_Processing_Access Joint_Fryer_Access
label variable Male_Fryer_Access "Male only Fryer access"
label variable Female_Fryer_Access "Female only Fryer access"
label variable Joint_Fryer_Access "joint Fryer access"
label variable Fryer_Access "Fryer household access, yes/no"

*presser*
use "/Users/Davis/Desktop/Methodology Paper/Stata/Data Cleaning Files/Cleaned Files/Asset Information/Processing assets/Processing Asset Access.dta"

keep if Sex==1
keep if Processing_Id==2
drop F02_male_female
drop Processing_Id
rename F01_Access Presser_Access
rename Male_Processing_Access Male_Presser_Access
rename Female_Processing_Access Female_Presser_Access
rename Joint_Processing_Access Joint_Presser_Access
label variable Male_Presser_Access "Male only Presser access"
label variable Female_Presser_Access "Female only Presser access"
label variable Joint_Presser_Access "joint Presser access"
label variable Presser_Access "Presser household access, yes/no"

*Grater*
use "/Users/Davis/Desktop/Methodology Paper/Stata/Data Cleaning Files/Cleaned Files/Asset Information/Processing assets/Processing Asset Access.dta"

keep if Sex==0
keep if Processing_Id==1
drop F02_male_female
drop Processing_Id
rename F01_Access Grater_Access
rename Male_Processing_Access Male_Grater_Access
rename Female_Processing_Access Female_Grater_Access
rename Joint_Processing_Access Joint_Grater_Access
label variable Male_Grater_Access "Male only Grater access"
label variable Female_Grater_Access "Female only Grater access"
label variable Joint_Grater_Access "joint Grater access"
label variable Grater_Access "Grater household access, yes/no"


