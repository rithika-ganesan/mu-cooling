#########################################################
#                                                       #
#                   Dispersion -- g4bl                  #
#                                                       #
#########################################################

########## Settings ##########

input_file = "singlecoil"
output_file = "dp10-xoffset20"

######## Dependencies ########

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os
from pathlib import Path
import re

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
        dfs[name] = df#[df["EventID"] == -1]

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

############ Main ############

files = get_files(filenametype="trace_*.txt")
dfs, channels = get_dfs(files)

solLength = float(extract_params("solLength")[0])
solPosition = 0
edges = [solPosition - solLength / 2, solPosition + solLength / 2]

df = dfs[output_file]

ref = df[df["EventID"] == -1]
test = df[df["EventID"] == 1]

template = 0
if template == 1:
    plt.figure(figsize=(8, 6))
    plt.title('')

    plt.xlabel('')
    plt.ylabel('')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../plots/_.png', dpi=300)
    plt.show()

xvz = 0
if xvz == 1:
    plt.figure(figsize=(8, 6))
    plt.title('x vs. z -- $\delta p=10$MeV/c')

    plt.plot(ref['z'], ref['x'], label="Reference particle, p=200MeV/c")
    plt.plot(test['z'], test['x'], label="Test particle, p=210MeV/c")
    plt.axvline(3500, ls='--', lw=0.5, c='b')
    plt.plot([3500, 3500], [95, 115], lw=2, c='b')

    plt.xlabel('z (mm)')
    plt.ylabel('x (mm)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../plots/{output_file}-xvzalt.png', dpi=300)
    plt.show()

yvz = 0
if yvz == 1:
    plt.figure(figsize=(8, 6))
    plt.title('y vs. z -- $\delta p=10$MeV/c')

    plt.plot(ref['z'], ref['y'], label="Reference particle, p=200MeV/c")
    plt.plot(test['z'], test['y'], label="Test particle, p=210MeV/c")
    plt.axvline(3500, ls='--', lw=0.5)
    plt.plot([3500, 3500], [-62, -50], lw=2, c='b')
    
    plt.xlabel('z (mm)')
    plt.ylabel('y (mm)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../plots/{output_file}-yvzalt.png', dpi=300)
    plt.show()

zvt = 0
if zvt == 1:
    plt.figure(figsize=(8, 6))
    plt.title('z vs. t -- $\delta p=10$MeV/c')

    plt.plot(ref['t'], ref['z'], label="Reference particle, p=200MeV/c")
    plt.plot(test['t'], test['z'], label="Test particle, p=210MeV/c")
    plt.axhline(3500, ls='--', lw=0.5)
    #plt.plot([3500, 3500], [-62, -50], lw=2, c='b')
    
    plt.xlabel('t (ns)')
    plt.ylabel('z (mm)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../plots/{output_file}-zvt.png', dpi=300)
    plt.show()

ref = ref.reset_index()
test = test.reset_index()

rx, ry, rz = ref['x'], ref['y'], ref['z']
tx, ty, tz = test['x'], test['y'], test['z']

dx, dy, dz = rx - tx, ry - ty, rz - tz

s = np.sqrt(dx**2 + dy**2)

p = 200
dp = 10    
D = s * p / dp

plots = 1
if plots == 1:
    plt.figure(figsize=(8, 6))
    plt.title('s vs. z -- $\delta p=10$MeV/c')

    plt.scatter(ref['z'], s, s=0.01)

    plt.xlabel('z (mm)')
    plt.ylabel('s (mm)')
    #plt.legend()
    plt.tight_layout()
    plt.savefig(f'../plots/{output_file}-s.png', dpi=300)
    plt.show()

plotd = 1
if plotd == 1:
    plt.figure(figsize=(8, 6))
    plt.title('D vs. z -- $\delta p=10$MeV/c')

    plt.scatter(ref['z'], D, s=0.01)

    plt.xlabel('z (mm)')
    plt.ylabel('D (mm)')
    #plt.legend()
    plt.tight_layout()
    plt.savefig(f'../plots/{output_file}-D.png', dpi=300)
    plt.show()
