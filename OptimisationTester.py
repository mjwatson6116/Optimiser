__author__ = 'Bat Cave'

import numpy as np
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be
import HouseholdType as ht
import Eliminate as el
import Substitute as sb
import Minimise as mn
import Shifting as sh


def testsettings(demand, routine, mininterval, cost, hh_threshold, shifting, test, mealappliance, devicetype,
                 elim_thres, mini_thres, mini_saving, mini_cyclemax, mini_time, shift_thres, shift_time, sub_thres,
                 sub_type, sub_time, sub_demand, sub_saving):

    # mealappliance = 0                          # 0 if device not used in meal prep/ 1 if device is used in prep
    # devicetype = "Duration"                    # "Duration" if occupant needed at start and end otherwise "Cycle"
    #
    # # inputs especially for kettle optimsiation using elimination:
    # elim_thres = 7                             # how much effort it takes to eliminate device usage
    #
    # # inputs especially for kettle optimsiation using minimisation:
    # mini_thres = 5                             # how much effort it takes to minimise device usage
    # mini_saving = 15                           # if type duration, what percentage will be saved (0 nothing - 100)
    # mini_cyclemax = 2                          # if type cycle, what is the maximum amount of cycles...
    # mini_time = 120                            # if type cycle, ...within a given time frame
    #
    # # inputs especially for kettle optimsiation using shifting:
    # shift_thres = 5                            # how much effort it takes to shift device usage
    # shift_time = 120                           # how long can the use of the device be shifted
    #
    # # inputs especially for kettle optimsiation using substitution:
    # sub_thres = 5                              # how much effort it takes to substitue the device usage
    # sub_type = "Duration"                      # what device type is the substitue. "Duration" or "Cycle"
    # sub_time = 45                              # if subtype cycle, how much time the sub takes to complete a cycle
    # sub_demand = 15                            # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    # sub_saving = 15                            # if subtype duration, what percentage of electricity does it
    #                                            # save relative to current device (0 saves nothing - 100)
    if test == 1:
        demand_amounts = [x for i, x in enumerate(demand) if x > 0]
        demand_indices = [i for i, x in enumerate(demand) if x > 0]
        print "[Intervals with demand = " + str(np.count_nonzero(demand)) + "] [Average demand = " + \
              str(np.mean(demand_amounts)) + "] [Demand indices = " + str(len(demand_indices)) + \
              " " + str(demand_indices) + "]"
        print "Device: " + str(devicetype[0]) + "        Cost: " + str(cost)
        print "Meal: " + str(mealappliance) + "       Routine: " + str(routine) + "  (" + str(len(routine)) + ")"

    # ****** Optimisation ******
    if test == 1:
        print "           Demand: (" + str(hh_threshold) + ") " + str(demand) + "  (" + str(len(demand)) + ")"
    if hh_threshold >= elim_thres:            # apply elimintion optimisations if effort threshold >= elim threshold
        optimised_demand = el.eliminate(demand, routine, mealappliance, devicetype)
                                               # implement applicable device usage optimsiations
    else:                                      # if it is less then six
        optimised_demand = demand                  # device usage is not optimised
    if test == 1:
        print "Opti Elim Demand1: (" + str(elim_thres) + ") " + str(optimised_demand) + " (" + str(len(optimised_demand)) + ")"

    # ****** Minimisation ******
    if hh_threshold >= mini_thres:          # apply minimisation optimisations if effort threshold >= mini threshold
        optimised_demand = mn.minimise(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                       mini_saving, mini_cyclemax, mini_time)
                                               # return optimised device usage
    else:                                      # if effort threshold lower then value
        optimised_demand = optimised_demand            # device usage is not optimised
    if test == 1:
        print "Opti Mini Demand2: (" + str(mini_thres) + ") " + str(optimised_demand) + " (" + str(len(optimised_demand)) + ")"

    # ****** Shifting ******
    if hh_threshold >= shift_thres and shifting == 1:
                                        # apply shifting optimisation if shifting on & threshold >= shift thres
        optimised_demand = sh.shifter(optimised_demand, routine, mealappliance, devicetype, mininterval, shift_time,
                                      cost)
                                               # return optimised device usage
    else:                                      # if effort theshold low then value or shifting is off
        optimised_demand = optimised_demand             # device usage is not optimsied
    if test == 1:
        print "Opti Shif Demand3: (" + str(shift_thres) + ") " + str(optimised_demand) + " (" + str(len(optimised_demand)) + ")"

    # ****** Substitution ******
    if hh_threshold >= sub_thres:          # apply substituation optimisations if effort threshold >= sub threshold
        optimised_demand = sb.substitute(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                         sub_type, sub_time, sub_demand, sub_saving)
                                               # return optimised device usage
    else:                                      # if effort threshold lower then value
        optimised_demand = optimised_demand            # device usage is not optimised
    if test == 1:
        print "Opti Subs Demand4: (" + str(sub_thres) + ") " + str(optimised_demand) + " (" + str(len(optimised_demand)) + ")\n "

    demand_variation = [a - b for a, b in zip(optimised_demand, demand)]
                                                # difference between optimised & original demand for each interval
    return demand_variation


def test0():                    # no meal, duration, no elim, mini 15%, shifting off, sub 15%
    testing_ = 1
    threshold = 6
    shifting_ = 0
    min_interval = 15
    routine_ = [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    cost_ = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [-2.7750000000000004, -2.7750000000000004, 0.0, 0.0, -2.7750000000000004, -2.7750000000000004, 0.0, 0.0,
                 0.0, -2.7750000000000004, -2.7750000000000004]
    meal_appliance = 0
    device_type = "Duration"
    elimthres = 7
    minithres = 5
    minisaving = 15
    minicyclemax = 2
    minitime = 120
    shiftthres = 5
    shifttime = 120
    subthres = 5
    subtype = "Duration"
    subtime = 45
    subdemand = 15
    subsaving = 15
    print "** Test 0 **"
    variation = testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_, meal_appliance,
                             device_type, elimthres, minithres, minisaving, minicyclemax, minitime, shiftthres,
                             shifttime, subthres, subtype, subtime, subdemand, subsaving)
    print "\n        Variation: " + str(variation)
    if variation == expected_:
        print "Pass test 0: no meal, duration, no elim, mini 15%, shifting off, sub 15%\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 0: no meal, duration, no elim, mini 15%, shifting off, sub 15%\n"


def test1():                    # no meal, duration, no elim, mini 15%, shifting on (4), sub 15%
    testing_ = 1
    threshold = 6
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [-2.7750000000000004, -2.7750000000000004, 0.0, 0.0, -10.0, -10.0, 7.225, 7.225, 0.0,
                 -2.7750000000000004, -2.7750000000000004]
    meal_appliance = 0
    device_type = "Duration"
    elimthres = 7
    minithres = 5
    minisaving = 15
    minicyclemax = 2
    minitime = 120
    shiftthres = 5
    shifttime = 60
    subthres = 5
    subtype = "Duration"
    subtime = 45
    subdemand = 15
    subsaving = 15
    print "** Test 1 **"
    variation = testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_, meal_appliance,
                             device_type, elimthres, minithres, minisaving, minicyclemax, minitime, shiftthres,
                             shifttime, subthres, subtype, subtime, subdemand, subsaving)
    print "\n        Variation: " + str(variation)
    if variation == expected_:
        print "Pass test 1: no meal, duration, no elim, mini 15%, shifting on (4), sub 15%\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 1: # no meal, duration, no elim, mini 15%, shifting on (4), sub 15%\n"


def test2():                    # meal, duration, no elim, mini 15%, shifting on (4), sub 15%
    testing_ = 1
    threshold = 6
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [-2.7750000000000004, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, -2.7750000000000004]
    meal_appliance = 1
    device_type = "Duration"
    elimthres = 7
    minithres = 5
    minisaving = 15
    minicyclemax = 2
    minitime = 120
    shiftthres = 5
    shifttime = 60
    subthres = 5
    subtype = "Duration"
    subtime = 45
    subdemand = 15
    subsaving = 15
    print "** Test 2 **"
    variation = testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_, meal_appliance,
                             device_type, elimthres, minithres, minisaving, minicyclemax, minitime, shiftthres,
                             shifttime, subthres, subtype, subtime, subdemand, subsaving)
    print "\n        Variation: " + str(variation)
    if variation == expected_:
        print "Pass test 2: meal, duration, no elim, mini 15%, shifting on (4), sub 15%\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 2: meal, duration, no elim, mini 15%, shifting on (4), sub 15%\n"


def test3():                    # Test elimination with meal on, duration type
    testing_ = 1
    threshold = 6
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [-10.0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, -10.0]
    meal_appliance = 1
    device_type = "Duration"
    elimthres = 6
    minithres = 5
    minisaving = 15
    minicyclemax = 2
    minitime = 120
    shiftthres = 5
    shifttime = 60
    subthres = 5
    subtype = "Duration"
    subtime = 45
    subdemand = 15
    subsaving = 15
    print "** Test 2 **"
    variation = testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_, meal_appliance,
                             device_type, elimthres, minithres, minisaving, minicyclemax, minitime, shiftthres,
                             shifttime, subthres, subtype, subtime, subdemand, subsaving)
    print "\n        Variation: " + str(variation)
    if variation == expected_:
        print "Pass test 3: Test elimination with meal on, duration type\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 3: Test elimination with meal on, duration type\n"


def test4():                    # Test elimination with meal on, Cycle type
    testing_ = 1
    threshold = 6
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [-10, -10, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    meal_appliance = 1
    device_type = "Cycle"
    elimthres = 6
    minithres = 5
    minisaving = 15
    minicyclemax = 2
    minitime = 120
    shiftthres = 5
    shifttime = 60
    subthres = 5
    subtype = "Cycle"
    subtime = 45
    subdemand = 15
    subsaving = 15
    print "** Test 4 **"
    variation = testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_, meal_appliance,
                             device_type, elimthres, minithres, minisaving, minicyclemax, minitime, shiftthres,
                             shifttime, subthres, subtype, subtime, subdemand, subsaving)
    print "\n        Variation: " + str(variation)
    if variation == expected_:
        print "Pass test 4: test elimination with meal on, Cycle type\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 4: test elimination with meal on, Cycle type\n"


def test5():                    # loop hh threshold, meal on, type cycle, sub 15/3, shift 4, min 2/8
    testing_ = 1
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [[-5.0, -5.0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0], [-5.0, -5.0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [-5.0, -5.0, 5.0, 0, 0, 0, 0, 0, 0, 0, 0], [-10, -10, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    meal_appliance = 1
    device_type = "Cycle"
    elimthres = 7
    minithres = 6
    minisaving = 15
    minicyclemax = 2
    minitime = 120
    shiftthres = 5
    shifttime = 60
    subthres = 4
    subtype = "Cycle"
    subtime = 45
    subdemand = 15
    subsaving = 15
    variation = []
    print "** Test 5 **"
    hhthreshold = [4, 5, 6, 7]
    for q in np.arange(0, len(hhthreshold)):
        threshold = hhthreshold[q]
        variation.append(testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_,
                                      meal_appliance, device_type, elimthres, minithres, minisaving, minicyclemax,
                                      minitime, shiftthres, shifttime, subthres, subtype, subtime, subdemand,
                                      subsaving))
    print "       Variations: " + str(variation)
    if variation == expected_:
        print "Pass test 5: loop hh threshold, meal on, type cycle, sub 15/3, shift 4, min 2/8\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 5: loop hh threshold, meal on, type cycle, sub 15/3, shift 4, min 2/8\n"


def test6():                    # loop hh threshold, meal off, type cycle, sub 15/3, shift 4, min 2/9
    testing_ = 1
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [[-5.0, -5.0, 5.0, 0, -5.0, -5.0, 5.0, 0, 0, 0, 0], [-5.0, -5.0, 5.0, 0, -10, -10, 5.0, 5.0, 5.0, 0, 0],
                 [-5.0, -5.0, 5.0, 0, -10, -10, 5.0, 5.0, 5.0, -10, -10], [-10, -10, 0, 0, -10, -10, 0, 0, 0, -10, -10]]
    meal_appliance = 0
    device_type = "Cycle"
    elimthres = 7
    minithres = 6
    minisaving = 15
    minicyclemax = 2
    minitime = 135
    shiftthres = 5
    shifttime = 60
    subthres = 4
    subtype = "Cycle"
    subtime = 45
    subdemand = 15
    subsaving = 15
    variation = []
    print "** Test 6 **"
    hhthreshold = [4, 5, 6, 7]
    for q in np.arange(0, len(hhthreshold)):
        threshold = hhthreshold[q]
        variation.append(testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_,
                                      meal_appliance, device_type, elimthres, minithres, minisaving, minicyclemax,
                                      minitime, shiftthres, shifttime, subthres, subtype, subtime, subdemand,
                                      subsaving))
    print "       Variations: " + str(variation)
    if variation == expected_:
        print "Pass test 6: loop hh threshold, meal off, type cycle, sub 15/3, shift 4, min 2/9\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 6: loop hh threshold, meal off, type cycle, sub 15/3, shift 4, min 2/9\n"


def test7():                    # loop hh threshold, meal off, type duration, sub 15%, shift 4, min 20%
    testing_ = 1
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [[-1.5, -1.5, 0, 0, -1.5, -1.5, 0.0, 0.0, 0.0, -1.5, -1.5],
                 [-1.5, -1.5, 0, 0, -10.0, -10.0, 8.5, 8.5, 0.0, -1.5, -1.5],
                 [-3.2, -3.2, 0, 0, -10.0, -10.0, 6.8, 6.8, 0.0, -3.2, -3.2],
                 [-10.0, -10.0, 0, 0, -10.0, -10.0, 0.0, 0.0, 0.0, -10.0, -10.0]]
    meal_appliance = 0
    device_type = "Duration"
    elimthres = 7
    minithres = 6
    minisaving = 20
    minicyclemax = 2
    minitime = 135
    shiftthres = 5
    shifttime = 60
    subthres = 4
    subtype = "Duration"
    subtime = 45
    subdemand = 15
    subsaving = 15
    variation = []
    print "** Test 7 **"
    hhthreshold = [4, 5, 6, 7]
    for q in np.arange(0, len(hhthreshold)):
        threshold = hhthreshold[q]
        variation.append(testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_,
                                      meal_appliance, device_type, elimthres, minithres, minisaving, minicyclemax,
                                      minitime, shiftthres, shifttime, subthres, subtype, subtime, subdemand,
                                      subsaving))
    print "       Variations: " + str(variation)
    if variation == expected_:
        print "Pass test 7: loop hh threshold, meal off, type duration, sub 15%, shift 4, min 20%\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 7: loop hh threshold, meal off, type duration, sub 15%, shift 4, min 20%\n"


def test8():                    # loop hh threshold, meal on, type duration, sub 15%, shift 4, min 20%
    testing_ = 1
    shifting_ = 1
    min_interval = 15
    routine_ = [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [[-1.5, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, -1.5], [-1.5, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, -1.5],
                 [-3.2, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, -3.2], [-10.0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, -10.0]]
    meal_appliance = 1
    device_type = "Duration"
    elimthres = 7
    minithres = 6
    minisaving = 20
    minicyclemax = 2
    minitime = 135
    shiftthres = 5
    shifttime = 60
    subthres = 4
    subtype = "Duration"
    subtime = 45
    subdemand = 15
    subsaving = 15
    variation = []
    print "** Test 8 **"
    hhthreshold = [4, 5, 6, 7]
    for q in np.arange(0, len(hhthreshold)):
        threshold = hhthreshold[q]
        variation.append(testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_,
                                      meal_appliance, device_type, elimthres, minithres, minisaving, minicyclemax,
                                      minitime, shiftthres, shifttime, subthres, subtype, subtime, subdemand,
                                      subsaving))
    print "       Variations: " + str(variation)
    if variation == expected_:
        print "Pass test 8: loop hh threshold, meal on, type duration, sub 15%, shift 4, min 20%\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 8: loop hh threshold, meal off, type duration, sub 15%, shift 4, min 20%\n"


def test9():                    # loop hh threshold, meal on, type duration, sub 15%, shift 4, min 20%
    testing_ = 1
    shifting_ = 1
    min_interval = 15
    threshold = 6
    cost_ = [15, 15, 30, 30, 45, 45, 15, 15, 15, 15, 15]
    demand_ = [10, 10, 0, 0, 10, 10, 0, 0, 0, 10, 10]
    expected_ = [[-3.2, -3.2, 0.0, 0.0, -10.0, -10.0, 6.8, 6.8, 0.0, -3.2, -3.2],
                 [0, 0, 0.0, 0.0, -10.0, -10, 8.0, 10, 0.0, -3.2, -3.2],
                 [0, 0, 0.0, 0, -10.0, -10, 0, 6.8, 8.5, 0, -3.2],
                 [-3.2, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, -3.2]]
    expected_saving = [-3.2, -3.2, 0.0, 0.0, -10.0, -10.0, 6.8, 6.8, 0.0, -3.2, -3.2]
    meal_appliance = 1
    device_type = "Duration"
    elimthres = 7
    minithres = 6
    minisaving = 20
    minicyclemax = 2
    minitime = 135
    shiftthres = 5
    shifttime = 60
    subthres = 4
    subtype = "Duration"
    subtime = 45
    subdemand = 15
    subsaving = 15
    variation = []
    print "** Test 9 **"
    hh_routine = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2],
                  [0, 1, 2, 0, 2, 1, 0, 2, 2, 0, 2], [2, 1, 0, 0, 1, 1, 2, 2, 2, 1, 2]]
    for q in np.arange(0, len(hh_routine)):
        routine_ = hh_routine[q]
        variation.append(testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_,
                                      meal_appliance, device_type, elimthres, minithres, minisaving, minicyclemax,
                                      minitime, shiftthres, shifttime, subthres, subtype, subtime, subdemand,
                                      subsaving))
    print "       Variations: " + str(variation)

    vary_calc = []                                              # define variation calculation as a list
    max_saving = []                                             # define maximum savings as a list
    for m in np.arange(0, len(variation)):                      # for all the different variations
        vary_calc.append(sum(variation[m]))                     # sum all the optimisation changes and add to a list
    min_variation_index = [i for i, x in enumerate(vary_calc) if x == min(vary_calc)]   # find index of greatest saving
    for y in np.arange(0, len(min_variation_index)):            # for all scenerios where the greatest saving is made
        max_saving.append(variation[min_variation_index[y]])    # add the variations to a list
    print " Saving Variation: " + str(max_saving[0])            # print the max saving variation pattern list

    if variation == expected_ and max_saving[0] == expected_saving:
        print "Pass test 9: loop routine, meal off, type duration, sub 15%, shift 4, min 20% \n"
    else:
        print "         Expected: " + str(expected_)
        print "  Expected saving: " + str(expected_saving)
        print "***** Fail ***** test 9: loop routine, meal off, type duration, sub 15%, shift 4, min 20%\n"


def test10():                    # real kettle data treated as a cycle
    optigoal = "Bill"
    testing_ = 1
    shifting_ = 0
    min_interval = 180
    c_load = 0
    meter = 1
    threshold = 6
    csv = "74-kettle-101-consumption.csv"
    csvpath = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\h1_150120\h1" + "\\" + "141229_150104_50_h1" + "\\" \
              + str(csv)
    kettledata = ida.aggregatedatacsv(csvpath, min_interval)
    demand_ = kettledata[1]
    occupants = [1, 1, 1, 1, 1, 1]
    routine_ = rb.routine_builder(demand_, min_interval, occupants)
    bill_type = 1
    bill_number = 1
    if optigoal == "Bill" and bill_type == 3:                    # if optimising for bill and eval at ToU bill
        shifting_ = 1                                             # enable appliance shifting
    cost_ = be.bill_eval(demand_, bill_type, bill_number, min_interval, 0, c_load, meter)
    expected_ = [[0.0, 0.0, 0.0, -68021.64893168, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -74762.03088144002, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0, -96389.143949120044, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -160431.63805943992,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -75922.154274079978, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  -103159.85328527998, -68490.919669680006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -58786.738587680011, 0.0,
                  0.0, 0.0, 0.0, 0.0]]
    expected_saving = [[0.0, 0.0, 0.0, -68021.64893168, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -74762.03088144002,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -96389.143949120044, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        -160431.63805943992, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -75922.154274079978, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, -103159.85328527998, -68490.919669680006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        -58786.738587680011, 0.0, 0.0, 0.0, 0.0, 0.0]]
    meal_appliance = 0
    device_type = "Cycle"
    elimthres = 7
    minithres = 6
    minisaving = 20
    minicyclemax = 1
    minitime = 3600
    shiftthres = 5
    shifttime = 60
    subthres = 4
    subtype = "Cycle"
    subtime = 45
    subdemand = 1000
    subsaving = 15
    variation = []
    print "** Test 10 **"
    for q in np.arange(0, 1):
        variation.append(testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_,
                                      meal_appliance, device_type, elimthres, minithres, minisaving, minicyclemax,
                                      minitime, shiftthres, shifttime, subthres, subtype, subtime, subdemand,
                                      subsaving))
    print "       Variations: " + str(variation)

    vary_calc = []                                              # define variation calculation as a list
    max_saving = []                                             # define maximum savings as a list
    for m in np.arange(0, len(variation)):                      # for all the different variations
        vary_calc.append(sum(variation[m]))                     # sum all the optimisation changes and add to a list
    min_variation_index = [i for i, x in enumerate(vary_calc) if x == min(vary_calc)]   # find index of greatest saving
    for y in np.arange(0, len(min_variation_index)):            # for all scenerios where the greatest saving is made
        max_saving.append(variation[min_variation_index[y]])    # add the variations to a list
    print " Saving Variation: " + str(max_saving)               # print the max saving variation pattern list
    print "   Intervals optimised " + str(np.count_nonzero(max_saving[0]))

    if variation == expected_ and max_saving == expected_saving:
        print "Pass test 10: real data \n"
    else:
        print "         Expected: " + str(expected_)
        print "  Expected saving: " + str(expected_saving)
        print "***** Fail ***** test 10: real data\n"


def test11():                    # real kettle data treated as a cycle
    optigoal = "Bill"
    testing_ = 1
    shifting_ = 0
    min_interval = 60
    threshold = 1
    meal_appliance = 0
    c_load = 0
    meter = 1
    device_type = "Cycle"
    elimthres = 7
    minithres = 6
    minisaving = 20
    minicyclemax = 1
    minitime = 3600
    shiftthres = 5
    shifttime = 180
    subthres = 4
    subtype = "Cycle"
    subtime = 45
    subdemand = 1000
    subsaving = 15
    csv = "sound-system.csv"
    csvpath = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house" + "\\" + str(csv)
    data = ida.aggregatedatacsv(csvpath, min_interval)
    demand_ = data[1]
    occupants = [1, 1, 1, 1, 1, 1]
    routine_ = rb.routine_builder(demand_, min_interval, occupants)
    bill_type = 2
    bill_number = 1
    if optigoal == "Bill" and bill_type == 2:                    # if optimising for bill and eval at ToU bill
        shifting_ = 1                                             # enable appliance shifting
    all_billing = be.bill_eval(demand_, bill_type, bill_number, min_interval, 0, c_load, meter)
    cost_ = all_billing[1]
    expected_ = [[]]
    expected_saving = [[]]
    print "** Test 11 ** " + str(csv)
    variation = []
    for q in np.arange(0, 1):
        variation.append(testsettings(demand_, routine_, min_interval, cost_, threshold, shifting_, testing_,
                                      meal_appliance, device_type, elimthres, minithres, minisaving, minicyclemax,
                                      minitime, shiftthres, shifttime, subthres, subtype, subtime, subdemand,
                                      subsaving))

    vary_calc = []                                              # define variation calculation as a list
    max_saving = []                                             # define maximum savings as a list
    for m in np.arange(0, len(variation)):                      # for all the different variations
        vary_calc.append(sum(variation[m]))                     # sum all the optimisation changes and add to a list
    min_variation_index = [i for i, x in enumerate(vary_calc) if x == min(vary_calc)]   # find index of greatest saving
    for y in np.arange(0, len(min_variation_index)):            # for all scenerios where the greatest saving is made
        max_saving.append(variation[min_variation_index[y]])    # add the variations to a list

    print "   Intervals optimised " + str(np.count_nonzero(max_saving[0]))
    print "       Variations: " + str(variation)
    print " Saving Variation: " + str(max_saving)               # print the max saving variation pattern list

    if variation == expected_ and max_saving == expected_saving:
        print "Pass test 11: real data \n"
    else:
        print "         Expected: " + str(expected_)
        print "  Expected saving: " + str(expected_saving)
        print "***** Fail ***** test 11: real data\n"

if __name__ == '__main__':

    tests = "Mix"                   # select tests to be ran

    testing = []
    if tests == "Mix":     # (0 off/1 on)
        testing.append(0)  # test 0: no meal, duration, no elim, mini 15%, shifting off, sub 15%
        testing.append(0)  # test 1: no meal, duration, no elim, mini 15%, shifting on (4), sub 15%
        testing.append(0)  # test 2: meal, duration, no elim, mini 15%, shifting on (4), sub 15%
        testing.append(0)  # test 3: test elimination with meal on, duration type
        testing.append(0)  # test 4: test elimination with meal on, Cycle type
        testing.append(0)  # test 5: loop hh threshold, meal on, type cycle, sub 15/3, shift 4, min 2/8
        testing.append(0)  # test 6: loop hh threshold, meal off, type cycle, sub 15/3, shift 4, min 2/9
        testing.append(0)  # test 7: loop hh threshold, meal off, type duration, sub 15%, shift 4, min 20%
        testing.append(8)  # test 8: loop hh threshold, meal on, type duration, sub 15%, shift 4, min 20%
        testing.append(0)  # test 9: loop routine, meal off, type duration, sub 15%, shift 4, min 20%
        testing.append(0)  # test 10: # real kettle data treated as a cycle
        testing.append(0)  # test 11: # real kettle data treated as a duration
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