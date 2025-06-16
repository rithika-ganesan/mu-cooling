#################################################################
#                                                               #
#            g4bl analysis script -- matching hfofo             #
#                rithika ganesan | 06.16.2025                   #
#                                                               #
#################################################################

input_file = "matching"   

#========================== Dependencies ========================

import re
import glob
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from betterplots import *

#============================ Labels ============================

# Labels for trace output file data columns
tuple_labels=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight", "Bx", "By", "Bz", "Ex", "Ey", "Ez"]

# Units for the trace output file data
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

# Plot labels
col_labels = {
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

#========================== Functions ===========================

# Gets list of file paths matching input file type in ../output/ 
def get_files(filenametype):
    ROOT_DIR = Path(__file__).parent.parent
    file_ex = ROOT_DIR / 'output' / filenametype
    files = sorted(glob.glob(f"{file_ex}"))
    return files

# Read a .txt file as a pd dataframe
def read_ascii(path, comment='#'):
    df = pd.read_csv(f'{path}', comment=comment, header=None, sep='\\s+')
    length = df.shape[1]
    df.columns = tuple_labels[:length]
    return df

# Get a dictionary of dataframes with the 'channel' name as keys
def get_dfs(files):
    dfs = {}
    for file in files:
        name = re.search(r'trace_(.*)\.txt$', file).group(1)
        df = read_ascii(file)
        dfs[name] = df#[df["EventID"] == -1]

    channels = list(dfs.keys())

    return dfs, channels

# Get parameters from input file 
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

# Create and add patch for g4bl element along the z-axis
def add_element_patch(ax, name, length, inner, outer, z, facecolor, alpha=0.3):
    x = z - (length / 2)
    y = -inner
    xlen = length
    ylen = inner*2

    middle = patches.Rectangle((x, y), xlen, ylen, facecolor=facecolor, alpha=alpha*0.5, label=name)

    yt = inner
    yb = -outer
    yylen = outer - inner

    top = patches.Rectangle((x, yt), xlen, yylen, facecolor=facecolor, alpha=alpha)    
    bottom = patches.Rectangle((x, yb), xlen, yylen, facecolor=facecolor, alpha=alpha)

    ax.add_patch(top)
    ax.add_patch(bottom)
    ax.add_patch(middle)
    ax.legend()
    ax.set_zorder(1)
    ax.patch.set_visible(False)

    return ax

# Create and add patch for g4bl element along the z-axis
# Angle is in degrees and is anticlockwise from x-axis
def add_element_patch(ax, name, length, inner, outer, z, pitch, facecolor, alpha=0.3):
    x = z - (length / 2)
    y = -inner
    xlen = length
    ylen = inner*2

    middle = patches.Rectangle((x, y), xlen, ylen, facecolor=facecolor, alpha=alpha*0.5, label=name, rotation_point='center', angle=pitch)

    yt = inner
    yb = -outer
    yylen = outer - inner

    top = patches.Rectangle((x, yt), xlen, yylen, facecolor=facecolor, alpha=alpha, rotation_point='center', angle=pitch)    
    bottom = patches.Rectangle((x, yb), xlen, yylen, facecolor=facecolor, alpha=alpha, rotation_point='center', angle=pitch)

    ax.add_patch(top)
    ax.add_patch(bottom)
    ax.add_patch(middle)
    ax.legend()
    ax.set_zorder(1)
    ax.patch.set_visible(False)

    return ax

# Make a plot directly from the dataframe
def lineplot(channel, x, y, eventid,
            figsize=(12, 9),
            fig=None,
            ax=None,
            title=None,
            xlims=None,
            ylims=None,
            lw=1,
            ls='-',
            col_labels=col_labels,
            label=None
    ):
    df = dfs[channel]
    df = df[df["EventID"] == eventid]

    if title == None:
        title = f"{col_labels[y]} vs. {col_labels[x]}"

    #if label == None:
    #    label = f'{col_labels[y]}'
    
    if fig == None and ax == None:
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlabel(col_labels[x])
        ax.set_ylabel(col_labels[y])
        if xlims != None:
            ax.set_xlim(xlims)
        if ylims != None:
            ax.set_ylim(ylims)
        ax.set_title(title)
        fig.tight_layout()
    
    ax.plot(df[x], df[y], lw=lw, ls=ls, label=label)
    
    if len(ax.lines) > 1:
        ax.legend()
    
    return fig, ax


def scatterplot(channel, x, y, eventid,
            figsize=(12, 9),
            fig=None,
            ax=None,
            title=None,
            xlims=None,
            ylims=None,
            s=3,
            m='o',
            col_labels=col_labels,
            label=None
    ):
    df = dfs[channel]
    df = df[df["EventID"] == eventid]
    
    if title == None:
        title = f"{col_labels[y]} vs. {col_labels[x]}"

    #if label == None:
    #    label = f'{col_labels[y]}'
    
    if fig == None and ax == None:
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlabel(col_labels[x])
        ax.set_ylabel(col_labels[y])
        if xlims != None:
            ax.set_xlim(xlims)
        if ylims != None:
            ax.set_ylim(ylims)
        ax.set_title(title)
        fig.tight_layout()
    
    ax.scatter(df[x], df[y], s=s, marker=m, label=label)

    if len(ax.collections) > 1:
        ax.legend()

    return fig, ax

#============================= Main =============================


files = get_files(filenametype="*.txt")
dfs, channels = get_dfs(files)

df = dfs['solenoids-nostoc']

print(dfs.keys())

fig, ax = lineplot('solenoids-nostoc', 'z', 'x', -1, label=None)

#for i in np.arange(2, 11, 1):
#    fig, ax = lineplot('solenoids-nostoc', 'z', 'x', i, fig=fig, ax=ax, label=None)

#rotsol = patches.Rectangle((-6000, -350), 6000, 700, linewidth=0, facecolor=params["RotSol"]["color"], alpha=0.3, label="RotSol")
#rotsoltop = patches.Rectangle((-6000, 350), 6000, 150, linewidth=0, facecolor=params["RotSol"]["color"], alpha=0.9)
#rotsolbottom = patches.Rectangle((-6000, -500), 6000, 150, linewidth=0, facecolor=params["RotSol"]["color"], alpha=0.9)

#terminus = patches.Rectangle((-1000, -360), 1, 720, linewidth=1, color='gray', facecolor=(0.1, 0.1, 0.1), alpha=0.9, label="Terminus")

#solpos = patches.Rectangle((-350, -420), 300, 840, linewidth=0, facecolor=(1.0, 0.0, 0.0), alpha=0.5, label="SolPos")

#rect2 = patches.Rectangle((600, -100), 200, 200, linewidth=0, facecolor='blue', alpha=0.2)

#ax.add_patch(rotsol)
#ax.add_patch(rotsoltop)
#ax.add_patch(rotsolbottom)
#ax.add_patch(terminus)
#ax.add_patch(solpos)

ax = add_element_patch(ax, "RotSol", 6000, 360, 500, -3000, 0, (1.0, 0.8, 1.0), 0.5)
ax = add_element_patch(ax, "SolPos", 300, 420, 600, 500, 0, (1.0, 0.0, 0.0), 0.5)
ax = add_element_patch(ax, None, 300, 420, 600, 1900, 0.08864577034195348, (1.0, 0.0, 0.0), 0.5)
ax = add_element_patch(ax, None, 300, 420, 600, 3300, 0.08629462092385154, (1.0, 0.0, 0.0), 0.5)
ax = add_element_patch(ax, "SolNeg", 300, 420, 600, 1200, 0, (0.0, 0.0, 1.0), 0.5)
ax = add_element_patch(ax, None, 300, 420, 600, 2600, 0.12464581967694571, (0.0, 0.0, 1.0), 0.5)
ax = add_element_patch(ax, None, 300, 420, 600, 4000, 0.08165184417494886, (0.0, 0.0, 1.0), 0.5)

ax.set_title("Trajectory in x with only solenoids present (no stochastics)")

#plt.savefig(f"../plots/xvz-onlysolenoids.png", dpi=300)
plt.show()



