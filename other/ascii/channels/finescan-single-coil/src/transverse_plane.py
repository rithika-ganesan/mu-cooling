######################################################
#                                                    #
#       Script for plotting g4beamline output        #
#                                                    #
######################################################

######## This script only plots the transverse B-field

########## Settings ##########

input_file = "singlecoil"        #name of the g4bl input file
use_channel = "nodet-xoffset020"          #name of single channel
#use_channel = None
single_channel = 1

multiplot_options = {
    'pz vs. z vary x-offset': [0, 1, 1],
    'p^2 vs. z vary x-offset': [0, 1, 1],
    'del p^2 vs. z vary x-offset': [0, 1, 1],
    '|del p^2| vs. z vary x-offset': [0, 1, 1]
}

channel_labels = {
    "deltap0": "$\delta p = 0.0$",
    "nodet-xoffset000": "No detectors, beam at X=0mm, Y=0mm",
    "nodet-xoffset020": "No detectors, beam at X=+20mm, Y=0mm",
    "nodet-xoffsetm020": "No detectors, beam at X=-20mm, Y=0mm",
    "nodet-yoffset020": "No detectors, beam at X=0mm, Y=+20mm",
    "nodet-yoffsetm020": "No detectors, beam at X=0mm, Y=-20mm",
    "nodet-xoffset020-yoffset020": "No detectors, beam at X=20mm, Y=20mm",
    "nodet-lb-xoffset020": "Beam starts at -10000"
}

######## Dependencies ########

import re
import glob
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import os

########### Labels ###########

#===== Labels for the data columns =====
tuple_labels=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "Tr    ackID", "ParentID", "Weight", "Bx", "By", "Bz", "Ex", "Ey", "Ez"]

#========== Units for the data =========
units = {
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

#============= Plot labels ==============
labels = {
    "x": "x (mm)",
    "y": "y (mm)",
    "z": "z (mm)",
    "Px": "$p_x$ (MeV/c)", 
    "Py": "$p_y$ (MeV/c)",
    "Pz": "$p_z$ (MeV/c)",
    "t": "$t$ (ns)",
    "PDGid": None,
    "EventID": None,
    "TrackID": None,
    "ParentID": None,
    "Weight": None,
    "Bx": "$B_x$ (T)",
    "By": "$B_y$ (T)",
    "Bz": "$B_z$ (T)",
    "Ex": "$E_x$ (MV/m)",
    "Ey": "$E_y$ (MV/m)",
    "Ez": "$E_z$ (MV/m)"
}

######### Functions ##########

#======= Get paths for input files ======
# Gets list of file paths matching input file type in ../output/ 
def get_files(filenametype):
    ROOT_DIR = Path(__file__).parent.parent
    file_ex = ROOT_DIR / 'output' / filenametype
    files = sorted(glob.glob(f"{file_ex}"))
    return files

#============= Read in data =============
# Read a .txt file as a pd dataframe
def read_ascii(path, comment='#'):
    df = pd.read_csv(f'{path}', comment=comment, header=None, sep='\\s+')
    length = df.shape[1]
    df.columns = tuple_labels[:length]
    return df

#====== Get dataframes and labels =======
# Get a dictionary of dataframes with the 'channel' name as keys
def get_dfs(files):
    dfs = {}
    for file in files:
        name = re.search(r'trace_(.*)\.txt$', file).group(1)
        df = read_ascii(file)
        dfs[name] = df[df["EventID"] == -1]

    channels = list(dfs.keys())

    return dfs, channels

#==== Get parameters from input file ====
def extract_params(match_word, filename_base=input_file, ext="in"):
    script_dir = Path(__file__).parent
    filepath = script_dir / f"{filename_base}.{ext}"

    # Match: param <match_word> = <val>
    pattern = re.compile(rf"\bparam\s+{re.escape(match_word)}\s*=\s*(\S+)\b")
    vals = []

    with filepath.open('r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                vals.append(match.group(1))  # Extract value after '='

    return vals

#===== Write position vector input ======
def get_position_vector(x, y):
    X = np.array([0, x])
    Y = np.array([0, y])
    return X, Y

############ Main ############

files = get_files(filenametype="trace_*.txt")
dfs, channels = get_dfs(files)

print(dfs.keys())

if use_channel != None:
    channels_ = channels
    channels = [use_channel]

solLength = float(extract_params("solLength")[0])
solPosition = 0
edges = [solPosition - solLength / 2, solPosition + solLength / 2]

channel = use_channel
#### plot one channel at a time:
df = dfs[channel]
df = df[df["EventID"] == -1] #reference particle
lbl = channel_labels[channel]
#lbl = "Reference particle, no offsets" 

z = df['z']
print(min(z), max(z))
br = np.sqrt(df['Bx']**2 + df['By']**2)
bnorm = max(br)

#=============== transverse plane r and B ================
frames = 1
val = 0
if frames == 1:
    for index, row in df.iterrows():
        if index % 1 == 0:
            z = row['z']
            fig = plt.figure(figsize=(6, 6))
            ax = fig.gca()
            plt.title(f'z = {z}mm')
            plt.axvline(0, ls='--', c='k', lw=0.5)
            plt.axhline(0, ls='--', c='k', lw=0.5)
            circle1 = plt.Circle((0.0, 0.0), 400, ls='--', lw=0.5, color='k', fill=False, label='Solenoid')
            circle2 = plt.Circle((0.0, 0.0), 500, ls='--', lw=0.5, color='k', fill=False)
            
            ax.add_patch(circle1)
            ax.add_patch(circle2)

            x, y, Bx, By = row['x'], row['y'], row['Bx'], row['By']
            r = np.sqrt(x**2 + y**2)
            #x, y = x * 1.1 / r, y * 1.1 / r
            rb = np.sqrt(Bx**2 + By**2)
            Bx, By = Bx * 300 / bnorm, By * 300 / bnorm
           
            plt.arrow(0, 0, Bx, By, head_width=25, head_length=25, lw=2, ec='tab:orange', facecolor='tab:orange', label='$B_T$', alpha=1)
            plt.scatter(x, y, s=10, c='tab:blue')
            plt.arrow(0, 0, x, y, head_width=0.03, head_length=0.05, lw=1.5, ec='tab:blue', facecolor='tab:blue', label='Position', alpha=1)
            
            plt.xlim([-600, 600])
            plt.ylim([-600, 600])
            #plt.xticks([-1, 0, 1])
            #plt.yticks([-1, 0, 1])
            plt.xticks([])
            plt.yticks([])
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend(loc='upper right')
            plt.tight_layout()
            plt.savefig(f'../plots/f3/im{index}.png', dpi=300)
            plt.close()
            #plt.show()



















