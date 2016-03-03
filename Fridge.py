__author__ = 'Bat Cave'

import numpy as np
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be


def fridge(device_demand, test):
    #import and aggregate clothes dryer data
    optimised_demand = device_demand
    if test == 1:
        demand_amounts = [x for i, x in enumerate(device_demand) if x > 0]
        demand_indices = [i for i, x in enumerate(device_demand) if x > 0]
        print "[Intervals with demand = " + str(np.count_nonzero(device_demand)) + "] [Total demand = " + \
              str(np.sum(demand_amounts)) + "] [Average demand = " + str(np.mean(demand_amounts)) + \
              "] [Demand indices = " + str(len(demand_indices)) + " " + str(demand_indices) + "]"

    demand_variation = [a - b for a, b in zip(optimised_demand, device_demand)]
                                                # difference between optimised & original demand for each interval
    return demand_variation


def test0():                    # test shifting
    testing_ = 1
    min_interval = 15
    csv_directory = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house2"
    csv = "consumption.csv"
    csvpath = str(csv_directory) + "\\" + str(csv)
    housedata = ida.aggregatedatacsv(csvpath, min_interval)
    expected_ = []
    appliancedemand = ida.deviceimport(housedata, min_interval, csv_directory, "No", "No", "No", "No", "Yes", "No",
                                       "No", "No", "No", "No", "No", "No", "No", "No")
    device_demand = appliancedemand[0][4]
    variation = fridge(device_demand, testing_)
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