__author__ = 'Bat Cave'
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt


def aggregatedatacsv(csvname, mins_rounding):
    interval = 0
    intervaldemand = []
    intervaltime = []
    sec_rounding = mins_rounding * 60                           # multiply mins by 60 to get secs between intervals
    data = pd.read_csv(csvname, header=0, names=['Meter', 'Starttime', 'Endtime', 'Demand', 'Consumption'])
    end_time = np.trunc(data.Endtime / (sec_rounding * 1000)) * sec_rounding
    # time since EPOCH, divided by millisconds in hour, rounded down to set interval, multiplied by minutes in interval
    demand = data.Demand/3600000                                # convert Ws to kWh
    arraycount = len(demand)                                    # count how many demand measurements were imported
    for z in np.arange(0, arraycount):                          # loop through logic for each unit
        if z == 0 or end_time[z] == end_time[z - 1]:            # if the current aggregate time is the same as the last
            interval += demand[z]                               # add the demand to the current interval
            if z + 1 == arraycount:                             # if it is the last unit
                if interval > 0:
                    intervaldemand.append(interval)             # add interval demand to the interval demand list
                elif interval == 0:
                    intervaldemand.append(0)                    # add zero to the interval demand list
                else:
                    sys.exit("Aggregate Data CSV Error 1: Can not have negative demand")
                intervaltime.append(end_time[z])                # add the time to the time demand list

        elif end_time[z] > end_time[z - 1]:                     # if the current time is greater then the previous time
            if interval > 0:
                intervaldemand.append(interval)                 # add interval demand to the interval demand list
            elif interval == 0:
                intervaldemand.append(0)                        # add zero to the interval demand list
            else:
                sys.exit("Aggregate Data CSV Error 2: Can not have negative demand")
            intervaltime.append(end_time[z-1])                  # add the previous time to the time list
            gap = (end_time[z] - end_time[z - 1]) / sec_rounding        # calc the number of time periods current
                                                                # time period and previous time period
            if gap > 1:                                         # if the gap is bigger then one time period
                interval = demand[z] / gap                      # average out the current demand over skipped time
                for w in np.arange(0, gap - 1):                 # loop once for each skipped time period
                    if interval > 0:
                        intervaldemand.append(interval)         # add interval demand to the interval demand list
                        intervaltime.append(end_time[z - 1] + sec_rounding * (w + 1))
                    elif interval == 0:
                        intervaldemand.append(0)                # add zero to the interval demand list
                        intervaltime.append(end_time[z - 1] + sec_rounding * (w + 1))
                    else:
                        sys.exit("Aggregate Data CSV Error 3: Can not have negative demand")
            else:                                               # if the gap is one time period
                interval = demand[z]                            # make the interval equal to the demand
                if z + 1 == arraycount:                         # if it is the last unit
                    if interval > 0:
                        intervaldemand.append(interval)         # add interval demand to the interval demand list
                    elif interval == 0:
                        intervaldemand.append(0)                # add zero to the interval demand list
                    else:
                        sys.exit("Aggregate Data CSV Error 4: Can not have negative demand")
                    intervaltime.append(end_time[z])            # add the time to the time list
        else:                                                   # if the system goes into an unknown state
            sys.exit("Aggregate Data CSV Error 5: inccorect summing of demand")          # print an error message
                                                                # return the aggregated times and demand
    return intervaltime, intervaldemand


def syncdata(housedata, device_data, device_name):
    if device_data[0][0] != housedata[0][0]:                    # if the first timestamps do not match
        if device_data[0][0] > housedata[0][0]:                 # if the device starts after the house level data
            print "House level starts: " + str(housedata[0][0]) + " Device starts: " + str(device_data[0][0])
            sys.exit("Device Data Error4: " + str(device_name) + " data starts after the house level data")
            # print debug message
        else:                                                   # otherwise
            for k in np.arange(0, len(device_data[0])):         # loop through all the device data
                if device_data[0][0] < housedata[0][0]:         # if device start earlier then house level data
                    device_data[0].pop(0)                       # remove earlier times from the list
                    device_data[1].pop(0)                       # and remove the associated demand data
                elif device_data[0][0] == housedata[0][0]:      # when the start times match
                    break                                       # break loop
                else:                                           # if the device data starts after the house level data
                    sys.exit("Device Data Error1: " + str(device_name) + " start timestamps never syncs")
    if device_data[0][-1] != housedata[0][-1]:                  # if the last timestamps do not match
        if device_data[0][-1] < housedata[0][-1]:               # if the device data ends before the house data
                print "House level ends: " + str(housedata[0][-1]) + " Device ends: " + str(device_data[0][-1])
                sys.exit("Device Data Error2: " + str(device_name) + " data ends before house level data")
                # print debug information
        else:                                                   # if not then
            for k in np.arange(len(device_data[0])-1, 0, -1):   # loop from last to first device interval
                if device_data[0][-1] > housedata[0][-1]:       # if device timestamp after end of house level data
                    device_data[0].pop(-1)                      # delete time from the device timestamps list
                    device_data[1].pop(-1)                      # delete demand from the device demand list
                elif device_data[0][-1] == housedata[0][-1]:    # once the device and house level timestamps match
                    break                                       # break the loop
                else:                                           # if the end times never sync then print debug message
                    sys.exit("Device Data Error3: " + str(device_name) + " end timestamps do not sync")
    if len(housedata[1]) != len(device_data[1]):                # if number of house and device intervals do not match
        print str(len(housedata[0])) + "    " + str(housedata[0])               # print debug info
        print str(len(device_data[0])) + "    " + str(device_data[0])
        sys.exit("The number of house level intervals does not equal the number of " + str(device_name) + " intervals")

    return device_data


def deviceimport(housedata, mininterval, csv_directory, airconditioner, clothesdryer, clotheswasher, dishwasher,
                 fridgefreezer, secondfridgefreezer, standalonefridge, standalonefreezer, kettle,
                 microwave, soundsystem, television, toaster, waterheater):
    optimisation_potential = 0
    appliance_demand = []
    if airconditioner == "Yes":                                # 0
        csv = "air-conditioner.csv"                            # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if clothesdryer == "Yes":                                  # 1
        csv = "clothes-dryer.csv"                              # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if clotheswasher == "Yes":                                 # 2
        csv = "clothes-washer.csv"                             # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if dishwasher == "Yes":                                    # 3
        csv = "dishwasher.csv"                                 # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if fridgefreezer == "Yes":                                 # 4
        csv = "fridgefreezer.csv"                              # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if secondfridgefreezer == "Yes":                           # 5
        csv = "secondfridgefreezer.csv"                        # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if standalonefridge == "Yes":                              # 6
        csv = "standalonefridge.csv"                           # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if standalonefreezer == "Yes":                             # 7
        csv = "standalonefreezer.csv"                          # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if kettle == "Yes":                                        # 8
        csv = "kettle.csv"                                     # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if microwave == "Yes":                                     # 9
        csv = "microwave.csv"                                  # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if soundsystem == "Yes":                                   # 10
        csv = "sound-system.csv"                               # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])

    else:
        appliance_demand.append(0)

    if television == "Yes":                                    # 11
        csv = "television.csv"                                 # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if toaster == "Yes":                                       # 12
        csv = "toaster.csv"                                    # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    if waterheater == "Yes":                                   # 12
        csv = "IHWH.csv"                                       # only relate to the demand of the device being optimised
        csvpath = csv_directory + "\\" + str(csv)              # connect the csv name & directory to identify file path
        device_data = aggregatedatacsv(csvpath, mininterval)   # import and aggregate the timestamps and data
        device_data = syncdata(housedata, device_data, csv[:-4])         # ensure device data syncs with house data
        appliance_demand.append(device_data[1])                # isolate just the aggregated demand data as demand
        optimisation_potential += sum(device_data[1])
    else:
        appliance_demand.append(0)

    return appliance_demand, optimisation_potential


def peacon_street(csvpath, mininterval):
    df = pd.read_csv(csvpath, sep=';')
    drop_cols = ["dataid", "bathroom1", "bathroom2", "bedroom1", "bedroom2", "bedroom3", "bedroom4", "bedroom5", "diningroom1", "diningroom2", "garage1", "garage2", "gen", "grid", "kitchen1", "kitchen2", "kitchenapp1", "kitchenapp2", "lights_plugs1", "lights_plugs2", "lights_plugs3", "lights_plugs4", "lights_plugs5", "lights_plugs6", "livingroom1", "livingroom2", "office1", "outsidelights_plugs1", "outsidelights_plugs2", "shed1", "unknown1", "unknown2", "unknown3", "unknown4", "utilityroom1"]
    for col in drop_cols:
        df = df.drop(col, axis=1)
    df = df.rename(columns={'local_15min': 'time'})
    df['time'] = pd.to_datetime(df['time'], unit='s', infer_datetime_format=True)
    df = df.drop_duplicates('time')
    df = df.sort('time')
    date_time = df['time']
    df.set_index('time', inplace=True)
    df.fillna(0, inplace=True)
    df = df.asfreq(str(mininterval) + "Min", method='backfill')
    df /= (60/mininterval)                                          # convert from kW to kWh
    return [date_time, [df.use, df.air1, df.air2, df.air3, df.airwindowunit1, df.aquarium1, df.car1, df.clotheswasher1, df.clotheswasher_dryg1, df.dishwasher1, df.disposal1, df.drye1, df.dryg1, df.freezer1, df.furnace1, df.furnace2, df.heater1, df.housefan1, df.icemaker1, df.jacuzzi1, df.microwave1, df.oven1, df.oven2, df.pool1, df.pool2, df.poollight1, df.poolpump1, df.pump1, df.range1, df.refrigerator1, df.refrigerator2, df.security1, df.sprinkler1, df.venthood1, df.waterheater1, df.waterheater2, df.winecooler1]]


def test0():
    path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house2\consumption.csv"
    minsrounding = 15
    data_ = aggregatedatacsv(path, minsrounding)
    interval_time = data_[0]
    interval_demand = data_[1]
    # Test output
    if minsrounding == 15:
        print "15 mins first interval rounding"
        print "Expected demand: " + str(0.333469165493333) + "   Expected time: " + str(1426464000.0)
        print "  Actual demand: " + str(interval_demand[0]) + "     Actual time: " + str(interval_time[0]) + "\n"
        print "15 mins last interval rounding"
        print "Expected demand: " + str(0.153008370741333) + "   Expected time: " + str(1427154300.0)
        print "  Actual demand: " + str(interval_demand[-1]) + "     Actual time: " + str(interval_time[-1])
        print " Expected Count: " + str(768) + " Actual Count: " + str(len(interval_demand))

    if minsrounding == 30:
        print "30 mins first interval rounding"
        print "Expected demand: " + str(0.692971822565) + "   Expected time: " + str(1426464000.0)
        print "  Actual demand: " + str(interval_demand[0]) + "     Actual time: " + str(interval_time[0]) + "\n"
        print "30 mins last interval rounding"
        print "Expected demand: " + str(0.304271730655) + "   Expected time: " + str(1427153400.0)
        print "  Actual demand: " + str(interval_demand[-1]) + "     Actual time: " + str(interval_time[-1])
        print " Expected Count: " + str(384) + " Actual Count: " + str(len(interval_demand))

    if minsrounding == 60:
        print "60 mins first interval rounding"
        print "Expected demand: " + str(0.995302607333) + "   Expected time: " + str(1426464000)
        print "  Actual demand: " + str(interval_demand[0]) + "     Actual time: " + str(interval_time[0]) + "\n"
        print" 60 mins last interval rounding"
        print "Expected demand: " + str(0.458666051259) + "   Expected time: " + str(1427151600)
        print "  Actual demand: " + str(interval_demand[-1]) + "     Actual time: " + str(interval_time[-1])
        print " Expected Count: " + str(192) + " Actual Count: " + str(len(interval_demand))

    print "   Demand count: " + str(len(interval_demand)) + " Timestamp count " + str(len(interval_time)) + "\n"


def test1():
    csv_directory = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\house"
    mininterval = 30
    csv = "consumption.csv"
    csvpath = str(csv_directory) + "\\" + str(csv)
    housedata = aggregatedatacsv(csvpath, mininterval)
    airconditioner = "Yes"
    clothesdryer = "No"
    clotheswasher = "No"
    dishwasher = "Yes"
    fridgefreezer = "No"
    secondfridgefreezer = "No"
    standalonefridge = "No"
    standalonefreezer = "No"
    kettle = "Yes"
    microwave = "Yes"
    soundsystem = "Yes"
    television = "Yes"
    toaster = "No"
    computer = "No"
    appliance_data = deviceimport(housedata, mininterval, csv_directory, airconditioner, clothesdryer,
                                  clotheswasher, dishwasher, fridgefreezer, secondfridgefreezer, standalonefridge,
                                  standalonefreezer, kettle, microwave, soundsystem, television, toaster, computer)
    for n in np.arange(0, len(appliance_data)):
        print(appliance_data[0][n])


def test2():
    path = "C:\Users\Bat Cave\Dropbox\My Files\Raw Data\h1_150120\h1" + "\\" + "141229_150104_50_h1" + "\\" \
           + "50-house1-132-consumption.csv"
    minsrounding = 1
    data_ = aggregatedatacsv(path, minsrounding)
    interval_time = data_[0]
    interval_demand = data_[1]
    print(len(interval_time))
    print(interval_time)
    print(interval_demand)
    print(sum(interval_demand))


def test3():
    csvpath = "C:\Users\Bat Cave\Dropbox\My Files\Uni Work\Capstone\PeaconStreet\dataid_6910_localdate_07012013_AND_09302013.csv"
    mininterval = 15
    df = peacon_street(csvpath, mininterval)
    # for cols in df:
    #     if np.sum(cols) > 0:
    #         roll_sum = cols.cumsum()
    #         roll_sum.plot()
    # plt.legend(loc="best", fontsize='small')
    # plt.show()

if __name__ == '__main__':

    tests = "Mix"                   # select tests to be ran

    testing = []
    if tests == "Mix":     # (0 off/1 on)
        testing.append(0)  # test 0: Testing time rounding and demand aggregation
        testing.append(0)  # test 1: Test appliance data import
        testing.append(0)  # test 2: Sum demand
        testing.append(1)  # test 3: print peacon street data
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
    if testing[3] > 0:
        test3()