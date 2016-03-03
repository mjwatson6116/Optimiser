__author__ = 'Bat Cave'

import numpy as np


def minimise(demand, routine, mealappliance, devicetype, mininterval, saving, cyclemax, mintime, test):
    intervalcount = len(demand)                             # count how many intervals to be evaluated over
    demandoptimise = [0 for i in range(intervalcount)]      # write zeros for every potential interval
    skipinterval = []                                       # defines skipinterval as a list
    finish_times = []                                       # define finish_times as a list
    min_place = []
    useagecount = 0                                         # set the device usage count to zero
    if devicetype != "Duration" and devicetype != "Cycle":
        print "Please enter a valid usage type"
    percentagereduce = (100.0 - float(saving))/100.0        # convert from a percentage saved into a reduction amount
    minperiods = np.ceil(np.divide(np.float64(mintime), np.float64(mininterval)))
                                                            # convert min time between number of cycles into
                                                            # min interval. Rounding up to nearest interval
    for z in np.arange(0, intervalcount):                   # loop through all the intervals
        cyclecount = 0                                      # reset the count of how many hours the use went for
        if demand[z] > 0:                                   # if demand is on check how many intervals it runs for
            for k in np.arange(z, intervalcount):           # from next hour until the end (inclusive of last hour)
                if demand[k] > 0:                           # if next hour is greater then zero eg still in use
                    cyclecount += 1                         # add one more to count of cycle length
                else:                                       # if next hour is zero eg device usage stopped
                    break                                   # break counting loop
        if z not in skipinterval and cyclecount > 0:        # skip intervals that have already been optimised
            if mealappliance == 1 and routine[z] == 1:      # if device is used in meal prep and it is meal time
                if devicetype == "Cycle":
                    for e in np.arange(0, cyclecount):          # for all intervals that cycle runs over
                        demandoptimise[z + e] = demand[z + e]   # do not optimse demand
                        skipinterval.append(z + e)              # add optimised intervals to interval skip list
                        if useagecount == cyclemax:
                            finish_times.append(z + cyclecount - 1)   # add time when the cycle ends to finish time list
                            finish_times.remove(finish_times[0])      # remove first recorded time in the list
                        else:
                            useagecount += 1                          # add one to the device useage count
                            finish_times.append(z + cyclecount - 1)   # add time when the cycle ends to finish time list
                elif devicetype == "Duration":
                    demandoptimise[z] = demand[z]
                else:
                    print "Minimisation Error: Check spelling of device type"
            elif devicetype == "Duration":               # when device usage is classified as a duration usage
                interval_reduction = cyclecount * percentagereduce
                for x in np.arange(0, int(interval_reduction)):
                    demandoptimise[z + x] = demand[z + x]
                    skipinterval.append(z + x)
                for x in np.arange(int(interval_reduction), cyclecount):
                    if interval_reduction - int(interval_reduction) > 0 and x == int(interval_reduction):
                        if routine[z + x] > 1 or (routine[z + x] > 0 and mealappliance == 0):
                            demandoptimise[z + x] = demand[z + x] * (interval_reduction - int(interval_reduction))
                        else:
                            demandoptimise[z + x] = demand[z + x]
                        skipinterval.append(z + x)
                    else:
                        if routine[z + x] > 1 or (routine[z + x] > 0 and mealappliance == 0):
                            demandoptimise[z + x] = demand[z + x] * (interval_reduction - int(interval_reduction))
                        else:
                            demandoptimise[z + x] = demand[z + x]
                        skipinterval.append(z + x)
                min_place.append([z])
            elif devicetype == "Cycle":                         # when device usage is classified as a cycle usage
                if useagecount == cyclemax:                     # if device turned on when usage count is maxed out
                    finish_times.append(z + cyclecount - 1)     # add time when the cycle ends to the finish time list
                    if minperiods > z - finish_times[0]:        # if device usage is within device min periods limit
                        for e in np.arange(0, cyclecount):      # for all intervals that cycle runs over
                            demandoptimise[z + e] = 0           # eliminate usage
                            skipinterval.append(z + e)          # add optimised intervals to skipped list
                        finish_times = []                       # clear the finish time list
                        useagecount = 0                         # clear the usage counter
                        min_place.append([z])
                    else:                                               # if it is greater then min periods limit
                        for e in np.arange(0, cyclecount):              # for all intervals that cycle runs over
                            demandoptimise[z + e] = demand[z + e]       # do not optimse demand
                            skipinterval.append(z + e)                  # add optimised intervals to skipped list
                        finish_times.remove(finish_times[0])        # remove first recorded time in the list

                else:                                           # if device is on when usage count isn't maxed out
                    useagecount += 1                            # add one to the device useage count
                    finish_times.append(z + cyclecount - 1)     # add time when the cycle ends to the finish time list
                    for e in np.arange(0, cyclecount):          # for all intervals that cycle runs over
                        demandoptimise[z + e] = demand[z + e]   # do not optimse demand
                        skipinterval.append(z + e)              # add optimised intervals to skipped list
            else:
                print "Minimisation Error: Check spelling of device type [Cycle or Duration]"
                break
    if test == 2:
        print "  Min place : (" + str(len(min_place)) + ") " + str(min_place)
    return demandoptimise


def test0():                # Duration, 20% saving and NO meal appliance optimisation
    meal_appliance = 0
    saving_ = 20
    operation_mode = "Duration"
    cycle_max = 0
    min_time = 0
    min_interval = 60                                   # 60 minute intervals
    routine_ = [0, 2, 1, 1, 2, 0, 0]
    demand_ = [0, 5, 10, 0, 3, 0, 4]
    expected_ = [0, 5, 6.000000000000001, 0, 2.4000000000000004, 0, 4]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "Routine   " + str(routine_)
    print "Original  " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 0: Duration, 20% saving and NO meal appliance optimisation \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 0: Duration, 20% saving and NO meal appliance optimisation \n"


def test1():                        # Duration, 20% saving and meal appliance optimisation
    meal_appliance = 1
    saving_ = 20
    operation_mode = "Duration"
    cycle_max = 0
    min_time = 0
    min_interval = 60
    routine_ = [0, 2, 2, 1, 1, 0, 0]
    demand_ = [0, 5, 10, 0, 3, 0, 4]
    expected_ = [0, 5, 6.000000000000001, 0, 3, 0, 4]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "Routine   " + str(routine_)
    print "Original  " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 1: Duration, 20% saving and meal appliance optimisation \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 1: Duration, 20% saving and meal appliance optimisation \n"


def test2():                        # Duration, 20% saving, meal appliance optimisation and optimise last interval
    meal_appliance = 1
    saving_ = 20
    operation_mode = "Duration"
    cycle_max = 0
    min_time = 0
    min_interval = 60
    routine_ = [0, 2, 1, 0, 0, 2, 2]
    demand_ = [0, 5, 10, 0, 0, 3, 4]
    expected_ = [0, 5, 10, 0, 0, 3, 2.4000000000000004]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "Routine   " + str(routine_)
    print "Original  " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 2: Duration, 20% saving, meal appliance optimisation and optimise last interval \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 2: Duration, 20% saving, meal appliance optimisation and optimise last interval \n"


def test3():                # Cycle, 2 cycle max within 4 intervals and no meal appliance optimisation
    meal_appliance = 0
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 2                           # more then 2 times
    min_time = 4                            # in 4 hours
    min_interval = 1                        # (time intervals are 1 hour)
    routine_ = [1, 1, 0, 1, 2, 1, 1]
    demand_ = [10, 0, 10, 0, 10, 0, 4]
    expected_ = [10, 0, 10, 0, 10, 0, 4]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 3: Cycle, more then 2 within 4 intervals and no meal appliance optimisation\n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 3: Cycle, more then 2 within 4 intervals and no meal appliance optimisation\n"


def test4():                # Cycle, more then 2 within 6 intervals and no meal appliance optimisation
    meal_appliance = 0
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 2                           # more then 2 times
    min_time = 6                            # in 6 hours
    min_interval = 1                        # (time intervals are 1 hour)
    routine_ = [1, 1, 0, 1, 2, 1, 1, 1]
    demand_ = [10, 0, 10, 10, 0, 10, 10, 0]
    expected_ = [10, 0, 10, 10, 0, 0, 0, 0]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 4: Cycle, more then 2 within 6 intervals and no meal appliance optimisation\n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 4: Cycle, more then 2 within 6 intervals and no meal appliance optimisation\n"


def test5():                # Cycle, more then 2 within 6 intervals and meal appliance optimisation
    meal_appliance = 1
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 2                           # more then 2 times
    min_time = 6                            # in 6 hours
    min_interval = 1                        # (time intervals are 1 hour)
    routine_ = [2, 2, 2, 2, 2, 1, 1, 1]
    demand_ = [10, 0, 10, 10, 0, 10, 10, 0]
    expected_ = [10, 0, 10, 10, 0, 10, 10, 0]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 5: Cycle, more then 2 within 6 intervals and meal appliance optimisation \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 5: Cycle, more then 2 within 6 intervals and meal appliance optimisation\n"


def test6():                # Cycle, more then 2 within 6 intervals and meal appliance optimisation (2)
    meal_appliance = 1
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 2                           # more then 2 times
    min_time = 6                            # in 6 hours
    min_interval = 1                        # (time intervals are 1 hour)
    routine_ = [1, 0, 0, 0, 2, 2, 2, 2]
    demand_ = [10, 0, 10, 10, 0, 10, 10, 0]
    expected_ = [10, 0, 10, 10, 0, 0, 0, 0]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 6: Cycle, more then 2 within 6 intervals and meal appliance optimisation (2) \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 6: Cycle, more then 2 within 6 intervals and meal appliance optimisation (2)\n"


def test7():                # Cycle, more then 1 time within 3 intervals, no meal and repeat optimising
    meal_appliance = 0
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 1                           # more then 1 time
    min_time = 3                            # in 3 hours
    min_interval = 1                        # (time intervals are 1 hour)
    routine_ = [1, 1, 1, 1, 2, 2, 2, 2]
    demand_ = [10, 0, 10, 10, 0, 10, 0, 10]
    expected_ = [10, 0, 0, 0, 0, 10, 0, 0]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 7: Cycle, more then 1 time within 3 intervals, no meal and repeat optimising \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 7: Cycle, more then 1 time within 3 intervals, no meal and repeat optimising \n"


def test8():                # Cycle, more then 1 time within 3 intervals, meal and repeat optimising
    meal_appliance = 1
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 1                           # more then 1 time
    min_time = 3                            # in 3 hours
    min_interval = 1                        # (time intervals are 1 hour)
    routine_ = [1, 1, 1, 1, 2, 2, 2, 2]
    demand_ = [10, 0, 10, 10, 0, 10, 0, 10]
    expected_ = [10, 0, 10, 10, 0, 0, 0, 10]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 8: Cycle, more then 1 time within 3 intervals, meal and repeat optimising \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 8: Cycle, more then 1 time within 3 intervals, meal and repeat optimising \n"


def test9():                # Cycle, more then 2 time within 35 mins, 30 min intervals and no meal
    meal_appliance = 0
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 1                            # more then 1 cycle
    min_time = 65                            # in 65 min
    min_interval = 30                        # time intervals are 30 mins (round up to more then 1 in 3 intervals)
    routine_ = [1, 1, 1, 1, 2, 2, 2, 2]
    demand_ = [10, 0, 10, 10, 0, 10, 0, 10]
    expected_ = [10, 0, 0, 0, 0, 10, 0, 0]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 9: Cycle, more then 2 time within 35 mins, 30 min intervals and no meal \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 9: Cycle, more then 2 time within 35 mins, 30 min intervals and no meal \n"


def test10():                # Meal changeover halfway through duration usage
    meal_appliance = 1
    saving_ = 15
    operation_mode = "Duration"
    cycle_max = 1                            # more then 1 cycle
    min_time = 65                            # in 65 min
    min_interval = 30                        # time intervals are 30 mins (round up to more then 1 in 3 intervals)
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 8.5]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 10: Meal changeover halfway through duration usage \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 10: Meal changeover halfway through duration usage \n"


def test11():                # Dishwasher debug: removing finishing times from finish time list (Line 60)
    meal_appliance = 0
    saving_ = 100
    operation_mode = "Cycle"
    cycle_max = 1                            # limit to 1 cycle
    min_time = 2880                          # every two days
    min_interval = 30                        # time intervals are 30 mins (round up to more then 1 in 3 intervals)
    routine_ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0]
    demand_ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.028019002157666686, 0.03530552126800026, 0.19516753753106672, 0.038499145804133481, 0.059074412415000069, 0.0025239459077999989, 0.26858423478513338, 0.31593440898186687, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00087603914699999996, 0.057025214576000016, 0.004245532288799988, 0.22949339157313364, 0.0014995978924666677, 0.056525161548000094, 0.005743552527000019, 0.35222161216073433, 0.19509844074700014, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0021801126479333338, 0.049497733206333508, 0.064089931575933373, 0.15741152528873398, 0.049535646553600036, 0.0052247203348666834, 0.12867921848466674, 0.40173185144580087, 0.017293674606133343, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    expected_ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.028019002157666686, 0.03530552126800026, 0.19516753753106672, 0.03849914580413348, 0.05907441241500007, 0.002523945907799999, 0.2685842347851334, 0.31593440898186687, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.000876039147, 0.057025214576000016, 0.004245532288799988, 0.22949339157313364, 0.0014995978924666677, 0.056525161548000094, 0.005743552527000019, 0.35222161216073433, 0.19509844074700014, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.002180112647933334, 0.04949773320633351, 0.06408993157593337, 0.15741152528873398, 0.049535646553600036, 0.005224720334866683, 0.12867921848466674, 0.40173185144580087, 0.017293674606133343, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    demand_optimised = minimise(demand_, routine_, meal_appliance, operation_mode, min_interval, saving_, cycle_max,
                                min_time, 0)
    print "  Routine " + str(routine_)
    print " Original " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 11: Dishwasher debug: removing finishing times from finish time list (Line 60)\n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 11: Dishwasher debug: removing finishing times from finish time list (Line 60) \n"

if __name__ == '__main__':

    tests = "All"                   # select tests to be ran

    testing = []
    if tests == "Mix":     # (0 off/1 on)
        testing.append(1)  # test 0: Duration, 20% saving and NO meal appliance optimisation
        testing.append(0)  # test 1: Duration, 20% saving and meal appliance optimisation
        testing.append(0)  # test 2: Duration, 20% saving, meal appliance optimisation and optimise last interval
        testing.append(0)  # test 3: Cycle, more then 2 within 4 intervals and no meal appliance optimisation
        testing.append(0)  # test 4: Cycle, more then 2 within 6 intervals and no meal appliance optimisation
        testing.append(0)  # test 5: Cycle, more then 2 within 6 intervals and meal appliance optimisation
        testing.append(0)  # test 6: Cycle, more then 2 within 6 intervals and meal appliance optimisation (2)
        testing.append(0)  # test 7: Cycle, more then 1 time within 3 intervals, no meal and repeat optimising
        testing.append(0)  # test 8: Cycle, more then 1 time within 3 intervals, meal and repeat optimising
        testing.append(0)  # test 9: Cycle, more then 2 time within 35 mins, 30 min intervals and no meal
        testing.append(0)  # test 10: Meal changeover halfway through duration usage
        testing.append(0)  # test 11: Dishwasher debug: removing finishing times from finish time list (Line 60)
    elif tests == "None":
        testing = [0 for w in range(0, 12)]
    elif tests == "All":
        testing = [1 for w in range(0, 12)]
    if testing[0] > 0:
        test0()
    if testing[1] > 0:
        test1()
    if testing[2] > 0:
        test2()
    if testing[3] > 0:
        test3()
    if testing[4] > 0:
        test4()
    if testing[5] > 0:
        test5()
    if testing[6] > 0:
        test6()
    if testing[7] > 0:
        test7()
    if testing[8] > 0:
        test8()
    if testing[9] > 0:
        test9()
    if testing[10] > 0:
        test10()
    if testing[11] > 0:
        test11()