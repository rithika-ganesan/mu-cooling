# Plot Br vs z, Bz vs z for the reference particle
# Rithika Ganesan | May 2025

import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

######## Get filepaths ##########
directory = '/Users/rithika/utkcms/hfofo/'
path_format = 'basics/AllTracks.txt'
file_path = directory + path_format

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

# Read a .txt file produced from g4bl 
def read_ascii(path, comment='#'):
    df = pd.read_csv(f'{path}', comment=comment, header=None, sep='\\s+')
    if df.shape[1] == 12:
        df.columns = tuple_labels_noEM
    elif df.shape[1] == 18:
        df.columns = tuple_labels
    else:
        raise ValueError("Unknown parameters in data file.")
    
    return df

# If two successive entries have the same value under col_name, latter entry is dropped
def drop_copies(df, col_name='z'):
    length = len(df)
    col = df[col_name]
    indices = []
    for i in range(length - 1):
        denom = col[i+1] - col[i]
        if denom == 0.0:
            indices.append(i+1)
    
    df = df.drop(indices).reset_index(drop=True)

    return df, indices

# Get new z and Br 
def get_br(df):
    # Assuming B_r(r, z) = -\frac{r}{2} \frac{\partial B_z}{\partial z}
    # First get r
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
    return z_, Br

############### MAIN  ###############

#plot_dir_path = directory + "/plots/" + "br"
#os.makedirs(plot_dir_path, exist_ok=True)

df = read_ascii(file_path)
print("Length of file before dropping copies:", len(df))

df, indices = drop_copies(df)
print("Length of file after dropping copies:", len(df))

df = df[df["EventID"] == -1]
df = df.reset_index()
print("Length of file after getting only ref particle:", len(df))

z, Bz = df['z'], df['Bz']
z_, Br = get_br(df)
eventid = df['EventID'].iloc[0]

max_x = max(max(z), max(z_))
min_x = min(min(z), min(z_))
period = 4200

n = np.ceil((max_x - min_x) / period).astype(int)

#n=10

#for i in range(n):
#    l, m = i*period, i*period + period

fig, axs = plt.subplots(2, 1, figsize=(8, 6))

axs[0].plot(z, Bz, color='k', linewidth=1)
axs[0].scatter(z, Bz, s=3, color='red')
axs[0].set_xlabel('z (mm)')
#axs[0].set_xlim([l, m])
axs[0].set_ylabel('$B_z$ (T)')
axs[0].set_title(f'$B_z$ vs. z')

axs[1].plot(z_, Br, color='k', linewidth=1)
axs[1].scatter(z_, Br, s=3, color='blue')
axs[1].set_xlabel('z (mm)')
#axs[1].set_xlim([l, m])
axs[1].set_ylabel('$B_r$ (T)')
axs[1].set_title(f'$B_r$ vs. z')

plt.tight_layout()
plt.savefig(f'refsingle.png', dpi=300)
plt.show()

# Okay to loop as long as there are 20 or fewer files
# for i, file in enumerate(files):
#     df = read_ascii(file)
#     z, Bz = df['z'], df['Bz']
#     df, indices = drop_copies(df)
#     z_, Br = get_br(df)
#     eventid = df['EventID'][0]
# 
#     fig, axs = plt.subplots(2, 1, figsize=(8, 6))
#    
#     axs[0].plot(z, Bz, color='k', linewidth=1)
#     axs[0].scatter(z, Bz, s=3, color='red')
#     axs[0].set_xlabel('z (mm)')
#     axs[0].set_ylabel('$B_z$ (T)')
#     axs[0].set_title(f'$B_r$')
# 
#     axs[1].plot(z_, Br, color='k', linewidth=1)
#     axs[1].scatter(z_, Br, s=3, color='blue')
#     axs[1].set_xlabel('z (mm)')
#     axs[1].set_ylabel('$B_r$ (T)')
#     axs[1].set_title(f'$B_r$ vs. z (Event {eventid})')
# 
#     plt.tight_layout()
#     plt.savefig(f'{plot_dir_path}/br_bz_{i}.png')
# 
#     plt.show()











