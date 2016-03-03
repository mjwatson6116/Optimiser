__author__ = 'Bat Cave'

import numpy as np
import sys


def shifter(demand, routine, mealappliance, devicetype, mininterval, shifttime, cost, test):
    shiftrange = np.int64(np.floor(np.divide(np.float64(shifttime), np.float64(mininterval))))
                                                        # convert max shift time into max intervals (rounding down)
    intervalcount = len(demand)
    demandoptimise = [0 for i in range(intervalcount)]  # write zeros for every potential hour
    skipinterval = []
    shift_place = []
    if devicetype != "Duration" and devicetype != "Cycle":
        sys.exit("Please enter a valid usage type")

    for z in np.arange(0, intervalcount):
        cyclecount = 0                              # reset the count of how many hours the use went for
        if demand[z] > 0:                           # if demand is greater then zero check how many hours it runs for
            for w in np.arange(z, intervalcount):   # from next hour until the end (inclusive of last hour)
                if demand[w] > 0:                   # if next hour is greater then zero add one more to count
                    cyclecount += 1
                else:                               # if next hour is zero then the device usage stopped
                    break
        if z not in skipinterval and cyclecount > 0:                # skip intervals that have already been optimised
            if mealappliance == 1 and routine[z] == 1:    # if no body is home OR meal appliance
                for e in np.arange(0, cyclecount):                  # for all intervals that cycle runs over
                    demandoptimise[z + e] = demand[z + e]           # do not optimse demand
                    skipinterval.append(z + e)     # add intervals to list of intervals to skip in further evaluations
            else:
                mincostindex = []                       # established array
                mincost = []                            # established array
                maxshift = min(intervalcount, z + shiftrange + cyclecount)-(z + cyclecount)
                                                        # limit shifting to within range being optimised
                for k in np.arange(0, maxshift+1):      # cycle through possible shifting amounts from 0 to max
                    if k == 0:                          # when the demand is not shifted at all
                        minusz = 1
                    elif cyclecount <= k:               # when duration of use is less then or equal to shifting amount
                        minusz = cyclecount
                    else:                               # when duration of use is greater then shifting amount
                        minusz = k

                    maxz = z + cyclecount + k           # last z value of the whole cylce/ usage after shifting
                    minz = maxz - minusz                # last z value not already part of un-shifted cycle

                    routinepass = 0                             # clear routine pass
                    if (devicetype == "Cycle" and z + k > intervalcount) or \
                            (devicetype == "Duration" and z + k + cyclecount > intervalcount):
                        routinepass = 0
                    elif devicetype == "Cycle" and routine[z+k] > 0:   # if cycle type and someone is home at shift time
                        routinepass = 1                         # allow the cycle to be included
                    elif devicetype == "Duration" and routine[z+k] > 0 and routine[z+k+cyclecount-1] > 0:
                                         # if it is a duration type and someone is home at shift start time & end time
                        routinepass = 1                         # allow the duration to be included

                    if (sum(demand[minz:maxz]) == 0 and routinepass == 1) or k == 0:
                    # if no demand during shift period and some is home at shifting time or adding current position
                        shiftsum = 0                            # zero the sum of demand * cost
                        for abc in np.arange(0, cyclecount):    # for all the hours that the cycle runs over
                            shiftsum = shiftsum + demand[z + abc]*cost[z + k + abc]  # sum the demand * cost
                        mincost.append(shiftsum)                # add the sum to a list
                        mincostindex.append(k)                  # record the shifting amount for each sum

                shiftamount = mincostindex[mincost.index(min(mincost))]  # find shift time when cheapest cycle cost
                if shiftamount > 0:
                    shift_place.append([z, shiftamount])

                for e in np.arange(0, cyclecount):                  # for all intervals that cycle runs over
                    demandoptimise[z + e + shiftamount] = demand[z + e]     # shift demand to optimised time
                    skipinterval.append(z + e)              # add optimised intervals to list of intervals to be skipped

    #     print "\nShift range: " + str(shiftrange)
    #     print "Cost      " + str(cost) + " Length = " + str(len(cost))
    #     print "Routine   " + str(routine) + " Length = " + str(len(routine))
    #     print "Original  " + str(demand) + " Length = " + str(len(demand))
    #     print "Optimised " + str(demandoptimise) + " Length = " + str(len(demandoptimise))
    if test == 2:
        print "Shift place : (" + str(len(shift_place)) + ") " + str(shift_place)
    return demandoptimise


if __name__ == '__main__':
    # select tests to be ran
    tests = "All"
    testing = []
    if tests == "Mix":
        testing.append(0)   # test 0 (0 off/1 on)
        testing.append(1)   # test 1 (0 off/1 on)
        testing.append(0)   # test 2 (0 off/1 on)
        testing.append(0)   # test 3 (0 off/1 on)
        testing.append(0)   # test 4 (0 off/1 on)
        testing.append(0)   # test 5 (0 off/1 on)
        testing.append(0)   # test 6 (0 off/1 on)
        testing.append(0)   # test 7 (0 off/1 on)
    elif tests == "None":
        testing = [0 for i in range(0, 8)]
    elif tests == "All":
        testing = [1 for i in range(0, 8)]

    # test 1 inputs SHIFTING SINGLE HOUR TEST
    shifting = 1            # 0 = shifting off, 1 = shifting on
    shift_time = 2          # maximum time device is able to be shifted. Must be greater then 0 if shifting on
    min_interval = 1
    meal_appliance = 0      # 0 = not used in meal preperations, 1 = used in meal preperations
    usage_type = "Cycle"          # Cycle or Duration
    cost_ = [30, 30, 30, 20, 15, 15, 15, 15]
    routine_ = [1, 1, 2, 1, 1, 2, 1, 1]
    demand_ = [0, 10, 0, 0, 5, 5, 5, 0]
    testresult = [0, 0, 0, 10, 5, 5, 5, 0]

    if shifting == 1 and testing[1] == 1:
        hourdemand_opti = shifter(demand_, routine_, meal_appliance, usage_type, min_interval, shift_time, cost_, 0)
        if hourdemand_opti == testresult:
            print "Pass Test 1: SHIFTING SINGLE HOUR TEST"
        else:
            print "Original  " + str(demand_) + " Length = " + str(len(demand_))
            print "  Actual  " + str(hourdemand_opti) + " Length = " + str(len(hourdemand_opti))
            print "Expected  " + str(testresult) + " Length = " + str(len(testresult))
            print "** Fail ** Test 1: SHIFTING SINGLE HOUR TEST"

    # test 2 inputs SHIFTING WHOLE CYCLE TEST
    shifting = 1            # 0 = shifting off, 1 = shifting on
    meal_appliance = 0      # 0 = not used in meal preperations, 1 = used in meal preperations
    usage_type = "Cycle"          # Cycle or Duration
    cost_ = [30, 20, 20, 20, 20, 20, 15, 15]
    routine_ = [1, 1, 2, 1, 1, 2, 1, 1]
    demand_ = [0, 10, 0, 0, 5, 5, 0, 0]
    testresult = [0, 10, 0, 0, 0, 0, 5, 5]

    if shifting == 1 and testing[2] == 1:
        hourdemand_opti = shifter(demand_, routine_, meal_appliance, usage_type, min_interval, shift_time, cost_, 0)
        if hourdemand_opti == testresult:
            print "Pass Test 2: SHIFTING WHOLE CYCLE TEST"
        else:
            print "Original  " + str(demand_) + " Length = " + str(len(demand_))
            print "  Actual  " + str(hourdemand_opti) + " Length = " + str(len(hourdemand_opti))
            print "Expected  " + str(testresult) + " Length = " + str(len(testresult))
            print "** Fail ** Test 2: SHIFTING WHOLE CYCLE TEST"

    # test 3 inputs MEAL APPLIANCE TEST
    shifting = 1            # 0 = shifting off, 1 = shifting on
    meal_appliance = 1      # 0 = not used in meal preperations, 1 = used in meal preperations
    usage_type = "Cycle"          # Cycle or Duration
    cost_ = [30, 20, 15, 15, 20, 20, 15, 15]
    routine_ = [1, 1, 2, 1, 2, 2, 1, 1]
    demand_ = [0, 10, 0, 0, 5, 5, 0, 0]
    testresult = [0, 10, 0, 0, 0, 0, 5, 5]

    if shifting == 1 and testing[3] == 1:
        hourdemand_opti = shifter(demand_, routine_, meal_appliance, usage_type, min_interval, shift_time, cost_, 0)
        if hourdemand_opti == testresult:
            print "Pass Test 3: MEAL APPLIANCE TEST"
        else:
            print "Original  " + str(demand_) + " Length = " + str(len(demand_))
            print "  Actual  " + str(hourdemand_opti) + " Length = " + str(len(hourdemand_opti))
            print "Expected  " + str(testresult) + " Length = " + str(len(testresult))
            print "** Fail ** Test 3: MEAL APPLIANCE TEST"

    # test 4 inputs NO SHIFT ROUTINE TEST
    shifting = 1            # 0 = shifting off, 1 = shifting on
    shift_time = 3         # maximum hours device is able to be shifted. Must be greater then 0 if shifting on
    meal_appliance = 0      # 0 = not used in meal preperations, 1 = used in meal preperations
    usage_type = "Cycle"          # Cycle or Duration
    cost_ = [30, 20, 20, 15, 15, 15, 15, 15]
    routine_ = [0, 0, 0, 0, 0, 0, 0, 0]
    demand_ = [0, 10, 15, 5, 0, 0, 0, 0]
    testresult = [0, 10, 15, 5, 0, 0, 0, 0]

    if shifting == 1 and testing[4] == 1:
        hourdemand_opti = shifter(demand_, routine_, meal_appliance, usage_type, min_interval, shift_time, cost_, 0)
        if hourdemand_opti == testresult:
            print "Pass Test 4: NO SHIFT ROUTINE TEST"
        else:
            print "Original  " + str(demand_) + " Length = " + str(len(demand_))
            print "  Actual  " + str(hourdemand_opti) + " Length = " + str(len(hourdemand_opti))
            print "Expected  " + str(testresult) + " Length = " + str(len(testresult))
            print "** Fail ** Test 4: NO SHIFT ROUTINE TEST"

    # test 5 inputs CYCLE SHIFT ROUTINE TEST
    shifting = 1            # 0 = shifting off, 1 = shifting on
    shift_time = 3         # maximum hours device is able to be shifted. Must be greater then 0 if shifting on
    meal_appliance = 0      # 0 = not used in meal preperations, 1 = used in meal preperations
    usage_type = "Cycle"          # Cycle or Duration
    cost_ = [30, 20, 15, 15, 15, 15, 15, 15]
    routine_ = [2, 2, 0, 0, 1, 0, 1, 1]
    demand_ = [0, 10, 10, 10, 0, 0, 0, 0]
    testresult = [0, 0, 0, 0, 10, 10, 10, 0]

    if shifting == 1 and testing[5] == 1:
        hourdemand_opti = shifter(demand_, routine_, meal_appliance, usage_type, min_interval, shift_time, cost_, 0)
        if hourdemand_opti == testresult:
            print "Pass Test 5: CYCLE SHIFT ROUTINE TEST"
        else:
            print "Original  " + str(demand_) + " Length = " + str(len(demand_))
            print "  Actual  " + str(hourdemand_opti) + " Length = " + str(len(hourdemand_opti))
            print "Expected  " + str(testresult) + " Length = " + str(len(testresult))
            print "** Fail ** Test 5: CYCLE SHIFT ROUTINE TEST"

    # test 6 inputs DURATION CYCLE TYPE TEST
    shifting = 1            # 0 = shifting off, 1 = shifting on
    shift_time = 3         # maximum hours device is able to be shifted. Must be greater then 0 if shifting on
    meal_appliance = 1      # 0 = not used in meal preperations, 1 = used in meal preperations
    usage_type = "Duration"          # Cycle or Duration
    cost_ = [30, 20, 20, 15, 15, 15, 15, 15]
    routine_ = [2, 2, 2, 0, 1, 0, 1, 1]
    demand_ = [0, 10, 10, 10, 0, 0, 0, 0]
    testresult = [0, 0, 0, 0, 10, 10, 10, 0]

    if shifting == 1 and testing[6] == 1:
        hourdemand_opti = shifter(demand_, routine_, meal_appliance, usage_type, min_interval, shift_time, cost_, 0)
        if hourdemand_opti == testresult:
            print "Pass Test 6: DURATION CYCLE TYPE TEST"
        else:
            print "Original  " + str(demand_) + " Length = " + str(len(demand_))
            print "  Actual  " + str(hourdemand_opti) + " Length = " + str(len(hourdemand_opti))
            print "Expected  " + str(testresult) + " Length = " + str(len(testresult))
            print "** Fail ** Test 6: DURATION CYCLE TYPE TEST"

    # test 7 inputs SHIFT OVER FINISH
    shifting = 1            # 0 = shifting off, 1 = shifting on
    shift_time = 5         # maximum hours device is able to be shifted. Must be greater then 0 if shifting on
    meal_appliance = 0      # 0 = not used in meal preperations, 1 = used in meal preperations
    usage_type = "Duration"          # Cycle or Duration
    cost_ = [30, 20, 15, 15, 15, 15, 10, 10]
    routine_ = [2, 2, 2, 0, 1, 1, 1, 1]
    demand_ = [0, 0, 10, 10, 10, 0, 0, 0]
    testresult = [0, 0, 0, 0, 0, 10, 10, 10]

    if shifting == 1 and testing[7] == 1:
        hourdemand_opti = shifter(demand_, routine_, meal_appliance, usage_type, min_interval, shift_time, cost_, 0)
        if hourdemand_opti == testresult:
            print "Pass Test 7: SHIFT OVER FINISH"
        else:
            print "Original  " + str(demand_) + " Length = " + str(len(demand_))
            print "  Actual  " + str(hourdemand_opti) + " Length = " + str(len(hourdemand_opti))
            print "Expected  " + str(testresult) + " Length = " + str(len(testresult))
            print "** Fail ** Test 7: SHIFT OVER FINISH"