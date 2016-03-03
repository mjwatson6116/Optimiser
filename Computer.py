__author__ = 'Bat Cave'

import numpy as np
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be
import Eliminate as el
import Substitute as sb
import Minimise as mn
import Shifting as sh


def computer(device_demand, routine, mininterval, cost, hh_threshold, shifting, test):
    # general computer inputs
    devicetype = "Duration"                     # "Duration" if occupant needed at start and end otherwise "Cycle"
    mealappliance = 0                           # 0 if device not used in meal prep/ 1 if device is used in prep

    # inputs especially for computer optimsiation using elimination:
    elim_thres = 9                              # how much effort it takes to eliminate device usage

    # inputs especially for computer optimsiation using minimisation 1:
    mini1_thres = 7                             # how much effort it takes to minimise device usage
    mini1_saving = 60                           # if type duration, what percentage will be saved (0 nothing - 100)
    mini1_cyclemax = 1000                       # if type cycle, what is the maximum amount of cycles...
    mini1_time = 1000                           # if type cycle, ...within a given time frame
    # inputs especially for computer optimsiation using minimisation 2:
    mini2_thres = 5                             # how much effort it takes to minimise device usage
    mini2_saving = 40                           # if type duration, what percentage will be saved (0 nothing - 100)
    mini2_cyclemax = 1000                       # if type cycle, what is the maximum amount of cycles...
    mini2_time = 1000                           # if type cycle, ...within a given time frame
    # inputs especially for computer optimsiation using minimisation 3:
    mini3_thres = 4                             # how much effort it takes to minimise device usage
    mini3_saving = 20                           # if type duration, what percentage will be saved (0 nothing - 100)
    mini3_cyclemax = 1000                       # if type cycle, what is the maximum amount of cycles...
    mini3_time = 1000                           # if type cycle, ...within a given time frame

    # inputs especially for computer optimsiation using shifting 1:
    shift1_thres = 6                            # how much effort it takes to shift device usage
    shift1_time = 60                            # how long can the use of the device be shifted
    # inputs especially for computer optimsiation using shifting 2:
    shift2_thres = 5                            # how much effort it takes to shift device usage
    shift2_time = 30                            # how long can the use of the device be shifted
    # inputs especially for computer optimsiation using shifting 3:
    shift3_thres = 4                            # how much effort it takes to shift device usage
    shift3_time = 15                            # how long can the use of the device be shifted

    # inputs especially for computer optimsiation using substitution:
    sub1_thres = 7                               # how much effort it takes to substitue the device usage
    sub1_type = "Duration"                       # what device type is the substitue. "Duration" or "Cycle"
    sub1_time = 1                                # if subtype cycle, how much time the sub takes to complete a cycle
    sub1_demand = 0                              # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    sub1_saving = 100                            # if subtype duration, what percentage of electricity does it
                                                 # save relative to current device (0 saves nothing - 100)

    #import and aggregate clothes dryer data
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
    # ****** Minimisation 2 ******
    elif hh_threshold >= mini2_thres:          # apply minimisation optimisations if effort threshold >= mini threshold
        optimised_demand = mn.minimise(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                       mini2_saving, mini2_cyclemax, mini2_time)  # return optimised device usage
    # ****** Minimisation 3 ******
    elif hh_threshold >= mini3_thres:          # apply minimisation optimisations if effort threshold >= mini threshold
        optimised_demand = mn.minimise(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                       mini3_saving, mini3_cyclemax, mini3_time)  # return optimised device usage
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
                                      cost)                     # return optimised device usage
    # ****** Shifting 2 ******
    elif hh_threshold >= shift2_thres and shifting == 1:
                                        # apply shifting optimisation if shifting on & threshold >= shift thres
        optimised_demand = sh.shifter(optimised_demand, routine, mealappliance, devicetype, mininterval, shift2_time,
                                      cost)                     # return optimised device usage
    # ****** Shifting 3 ******
    elif hh_threshold >= shift3_thres and shifting == 1:
                                        # apply shifting optimisation if shifting on & threshold >= shift thres
        optimised_demand = sh.shifter(optimised_demand, routine, mealappliance, devicetype, mininterval, shift3_time,
                                      cost)                     # return optimised device usage
    else:                                                       # if effort theshold low then value or shifting is off
        optimised_demand = optimised_demand                     # device usage is not optimsied

    if test == 1 and hh_threshold >= shift1_thres:
        print " Opti Shif1 Demand: (" + str(shift1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1 and hh_threshold >= shift2_thres:
        print " Opti Shif2 Demand: (" + str(shift2_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1 and hh_threshold >= shift3_thres:
        print " Opti Shif3 Demand: (" + str(shift3_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1:
        print " Opti ShifP Demand: (" + str(shift3_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)

    # ****** Substitution ******
    if hh_threshold >= sub1_thres:          # apply substituation optimisations if effort threshold >= sub threshold
        optimised_demand = sb.substitute(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                         sub1_type, sub1_time, sub1_demand, sub1_saving)  # return optimised usage
    else:                                      # if effort threshold lower then value
        optimised_demand = optimised_demand            # device usage is not optimised

    if test == 1 and hh_threshold >= sub1_thres:
        print " Opti Subs1 Demand: (" + str(sub1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "
    elif test == 1:
        print " Opti SubsP Demand: (" + str(sub1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "

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
    appliancedemand = ida.deviceimport(housedata, min_interval, csv_directory, "No", "No", "No", "No", "No", "No",
                                       "No", "No", "No", "No", "No", "No", "No", "Yes")
    device_demand = appliancedemand[0][13]
    variation = computer(device_demand, routine_, min_interval, cost_, threshold, shifting_, testing_)
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