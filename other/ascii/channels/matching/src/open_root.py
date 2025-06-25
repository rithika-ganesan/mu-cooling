import uproot
import numpy as np
import pandas as pd

path = "solenoids-2.root"

with uproot.open(path) as file:
    tree = file['Trace/AllTracks;1']
    print(file.classnames())

#tree.show()

dfr = tree.arrays(library='pd')

eid = 2

df = dfr[dfr["EventID"] == eid]

print(df['z'])
print(df['x'])
