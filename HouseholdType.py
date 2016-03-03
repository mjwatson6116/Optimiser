__author__ = 'Bat Cave'

import numpy as np
import sys


def householdtype(household_type_eval, household_type):   # finds range of options to be included
    if household_type_eval == "All":                      # all includes every option
        a = 0
        b = len(household_type)
    elif household_type_eval == "PP":                     # only includes the penny pincher option
        a = 0
        b = 1
    elif household_type_eval == "EW":                     # only includes the eco warrior option
        a = 1
        b = 2
    elif household_type_eval == "TE":                     # only includes the tech enthusiest option
        a = 2
        b = 3
    else:
        sys.exit("Household Type Error1: Please enter a valid household type (All, PP, EW or TE)")
    return a, b


def householdthreshold(xyz, household_type, optigoal):
    if household_type[xyz] == "PP":        # Penny Pincher
        money_thres = 8
        environ_thres = 3
    elif household_type[xyz] == "EW":      # Eco Warrior
        money_thres = 5
        environ_thres = 8
    elif household_type[xyz] == "TE":      # Tech Enthusiast
        money_thres = 3
        environ_thres = 3
    else:
        sys.exit("Household Threshold Error1: Please enter a valid household type")

    if optigoal == "Bill":
        return money_thres
    elif optigoal == "Enviro":
        return environ_thres
    else:
        sys.exit("Household Threshold Error2: Please enter valid optimisation goal")


def test0():
    count = 0
    household_threshold = (10, 10)
    opti_goal = "Enviro"                                                      # optimisation goal Bill or Enviro
    household_type_eval = "All"                                             # select from All, PP, EW or TE
    household_type = ["PP", "EW", "TE"]                                     # default options
    householdselect = householdtype(household_type_eval, household_type)    # returns range to be evaluated over
    for xyz in np.arange(householdselect[0], householdselect[1]):           # for all values between the returned range
        household_threshold = householdthreshold(xyz, household_type, opti_goal)    # return the threshold and then loop
        print "      Goal: " + str(opti_goal)
        print "      Type: " + str(household_type[xyz])
        print " Threshold: " + str(household_threshold)
        count += 1

    if household_type_eval == "All" and count == 3:
        print "Pass test 0"
    elif household_type_eval == "PP" and household_threshold == 8 and opti_goal == 0:
        print "Pass test 0"
    elif household_type_eval == "PP" and household_threshold == 3 and opti_goal == 1:
        print "Pass test 0"
    elif household_type_eval == "EW" and household_threshold == 3 and opti_goal == 0:
        print "Pass test 0"
    elif household_type_eval == "EW" and household_threshold == 8 and opti_goal == 1:
        print "Pass test 0"
    elif household_type_eval == "TE" and household_threshold[0] == 3:
        print "Pass test 0"
    else:
        print "*****Failed****** test 0"
    print "\n"

if __name__ == '__main__':
    # select tests to be ran
    tests = "All"
    testing = []
    if tests == "Mix":
        testing.append(0)  # test 0 (0 off/1 on)
    elif tests == "None":
        testing = [0 for w in range(0, 12)]
    elif tests == "All":
        testing = [1 for w in range(0, 12)]

    if testing[0] == 1:  #
        test0()