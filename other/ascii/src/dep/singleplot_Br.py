# Show transformed and original radii are the same
# Rithika Ganesan | May 2025

import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np


######## Get filepaths ##########
directory = '/Users/rithika/utkcms/hfofo/'
path_format = 'flipped/Ev*Trk*.txt'
dir_path = directory + path_format
files = sorted(glob.glob(dir_path))

######## Parameters #############
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

######### Main  ####################
#plot_dir_path = directory + "/plots/" + "flipped"
#os.makedirs(plot_dir_path, exist_ok=True)

# Okay to loop as long as there are 20 or fewer files
# dfs = []
# for i, file in enumerate(files):
#     df = read_ascii(file)
#     dfs.append(df)

df_raw = read_ascii(files[1])

#plt.scatter(df['z'], r, marker='.', s=2)
#plt.xlabel('z (mm)')
#plt.ylabel('r (mm)')
#plt.show()

############### Getting B_r ###############

# Assuming B_r(r, z) = -\frac{r}{2} \frac{\partial B_z}{\partial z}

# First dropping tracks with same z value as previous hit:
length = len(df_raw)
z = df_raw['z']
indices = []
for i in range(length - 1):
    denom = z[i+1] - z[i]
    if denom == 0.0:
        indices.append(i+1)

df = df_raw.drop(indices).reset_index(drop=True)

# First get r from df:
r = np.sqrt(df['x']**2 + df['y']**2)

# Get dB/dz for each interval:
z, bz = df['z'], df['Bz']
fracs = []
radii = []
for i in range(len(z) - 1):
    numerator = (bz[i+1] - bz[i]) 
    denominator = (z[i+1] - z[i])
    rad = (r[i+1] + r[i]) / 2
    radii.append(rad)
    fracs.append(numerator / denominator)

fracs, radii = np.array(fracs), np.array(radii)
z_ = z[1:]

Br = -0.5 * radii * fracs

fig = plt.figure(figsize=(8, 6))
plt.plot(z_, Br, color='k', linewidth=1)
plt.scatter(z_, Br, s=5, color='blue')
plt.xlabel('z (mm)')
plt.ylabel('$B_r$ (T)')
plt.show()

















