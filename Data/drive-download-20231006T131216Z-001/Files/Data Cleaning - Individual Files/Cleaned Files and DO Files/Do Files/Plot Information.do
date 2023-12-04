replace D06_1_B_loc_imp=0 if D06_1_B_loc_imp==.
replace D06_1_C_loc_imp=0 if D06_1_C_loc_imp==.
replace D06_1_D_loc_imp=0 if D06_1_D_loc_imp==.
replace D06_1_E_loc_imp=0 if D06_1_E_loc_imp==.
replace D06_1_loc_imp=0 if D06_1_loc_imp==.

gen ICV=0

replace ICV=1 if (D06_1_loc_imp+ D06_1_B_loc_imp+ D06_1_C_loc_imp+ D06_1_D_loc_imp+ D06_1_E_loc_imp)>0

gen NonICV=0
replace NonICV=1 if ICV==0

gen Male_Managed=0
replace Male_Managed=1 if D08_Plot_manager==1
gen Women_Managed=0
replace Women_Managed=1 if D08_Plot_manager==0
gen Joint_Manage=0
replace Joint_Manage=1 if D08_Plot_manager==2

gen Male_ICV_Managed=(ICV*Male_Managed)
gen Female_ICV_Managed=(ICV*Women_Managed)
rename Women_Managed Female_Managed
gen Joint_ICV_Managed=(ICV*Joint_Manage)
rename Joint_Manage Joint_Managed

gen Male_NonICV_Managed=(NonICV*Male_Managed)
gen Female_NonICV_Managed=(NonICV*Female_Managed)
gen Joint_NonICV_Managed=(NonICV*Joint_Managed)


gen Household_ICV=(Male_ICV_Managed+ Female_ICV_Managed+ Joint_ICV_Managed)
gen Household_NonICV=(Male_NonICV_Managed+ Female_NonICV_Managed+ Joint_NonICV_Managed)
gen Household_Plots=1

gen ICV_Plot_Size=(ICV*J13_Plotsize_metersqure_GPS)
gen NonICV_Plot_Size=(NonICV*J13_Plotsize_metersqure_GPS)
gen Male_ICV_PlotSize=(Male_ICV_Managed*J13_Plotsize_metersqure_GPS)
gen Female_ICV_PlotSize=(Female_ICV_Managed*J13_Plotsize_metersqure_GPS)
gen Joint_ICV_PlotSize=(Joint_ICV_Managed*J13_Plotsize_metersqure_GPS)

gen Male_NonICV_PlotSize=(J13_Plotsize_metersqure_GPS*Male_NonICV_Managed)
gen Female_NonICV_PlotSize=(J13_Plotsize_metersqure_GPS*Female_NonICV_Managed)
gen Joint_NonICV_PlotSize=(J13_Plotsize_metersqure_GPS*Joint_NonICV_Managed)

gen Household_ICV_Total_Size=(Household_ICV*J13_Plotsize_metersqure_GPS)
gen Household_NonICV_Total_Size=(J13_Plotsize_metersqure_GPS*Household_NonICV)
gen House_Cassava_Plot_TotalSize=(Household_Plots*J13_Plotsize_metersqure_GPS)
gen Avg_Plot_Size= J13_Plotsize_metersqure_GPS

collapse (sum)Male_Managed Female_Managed Joint_Managed Male_ICV_Managed Female_ICV_Managed Joint_ICV_Managed Male_NonICV_Managed Female_NonICV_Managed Joint_NonICV_Managed Household_ICV Household_NonICV Household_Plots ICV_Plot_Size NonICV_Plot_Size Male_ICV_PlotSize Female_ICV_PlotSize Joint_ICV_PlotSize Male_NonICV_PlotSize Female_NonICV_PlotSize Joint_NonICV_PlotSize Household_ICV_Total_Size Household_NonICV_Total_Size House_Cassava_Plot_TotalSize (mean) Avg_Plot_Size, by(HouseID)

label variable Female_NonICV_PlotSize "total land, square meters, of female managed nonICV plots"
label variable Joint_NonICV_PlotSize "total land, square meters, of joint managed nonICV plots"
label variable Household_ICV_Total_Size "total land, square meters, of all ICV plots"
label variable Household_NonICV_Total_Size "total land, square meters, of all nonICV plots"
label variable House_Cassava_Plot_TotalSize "total land, square meters, of all cassava plots
label variable Avg_Plot_Size "avg size of cassava plot"
label variable Male_NonICV_PlotSize "total land, square meters, of male managed nonICV plots"
label variable Male_Managed "number of male managed plots"
label variable Female_Managed "number of female managed plots"
label variable Joint_Managed "number of joint managed plots"
label variable Male_ICV_Managed "number of ICV plots male managed"
label variable Female_ICV_Managed "number of ICV plots female managed"
label variable Joint_ICV_Managed "number of ICV plots joint managed"
label variable Male_NonICV_Managed "number of nonICV plots male managed"
label variable Female_NonICV_Managed "number of nonICV plots female managed"
label variable Joint_NonICV_Managed "number of nonICV plots joint managed"
label variable Household_NonICV "number of nonICV plots of house"
label variable Household_ICV "number of ICV plots of house
label variable Household_Plots "number of cassava plots"
label variable ICV_Plot_Size "total land, square meters, of ICV plots"
label variable NonICV_Plot_Size "total land, square meters, of nonICV plots"
label variable Male_ICV_PlotSize "total land, square meters, of male managed ICV plots"
label variable Female_ICV_PlotSize "total land, square meters, of female managed ICV plots"
label variable Joint_ICV_PlotSize "total land, square meters, of joint managed ICV plots"

