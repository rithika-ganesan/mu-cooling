# Read g4beamline ascii output from a single .txt file and finds 'dB_z / dz'
# Currently only for one portion.
# Rithika Ganesan | May 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import numpy as np
import argparse

# Get input path from parser
parser = argparse.ArgumentParser(description="Read g4bl ASCII output files")

parser.add_argument('--input_path', '-i', type=str, required=True, help='Input file path')
parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
  
args = parser.parse_args()

# if args.verbose:
#     print(f"Reading from: {args.input}")
#     print(f"Writing to: {args.output}")

# Data params
tuple_labels_noEM=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]
tuple_labels=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight", "Bx", "By", "Bz", "Ex", "Ey", "Ez"]

tuple_units = {
    "x": "mm",
    "y": "mm",
    "z": "mm",
    "Px": "MeV/c", 
    "Py": "MeV/c",
    "Pz": "MeV/c",
    "t": "ns",
    "PDGid": None,
    "EventID": None,
    "TrackID": None,
    "ParentID": None,
    "Weight": None,
    "Bx": "T",
    "By": "T",
    "Bz": "T",
    "Ex": "MV/m",
    "Ey": "MV/m",
    "Ez": "MV/m"
}

########## Functions ###############

def read_ascii(path, comment='#'):
    df = pd.read_csv(f'{path}', comment=comment, header=None, sep='\\s+')
    if df.shape[1] == 12:
        df.columns = tuple_labels_noEM
    elif df.shape[1] == 18:
        df.columns = tuple_labels
    else:
        raise ValueError("Unknown parameters in data file.")
    
    return df

def plot_Bz_vs_z(df):
    return None

def slice(col, min_in, max_in):
    return col[min_in:max_in]

def ceil_to_scale(x, place=10000):
    #factor = 10 ** place
    return math.ceil(x / place) * place

###########  Main  #################
path = args.input_path 

df = read_ascii(path=path)

z, bz = df['z'], df['Bz']

# in = 50000
# len = 43701

N = int(ceil_to_scale(len(df))) #This defines the total 'number of indices' to scan over --> here it's 50000.
r, c = 2, 5 #These are the number of rows, columns respectively to go into the subfigure. 
n = r * c #Total number of subfigures you want. 
step_size = int(N / n) #Calculates what the size of each slice is. 

ranges = []
for i in range(n): #Gets min and max indices for each slice
    ranges.append([i*step_size, i*step_size + step_size])

##### PLOT #########
fig, axes = plt.subplots(r, c, figsize=(15, 4))  
axes = axes.flatten()

for i, vals in enumerate(ranges): #Gets the slice and plots it
    z_, bz_ = slice(z, *vals), slice(bz, *vals) 
    axes[i].scatter(z_, bz_, s=2, marker='.')
    axes[i].set_title(f'Plot {i+1}')

plt.tight_layout()
plt.show()


#vals = [0, 100000]

#bz, z = slice(bz, *vals), slice(z, *vals) 

#plt.plot(z, bz, color='k')
#plt.scatter(z, bz, s=0.2)
#plt.show()
