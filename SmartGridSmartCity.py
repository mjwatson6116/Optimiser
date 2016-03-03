__author__ = 'Bat Cave'
import pandas as pd


df = pd.read_csv("C:\Users\Bat Cave\Dropbox\My Files\Uni Work\Capstone\Research\Smart Grid Smart City\home_plug_readings\HAN_PLUG_READ.csv", names=['ID', 'Device', 'DateTime', 'RollingConsumption', 'Reading', 'Unit'])
drop_cols = ["Reading", "Unit"]
for col in drop_cols:
    df = df.drop(col, axis=1)
df['DateTime'] = pd.to_datetime(df['DateTime'], unit='s', infer_datetime_format=True)
# df = df.drop_duplicates('time')
df = df.sort(['ID', 'Device', 'DateTime'])
df.set_index('DateTime', inplace=True)
df_new = df.ID('8145135')
# df.fillna(0, inplace=True)
# df = df.asfreq(str(mininterval) + "Min", method='backfill')
# df /= (60/mininterval)                                                  # convert from kW to kWh value
print(df_new)
