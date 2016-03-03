__author__ = 'Bat Cave'

import pandas as pd
import numpy as np
import ImportDataandAggregate as ida
import sys


def bill_eval(demand, bill_type, cost_number, mininterval, c_load, meter, test_):
    cost_ = []
    cap_ = []
    if bill_type == 3:
        bill_type = 2
    # main code
    if bill_type == 0:  # flat rate = fixed rate + connection fee
        csv_ = "Flat.csv"
        if c_load == 1:
            csv_ = "CFlat.csv"
        if c_load == 1 and test_ == 1:
            csv_ = "CFlatTest.csv"
        elif test_ == 1:
            csv_ = "FlatTest.csv"
        csv_path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data" + "\\" + str(csv_)
        costcsv = pd.read_csv(csv_path, names=["connect", "perkwh", "controlperkwh"])
        if test_ == 1:
            print(costcsv)
        cost_.append(costcsv.perkwh[cost_number])

    elif bill_type == 1:  # cap rate = tiered fee structure based on consumption + connection fee
        csv_ = "Cap.csv"
        if c_load == 1:
            csv_ = "CCap.csv"
        if c_load == 1 and test_ == 1:
            csv_ = "CCapTest.csv"
        elif test_ == 1:
            csv_ = "CapTest.csv"
        csv_path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data" + "\\" + str(csv_)
        costcsv = pd.read_csv(csv_path, names=["connect", "cap1", "cap2", "perkwh1", "perkwh2", "perkwh3",
                                               "controlperkwh"])
        if test_ == 1:
            print(costcsv)
        cost_.append(costcsv.perkwh1[cost_number])
        cost_.append(costcsv.perkwh2[cost_number])
        cost_.append(costcsv.perkwh3[cost_number])
        cap_.append(costcsv.cap1[cost_number])
        cap_.append(costcsv.cap2[cost_number])

    elif bill_type == 2 and meter > 0:              # Time of Use = variable rate + connection fee
        csv_ = "TimeOfUse.csv"
        if c_load == 1:
            csv_ = "CTimeOfUse.csv"
        if c_load == 1 and test_ == 1:
            csv_ = "CTimeOfUseTest.csv"
        elif test_ == 1:
            csv_ = "TimeOfUseTest.csv"
        csv_path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data" + "\\" + str(csv_)
        costcsv = pd.read_csv(csv_path, names=["connect", "perkwh1", "perkwh2", "perkwh3", "controlperkwh"])
        if test_ == 1:
            print(costcsv)
        week_cost = []
        for k in np.arange(0, 168):
            v = k
            while v > 23:
                v -= 24  # reduce hour to less then 24 hours
            if k / 24 < 5:  # less then five is assumed to be weekday (week start mindnight mon)
                if v < 7 or 22 <= v < 24:  # weekday off-peak hours
                    week_cost.append(costcsv.perkwh3[cost_number])
                elif 7 <= v < 14 or 20 <= v < 22:  # weekday shoulder periods
                    week_cost.append(costcsv.perkwh2[cost_number])
                elif 14 <= v < 20:  # weekday peak hours
                    week_cost.append(costcsv.perkwh1[cost_number])
                else:
                    sys.exit("Bill Eval Error1: Error aligning weekday ToU hours")

            elif 5 <= k / 24 < 7:  # greater then five is either sat or sun (week start mindnight mon)
                if v < 7 or 21 <= v < 24:  # weekend off-peak hours
                    week_cost.append(costcsv.perkwh3[cost_number])
                elif 7 <= v < 21:  # weekday shoulder periods
                    week_cost.append(costcsv.perkwh2[cost_number])
                else:
                    sys.exit("Bill Eval Error2: Error aligning weekend ToU hours")
        interval_cost = []
        splitter = 60.0/mininterval                                     # how many intervals in an hour
        if splitter > 1:                                                # if more then one interval per hour
            for k in np.arange(0, 168):                                 # loop through the hours in a billing week
                for w in np.arange(0, splitter):                        # for each interval in an hour
                    interval_cost.append(week_cost[k])                  # copy the hours rate to the interval
        elif splitter == 1:                                             # if the interval length is an hour
            for k in np.arange(0, 168):                                 # loop though the hours in a billing week
                interval_cost.append(week_cost[k])                      # copying all the billing hours to the new list
        elif 0 < splitter < 1:                                          # if there is less then one interval per hour
            splitter = 1/splitter                                       # loop though the hours in a billing week
            for k in np.arange(0, 168, splitter):                       # skipping hours at the interval rate
                interval_cost.append(np.mean(week_cost[k:k+splitter]))  # find the mean of the skipped hours and average

        for z in np.arange(0, len(demand)):                       # loop as many times as demand intervals
            count = z                                                   # copy current loop number
            if count > len(interval_cost) - 1:                          # if loop number greater then week of intervals
                while count > len(interval_cost) - 1:                   # continue to loop until less then a week
                    count -= len(interval_cost)                         # minusing a wekk of intervals each loop
            cost_.append(interval_cost[count])                   # once count < week copy interval cost to list
    elif bill_type == 2:
        sys.exit("Bill Eval Error3: Only electronic meters are capable of ToU billing")
    else:
        sys.exit("Bill Eval Error4: Please enter the correct bill type number Flat:0, Cap:1, ToU:2 or Ave:3")

    interval_ = 1440 / mininterval                              # calculate how many intervals are needed per day
    connectcost = np.divide(np.float64(costcsv.connect[cost_number]), np.int64(interval_))
    controlled = costcsv.controlperkwh[cost_number]
    return connectcost, cost_, cap_, controlled


def billing_calc(optimised_demand, opti_controlled_demand, bill_type, connection_fee, cost_, cap_, control_):
    billing = []
    if bill_type == 3:
        bill_type = 2
    # main code
    if bill_type == 0:                                                   # flat rate = fixed rate + connection fee
        for i in np.arange(0, len(optimised_demand)):
            billing.append(optimised_demand[i] * cost_[0] + opti_controlled_demand[i] * control_ + connection_fee)

    elif bill_type == 1:                        # cap rate = tiered fee structure based on consumption + connection fee
        opti_demand_sum = 0                                              # clear
        for i in np.arange(0, len(optimised_demand)):                    # loop once for each interval
            opti_demand_sum += optimised_demand[i]                       # sum the demand since start of billing period
            if opti_demand_sum < cap_[0]:                                # when sum is less then first cap
                billing.append(optimised_demand[i] * cost_[0] + opti_controlled_demand[i] * control_ + connection_fee)
                                                                         # apply kWh1 to interval
            elif opti_demand_sum < cap_[1] + cap_[0]:               # when sum is greater then cap 0 but less then cap 1
                if opti_demand_sum - optimised_demand[i] < cap_[0] < opti_demand_sum:
                                                                    # if the interval's demand spans over cap 0
                    gap = cap_[0] - (opti_demand_sum - optimised_demand[i])  # find how much is left in cap 0
                    billing.append(gap * cost_[0] + (optimised_demand[i] - gap) * cost_[1] +
                                   opti_controlled_demand[i] * control_ + connection_fee)
                                                  # charge remained rate 1 and everything else rate 2 + connection fee
                else:                             # if not on boarder whole interval charged rate 2
                    billing.append(optimised_demand[i] * cost_[1] + opti_controlled_demand[i] * control_
                                   + connection_fee)
            else:                                 # else sum of demand greater then cap 1
                if opti_demand_sum - optimised_demand[i] < cap_[1] + cap_[0] < opti_demand_sum:
                                                  # if the interval's demand spans over cap 1
                    gap = cap_[1] + cap_[0] - (opti_demand_sum - optimised_demand[i])  # find how much is left in cap 1
                    billing.append(gap * cost_[1] + (optimised_demand[i] - gap) * cost_[2] +
                                   opti_controlled_demand[i] * control_ + connection_fee)
                                                  # charge remained rate 2 and everything else rate 3 + connection fee
                else:                             # if not on boarder whole interval charged rate 2
                    billing.append(optimised_demand[i] * cost_[2] + opti_controlled_demand[i] * control_
                                   + connection_fee)

    elif bill_type == 2:                        # cap rate = tiered fee structure based on consumption + connection fee
        for i in np.arange(0, len(optimised_demand)):
            billing.append(optimised_demand[i] * cost_[i] + opti_controlled_demand[i] * control_ + connection_fee)

    else:
        sys.exit("Billing Calc Error1: Bill type exceeds range")

    billing = [a/100 for a in billing]                          # convert from cents to dollars

    return billing


def bill_selection(bill_select):
    if bill_select == "Flat":
        lower = 0
        upper = 1
    elif bill_select == "Cap":
        lower = 1
        upper = 2
    elif bill_select == "ToU":
        lower = 2
        upper = 3
    elif bill_select == "All":
        lower = 0
        upper = 3
    elif bill_select == "Ave":
        lower = 3
        upper = 4
    else:
        sys.exit("Bill Selection Error1: Please enter a valid bill type (Flat, Cap, ToU, All or Ave")

    return lower, upper


def costvariations(bill_type, controlled_load, testing_):
    if 0 <= bill_type < 4:
        if bill_type == 0:
            csv_name = "Flat"
        elif bill_type == 1:
            csv_name = "Cap"
        elif bill_type == 3:
            return 54, 55
        else:
            csv_name = "TimeOfUse"
        csv_ = str(csv_name) + ".csv"
        if controlled_load == 1:
            csv_ = "C" + str(csv_name) + ".csv"
        if testing_ == 1 and controlled_load == 1:
            csv_ = "C" + str(csv_name) + "Test.csv"
        elif testing_ == 1:
            csv_ = str(csv_name) + "Test.csv"
        csv_path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data" + "\\" + str(csv_)
        costcsv = pd.read_csv(csv_path, names=["connect"])
        upper = len(costcsv.connect)
        return 0, upper
    else:
        sys.exit("Cost Variations Error1: Bill type out of range")


def original_bill_cal(housedata, controlled_demand, controlledload, mininterval, current_bill_type, current_cost,
                      current_cap, current_connect, current_control):

    connect_per_interval = (float(current_connect)*mininterval)/(24*60)
    if current_bill_type == "ToU":
        week_cost = []
        for k in np.arange(0, 168):
            v = k
            while v > 23:
                v -= 24  # reduce hour to less then 24 hours
            if k / 24 < 5:  # less then five is assumed to be weekday (week start mindnight mon)
                if v < 7 or 22 <= v < 24:  # weekday off-peak hours
                    week_cost.append(current_cost[2])
                elif 7 <= v < 14 or 20 <= v < 22:  # weekday shoulder periods
                    week_cost.append(current_cost[1])
                elif 14 <= v < 20:  # weekday peak hours
                    week_cost.append(current_cost[0])
                else:
                    sys.exit("Bill Eval Error1: Error aligning weekday ToU hours")

            elif 5 <= k / 24 < 7:  # greater then five is either sat or sun (week start mindnight mon)
                if v < 7 or 21 <= v < 24:  # weekend off-peak hours
                    week_cost.append(current_cost[2])
                elif 7 <= v < 21:  # weekday shoulder periods
                    week_cost.append(current_cost[1])
                else:
                    sys.exit("Bill Eval Error2: Error aligning weekend ToU hours")
        interval_cost = []
        splitter = 60.0/mininterval                                     # how many intervals in an hour
        if splitter > 1:                                                # if more then one interval per hour
            for k in np.arange(0, 168):                                 # loop through the hours in a billing week
                for w in np.arange(0, splitter):                        # for each interval in an hour
                    interval_cost.append(week_cost[k])                  # copy the hours rate to the interval
        elif splitter == 1:                                             # if the interval length is an hour
            for k in np.arange(0, 168):                                 # loop though the hours in a billing week
                interval_cost.append(week_cost[k])                      # copying all the billing hours to the new list
        elif 0 < splitter < 1:                                          # if there is less then one interval per hour
            splitter = 1/splitter                                       # loop though the hours in a billing week
            for k in np.arange(0, 168, splitter):                       # skipping hours at the interval rate
                interval_cost.append(np.mean(week_cost[k:k+splitter]))  # find the mean of the skipped hours and average
        current_cost = []
        for z in np.arange(0, len(housedata[1])):                       # loop as many times as demand intervals
            count = z                                                   # copy current loop number
            if count > len(interval_cost) - 1:                          # if loop number greater then week of intervals
                while count > len(interval_cost) - 1:                   # continue to loop until less then a week
                    count -= len(interval_cost)                         # minusing a wekk of intervals each loop
            current_cost.append(interval_cost[count])                   # once count < week copy interval cost to list

    # ******** Flat ********
    if current_bill_type == "Flat" and controlledload == "Yes":
        return billing_calc(housedata[1], controlled_demand, 0, connect_per_interval, current_cost, 0, current_control)
    elif current_bill_type == "Flat":
        return billing_calc(housedata[1], controlled_demand, 0, connect_per_interval, current_cost, 0, 0)

    # ******** Cap ********
    elif current_bill_type == "Cap" and controlledload == "Yes":
        return billing_calc(housedata[1], controlled_demand, 1, connect_per_interval, current_cost, current_cap, current_control)
    elif current_bill_type == "Cap":
        return billing_calc(housedata[1], controlled_demand, 1, connect_per_interval, current_cost, current_cap, 0)

    # ******** Time Of Use ********
    elif current_bill_type == "ToU" and controlledload == "Yes":
        return billing_calc(housedata[1], controlled_demand, 2, connect_per_interval, current_cost, current_cap, current_control)
    elif current_bill_type == "ToU":
        return billing_calc(housedata[1], controlled_demand, 2, connect_per_interval, current_cost, current_cap, 0)

    else:
        sys.exit("Original Bill Error1: Please enter original bill type as Flat, Cap or ToU")


def test0():
    interval_ = 60               # how many minutes in a single interval
    csv_ = "50-house1-132-consumption.csv"
    csv_path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\h1_150120\h1" + "\\" + "141229_150104_50_h1" + "\\" + str(
        csv_)
    house_data = ida.aggregatedatacsv(csv_path, interval_)
    demand_ = house_data[1]
    test_ = 1
    billtype_ = 0
    costnumber_ = 0
    cload_ = 0
    meter = 1
    testresult_ = bill_eval(demand_, billtype_, costnumber_, interval_, cload_, meter, test_)
    expectedtestresult_ = (0.050000000000000003, [0.26], [], 0.0)
    if testresult_ == expectedtestresult_:
        print("Pass test 0: Flat rate billing rate test \n")
    else:
        print("***** FAIL ***** TEST 0: Flat rate billing rate test")
        print("         Cost number: " + str(costnumber_))
        print("  Actual test result: " + str(testresult_))
        print("Expected test result: " + str(expectedtestresult_) + "\n")


def test1():
    interval_ = 60               # how many minutes in a single interval
    csv_ = "50-house1-132-consumption.csv"
    csv_path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\h1_150120\h1" + "\\" + "141229_150104_50_h1" + "\\" + str(
        csv_)
    house_data = ida.aggregatedatacsv(csv_path, interval_)
    demand_ = house_data[1]
    test_ = 1
    billtype_ = 0
    costnumber_ = 2
    cload_ = 0
    meter = 1
    testresult_ = bill_eval(demand_, billtype_, costnumber_, interval_, cload_, meter, test_)
    expectedtestresult_ = (0.085416666666666669, [0.28], [], 0.0)
    if testresult_ == expectedtestresult_:
        print("Pass test 1: Flat rate billing test with rate shifting & non int per hour connect fee \n")
    else:
        print("***** FAIL ***** TEST 1: Flat rate billing test with rate shifting & non int per hour connect fee")
        print("         Cost number: " + str(costnumber_))
        print("  Actual test result: " + str(testresult_))
        print("Expected test result: " + str(expectedtestresult_) + "\n")


def test2():
    print "Bill type: Flat,  testing variations = " + str(costvariations(0, 0, 1))
    print "Bill type: CFlat, testing variations = " + str(costvariations(0, 1, 1))
    print "Bill type: Flat,     real variations = " + str(costvariations(0, 0, 0))
    print "Bill type: CFlat,    real variations = " + str(costvariations(0, 1, 0))
    print "Bill type: Cap,   testing variations = " + str(costvariations(1, 0, 1))
    print "Bill type: CCap,  testing variations = " + str(costvariations(1, 1, 1))
    print "Bill type: Cap,      real variations = " + str(costvariations(1, 0, 0))
    print "Bill type: CCap,     real variations = " + str(costvariations(1, 1, 0))
    print "Bill type: ToU,   testing variations = " + str(costvariations(2, 0, 1))
    print "Bill type: CToU,  testing variations = " + str(costvariations(2, 1, 1))
    print "Bill type: ToU,      real variations = " + str(costvariations(2, 0, 0))
    print "Bill type: CToU,     real variations = " + str(costvariations(2, 1, 0)) + "\n"


def test3(demand_, interval_):
    test_ = 1
    billtype_ = 1  # Test setting: 1
    costnumber_ = 2  # Test setting: 2
    cload_ = 0
    meter = 1
    testresult_ = bill_eval(demand_, billtype_, costnumber_, interval_, cload_, meter, test_)
    expectedtestresult_ = (0.032986250000000002, [0.231, 0.2409, 0.242], [1000000, 1000000], 0.0)
    if testresult_ == expectedtestresult_:
        print("Pass test 3: Cap rate billing test with rate shifting & non int per hour connect fee \n")
    else:
        print("***** FAIL ***** TEST 3: Cap rate billing test with rate shifting & non int per hour connect fee")
        print("         Cost number: " + str(costnumber_))
        print("  Actual test result: " + str(testresult_))
        print("Expected test result: " + str(expectedtestresult_) + "\n")


def test4(demand_, interval_):
    test_ = 1
    billtype_ = 2               # Test setting: 2
    costnumber_ = 1             # Test setting: 1
    cload_ = 0
    meter = 1
    testresult_ = bill_eval(demand_, billtype_, costnumber_, interval_, cload_, meter, test_)
    print(testresult_)
    shorttestresult_ = [testresult_[0], [testresult_[1][0], testresult_[1][79], testresult_[1][14],
                        testresult_[1][135]], testresult_[2]]
    expectedtestresult_ = [0.041666666666666664, [0.18, 0.25, 0.35, 0.25], []]
    if shorttestresult_ == expectedtestresult_:
        print("Pass test 4: ToU rate billing test with rate shifting and non int per hour connect fee \n")
    else:
        print("***** FAIL ***** TEST 4: ToU rate billing test with rate shifting & non int per hour connect fee")
        print("         Cost number: " + str(costnumber_))
        print("  Actual test result: " + str(testresult_))
        print(" Shorten test result: " + str(shorttestresult_))
        print("Expected test result: " + str(expectedtestresult_) + "\n")


def test5(interval_):
    test_ = 1
    billtype_ = 0
    costnumber_ = 0
    demand_ = [10, 20, 30, 40, 30]
    controlled_demand = [10, 20, 30, 40, 30]
    cload_ = 0
    meter = 1
    ratetestresult_ = bill_eval(demand_, billtype_, costnumber_, interval_, cload_, meter, test_)
    billtestresult_ = billing_calc(demand_, controlled_demand, billtype_, ratetestresult_[0], ratetestresult_[1],
                                   ratetestresult_[2], ratetestresult_[3])
    expectedtestresult_ = [0.026499999999999999, 0.052499999999999998, 0.0785, 0.10450000000000001, 0.0785]
    if billtestresult_ == expectedtestresult_:
        print("Actual billing result: " + str(billtestresult_))
        print("Pass test 5: Flat rate billing cost test \n")
    else:
        print("***** FAIL ***** TEST 5: Flat rate billing cost test")
        print("         Cost number: " + str(costnumber_))
        print("    Rate test result: " + str(ratetestresult_))
        print("  Actual test result: " + str(billtestresult_))
        print("Expected test result: " + str(expectedtestresult_) + "\n")


def test6(interval_):
    test_ = 1
    billtype_ = 0
    costnumber_ = 2
    cload_ = 0
    meter = 1
    demand_ = [10, 20, 30, 40, 30]
    controlled_demand = [10, 20, 30, 40, 30]
    ratetestresult_ = bill_eval(demand_, billtype_, costnumber_, interval_, cload_, meter, test_)
    billtestresult_ = billing_calc(demand_, controlled_demand, billtype_, ratetestresult_[0], ratetestresult_[1],
                                   ratetestresult_[2], ratetestresult_[3])
    expectedtestresult_ = [0.02885416666666667, 0.056854166666666671, 0.084854166666666675, 0.11285416666666669, 0.084854166666666675]
    if billtestresult_ == expectedtestresult_:
        print("Actual billing result: " + str(billtestresult_))
        print("Pass test 6: Flat rate billing cost test with varied cost number \n")
    else:
        print("***** FAIL ***** TEST 6: Flat rate billing cost test")
        print("         Cost number: " + str(costnumber_))
        print("    Rate test result: " + str(ratetestresult_))
        print("  Actual test result: " + str(billtestresult_))
        print("Expected test result: " + str(expectedtestresult_) + "\n")


def test7():
    min_interval = 15
    csv_directory = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house"
    csv_ = "consumption.csv"
    csv_path = str(csv_directory) + "\\" + str(csv_)
    housedata = ida.aggregatedatacsv(csv_path, min_interval)
    controlledload = "No"
    controlled_demand = [0 for i in np.arange(len(housedata[0]))]
    #current bill
    current_bill_type = "Flat"                   # input type of bill the household is currently on Flat, Cap or ToU
    current_cost = [28.76]           # how much is the household paying cents/kWh  (kWh1, kWh2, kWh3)
    current_cap = []                 # what are the intervals that the price increases at (cap1, cap2) (Watts)
    current_connect = 70                        # how much are the current per day connection fees (cents/day)
    current_control = 0                         # how much is the household paying cents/kWh on the controlled load

    connect_per_interval = (float(current_connect)*min_interval)/(24*60)
    if current_bill_type == "ToU":
        week_cost = []
        for k in np.arange(0, 168):
            v = k
            while v > 23:
                v -= 24  # reduce hour to less then 24 hours
            if k / 24 < 5:  # less then five is assumed to be weekday (week start mindnight mon)
                if v < 7 or 22 <= v < 24:  # weekday off-peak hours
                    week_cost.append(current_cost[2])
                elif 7 <= v < 14 or 20 <= v < 22:  # weekday shoulder periods
                    week_cost.append(current_cost[1])
                elif 14 <= v < 20:  # weekday peak hours
                    week_cost.append(current_cost[0])
                else:
                    sys.exit("Bill Eval Error1: Error aligning weekday ToU hours")

            elif 5 <= k / 24 < 7:  # greater then five is either sat or sun (week start mindnight mon)
                if v < 7 or 21 <= v < 24:  # weekend off-peak hours
                    week_cost.append(current_cost[2])
                elif 7 <= v < 21:  # weekday shoulder periods
                    week_cost.append(current_cost[1])
                else:
                    sys.exit("Bill Eval Error2: Error aligning weekend ToU hours")
        interval_cost = []
        splitter = 60.0/min_interval                                     # how many intervals in an hour
        if splitter > 1:                                                # if more then one interval per hour
            for k in np.arange(0, 168):                                 # loop through the hours in a billing week
                for w in np.arange(0, splitter):                        # for each interval in an hour
                    interval_cost.append(week_cost[k])                  # copy the hours rate to the interval
        elif splitter == 1:                                             # if the interval length is an hour
            for k in np.arange(0, 168):                                 # loop though the hours in a billing week
                interval_cost.append(week_cost[k])                      # copying all the billing hours to the new list
        elif 0 < splitter < 1:                                          # if there is less then one interval per hour
            splitter = 1/splitter                                       # loop though the hours in a billing week
            for k in np.arange(0, 168, splitter):                       # skipping hours at the interval rate
                interval_cost.append(np.mean(week_cost[k:k+splitter]))  # find the mean of the skipped hours and average
        current_cost = []
        for z in np.arange(0, len(housedata[1])):                       # loop as many times as demand intervals
            count = z                                                   # copy current loop number
            if count > len(interval_cost) - 1:                          # if loop number greater then week of intervals
                while count > len(interval_cost) - 1:                   # continue to loop until less then a week
                    count -= len(interval_cost)                         # minusing a wekk of intervals each loop
            current_cost.append(interval_cost[count])                   # once count < week copy interval cost to list

    # ******** Flat ********
    if current_bill_type == "Flat" and controlledload == "Yes":
        original_cost = billing_calc(housedata[1], controlled_demand, 0, connect_per_interval, current_cost, 0, current_control)
    elif current_bill_type == "Flat":
        original_cost = billing_calc(housedata[1], controlled_demand, 0, connect_per_interval, current_cost, 0, 0)

    # ******** Cap ********
    elif current_bill_type == "Cap" and controlledload == "Yes":
        original_cost = billing_calc(housedata[1], controlled_demand, 1, connect_per_interval, current_cost, current_cap, current_control)
    elif current_bill_type == "Cap":
        original_cost = billing_calc(housedata[1], controlled_demand, 1, connect_per_interval, current_cost, current_cap, 0)

    # ******** Time Of Use ********
    elif current_bill_type == "ToU" and controlledload == "Yes":
        original_cost = billing_calc(housedata[1], controlled_demand, 2, connect_per_interval, current_cost, current_cap, current_control)
    elif current_bill_type == "ToU":
        original_cost = billing_calc(housedata[1], controlled_demand, 2, connect_per_interval, current_cost, current_cap, 0)

    else:
        sys.exit("Original Bill Error1: Please enter original bill type as Flat, Cap or ToU")

    print(current_cost)
    print(np.sum(housedata[1]))
    print(housedata[1])
    print(original_cost)
    print(np.mean(original_cost))
    print(np.sum(original_cost))
    print "Pass test 7: Original demand cost calculator \n Expected result 10.4815802838 \n"


def test8():
    # settings
    optigoal = "Bill"                           # what is the goal of the optimsiation (Bill or Enviro)
    controlledload = "No"                       # if there is a controlled load set to Yes
    mininterval = 30                            # interval duation in minutes
    csv_directory = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house2"     # where the data is stored

    #current bill
    current_bill_type = "Cap"                   # input type of bill the household is currently on Flat, Cap or ToU
    current_cost = [24.62, 25.85, 27.35]        # how much is the household paying cents/kWh  [Peak, Shoulder, Off-peak]
    current_cap = [1063, 1063]                  # what are the intervals that the price increases at [cap1, cap2] (Watts)
    current_connect = 69.77                     # how much are the current per day connection fees (cents/day)
    current_control = 0                         # how much is the household paying cents/kWh on the controlled load
    print "Importing house level data...."
    # import house level data and aggregate
    csv_ = "consumption.csv"
    csvpath_ = str(csv_directory) + "\\" + str(csv_)
    house_data = ida.aggregatedatacsv(csvpath_, mininterval)

    controlled_demand = []                                           # included if controlled circuit/demand evaluated
    if controlledload == "No":                                       # if no controlled load create empty matrix
        controlled_demand = [0 for zero in range(0, len(house_data[1]))]   # zero value matrix for controlled demand

    print "Calculating original bill...."
    if optigoal == "Bill":
        original_bill = original_bill_cal(Housedata, controlled_demand, controlledload, mininterval, current_bill_type,
                                          current_cost, current_cap, current_connect, current_control)
    print(house_data[1])
    print(original_bill)


def test9(interval_):  # Time of use rate billing cost test with varied cost number (24 hours)
    test_ = 1
    billtype_ = 2
    costnumber_ = 2
    cload_ = 0
    meter = 1
    demand_ = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    controldemand_ = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    ratetestresult_ = bill_eval(demand_, billtype_, costnumber_, interval_, cload_, meter, test_)
    billtestresult_ = billing_calc(demand_, controldemand_, billtype_, ratetestresult_[0], ratetestresult_[1],
                                   ratetestresult_[2], ratetestresult_[3])
    shorttestresult_ = [billtestresult_[0], billtestresult_[7], billtestresult_[19], billtestresult_[20]]
    expectedtestresult_ = [0.015625, 0.018624999999999999, 0.073624999999999996, 0.018624999999999999]
    if shorttestresult_ == expectedtestresult_:
        print("Pass test 9: Time of use rate billing cost test with varied cost number \n")
    else:
        print("***** FAIL ***** TEST 9: Time of use rate billing cost test with varied cost number")
        print("         Cost number: " + str(costnumber_))
        print("  Actual test result: " + str(ratetestresult_))
        print(" Shorten test result: " + str(shorttestresult_))
        print("Expected test result: " + str(expectedtestresult_) + "\n")


def test10(demand_, interval_):
    # real deployment loop
    test = 1
    loopcount = 0
    cload_ = 0
    meter = 1
    controlled_demand = [0 for zero in range(0, len(demand_))]
    for bill_type in np.arange(0, 3):                       # test setting (0, 3)
        for cost_number in np.arange(0, 4):                 # test setting (0, 4)
            billing_info = bill_eval(demand_, bill_type, cost_number, interval_, cload_, meter, test)
            connectionfee = billing_info[0]
            cost = billing_info[1]
            cap = billing_info[2]
            control = billing_info[3]
            print "Bill type = " + str(bill_type) + " Cost number = " + str(cost_number)
            print(billing_calc(demand, controlled_demand, bill_type, connectionfee, cost, cap, control))
            loopcount += 1
    if loopcount == 12:
        print("Pass test 10 \n")
    else:
        print "****Fail***** test 10: Loop count = " + str(loopcount) + "\n"


def test11(demand_, interval_):
    # real deployment loop
    test = 1
    loopcount = 0
    cload_ = 0
    meter = 1
    controlled_load = 0                                                   # controlled load not part of billing eval
    billinput = "All"
    controlled_demand = [0 for zero in range(0, len(demand_))]            # zero value matrix for controlled demand
    billselect = bill_selection(billinput)                                # only include selected bill types
    for bill_type in np.arange(billselect[0], billselect[1]):             # iterate through selected bill types
        cost_vari = costvariations(bill_type, controlled_load, test)      # find how many costs for bill type
        for cost_number in np.arange(cost_vari[0], cost_vari[1]):         # iterate through costs for bill type
            billing_info = bill_eval(demand_, bill_type, cost_number, interval_, cload_, meter, test)
                                                                          # return  single cost info
            connectionfee = billing_info[0]                               # seperate connection fee
            cost = billing_info[1]                                        # seperate cost per hour values
            cap = billing_info[2]                                         # seperate cap values
            control = billing_info[3]                                     # seperate controlled load costs
            print "Bill: " + str(bill_type) + " Cost number: " + str(cost_number)

            # include optimisation loop here

            print(billing_calc(demand, controlled_demand, bill_type, connectionfee, cost, cap, control))
                                                                          # apply costs to optimised demand
            loopcount += 1

    if billinput == "Flat" and loopcount == 4:
        print("Pass test 11")
    elif billinput == "Split" and loopcount == 4:
        print("Pass test 11")
    elif billinput == "ToU" and loopcount == 4:
        print("Pass test 11")
    elif billinput == "All" and loopcount == 12:
        print("Pass test 11")
    else:
        print "*****Failed***** test 11: Bill select = " + str(billselect) + " Loopcount = " + str(loopcount)
    print("\n")


if __name__ == '__main__':
    # import data and aggregate
    interval = 60               # how many minutes in a single interval
    csv = "50-house1-132-consumption.csv"
    csvpath = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\h1_150120\h1" + "\\" + "141229_150104_50_h1" + "\\" + str(
        csv)
    Housedata = ida.aggregatedatacsv(csvpath, interval)
    demand = Housedata[1]
    costnumber = 0
    controlledcircuit = 0
    if controlledcircuit == 0:
        controlleddemand = testing = [0 for w in range(0, len(demand))]

    # select tests to be ran
    tests = "Mix"
    testing = []
    if tests == "Mix":
        testing.append(0)  # test 0 (0 off/1 on) Flat rate billing rate test
        testing.append(0)  # test 1 (0 off/1 on) Flat rate billing test with rate shifting & non int per hour connect
        testing.append(1)  # test 2 (0 off/1 on) Cost variations test
        testing.append(0)  # test 3 (0 off/1 on) Cap rate billing test with rate shifting & non int per hour connect
        testing.append(0)  # test 4 (0 off/1 on) Time of use rate billing test with rate shifting
        testing.append(0)  # test 5 (0 off/1 on) Flat rate billing cost test (demand*rate/hr)
        testing.append(0)  # test 6 (0 off/1 on) Flat rate billing cost test (demand*rate/hr) with varied cost number
        testing.append(0)  # test 7 (0 off/1 on) Billing debug: Calculating flat original bill
        testing.append(0)  # test 8 (0 off/1 on) Billing debug: Calculating cap original bill
        testing.append(0)  # test 9 (0 off/1 on) Time of use rate billing cost test (demand*rate/hr) varied cost number
        testing.append(0)  # test 10 (0 off/1 on) Cycling through all test
        testing.append(0)  # test 11 (0 off/1 on) Deployment code test
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
        test3(demand, interval)
    if testing[4] > 0:
        test4(demand, interval)
    if testing[5] > 0:
        test5(interval)
    if testing[6] > 0:
        test6(interval)
    if testing[7] > 0:
        test7()
    if testing[8] > 0:
        test8()
    if testing[9] > 0:
        test9(interval)
    if testing[10] > 0:
        test10(demand, interval)
    if testing[11] > 0:
        test11(demand, interval)