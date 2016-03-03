__author__ = 'Bat Cave'

import numpy as np
import sys


def substitute(demand, routine, mealappliance, devicetype, mininterval, subtype, subtime, subdemand, savepercent, weather_forecast, test):
    intervalcount = len(demand)  # count how many intervals to be evaluated over
    demandoptimise = [0 for i in range(intervalcount)]  # write zeros for every potential hour
    subintervalcount = int(np.ceil(np.divide(np.float64(subtime), np.float64(mininterval))))
    subintervaldemand = np.divide(float(subdemand), subintervalcount)
    subpercent = (100.0 - float(savepercent)) / 100
    sub_place = []
    skipinterval = []
    if (devicetype != "Duration" and devicetype != "Cycle") or (subtype != "Duration" and subtype != "Cycle"):
        sys.exit("Please enter a valid usage type (Duration or Cycle)")
    for z in np.arange(0, intervalcount):
        cyclecount = 0                                 # reset the count of how many hours the use went for
        if demand[z] > 0:                              # if demand is greater then zero check how many hours it runs for
            for k in np.arange(z, intervalcount):      # from next hour until the end (inclusive of last hour)
                if demand[k] > 0:                      # if next hour is greater then zero eg still in use
                    cyclecount += 1                    # add one more to count of cycle length
                else:                                  # if next hour is zero eg device usage stopped
                    break                              # break counting loop

        if z not in skipinterval and cyclecount > 0:    # skip intervals that have already been optimised or no demand

            sub_in = 1
            if devicetype == "Cycle" and max(demand[z], sum(demand[z:z+cyclecount])) < subdemand:
                sub_in = 0      # if the sum of the cycle demand is less then the substitue cycle demand, do not optimse

            if np.sum(weather_forecast) > 0:                       # if the weather is taken into account
                weather = 0
                for x in np.arange(z, z+cyclecount):               # find the maximum chance of rain over the cycle
                    if weather_forecast[x] > weather:
                        weather = weather_forecast[x]
            else:
                weather = 0

            devicecycletime = z + cyclecount                       # calc when the device finishes
            subcycletime = z + subintervalcount                    # calc when the substitue would finish

            if (mealappliance == 1 and routine[z] == 1) or sub_in == 0 or weather > 0.2:    # if substitute consumes
                                                                   # more electricity or the weather looks bad or
                                                                   # if device is used in meal prep and it is meal time
                if weather > 0.2:
                    sub_place.append([z, "weather: " + str(weather)])
                if devicetype == "Cycle":
                    for e in np.arange(0, cyclecount):             # for all intervals that the cycle runs over
                        demandoptimise[z + e] = demand[z + e]      # do not optimse demand
                        skipinterval.append(z + e)                 # add optimised intervals to skip list
                elif devicetype == "Duration":                     # for duration device types in this situation
                    demandoptimise[z] = demand[z]                  # do not optimise demand
                else:
                    sys.exit("Substitution Error1: Device type to be substituted is not a Cycle or Duration type")
            elif devicetype == "Cycle" and subtype == "Cycle":            # if device and sub usage type are cycle
                if devicecycletime < subcycletime and sum(demand[devicecycletime:subcycletime]) == 0 \
                        and subcycletime <= intervalcount:
                    sub_place.append([z])
                    # and device duration less then sub duration and subs is not used during the substitution period
                    for t in np.arange(0, subintervalcount):
                        demandoptimise[z + t] = subintervaldemand
                    for e in np.arange(0, cyclecount):
                        skipinterval.append(z + e)

                elif devicecycletime >= subcycletime:
                    sub_place.append([z])
                    for t in np.arange(0, subintervalcount):
                        demandoptimise[z + t] = subintervaldemand
                    for e in np.arange(0, cyclecount):
                        skipinterval.append(z + e)
                else:
                    for e in np.arange(0, cyclecount):                  # for all intervals that cycle runs over
                        demandoptimise[z + e] = demand[z + e]           # do not optimse demand
                        skipinterval.append(z + e)

            elif devicetype == "Duration" and subtype == "Duration":    # when a duration subs for a duration usage
                demandoptimise[z] = demand[z] * subpercent              # record optimised demand as % of demand
                sub_place.append([z])

            elif devicetype == "Cycle" and subtype == "Duration":
                sys.exit("Substitution Error: Device type = Cycle & Sub type = Duration")

            elif devicetype == "Duration" and subtype == "Cycle":
                sys.exit("Substitution Error: Device type = Duration & Sub type = Cycle")
            else:
                sys.exit("Substitution Error: in unknown substitute optimisation state")
    if test == 2:
        print "  Sub place : (" + str(len(sub_place)) + ") " + str(sub_place)
    return demandoptimise


def test0():
    meal_appliance = 0                              # if the appliance is used in the preperation of food
    min_interval = 60
    device_type = "Cycle"
    sub_time = 120
    sub_demand = 5.0
    sub_type = "Cycle"
    save_percent = 100
    routine_ = [1, 2, 1, 1, 2, 1, 1]
    demand_ = [10, 10, 0, 10, 10, 0, 10]
    expected_ = [2.5, 2.5, 0, 2.5, 2.5, 0, 10]

    opti_demand = substitute(demand_, routine_, meal_appliance, device_type, min_interval, sub_type, sub_time,
                             sub_demand, save_percent, 0, 0)

    print "    Sub type: " + str(sub_type)
    print "  Sub demand: " + str(sub_demand)
    print "    Sub time: " + str(sub_time)
    print "Save percent: " + str(save_percent)
    print "     Routine: " + str(routine_)
    print "    Original: " + str(demand_)
    print "   Optimised: " + str(opti_demand)

    if opti_demand == expected_:
        print "Pass test 0: One for one substitution (No meal, sub 5 over 2 intervals, sub type: cycle) \n"
    else:
        print "    Expected: " + str(expected_)
        print "***** Fail ***** test 0: One for one substitution (No meal, sub 5 over 2 intervals, sub type: cycle)\n"


def test1():                    # two for three substitution (No meal, sub 7.5 over 3 intervals, sub type: cycle)
    meal_appliance = 0                              # if the appliance is used in the preperation of food
    min_interval = 60
    device_type = "Cycle"
    sub_time = 150
    sub_demand = 7.5
    sub_type = "Cycle"
    save_percent = 100
    routine_ = [1, 2, 1, 1, 2, 1, 1]
    demand_ = [10, 10, 0, 10, 10, 0, 10]
    expected_ = [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 10]

    opti_demand = substitute(demand_, routine_, meal_appliance, device_type, min_interval, sub_type, sub_time,
                             sub_demand, save_percent, 0, 0)

    print "    Sub type: " + str(sub_type)
    print "  Sub demand: " + str(sub_demand)
    print "    Sub time: " + str(sub_time)
    print "Save percent: " + str(save_percent)
    print "     Routine: " + str(routine_)
    print "    Original: " + str(demand_)
    print "   Optimised: " + str(opti_demand)

    if opti_demand == expected_:
        print "Pass test 1: two for three substitution (No meal, sub 7.5 over 3 intervals, sub type: cycle) \n"
    else:
        print "    Expected: " + str(expected_)
        print "***** Fail ***** test 1: two 4 three substitution (No meal, sub 7.5 over 3 intervals, sub type: cycle)\n"


def test2():                    # no more substitution (No meal, try sub 100 over 20, sub type: cycle)
    meal_appliance = 0                              # if the appliance is used in the preperation of food
    min_interval = 60
    device_type = "Cycle"
    sub_time = 150
    sub_demand = 100.0
    sub_type = "Cycle"
    save_percent = 100
    routine_ = [1, 2, 1, 1, 2, 1, 1]
    demand_ = [10, 10, 0, 10, 10, 0, 10]
    expected_ = [10, 10, 0, 10, 10, 0, 10]

    opti_demand = substitute(demand_, routine_, meal_appliance, device_type, min_interval, sub_type, sub_time,
                             sub_demand, save_percent, 0, 0)

    print "    Sub type: " + str(sub_type)
    print "  Sub demand: " + str(sub_demand)
    print "    Sub time: " + str(sub_time)
    print "Save percent: " + str(save_percent)
    print "     Routine: " + str(routine_)
    print "    Original: " + str(demand_)
    print "   Optimised: " + str(opti_demand)

    if opti_demand == expected_:
        print "Pass test 2: no more substitution (No meal, try sub 100 over 20, sub type: cycle) \n"
    else:
        print "    Expected: " + str(expected_)
        print "***** Fail ***** test 2: no more substitution (No meal, try sub 100 over 20, sub type: cycle)\n"


def test3():                   # substitution shorter then device useage (No meal, demand 2 intervals, sub 1)
    meal_appliance = 0                              # if the appliance is used in the preperation of food
    min_interval = 60
    device_type = "Cycle"
    sub_time = 60
    sub_demand = 5.0
    sub_type = "Cycle"
    save_percent = 100
    routine_ = [1, 2, 1, 1, 2, 1, 1]
    demand_ = [10, 10, 0, 10, 10, 0, 10]
    expected_ = [5, 0, 0, 5, 0, 0, 5]

    opti_demand = substitute(demand_, routine_, meal_appliance, device_type, min_interval, sub_type, sub_time,
                             sub_demand, save_percent, 0, 0)

    print "    Sub type: " + str(sub_type)
    print "  Sub demand: " + str(sub_demand)
    print "    Sub time: " + str(sub_time)
    print "Save percent: " + str(save_percent)
    print "     Routine: " + str(routine_)
    print "    Original: " + str(demand_)
    print "   Optimised: " + str(opti_demand)

    if opti_demand == expected_:
        print "Pass test 3: substitution shorter then device useage (No meal, demand 2 intervals, sub 1) \n"
    else:
        print "    Expected: " + str(expected_)
        print "***** Fail ***** test 3: substitution shorter then device useage (No meal, demand 2 intervals, sub 1)\n"


def test4():                   # substitution duration
    meal_appliance = 1                              # if the appliance is used in the preperation of food
    min_interval = 60
    device_type = "Duration"
    sub_time = 60
    sub_demand = 5.0
    sub_type = "Duration"
    save_percent = 80
    routine_ = [1, 2, 1, 1, 2, 1, 1]
    demand_ = [10, 10, 0, 10, 10, 0, 10]
    expected_ = [10, 2.0, 0, 10, 2.0, 0, 10]

    opti_demand = substitute(demand_, routine_, meal_appliance, device_type, min_interval, sub_type, sub_time,
                             sub_demand, save_percent, 0, 0)

    print "    Sub type: " + str(sub_type)
    print "  Sub demand: " + str(sub_demand)
    print "    Sub time: " + str(sub_time)
    print "Save percent: " + str(save_percent)
    print "     Routine: " + str(routine_)
    print "    Original: " + str(demand_)
    print "   Optimised: " + str(opti_demand)

    if opti_demand == expected_:
        print "Pass test 4: meal related duration 4 duration substituations \n"
    else:
        print "    Expected: " + str(expected_)
        print "***** Fail ***** test 4: meal related duration 4 duration substituations\n"


def test5():                                        # cycle substitution
    meal_appliance = 0                              # if the appliance is used in the preperation of food
    min_interval = 15
    device_type = "Cycle"
    sub_time = 60
    sub_demand = 15.0
    sub_type = "Cycle"
    save_percent = 80
    routine_ = [1, 2, 1, 1, 2, 1, 1]
    demand_ = [10, 10, 0, 0, 10, 0, 10]
    expected_ = [3.75, 3.75, 3.75, 3.75, 10, 0, 10]

    opti_demand = substitute(demand_, routine_, meal_appliance, device_type, min_interval, sub_type, sub_time,
                             sub_demand, save_percent, 0, 0)

    print "    Sub type: " + str(sub_type)
    print "  Sub demand: " + str(sub_demand)
    print "    Sub time: " + str(sub_time)
    print "Save percent: " + str(save_percent)
    print "     Routine: " + str(routine_)
    print "    Original: " + str(demand_)
    print "   Optimised: " + str(opti_demand)

    if opti_demand == expected_:
        print "Pass test 5: Sub demand greater then one interval but less then sum of cycle\n"
    else:
        print "    Expected: " + str(expected_)
        print "***** Fail ***** test 5: Sub demand greater then one interval but less then sum of cycle\n"


def test6():                                    # 6: Meal appliance test + optimising multiple interval duration device
    meal_appliance = 1                          # if the appliance is used in the preperation of food
    min_interval = 15
    device_type = "Duration"
    sub_time = 45
    sub_demand = 15.0
    sub_type = "Duration"
    save_percent = 80
    routine_ = [1, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2]
    demand_ = [10, 10, 0, 0, 0, 0, 10, 10, 0, 10, 10]
    expected_ = [10, 10, 0, 0, 0.0, 0.0, 2.0, 2.0, 0.0, 2.0, 2.0]

    opti_demand = substitute(demand_, routine_, meal_appliance, device_type, min_interval, sub_type, sub_time,
                             sub_demand, save_percent, 0, 0)

    print "    Sub type: " + str(sub_type)
    print "  Sub demand: " + str(sub_demand)
    print "    Sub time: " + str(sub_time)
    print "Save percent: " + str(save_percent)
    print "     Routine: " + str(routine_)
    print "    Original: " + str(demand_)
    print "   Optimised: " + str(opti_demand)

    if opti_demand == expected_:
        print "Pass test 6: Meal appliance test + optimising multiple interval duration device\n"
    else:
        print "    Expected: " + str(expected_)
        print "***** Fail ***** test 6: Meal appliance test + optimising multiple interval duration device\n"

if __name__ == '__main__':

    tests = "All"  # select tests to be ran

    testing = []
    if tests == "Mix":
        testing.append(0)  # test 0 (0 off/1 on) 1:4:1 substitution (No meal, sub 5 over 2 intervals, sub type: cycle)
        testing.append(0)  # test 1 (0 off/1 on) 2:4:3 substitution (No meal, sub 7.5 over 3 intervals, sub type: cycle)
        testing.append(0)  # test 2 (0 off/1 on) no more substitution (No meal, try sub 100 over 20, sub type: cycle)
        testing.append(0)  # test 3 (0 off/1 on) substitution shorter then device useage (demand 2 intervals, sub 1)
        testing.append(0)  # test 4 (0 off/1 on) meal related duration 4 duration substituations
        testing.append(0)  # test 5 (0 off/1 on) Sub demand greater then one interval but less then sum of cycle
        testing.append(1)  # test 6 (0 off/1 on) Meal appliance test + optimising multiple interval duration device
    elif tests == "None":
        testing = [0 for w in range(0, 7)]
    elif tests == "All":
        testing = [1 for w in range(0, 7)]
    if testing[0] > 0:  # Non meal prep device optimisation test
        test0()
    if testing[1] > 0:  # Meal prep device optimisation test
        test1()
    if testing[2] > 0:  # Meal prep device optimisation test
        test2()
    if testing[3] > 0:  # Meal prep device optimisation test
        test3()
    if testing[4] > 0:  # Meal prep device optimisation test
        test4()
    if testing[5] > 0:  # Meal prep device optimisation test
        test5()
    if testing[6] > 0:  # Meal prep device optimisation test
        test6()