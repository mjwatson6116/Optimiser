__author__ = 'Bat Cave'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def weather(mininterval):
    df = pd.read_csv("C:\Users\Bat Cave\Dropbox\My Files\Uni Work\Capstone\PeaconStreet\weather_hour_localdate_07012013_AND_09302013.csv", sep=';')
    drop_cols = ['latitude', 'longitude', 'tz_offset', 'summary', 'ozone', 'ozone_error', 'temperature', 'temperature_error', 'dew_point', 'dew_point_error', 'humidity', 'humidity_error', 'visibility', 'visibility_error', 'apparent_temperature', 'apparent_temperature_error', 'pressure', 'pressure_error', 'wind_speed', 'wind_speed_error', 'cloud_cover', 'cloud_cover_error', 'wind_bearing', 'precip_intensity', 'precip_intensity_error', 'precip_type']
    for col in drop_cols:
        df = df.drop(col, axis=1)
    df = df.rename(columns={'localhour': 'time'})
    df['time'] = pd.to_datetime(df['time'], unit='s', infer_datetime_format=True)
    df = df.sort('time')
    df.set_index('time', inplace=True)
    df.fillna(0, inplace=True)
    df = df.asfreq(str(mininterval) + "Min", method='ffill')
    rain_probability = []
    for row in df.precip_probability:
        rain_probability.append(row)
    return rain_probability


def test0():
    print "Test 0 Empty"


def test1():
    print "Test 1 Empty"


def test2():
    print "Test 2 Empty"


def test3():
    min_interval = 15
    df = weather(min_interval)
    print df


if __name__ == '__main__':

    tests = "Mix"                   # select tests to be ran

    testing = []
    if tests == "Mix":     # (0 off/1 on)
        testing.append(0)  # test 0:
        testing.append(0)  # test 1:
        testing.append(0)  # test 2:
        testing.append(1)  # test 3: placing legend to the left of the plotted area
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