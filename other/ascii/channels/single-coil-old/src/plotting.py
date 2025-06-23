######################################################
#                                                    #
#       Script for plotting g4beamline output        #
#                                                    #
######################################################

########## Settings ##########

input_file = "singlecoil"        #name of the g4bl input file
use_channel = "deltap0"          #name of single channel

# switch, save, show
plot_options = {
    'x vs. z': [1, 0, 1],
    'y vs. z': [0, 0, 1],
    'p vs. x': [0, 0, 1],
    'px py pz vs. z': [0, 0, 1],
    'Bx By Bz vs. z': [0, 0, 1]
}

channel_labels = {
    "deltap0": "$\delta p = 0.0$"
}

######## Dependencies ########

import re
import glob
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

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

############ Main ############

files = get_files(filenametype="trace_*.txt")
dfs, channels = get_dfs(files)
if use_channel != None:
    channels_ = channels
    channels = [use_channel]

solLength = float(extract_params("solLength")[0])
solPosition = 0
edges = [solPosition - solLength / 2, solPosition + solLength / 2]

for channel in channels:
    df = dfs[channel]
    df = df[df["EventID"] == -1]
    #lbl = channel_labels[channel]
    lbl = "Reference particle, no offsets"
    

    #=============== x vs. z ================
    switch, save, show = plot_options['x vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'x vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['x'])
        plt.xlabel('z (mm)')
        plt.ylabel('x (mm)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'x-vs-z_{channel}.png', dpi=300)
        if show == 1:
            plt.show()


    #=============== y vs. z ================
    switch, save, show = plot_options['y vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'y vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['y'])
        plt.xlabel('z (mm)')
        plt.ylabel('y (mm)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'y-vs-z_{channel}.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== pi vs. xi ================
    switch, save, show = plot_options['p vs. x']
    if switch == 1:
        fig, axs = plt.subplots(1, 3, figsize=(12, 6))
        
        x, y = 'x', 'Px'
        axs[0].scatter(df[x], df[y])
        axs[0].plot(df[x], df[y], lw=1)
        axs[0].set_title(f'{labels[y]} vs. {labels[x]} -- {lbl}')
        axs[0].set_xlabel(f'{labels[x]}')
        axs[0].set_ylabel(f'{labels[y]}')

        x, y = 'y', 'Py'
        axs[1].scatter(df[x], df[y])
        axs[1].plot(df[x], df[y], lw=1)
        axs[1].set_title(f'{labels[y]} vs. {labels[x]} -- {lbl}')
        axs[1].set_xlabel(f'{labels[x]}')
        axs[1].set_ylabel(f'{labels[y]}')
        
        x, y = 'z', 'Pz'
        axs[2].plot(df[x], df[y], lw=1)
        axs[2].set_title(f'{labels[y]} vs. {labels[x]} -- {lbl}')
        axs[2].set_xlabel(f'{labels[x]}')
        axs[2].set_ylabel(f'{labels[y]}')

        plt.tight_layout()
        if save == 1:
            plt.savefig(f'p-vs-x_{channel}.png', dpi=300)
        if show == 1:
            plt.show()


    #=============== px py pz vs. z ================
    switch, save, show = plot_options['px py pz vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'p vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['Px'], label=f'{labels["Px"]}')
        plt.plot(df['z'], df['Py'], label=f'{labels["Py"]}')
        plt.plot(df['z'], df['Pz'], label=f'{labels["Pz"]}')
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('p (MeV/c)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'pxpypz-vs-z_{channel}.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== Bx By Bz vs. z ================
    switch, save, show = plot_options['Bx By Bz vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'B vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['Bx'], label=f'{labels["Bx"]}')
        plt.plot(df['z'], df['By'], label=f'{labels["By"]}')
        plt.plot(df['z'], df['Bz'], label=f'{labels["Bz"]}')
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('B (T)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'bxbybz-vs-z_{channel}.png', dpi=300)
        if show == 1:
            plt.show()
