__author__ = 'Bat Cave'

import numpy as np
import ImportDataandAggregate as ida
import RoutineBuilder as rb
import BillEvaluator as be
import Eliminate as el
import Substitute as sb
import Minimise as mn
import Shifting as sh


def XXXXX(device_demand, routine, mininterval, cost, hh_threshold, shifting, test):
    # general XXXXX inputs
    devicetype = ""                             # "Duration" if occupant needed at start and end otherwise "Cycle"
    mealappliance =                             # 0 if device not used in meal prep/ 1 if device is used in prep

    # inputs especially for XXXXX optimsiation using elimination:
    elim_thres = 11                             # how much effort it takes to eliminate device usage

    # inputs especially for XXXXX optimsiation using minimisation 1:
    mini1_thres = 11                            # how much effort it takes to minimise device usage
    mini1_saving =                              # if type duration, what percentage will be saved (0 nothing - 100)
    mini1_cyclemax =                            # if type cycle, what is the maximum amount of cycles...
    mini1_time =                                # if type cycle, ...within a given time frame
    # inputs especially for XXXXX optimsiation using minimisation 2:
    mini2_thres = 11                            # how much effort it takes to minimise device usage
    mini2_saving =                              # if type duration, what percentage will be saved (0 nothing - 100)
    mini2_cyclemax =                            # if type cycle, what is the maximum amount of cycles...
    mini2_time =                                # if type cycle, ...within a given time frame
    # inputs especially for XXXXX optimsiation using minimisation 3:
    mini3_thres = 11                            # how much effort it takes to minimise device usage
    mini3_saving =                              # if type duration, what percentage will be saved (0 nothing - 100)
    mini3_cyclemax =                            # if type cycle, what is the maximum amount of cycles...
    mini3_time =                                # if type cycle, ...within a given time frame

    # inputs especially for XXXXX optimsiation using shifting 1:
    shift1_thres = 11                           # how much effort it takes to shift device usage
    shift1_time =                               # how long can the use of the device be shifted
    # inputs especially for XXXXX optimsiation using shifting 2:
    shift2_thres = 11                           # how much effort it takes to shift device usage
    shift2_time =                               # how long can the use of the device be shifted
    # inputs especially for XXXXX optimsiation using shifting 3:
    shift3_thres = 11                           # how much effort it takes to shift device usage
    shift3_time =                               # how long can the use of the device be shifted

    # inputs especially for XXXXX optimsiation using substitution:
    sub1_thres = 11                             # how much effort it takes to substitue the device usage
    sub1_type = ""                              # what device type is the substitue. "Duration" or "Cycle"
    sub1_time =                                 # if subtype cycle, how much time the sub takes to complete a cycle
    sub1_demand =                               # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    sub1_saving =                               # if subtype duration, what percentage of electricity does it
                                                # save relative to current device (0 saves nothing - 100)
    # inputs especially for XXXXX optimsiation using substitution:
    sub2_thres = 11                             # how much effort it takes to substitue the device usage
    sub2_type = ""                              # what device type is the substitue. "Duration" or "Cycle"
    sub2_time =                                 # if subtype cycle, how much time the sub takes to complete a cycle
    sub2_demand =                               # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    sub2_saving =                               # if subtype duration, what percentage of electricity does it
                                                # save relative to current device (0 saves nothing - 100)
    # inputs especially for TV optimsiation using substitution:
    sub3_thres = 11                             # how much effort it takes to substitue the device usage
    sub3_type = ""                              # what device type is the substitue. "Duration" or "Cycle"
    sub3_time =                                 # if subtype cycle, how much time the sub takes to complete a cycle
    sub3_demand =                               # if subtype cycle, how much electricity is consumed in a cycle (Ws)
    sub3_saving =                               # if subtype duration, what percentage of electricity does it
                                                # save relative to current device (0 saves nothing - 100)
    # print test data
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
        print " Opti Mini2 Demand: (" + str(mini2_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1 and hh_threshold >= mini3_thres:
        print " Opti Mini3 Demand: (" + str(mini3_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)
    elif test == 1:
        print " Opti MiniP Demand: (" + str(mini2_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand)

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
    elif hh_threshold >= sub2_thres:          # apply substituation optimisations if effort threshold >= sub threshold
        optimised_demand = sb.substitute(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                         sub2_type, sub2_time, sub2_demand, sub2_saving)  # return optimised usage
    elif hh_threshold >= sub3_thres:          # apply substituation optimisations if effort threshold >= sub threshold
        optimised_demand = sb.substitute(optimised_demand, routine, mealappliance, devicetype, mininterval,
                                         sub3_type, sub3_time, sub3_demand, sub3_saving)  # return optimised usage
    else:                                      # if effort threshold lower then value
        optimised_demand = optimised_demand            # device usage is not optimised

    if test == 1 and hh_threshold >= sub1_thres:
        print " Opti Subs1 Demand: (" + str(sub1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "
    elif test == 1 and hh_threshold >= sub2_thres:
        print " Opti Subs2 Demand: (" + str(sub2_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "
    elif test == 1 and hh_threshold >= sub3_thres:
        print " Opti Subs3 Demand: (" + str(sub3_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "
    elif test == 1:
        print " Opti SubsP Demand: (" + str(sub1_thres) + ") (" + str(len(optimised_demand)) + ") " + str(optimised_demand) + "\n "

    demand_variation = [a - b for a, b in zip(optimised_demand, device_demand)]
                                                    # difference between optimised & original demand for each interval
    return demand_variation