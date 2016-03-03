import pandas as pd


def peacon_street():
    # add [, sep=';'] to the end of read_csv
    df = pd.read_csv("C:\Users\Bat Cave\Dropbox\My Files\Uni Work\Capstone\PeaconStreet\Trial.csv")
    drop_cols = ["bathroom1", "bathroom2", "bedroom1", "bedroom2", "bedroom3", "bedroom4", "bedroom5", "diningroom1", "diningroom2", "garage1", "garage2", "gen", "grid", "kitchen1", "kitchen2", "kitchenapp1", "kitchenapp2", "lights_plugs1", "lights_plugs2", "lights_plugs3", "lights_plugs4", "lights_plugs5", "lights_plugs6", "livingroom1", "livingroom2", "office1", "outsidelights_plugs1", "outsidelights_plugs2", "shed1", "unknown1", "unknown2", "unknown3", "unknown4", "utilityroom1"]
    for col in drop_cols:
        df = df.drop(col, axis=1)
    df.set_index('dataid', inplace=True)
    dataids = [160, 171]
    for n in dataids:
        print(df.loc[n])
#    print(df)
#    df.reset_index(inplace=True)
    return df.use, df.air1, df.air2, df.air3, df.airwindowunit1, df.aquarium1, df.car1, df.clotheswasher1, df.clotheswasher_dryg1, df.dishwasher1, df.disposal1, df.drye1, df.dryg1, df.freezer1, df.furnace1, df.furnace2, df.heater1, df.housefan1, df.icemaker1, df.jacuzzi1, df.microwave1, df.oven1, df.oven2, df.pool1, df.pool2, df.poollight1, df.poolpump1, df.pump1, df.range1, df.refrigerator1, df.refrigerator2, df.security1, df.sprinkler1, df.venthood1, df.waterheater1, df.waterheater2, df.winecooler1


def test0():
    x = peacon_street()

if __name__ == '__main__':

    tests = "Mix"                   # select tests to be ran

    testing = []
    if tests == "Mix":     # (0 off/1 on)
        testing.append(1)  # test 0:
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
    if testing[1] > 0:
        test1()
    if testing[2] > 0:
        test2()
    if testing[3] > 0:
        test3()