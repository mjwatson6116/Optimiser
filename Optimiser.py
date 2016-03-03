__author__ = 'Bat Cave'
print "Importing libraries..."

import numpy as np
import pandas as pd
import sys
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be
import HouseholdType as ht
import AirConditioner as ac
import ClothesDryer as cd
import ClothesWasher as cw
import Dishwasher as dw
import Fridge as fg
import Kettle as kt
import Microwave as mw
import SecondFridge as sf
import SoundSystem as ss
import Television as tv
import Toaster as to
import IHWH as ihwh
import matplotlib.pyplot as plt

print "Initialising data..."
# settings
optigoal = "Bill"                           # what is the goal of the optimsiation (Bill or Enviro)
controlledload = "No"                       # if there is a controlled load set to Yes
household_makeup = "Custom"                 # options Custom, Lone, Couple, Group, Fam1p, Fam2p or All
billinput = "All"                           # selects the type of bills to be evaluated (All, Flat, Cap, ToU, Ave)
mininterval = 15                            # interval duation in minutes
household_eval = "specific"                 # select type of household to be evaluated (All, PP, EW, TE, specific, loop)
metertype = "LED"                           # input what type of meter the household has (DISC, LED, SMART)
data_source = "pecan"                       # where is the data coming from (own, pecan)
graph = "Off"                                # graph the results (Yes or No)
test = 0                                    # print different information (0 = off, 1 = row by row, 2 = optimisations)
current_bill_type = "All"                   # input type of bill the household is currently on Flat, Cap or ToU

# data source
if data_source == "own":
    csv_directory = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house2"     # where the data is stored
elif data_source == "pecan":
    dataid = 4922
    csvpath = "C:\Users\Bat Cave\Dropbox\My Files\Uni Work\Capstone\PeaconStreet\dataid_" + str(dataid) + "_localdate_07012013_AND_09302013.csv"
else:
    sys.exit("Data Source Error 1: Please select a valid data source as either 'own' or 'peacon'")

if household_eval == "PP" or household_eval == "EW" or household_eval == "TE" or household_eval == "All":
    household_type = ["PP", "EW", "TE"]                                      # list of household type options
    householdselect = ht.householdtype(household_eval, household_type)  # return range of values
    min_loop = householdselect[0]
    max_loop = householdselect[1]
elif household_eval == "specific":
    min_loop = 10
    max_loop = min_loop + 1
elif household_eval == "loop":
    min_loop = 0
    max_loop = 11
else:
    sys.exit("Household Evaluation Error1: Please enter All, loop, specific, PP, EW, TE, All")

# list of appliances that have use cases in the system (Yes = to be optimise, No = not optimised)
airconditioner = "Yes"
clothesdryer = "Yes"
clotheswasher = "Yes"
dishwasher = "Yes"
fridgefreezer = "No"
secondfridgefreezer = "No"
standalonefridge = "No"
standalonefreezer = "No"
kettle = "No"
microwave = "No"
soundsystem = "No"
television = "No"
toaster = "No"
waterheater = "No"

# initialise settings
shifting = 0                                                 # shifting will automatically be turned on if applicable
total_loop_counter = 0
routinelist = []
total_interval_cost = []
total_cost = []
interval_opti_demand = []
total_opti_demand = []
combination_list = []
interval_opti_vari = []
threshold_variation = []
bill_type_variation = []
bill_number_variation = []
if metertype == "DISC":
    meter = 0
elif metertype == "LED" or metertype == "SMART":
    meter = 1
else:
    sys.exit("Meter Type Error: Please enter valid meter type (DISC, LED, SMART)")

print "Importing house level data...."
# import house level data and aggregate
if data_source == "own":
    current_cost = [49.70, 19.22, 11.00]        # how much is the household paying cents/kWh  [Peak, Shoulder, Off-peak]
    current_cap = [0, 0]                        # what are the intervals that the price increases at [cap1, cap2] (Watts)
    current_connect = 89.57                     # how much are the current per day connection fees (cents/day)
    current_control = 0                         # how much is the household paying cents/kWh on the controlled load
    csv = "consumption.csv"
    csvpath = str(csv_directory) + "\\" + str(csv)
    Housedata = ida.aggregatedatacsv(csvpath, mininterval)
    intervalcount = len(Housedata[0])
    house_demand = Housedata[1]

    controlled_demand = []                                            # included if controlled circuit/demand evaluated
    controlled_load = 1                                               # for billing purposes
    if controlledload == "No":                                        # if no controlled load create empty matrix
        controlled_load = 0                                           # switch off for billing purposes
        controlled_demand = [0 for zero in range(0, len(house_demand))]   # zero value matrix for controlled demand
    optimised_controlled_demand = controlled_demand                   # controlled demand is excluded from optimisation

    print "Calculating original bill...."
    if optigoal == "Bill":
        original_bill = be.original_bill_cal(house_demand, controlled_demand, controlledload, mininterval, current_bill_type,
                                             current_cost, current_cap, current_connect, current_control)

    print "Importing device data...."
    device_demand = ida.deviceimport(house_demand, mininterval, csv_directory, airconditioner, clothesdryer, clotheswasher,
                                     dishwasher, fridgefreezer, secondfridgefreezer, standalonefridge, standalonefreezer,
                                     kettle, microwave, soundsystem, television, toaster, waterheater)
    ac_demand = device_demand[0][0]
    cd_demand = device_demand[0][1]
    cw_demand = device_demand[0][2]
    dw_demand = device_demand[0][3]
    fgf_demand = device_demand[0][4]
    fgf2_demand = device_demand[0][5]
    sfg_demand = device_demand[0][6]
    sfz_demand = device_demand[0][7]
    kt_demand = device_demand[0][8]
    mw_demand = device_demand[0][9]
    ss_demand = device_demand[0][10]
    tv_demand = device_demand[0][11]
    to_demand = device_demand[0][12]
    ihwh_demand = device_demand[0][13]
elif data_source == "pecan":
    weather_forecast = cd.weather(mininterval)                          # import weather for the period being evaluated
    demand_data = ida.peacon_street(csvpath, mininterval)
    house_demand = demand_data[1][0]
    ac_demand = demand_data[1][1]
    cd_demand = demand_data[1][11]
    cw_demand = demand_data[1][7]
    dw_demand = demand_data[1][9]
    fgf_demand = demand_data[1][29]
    fgf2_demand = demand_data[1][30]
    sfg_demand = demand_data[1][30]
    sfz_demand = demand_data[1][13]
    kettle = "No"
    mw_demand = demand_data[1][30]
    soundsystem = "No"
    television = "No"
    toaster = "No"
    ihwh_demand = demand_data[1][34]
    bill_type = 2
    cost_number = 54
    controlled_load = 0
    controlled_demand = [0 for zero in range(0, len(house_demand))]   # zero value matrix for controlled demand
    optimised_controlled_demand = controlled_demand
    billing_info = be.bill_eval(house_demand, bill_type, cost_number, mininterval, controlled_load, meter, 0)
    original_bill = be.billing_calc(house_demand, controlled_demand, bill_type, billing_info[0], billing_info[1], billing_info[2], billing_info[3])
    if graph == "Yes":
        if optigoal == 'Bill':
            house_bill_cumsum = np.cumsum(original_bill)
            # plt.plot(house_bill_cumsum, label='Average Market ToU Rates Offer')
        else:
            house_demand_cumsum = np.cumsum(house_demand)
            plt.plot(house_demand_cumsum, label='Unoptimised Household Consumption')
else:
    sys.exit("Data Source Error 1: Please select a valid data source as either 'own' or 'pecan'")

# End of demand aggregator
# Start of routine builder
if household_makeup == "Custom" or household_makeup == "custom":      # if exact situation needs to be specified
    occupant = [0 for i in range(0, 6)]
    occupant[0] = 2                                             # number of occupants with full time jobs
    occupant[1] = 0                                             # number of occupants with part time jobs
    occupant[2] = 0                                             # number of occupants with casual time jobs
    occupant[3] = 0                                             # number of occupants that are unemployed
    occupant[4] = 0                                             # number of occupants that are retired
    occupant[5] = 0                                             # number of children at school
    for z in np.arange(0, len(occupant)):                       # loop through occupant list
        if occupant[z] > 1:                                     # if more then one occupant has the same job type
            occupant[z] = 1                                     # just enter 1, system treats it the same
    routinelist.append(rb.routine_builder(house_demand, mininterval, occupant))
                                                                # at to list of routines to be evaluated
else:
    routinelist = rb.routineselect(house_demand, mininterval, household_makeup)
                                                                # returns list of all routines that match criteria
routineloop = 0                                                 # counts how many routines that are evaluated
for routine in routinelist:                                     # looping through all applicable routines
    routineloop += 1                                            # add one to routine counter
    # End of routine builder
    # Start household type
    householdcount = 0                                           # counts how many household loops are completed
    for xyz in np.arange(min_loop, max_loop):                    # for each value between range
        if household_eval == "loop" or household_eval == "specific":
            threshold = xyz
        else:
            threshold = ht.householdthreshold(xyz, household_type, optigoal)    # return the threshold value
        householdcount += 1                                                  # count how many loops
        # Cost generation engine
        billoopcount = 0                                                     # counts how many routines are evaluated
        billselect = be.bill_selection(billinput)                            # only include selected bill types
        for bill_type in np.arange(billselect[0], billselect[1]):            # iterate through selected bill types
            cost_vari = be.costvariations(bill_type, controlled_load, 0)     # find how many costs for bill type
            for cost_number in np.arange(cost_vari[0], cost_vari[1]):        # iterate through costs for bill type
                billing_info = be.bill_eval(house_demand, bill_type, cost_number, mininterval, controlled_load, meter, 0)
                                                                             # return cost info
                connectionfee = billing_info[0]                              # seperate connection fee
                cost = billing_info[1]                                       # seperate cost per hour values
                cap = billing_info[2]                                        # seperate cap values
                control = billing_info[3]
                if optigoal == "Bill" and bill_type == 3:                    # if optimising using bill & ToU bill
                    shifting = 1                                             # enable appliance shifting
                # End of cost generation

                # End of household type
                # Insert appliance logic
                print str(total_loop_counter) + ": routine loop = " + str(routineloop) + " threshold = " + \
                    str(threshold) + " billtype = " + str(bill_type) + " cost number = " + str(cost_number)
                combination_list.append(str(total_loop_counter) + ": routine loop = " + str(routineloop) +
                                        " threshold = " + str(threshold) + " billtype = " + str(bill_type)
                                        + " cost number = " + str(cost_number))
                total_loop_counter += 1
                threshold_variation.append(threshold)
                bill_type_list = ["Flat", "IBT", "ToU", "ToU"]
                bill_type_variation.append(bill_type_list[bill_type])
                bill_number_variation.append(cost_number)

                variation = [0 for i in np.arange(len(house_demand))]
                if airconditioner == "Yes":
                    if test > 0:
                        print "\nAir-con"
                    ac_variation = ac.airconditioner(ac_demand, routine, mininterval, cost, threshold, shifting, test)
                    if test > 0:
                        print "Total Saving : " + str(np.sum(ac_variation))
                    variation = [a + b for a, b in zip(variation, ac_variation)]

                if clothesdryer == "Yes":
                    if test > 0:
                        print "\nDryer"
                    cd_variation = cd.clothesdryer(cd_demand, routine, mininterval, cost, threshold, shifting, weather_forecast, test)
                    if test > 0:
                        print "Total Saving : " + str(np.sum(cd_variation))
                    variation = [a + b for a, b in zip(variation, cd_variation)]

                if clotheswasher == "Yes":
                    if test > 0:
                        print "\nWashing machine"
                    cw_variation = cw.clotheswasher(cw_demand, routine, mininterval, cost, threshold, shifting, test)
                    if test > 0:
                        print "Total Saving : " + str(np.sum(cw_variation))
                    variation = [a + b for a, b in zip(variation, cw_variation)]

                if dishwasher == "Yes":
                    if test > 0:
                        print "\nDish"
                    dw_variation = dw.dishwasher(dw_demand, routine, mininterval, cost, threshold, shifting, test)
                    if test > 0:
                        print "Total Saving : " + str(np.sum(dw_variation))
                    variation = [a + b for a, b in zip(variation, dw_variation)]

                if fridgefreezer == "Yes":
                    if test > 0:
                        print "\nFridge"
                    fg_variation = fg.fridge(fgf_demand, 0)
                    variation = [a + b for a, b in zip(variation, fg_variation)]

                if secondfridgefreezer == "Yes":
                    if test > 0:
                        print "\n2ndFridge"
                    secondfg_variation = sf.secondfridge(fgf2_demand, routine, cost, threshold, test)
                    variation = [a + b for a, b in zip(variation, secondfg_variation)]

                if standalonefridge == "Yes":
                    if test > 0:
                        print "\nStandalone Fridge"
                    if fridgefreezer == "Yes":
                        sfridge_variation = sf.secondfridge(sfg_demand, routine, cost, threshold, test)
                    else:
                        sfridge_variation = fg.fridge(sfg_demand, test)
                    variation = [a + b for a, b in zip(variation, sfridge_variation)]

                if standalonefreezer == "Yes":
                    if test > 0:
                        print "\nStandalone Freezer"
                    if fridgefreezer == "Yes":
                        sfreezer_variation = sf.secondfridge(sfz_demand, routine, cost, threshold, test)
                    else:
                        sfreezer_variation = fg.fridge(sfz_demand, test)
                    variation = [a + b for a, b in zip(variation, sfreezer_variation)]

                if kettle == "Yes":
                    if test > 0:
                        print "\nKettle"
                    kt_variation = kt.kettle(kt_demand, routine, mininterval, cost, threshold, test)
                    variation = [a + b for a, b in zip(variation, kt_variation)]

                if microwave == "Yes":
                    if test > 0:
                        print "\nMicrowave"
                    mw_variation = mw.microwave(mw_demand, routine, mininterval, cost, threshold, test)
                    variation = [a + b for a, b in zip(variation, mw_variation)]

                if soundsystem == "Yes":
                    if test > 0:
                        print "\nSound"
                    ss_variation = ss.soundsystem(ss_demand, routine, mininterval, cost, threshold, shifting, test)
                    variation = [a + b for a, b in zip(variation, ss_variation)]

                if television == "Yes":
                    if test > 0:
                        print "\nTV"
                    tv_variation = tv.television(tv_demand, routine, mininterval, cost, threshold, shifting, test)
                    variation = [a + b for a, b in zip(variation, tv_variation)]

                if toaster == "Yes":
                    if test > 0:
                        print "\nToast"
                    to_variation = to.toaster(to_demand, routine, mininterval, cost, threshold, 0)
                    variation = [a + b for a, b in zip(variation, to_variation)]

                if waterheater == "Yes":
                    if test > 0:
                        print "\nHot Water"
                    ihwh_variation = ihwh.ihotwaterh(ihwh_demand, routine, mininterval, cost, threshold, shifting, test)
                    variation = [a + b for a, b in zip(variation, ihwh_variation)]
                # finished device optimisation
                # Minus from original house hourly consumption
                optimised_demand = [a + b for a, b in zip(house_demand, variation)]
                interval_opti_vari.append(variation)
                interval_opti_demand.append(optimised_demand)
                total_opti_demand.append([np.sum(optimised_demand), optimised_demand])
                if optigoal == "Bill":
                    demand_cost = be.billing_calc(optimised_demand, optimised_controlled_demand, bill_type,
                                                  connectionfee, cost, cap, control)        # find cost per interval
                    total_interval_cost.append(demand_cost)
                    total_cost.append(np.sum(demand_cost))   # add total cost of scenerio to total cost list
print("")

# if optigoal == "Enviro":
min_demand = min(total_opti_demand)
opti_result = [i for i, a in enumerate(total_opti_demand) if a == min_demand]
total_demand_before = np.around(np.sum(house_demand), 2)
total_demand_after = np.around(np.sum(interval_opti_demand[opti_result[0]]), 2)
demand_difference = np.around(total_demand_before - total_demand_after, 2)
demand_save = np.around(np.divide(demand_difference, total_demand_before)*100, 2)
print "Demand before optimisation : " + str(total_demand_before) + " kWh"
print " Demand after optimisation : " + str(total_demand_after) + " kWh"
print "         Demand difference : " + str(demand_difference) + " kWh"
print "          Percentage Saved : " + str(demand_save) + " %"
# elif optigoal == "Bill":
min_cost = np.min(total_cost)
max_cost = np.max(total_cost)
ave_cost = np.average(total_cost)
cost_range = max_cost - min_cost
opti_result = [i for i, a in enumerate(total_cost) if a == min_cost]
total_bill_before = np.sum(original_bill)
total_bill_after = total_cost[opti_result[0]]
bill_difference = total_bill_before - total_bill_after
bill_saving = (bill_difference/total_bill_before) * 100
print "  Bill before optimisation : $" + str(np.around(total_bill_before, decimals=2))
print "   Bill after optimisation : $" + str(np.around(total_bill_after, decimals=2))
print "           Bill difference : $" + str(np.around(bill_difference, decimals=2))
print "          Percentage Saved : " + str(np.around(bill_saving, decimals=2)) + " %"
print "                  Min Bill : $" + str(np.around(min_cost, decimals=2))
print "    Min cost contract info : " + str(bill_type_variation[opti_result[0]]) + " " + str(bill_number_variation[opti_result[0]])
print "                  Max Bill : $" + str(np.around(max_cost, decimals=2))
print "                Cost Range : $" + str(np.around(cost_range, decimals=2))
print "                   Average : $" + str(np.around(ave_cost, decimals=2))
# else:
#     sys.exit("Optimisation Goal Error1: Please enter valid optimisation goal (Bill or Enviro)")

if graph == "Yes":
    if optigoal == "Enviro":
        for x in np.arange(0, len(interval_opti_demand)):
            if x < 10:
                opti_demand_cumsum = np.cumsum(interval_opti_demand[x])
                plt.plot(opti_demand_cumsum, label='Household Motivation Level %i' % threshold_variation[x])
                plt.ylabel('Kilowatt hours of Electricity (kWh)')
                plt.title('Impact of Behavioural Change on House Level Consumption (Data ID:' + str(dataid) + ")")
    elif optigoal == "Bill":
        for x in np.arange(0, len(total_interval_cost)):
            if x < 1000:
                opti_cost_cumsum = np.cumsum(total_interval_cost[x])
                plt.plot(opti_cost_cumsum, label='%s Rate Bill: Variation %s' % (bill_type_variation[x], bill_number_variation[x]))
                plt.ylabel('Cost of Quarterly Electricity Bill ($)')
                plt.title('Impact of Electricity Contract Selection (Data ID:' + str(dataid) + ")")
    plt.legend(loc="best", fontsize='small')
    w = len(house_demand)
    plt.xlabel('Time Intervals (From 01/07/2013 [0] - 01/09/2013 [' + str(w) + '])')
    plt.show()

    interval_opti_vari = []
    interval_opti_demand = []
    total_opti_demand = []
    total_interval_cost = []
    total_cost = []
