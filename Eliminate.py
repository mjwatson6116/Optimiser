__author__ = 'Bat Cave'
import numpy as np
import sys


def eliminate(demand):
    intervalcount = len(demand)                             # count how many intervals to be evaluated over
    demandoptimise = [0 for i in range(intervalcount)]      # write zeros for every potential hour
    return demandoptimise


def test0():                # NOT meal appliance optimisation
    routine_ = [0, 2, 0, 1, 2, 0, 0]
    demand_ = [0, 5, 10, 0, 3, 0, 4]
    expected_ = [0, 0, 0, 0, 0, 0, 0]
    demand_optimised = eliminate(demand_)
    print "Routine   " + str(routine_)
    print "Original  " + str(demand_)
    print "Optimised " + str(demand_optimised)
    if demand_optimised == expected_:
        print "Pass test 0: NOT meal appliance optimisation \n"
    else:
        print " Expected " + str(expected_)
        print "***** Fail ***** test 0: NOT meal appliance optimisation \n"


def test1():                # Meal appliance optimisation
    routine_ = [0, 2, 0, 1, 1, 0, 0]
    demand_ = [0, 5, 10, 0, 3, 0, 4]
    expected_ = [0, 0, 0, 0, 0, 0, 0]
    demand_optimised = eliminate(demand_)
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