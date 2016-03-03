__author__ = 'Bat Cave'

import numpy as np
import sys
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be
import Eliminate as el


def secondfridge(device_demand, routine, cost, hh_threshold, test):
    # general 2nd fridge inputs
    devicetype = "Cycle"                        # "Duration" if occupant needed at start and end otherwise "Cycle"
    mealappliance = 1                           # 0 if device not used in meal prep/ 1 if device is used in prep
    elim_thres = 7

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
    if test == 1:
        print "            Demand: (" + str(hh_threshold) + ") " + str(device_demand) + "  (" + str(len(device_demand)) + ")"
    if hh_threshold >= elim_thres:            # apply elimintion optimisations if effort threshold >= elim threshold
        optimised_demand = el.eliminate(device_demand, routine, mealappliance, devicetype)
                                               # implement applicable device usage optimsiations
    else:                                      # if it is less then six
        optimised_demand = device_demand                  # device usage is not optimised
    if test == 1:
        print " Opti Elim Demand1: (" + str(elim_thres) + ") " + str(optimised_demand) + " (" + str(len(optimised_demand)) + ")"

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
    min_interval = 15
    csv_directory = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house2"
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
    devicedemand = ida.deviceimport(housedata, min_interval, csv_directory, "No", "No", "No", "No", "No", "No",
                                    "Yes", "No", "No", "No", "No", "No", "No", "No")
    device_demand = devicedemand[0][6]
    variation = secondfridge(device_demand, routine_, cost_, threshold, testing_)
    print "\n        Variation: " + str(variation)
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