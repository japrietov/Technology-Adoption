
*==============================================================================*
*                                                                              *
*   REPLICATION CODE                                                           *
*   "According to Whom? Spousal, Household and Plot Differences in             *
*    Improved Cassava Variety Adoption in Nigeria"                             *
*                                                                              *

*                                                                              *
*   Authors:  Jing Yi, Jeisson Prieto, Elisabeth Garner, Hale Ann Tufan       *
*   Contact:  Hale Ann Tufan, Cornell University (hat36@cornell.edu)           *
*   Date:     January 2026                                                     *
*   Stata Version: 18.0                                                         *
*                                                                              *
*   Repository: https://github.com/japrietov/Technology-Adoption              *
*                                                                              *
*==============================================================================*
*                                                                              *
*   DESCRIPTION                                                                *
*   -----------                                                                *
*   To estimate the heterogeneity of location on spousal differences in        *
*   adoption rates of improved cassava varieties (ICVs), we employed Probit    *
*   and Negative Binomial models. The choice of these models reflects the      *
*   nature of the dependent variables: a binary variable for whether the       *
*   respondent ever personally adopted an ICV ("Y/N ICV") at the individual    *
*   level and a continuous variable for the intensity of adoption ("Total ICV") *
*   at the household level (see Table 3). 									   *
*                                                                              *
*     Model 1: Probit model                                                    *
*              The dependent variable is a binary indicator of whether ICV      *
*              was adopted (1 = adopted, 0 = not adopted). These models        *
*              estimate the probability of ICV adoption based on the           *
*              specified dataset. Average marginal effects are also reported 
*   in Table S2.                                                               *
*                                                                              *
*     Model 2: Negative Binomial Regression                                    *
*              The dependent variable is defined as the number of ICVs.        *
*              The data are non-negative integers and exhibit considerable     *
*              overdispersion, with the variance substantially exceeding       *
*              the mean.                                                       *
*                                                                              *
*   Both models are estimated separately for three subsamples:                 *
*     (a) Wives     — female respondents (df_F_independent_tmp.csv)            *
*     (b) Husbands  — male respondents   (df_M_independent_tmp.csv)            *
*     (c) Household — household heads     (df_H_independent_tmp.csv)           *
*                                                                              *
*   We cluster the standard errors at the zone level to allow for arbitrary    *
*   correlation within zones and provide robust inference in the presence      *
*   of intra-zone dependence.                                                  *
*                                                                              *
*==============================================================================*
*                                                                              *
*   VARIABLE DEFINITIONS                                                       *
*   --------------------                                                       *
*   Dependent Variables:                                                       *
*     ynicv            — "Y/N ICV": binary indicator of whether respondent     *
*                         ever personally planted an ICV (1=adopted, 0=not)    *
*     totalicv         — "Total ICV": number of household plots on which       *
*                         respondent reports ICV was planted                    *
*                                                                              *
*   Key Independent Variables (Joint Decision-Making Indicators):              *
*     jointmanaged          — Joint plot management (1 = jointly managed)      *
*     jointcoop             — Joint cooperative membership                     *
*     jointcredit           — Joint access to credit                           *
*     jointprocessingaccess — Joint access to processing facilities            *
*                                                                              *
*   Control Variables:                                                         *
*     zone1, zone2, zone3   — Agro-ecological zone dummies                    *
*     age                   — Age of respondent (years)                        *
*     education             — Education level of respondent                    *
*     meninhouse            — Number of men in household                       *
*     womeninhouse          — Number of women in household                     *
*     kids                  — Number of children in household                  *
*     contributiontofarmwork — Contribution to farm work                       *
*                                                                              *
*   Clustering Variable:                                                       *
*     cluster               — Community-level cluster identifier               *
*                                                                              *
*==============================================================================*
*                                                                              *
*   DATA REQUIREMENTS                                                          *
*   -----------------                                                          *
*   Input files (CSV) should be placed in the ../Output/ directory:            *
*     - df_F_independent_tmp.csv  (Wives subsample)                            *
*     - df_M_independent_tmp.csv  (Husbands subsample)                         *
*     - df_H_independent_tmp.csv  (Household subsample)                        *
*                                                                              *
*   These CSV files are generated by the Python preprocessing scripts          *
*   in this repository (see Final graphs (Python).ipynb).                      *
*                                                                              *
*   Primary data source:                                                       *
*     The Cassava Monitoring Survey (CMS) in Nigeria — household and           *
*     plot-level data. Available at:                                            *
*     https://data.iita.org/dataset/the-cassava-monitoring-survey-cms-         *
*     in-nigeria-household-and-plot-level-data                                 *
*                                                                              *
*     Raw CMS data:  ../Data/CMS-raw/                                          *
*     Spouse-level:  ../Data/CMS-hh/ (available upon request)                  *
*                                                                              *
*==============================================================================*
*                                                                              *
*   TABLE MAPPING                                                              *
*   -------------                                                              *
*   This do-file produces results reported in:                                 *
*                                                                              *
*     Table S2: "Wives, Husbands, and Household regression with Y/N ICV        *
*               and Total ICV as the dependent variable."                      *
*               - Columns (1)-(3): Probit model (Y/N ICV)                      *
*                 (1) Wives, (2) Husbands, (3) Household Heads                 *
*               - Columns (4)-(6): Negative Binomial (Total ICV)               *
*                 (4) Wives, (5) Husbands, (6) Household Heads                 *
*               Output file: ../Output/Tables/tab_regressions                  *
*                                                                              *
*   Related manuscript tables:                                                 *
*     Table 1: Sampling and sex-disaggregation of previous studies             *
*     Table 2: Summary of datasets (Plot, Household Head, Intrahousehold)      *
*     Table 3: Variables used to determine adoption of ICV                     *
*     Table S1: Summary statistics for the Intrahousehold dataset              *
*                                                                              *
    
*==============================================================================*
*                                                                              *
*   MODEL SPECIFICATION                                                        *
*   -------------------                                                        *
*   Probit Model:                                                              *
*     For the binary variable y_ij, representing whether ICVs were adopted     *
*     by individual i in household j:                                          *
*       Pr(y_ij = 1 | x_ij) = F(x_ij * beta)                                 *
*     where F(.) is the cumulative distribution function.                      *
*     x_ij is a vector of individual- and household-level characteristics,     *
*     including plot management type, cooperative membership, access to         *
*     credit, access to processing facilities, zone, age, education,           *
*     number of men/women/children in the household, and contribution to       *
*     farm work.                                                               *
*                                                                              *
*   Negative Binomial Model:                                                   *
*     For the dependent variable T_ij, representing the total number of        *
*     plots cultivated with ICVs in household j, the data are non-negative     *
*     integers and exhibit considerable overdispersion, with the variance      *
*     substantially exceeding the mean. The NB model relaxes the       *
*     restriction by allowing Var(T) = E(T) + alpha * E(T)^2.                *
*                                                                              *
*   We cluster the standard errors at the zone level: vce(cluster cluster)     *
*                                                                              *
*==============================================================================*
*                                                                              *
*   SOFTWARE & PACKAGES                                                        *
*   -------------------                                                        *
*   Stata 18.0                                                                 *
*   No additional user-written packages required.                              *
*   Built-in commands used: probit, margins, nbreg                             *
*                                                                              *
*==============================================================================*


clear all
set more off

* ---- Set paths ----
* NOTE: Update the path below to match your local directory structure.
* The root should point to the Technology-Adoption-main folder.

local root "."
local datadir "`root'/../Output"


*==============================================================================*
*   (a) WIVES — Female Respondents                                             *
*==============================================================================*

import delimited "`datadir'/df_F_independent_tmp.csv", clear

* Label variables
label variable jointmanaged          "Joint Managed"
label variable jointcoop             "Joint Coop"
label variable jointcredit           "Joint Credit"
label variable jointprocessingaccess "Joint Processing Access"
label variable zone1                 "Zone 1"
label variable zone2                 "Zone 2"
label variable zone3                 "Zone 3"
label variable age                   "Age"
label variable education             "Education"
label variable meninhouse            "Men in House"
label variable womeninhouse          "Women in House"
label variable kids                  "Kids"
label variable contributiontofarmwork "Contribution to Farm Work"

* --- Model 1: Probit (Extensive Margin) ---
* → Table S2, Column (1): Wives — Probit (Y/N ICV)
* Estimates probability of adopting any improved cassava variety.
* Average marginal effects (AME) are reported via -margins-.

probit ynicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 ///
    age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)
margins, dydx(*) post

* --- Model 2: Negative Binomial Regression (Intensive Margin) ---
* → Table S2, Column (4): Wives — Negative Binomial (Total ICV)
* Estimates the count of improved cassava varieties adopted.

nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 ///
    age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)


*==============================================================================*
*   (b) HUSBANDS — Male Respondents                                            *
*==============================================================================*

import delimited "`datadir'/df_M_independent_tmp.csv", clear

* Label variables
label variable jointmanaged          "Joint Managed"
label variable jointcoop             "Joint Coop"
label variable jointcredit           "Joint Credit"
label variable jointprocessingaccess "Joint Processing Access"
label variable zone1                 "Zone 1"
label variable zone2                 "Zone 2"
label variable zone3                 "Zone 3"
label variable age                   "Age"
label variable education             "Education"
label variable meninhouse            "Men in House"
label variable womeninhouse          "Women in House"
label variable kids                  "Number of Children"
label variable contributiontofarmwork "Contribution to Farm Work"

* --- Model 1: Probit (Extensive Margin) ---
* → Table S2, Column (2): Husbands — Probit (Y/N ICV)

probit ynicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 ///
    age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)
margins, dydx(*) post

* --- Model 2: Negative Binomial Regression (Intensive Margin) ---
* → Table S2, Column (5): Husbands — Negative Binomial (Total ICV)

nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 ///
    age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)


*==============================================================================*
*   (c) HOUSEHOLD — Household-Level Estimation                                 *
*==============================================================================*

import delimited "`datadir'/df_H_independent_tmp.csv", clear

* Label variables
label variable jointmanaged          "Joint Managed"
label variable jointcoop             "Joint Coop"
label variable jointcredit           "Joint Credit"
label variable jointprocessingaccess "Joint Processing Access"
label variable zone1                 "Zone 1"
label variable zone2                 "Zone 2"
label variable zone3                 "Zone 3"
label variable age                   "Age"
label variable education             "Education"
label variable meninhouse            "Men in House"
label variable womeninhouse          "Women in House"
label variable kids                  "Number of Children"
label variable contributiontofarmwork "Contribution to Farm Work"

* --- Model 1: Probit (Extensive Margin) ---
* → Table S2, Column (3): Household Heads — Probit (Y/N ICV)

probit ynicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 ///
    age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)
margins, dydx(*) post

* --- Model 2: Negative Binomial Regression (Intensive Margin) ---
* → Table S2, Column (6): Household Heads — Negative Binomial (Total ICV)

nbreg totalicv jointmanaged jointcoop jointcredit jointprocessing ///
    zone1 zone2 zone3 ///
    age education meninhouse womeninhouse kids contributiontofarmwor, ///
    vce(cluster cluster)


*==============================================================================*
*   END OF FILE                                                                *
*==============================================================================*
