__author__ = 'Bat Cave'

import numpy as np
import matplotlib.pyplot as plt
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be
import Eliminate as el
import Substitute as sb
import Minimise as mn
import Shifting as sh


def airconditioner(device_demand, routine, mininterval, cost, hh_threshold, shifting, test):
    # general air-conditioner inputs
    devicetype = "Duration"                     # "Duration" if occupant needed at start and end otherwise "Cycle"
    mealappliance = 0                           # 0 if device not used in meal prep/ 1 if device is used in prep

    # inputs especially for air-conditioner optimsiation using elimination:
    elim_thres = 10                             # how much effort it takes to eliminate device usage

    # inputs especially for air-conditioner optimsiation using minimisation 1:
    mini1_thres = 9                             # how much effort it takes to minimise device usage
    mini1_saving = 40                           # if type duration, what percentage will be saved (0 nothing - 100)
    mini1_cyclemax = 9999                       # if type cycle, what is the maximum amount of cycles...
    mini1_time = 99999                          # if type cycle, ...within a given time frame
    # inputs especially for air-conditioner optimsiation using minimisation 2:
    mini2_thres = 8                             # how much effort it takes to minimise device usage
    mini2_saving = 20                           # if type duration, what percentage will be saved (0 nothing - 100)
    mini2_cyclemax = 9999                       # if type cycle, what is the maximum amount of cycles...
    mini2_time = 99999                          # if type cycle, ...within a given time frame
    # inputs especially for air-conditioner optimsiation using minimisation 3:
    mini3_thres = 7                             # how much effort it takes to minimise device usage
    mini3_saving = 10                           # if type duration, what percentage will be saved (0 nothing - 100)
    mini3_cyclemax = 9999                       # if type cycle, what is the maximum amount of cycles...
    mini3_time = 99999                          # if type cycle, ...within a given time frame

    # inputs especially for air-conditioner optimsiation using shifting 1:
    shift1_thres = 9                            # how much effort it takes to shift device usage
    shift1_time = 60                            # how long can the use of the device be shifted
    # inputs especially for air-conditioner optimsiation using shifting 2:
    shift2_thres = 8                            # how much effort it takes to shift device usage
    shift2_time = 30                            # how long can the use of the device be shifted

    # inputs especially for air-conditioner optimsiation using substitution:
    sub1_thres = 8                              # how much effort it takes to substitue the device usage
    sub1_type = "Duration"                      # what device type is the substitue. "Duration" or "Cycle"
    sub1_time = 1000                            # if subtype cycle, how much time the sub takes to complete a cycle
    sub1_demand = 100000                        # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    sub1_saving = 30                            # if subtype duration, what percentage of electricity does it
                                                # save relative to current device (0 saves nothing - 100)
    # inputs especially for air-conditioner optimsiation using substitution:
    sub2_thres = 7                             # how much effort it takes to substitue the device usage
    sub2_type = "Duration"                      # what device type is the substitue. "Duration" or "Cycle"
    sub2_time = 1000                            # if subtype cycle, how much time the sub takes to complete a cycle
    sub2_demand = 10000                         # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    sub2_saving = 20                             # if subtype duration, what percentage of electricity does it
                                                # save relative to current device (0 saves nothing - 100)
        # inputs especially for air-conditioner optimsiation using substitution:
    sub3_thres = 6                             # how much effort it takes to substitue the device usage
    sub3_type = "Duration"                      # what device type is the substitue. "Duration" or "Cycle"
    sub3_time = 1000                            # if subtype cycle, how much time the sub takes to complete a cycle
    sub3_demand = 10000                         # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    sub3_saving = 10                             # if subtype duration, what percentage of electricity does it
                                                # save relative to current device (0 saves nothing - 100)

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
        optimised_demand = el.eliminate(device_demand)
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
                                       mini1_saving, mini1_cyclemax, mini1_time, test)  # return optimised device usage
    # ****** Minimisation 2 ******
    elif hh_threshold >= mini2_thres:          # apply minimisation optimisations if effort threshold >= mini threshold
        optimised_demand = mn.minimise(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                       mini2_saving, mini2_cyclemax, mini2_time, test)  # return optimised device usage
    # ****** Minimisation 3 ******
    elif hh_threshold >= mini3_thres:          # apply minimisation optimisations if effort threshold >= mini threshold
        optimised_demand = mn.minimise(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                       mini3_saving, mini3_cyclemax, mini3_time, test)  # return optimised device usage
    else:                                      # if effort threshold lower then value
        optimised_demand = optimised_demand    # device usage is not optimised

    if test == 1 and hh_threshold >= mini1_thres:
        print " Opti Mini1 Demand: (" + str(mini1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1 and hh_threshold >= mini2_thres:
        print " Opti Mini2 Demand: (" + str(mini2_thres) + ") (" + str(len(optimised_demand)) + ")" + str(optimised_demand)
    elif test == 1 and hh_threshold >= mini3_thres:
        print " Opti Mini3 Demand: (" + str(mini3_thres) + ") (" + str(len(optimised_demand)) + ")" + str(optimised_demand)
    elif test == 1:
        print " Opti MiniP Demand: (" + str(mini2_thres) + ") (" + str(len(optimised_demand)) + ")" + str(optimised_demand)

    # ****** Shifting 1 ******
    if hh_threshold >= shift1_thres and shifting == 1:
                                        # apply shifting optimisation if shifting on & threshold >= shift thres
        optimised_demand = sh.shifter(optimised_demand, routine, mealappliance, devicetype, mininterval, shift1_time,
                                      cost, test)                     # return optimised device usage
    # ****** Shifting 2 ******
    elif hh_threshold >= shift2_thres and shifting == 1:
                                        # apply shifting optimisation if shifting on & threshold >= shift thres
        optimised_demand = sh.shifter(optimised_demand, routine, mealappliance, devicetype, mininterval, shift2_time,
                                      cost, test)                     # return optimised device usage
    else:                                                       # if effort theshold low then value or shifting is off
        optimised_demand = optimised_demand                     # device usage is not optimsied

    if test == 1 and hh_threshold >= shift1_thres:
        print " Opti Shif1 Demand: (" + str(shift1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1 and hh_threshold >= shift2_thres:
        print " Opti Shif2 Demand: (" + str(shift2_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1:
        print " Opti ShifP Demand: (" + str(shift2_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)

    # ****** Substitution ******
    if hh_threshold >= sub1_thres:          # apply substituation optimisations if effort threshold >= sub threshold
        optimised_demand = sb.substitute(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                         sub1_type, sub1_time, sub1_demand, sub1_saving, 0, test)  # return optimised usage
    elif hh_threshold >= sub2_thres:          # apply substituation optimisations if effort threshold >= sub threshold
        optimised_demand = sb.substitute(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                         sub2_type, sub2_time, sub2_demand, sub2_saving, 0, test)  # return optimised usage
    elif hh_threshold >= sub3_thres:          # apply substituation optimisations if effort threshold >= sub threshold
        optimised_demand = sb.substitute(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                         sub3_type, sub3_time, sub3_demand, sub3_saving, 0, test)  # return optimised usage
    else:                                      # if effort threshold lower then value
        optimised_demand = optimised_demand            # device usage is not optimised

    if test == 1 and hh_threshold >= sub1_thres:
        print " Opti Subs1 Demand: (" + str(sub1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "
    elif test == 1 and hh_threshold >= sub2_thres:
        print " Opti Subs2 Demand: (" + str(sub2_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "
    elif test == 1 and hh_threshold >= sub3_thres:
        print " Opti Subs2 Demand: (" + str(sub3_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "
    elif test == 1:
        print " Opti SubsP Demand: (" + str(sub3_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "

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
    appliancedemand = ida.deviceimport(housedata, min_interval, csv_directory, "Yes", "No", "No", "No", "No", "No",
                                       "No", "No", "No", "No", "No", "No", "No", "No")
    device_demand = appliancedemand[0][0]
    variation = airconditioner(device_demand, routine_, min_interval, cost_, threshold, shifting_, testing_)
    print "        Variation: " + str(variation)
    if variation == expected_:
        print "Pass test 0: Testing device optimisation using minimisation\n"
    else:
        print "         Expected: " + str(expected_)
        print "***** Fail ***** test 0: Testing device optimisation using minimisation\n"


def test1():
    optigoal = "Bill"
    dataid = 4922
    meter = 1
    shifting_ = 1
    csvpath = "C:\Users\Bat Cave\Dropbox\My Files\Uni Work\Capstone\PeaconStreet\dataid_" + str(dataid) + "_localdate_07012013_AND_09302013.csv"
    min_interval = 15
    df = ida.peacon_street(csvpath, min_interval)
    houselevel_data = []
    for row in df[1][0]:
        houselevel_data.append(row)
    houselevel_cum_sum = np.cumsum(houselevel_data)
    plt.plot(houselevel_cum_sum, label='Unoptimised Household Demand')
    print "Total house level consumption = " + str(np.around(houselevel_cum_sum[-1], 2)) + " kWh"
    c_load = [0 for zero in range(0, len(houselevel_data))]   # zero value matrix for controlled demand
    occupants = [2, 0, 0, 0, 0, 0]
    routine_ = rb.routine_builder(houselevel_data, min_interval, occupants)
    bill_type = 2
    cost_number = 54
    billing_info = be.bill_eval(houselevel_data, bill_type, cost_number, min_interval, c_load, meter, 0)
    house_cost = be.billing_calc(houselevel_data, c_load, bill_type, billing_info[0], billing_info[1], billing_info[2], billing_info[3])
    print "Costing a total of $ " + str(np.around(sum(house_cost), 2))
    device_data = []
    for row in df[1][1]:
        device_data.append(row)
    skiplist = []
    count = 0
    for x in np.arange(0, len(device_data)):
        if not x in skiplist:
            if device_data[x] > 0:
                count += 1
                for z in np.arange(x, len(device_data)):
                    skiplist.append(z)
                    if device_data[z] == 0:
                        break
    original_cum_sum = np.cumsum(device_data)
    plt.plot(original_cum_sum, label='Unoptimised Device Demand')
    device_per = np.around(np.divide(original_cum_sum[-1], houselevel_cum_sum[-1])*100, 2)
    device_cost = be.billing_calc(device_data, c_load, bill_type, 0, billing_info[1], billing_info[2], billing_info[3])
    print "Device accounts for " + str(device_per) + "% of household consumption"
    print "A total of " + str(np.around(original_cum_sum[-1], 2)) + " kWh"
    print "The device costings a total of $ " + str(np.around(sum(device_cost), 2))
    print "Occuring in " + str(count) + " blocks"
    for i in np.arange(7, 8):
        hh_threshold = i
        if hh_threshold >= 6:
            print "\nThreshold number = " + str(hh_threshold)
        vari = airconditioner(device_data, routine_, min_interval, billing_info[1], hh_threshold, shifting_, 0)
        print(np.sum(vari))
        var_cum_sum = np.cumsum(vari)
        optimised_cum_sum = original_cum_sum + var_cum_sum
        if hh_threshold >= 1000:
            plt.plot(optimised_cum_sum, label='Motivation Level = %i' % i)
            per_saved = np.around(100 - np.divide(np.max(optimised_cum_sum), np.max(original_cum_sum))*100, 2)
            print "Percentage Saved = " + str(per_saved) + "% & kWh saved = " + str(np.around((original_cum_sum[-1]-optimised_cum_sum[-1]), 2)) + " kWh"
            device_per = np.around(np.divide(optimised_cum_sum[-1], houselevel_cum_sum[-1]+var_cum_sum[-1])*100, 2)
            optimised_device_data = [a + b for a, b in zip(device_data, vari)]
            opti_device_cost = be.billing_calc(optimised_device_data, c_load, bill_type, 0, billing_info[1], billing_info[2], billing_info[3])
            print "Saving a total of $ " + str(np.around(sum(device_cost)-sum(opti_device_cost), 2))
            print "Device accounts for " + str(device_per) + "% of household consumption"
            house_per_save = np.around(100 - np.divide(houselevel_cum_sum[-1]+var_cum_sum[-1], houselevel_cum_sum[-1])*100, 2)
            print "Comparitive house level saving " + str(house_per_save) + "%"
            print "Optimised house level consumption " + str(np.around(houselevel_cum_sum[-1]+var_cum_sum[-1], 2)) + " kWh"
            optimised_house_level = [a + b for a, b in zip(houselevel_data, vari)]
            houselevel_cost = be.billing_calc(optimised_house_level, c_load, bill_type, 0, billing_info[1], billing_info[2], billing_info[3])
            print "Costing a total of $ " + str(np.around(sum(houselevel_cost), 2))
    # plt.legend(loc="best", fontsize='medium')
    # w = len(device_data)
    # plt.xlabel('Time Intervals (From 01/07/2013 [0] - 01/09/2013 [' + str(w) + '])')
    # plt.ylabel('Kilowatt hours of Electricity (kWh)')
    # plt.title('Impact of Behavioural Change on Dishwasher Use (Data ID:' + str(dataid) + ")")
    # plt.show()


def test2():
    optigoal = "Bill"
    dataid = 4922
    meter = 1
    shifting_ = 0
    csvpath = "C:\Users\Bat Cave\Dropbox\My Files\Uni Work\Capstone\PeaconStreet\dataid_" + str(dataid) + "_localdate_07012013_AND_09302013.csv"
    min_interval = 15
    df = ida.peacon_street(csvpath, min_interval)
    houselevel_data = []
    for row in df[1][0]:
        houselevel_data.append(row)
    houselevel_cum_sum = np.cumsum(houselevel_data)
    plt.plot(houselevel_cum_sum, label='Unoptimised Household Demand')
    device_data = []
    for row in df[1][1]:
        device_data.append(row)
    original_cum_sum = np.cumsum(device_data)
    plt.plot(original_cum_sum, label='Unoptimised Device Demand')
    plt.legend(loc="best", fontsize='medium')
    device_per = np.around(np.divide(original_cum_sum[-1], houselevel_cum_sum[-1])*100, 2)
    print "Device accounts for " + str(device_per) + "% of household consumption"
    w = len(device_data)
    plt.xlabel('Time Intervals (From 01/07/2013 [0] - 01/09/2013 [' + str(w) + '])')
    plt.ylabel('Kilowatt hours of Electricity (kWh)')
    plt.title('Impact of Behavioural Change on Air-Conditioner Use (Data ID:' + str(dataid) + ")")
    #plt.show()


if __name__ == '__main__':

    tests = "Mix"                   # select tests to be ran

    testing = []
    if tests == "Mix":     # (0 off/1 on)
        testing.append(0)  # test 0: Testing device optimisation
        testing.append(1)  # test 1: Evaluate impact of air-conditioner optimisation per motivation level
        testing.append(0)  # test 2: Evaluate original appliance consumption relative to household consumption
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
    if testing[1] > 0:
        test1()
    if testing[2] > 0:
        test2()