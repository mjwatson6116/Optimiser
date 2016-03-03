__author__ = 'Bat Cave'

import numpy as np
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be
import Eliminate as el
import Minimise as mn


def soundsystem(device_demand, routine, mininterval, cost, hh_threshold, shifting, test):
    # general TV inputs
    devicetype = "Duration"                     # "Duration" if occupant needed at start and end otherwise "Cycle"
    mealappliance = 0                           # 0 if device not used in meal prep/ 1 if device is used in prep

    # inputs especially for sound system optimsiation using elimination:
    elim_thres = 10                              # how much effort it takes to eliminate device usage

    # inputs especially for sound system optimsiation using minimisation 1:
    mini1_thres = 9                             # how much effort it takes to minimise device usage
    mini1_saving = 10                           # if type duration, what percentage will be saved (0 nothing - 100)
    mini1_cyclemax = 9999                       # if type cycle, what is the maximum amount of cycles...
    mini1_time = 99999                          # if type cycle, ...within a given time frame

    # print test information
    if test == 1:
        demand_amounts = [x for i, x in enumerate(device_demand) if x > 0]
        demand_indices = [i for i, x in enumerate(device_demand) if x > 0]
        print "[Intervals with demand = " + str(np.count_nonzero(device_demand)) + "] [Total demand = " + \
              str(np.sum(demand_amounts)) + "] [Average demand = " + str(np.mean(demand_amounts)) + \
              "] [Demand indices = " + str(len(demand_indices)) + " " + str(demand_indices) + "]"
        print "Device: " + str(devicetype[0]) + "         Cost: (" + str(len(cost)) + ") " + str(cost)
        print "Meal: " + str(mealappliance) + "        Routine: (" + str(len(routine)) + ") " + str(routine)

    # ****** Optimisation ******
    # ****** Elimination ******
    if test == 1:
        print "            Demand: (" + str(hh_threshold) + ") (" + str(len(device_demand)) + ") " + str(device_demand)
    if hh_threshold >= elim_thres:            # apply elimintion optimisations if effort threshold >= elim threshold
        optimised_demand = el.eliminate(device_demand, routine, mealappliance, devicetype)
                                               # implement applicable device usage optimsiations
    else:                                      # if it is less then six
        optimised_demand = device_demand                  # device usage is not optimised
    if test == 1 and hh_threshold >= elim_thres:
        print " Opti Elim1 Demand: (" + str(elim_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1:
        print " Opti ElimP Demand: (" + str(elim_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)

    # ****** Minimisation 1 ******
    if hh_threshold >= mini1_thres:            # apply minimisation optimisations if effort threshold >= mini threshold
        optimised_demand = mn.minimise(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                       mini1_saving, mini1_cyclemax, mini1_time)  # return optimised device usage
    else:                                      # if effort threshold lower then value
        optimised_demand = optimised_demand    # device usage is not optimised

    if test == 1 and hh_threshold >= mini1_thres:
        print " Opti Mini1 Demand: (" + str(mini1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1:
        print " Opti MiniP Demand: (" + str(mini1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)

    demand_variation = [a - b for a, b in zip(optimised_demand, device_demand)]
                                                    # difference between optimised & original demand for each interval
    return demand_variation


def test0():                    # test shifting
    testing_ = 1
    threshold = 6
    optigoal = "Bill"
    shifting_ = 0
    c_load = 0
    meter = 1
    min_interval = 60
    csv_directory = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house"
    csv = "consumption.csv"
    csvpath = str(csv_directory) + "\\" + str(csv)
    housedata = ida.aggregatedatacsv(csvpath, min_interval)
    demand_ = housedata[1]
    occupants = [1, 1, 1, 1, 1, 1]
    routine_ = rb.routine_builder(demand_, min_interval, occupants)
    bill_type = 2
    bill_number = 1
    if optigoal == "Bill" and bill_type == 2:                    # if optimising for bill and eval at ToU bill
        shifting_ = 1                                             # enable appliance shifting
    all_billing = be.bill_eval(demand_, bill_type, bill_number, min_interval, c_load, meter, 0)
    cost_ = all_billing[1]
    expected_ = []
    appliancedemand = ida.deviceimport(housedata, min_interval, csv_directory, "No", "No", "No", "No", "No", "No",
                                       "No", "No", "No", "No", "Yes", "No", "No", "No")
    device_demand = appliancedemand[0][10]
    variation = soundsystem(device_demand, routine_, min_interval, cost_, threshold, shifting_, testing_)
    print "        Variation: " + str(variation)
    if variation == expected_:
        print "Pass test 0: Testing device optimisation using minimisation\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 0: Testing device optimisation using minimisation\n"

if __name__ == '__main__':

    tests = "Mix"                   # select tests to be ran

    testing = []
    if tests == "Mix":     # (0 off/1 on)
        testing.append(1)  # test 0: Testing device optimisation
        testing.append(0)  # test 1:
        testing.append(0)  # test 2:
        testing.append(0)  # test 3:
        testing.append(0)  # test 4:
        testing.append(0)  # test 5:
        testing.append(0)  # test 6:
        testing.append(0)  # test 7:
        testing.append(0)  # test 8:
        testing.append(0)  # test 9:
    elif tests == "None":
        testing = [0 for w in range(0, 10)]
    elif tests == "All":
        testing = [1 for w in range(0, 10)]
    if testing[0] > 0:
        test0()