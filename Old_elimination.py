__author__ = 'Bat Cave'
import numpy as np
import sys


def eliminate(demand, routine, mealappliance, devicetype):
    intervalcount = len(demand)                             # count how many intervals to be evaluated over
    demandoptimise = [0 for i in range(intervalcount)]      # write zeros for every potential hour
    skipinterval = []
    for z in np.arange(0, intervalcount):                   # loop through all the intervals
        cyclecount = 0                                      # reset the count of how many hours the use went for
        if demand[z] > 0:                                   # if demand is on check how many intervals it runs for
            for k in np.arange(z, intervalcount):           # from next hour until the end (inclusive of last hour)
                if demand[k] > 0:                           # if next hour is greater then zero eg still in use
                    cyclecount += 1                         # add one more to count of cycle length
                else:                                       # if next hour is zero eg device usage stopped
                    break                                   # break counting loop
        if z not in skipinterval and cyclecount > 0:        # skip intervals that have already been optimised
            if routine[z] == 0 or (mealappliance == 1 and routine[z] == 1):    # if no body is home OR
                if devicetype == "Cycle":                   # if device is used in meal prep and it is meal time
                    for e in np.arange(0, cyclecount):      # for all intervals that cycle runs over
                        demandoptimise[z + e] = demand[z + e]   # do not optimse demand
                        skipinterval.append(z + e)          # add optimised intervals to list of intervals to be skipped
                elif devicetype == "Duration":
                    demandoptimise[z] = demand[z]
                else:
                    sys.exit("Elimination Error 1: Please check spelling of Cycle or Duration")
            else:                                           # if demand present, someone is home & able to be optimised
                if devicetype == "Cycle":
                    for e in np.arange(0, cyclecount):      # for all intervals that cycle runs over
                        demandoptimise[z + e] = 0           # record optimised demand as zero eg eliminate usage
                        skipinterval.append(z + e)          # add optimised intervals to list of intervals to be skipped
                elif devicetype == "Duration":
                    demandoptimise[z] = 0
                else:
                    sys.exit("Elimination Error 2: Please check spelling of Cycle or Duration")

    return demandoptimise


def test0():                # NOT meal appliance optimisation
    meal_appliance = 0
    routine_ = [0, 2, 0, 1, 2, 0, 0]
    demand_ = [0, 5, 10, 0, 3, 0, 4]
    expected_ = [0, 0, 0, 0, 0, 0, 4]
    device_type = "Cycle"
    demand_optimised = eliminate(demand_, routine_, meal_appliance, device_type)
    print "Routine   " + str(routine_)
    print "Original  " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 0: NOT meal appliance optimisation \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 0: NOT meal appliance optimisation \n"


def test1():                # Meal appliance optimisation
    meal_appliance = 1
    routine_ = [0, 2, 0, 1, 1, 0, 0]
    demand_ = [0, 5, 10, 0, 3, 0, 4]
    expected_ = [0, 0, 0, 0, 3, 0, 4]
    device_type = "Cycle"
    demand_optimised = eliminate(demand_, routine_, meal_appliance, device_type)
    print "Routine   " + str(routine_)
    print "Original  " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 1: Meal appliance optimisation \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 1: Meal appliance optimisation \n"

if __name__ == '__main__':

    tests = "All"                   # select tests to be ran

    testing = []
    if tests == "Mix":
        testing.append(1)  # test 0 (0 off/1 on) Not meal appliance optimisation
        testing.append(0)  # test 0 (0 off/1 on) Meal appliance optimisation
    elif tests == "None":
        testing = [0 for w in range(0, 12)]
    elif tests == "All":
        testing = [1 for w in range(0, 12)]
    if testing[0] == 1:  # Flat rate billing rate test
        test0()
    if testing[1] == 1:  # Flat rate billing rate test
        test1()