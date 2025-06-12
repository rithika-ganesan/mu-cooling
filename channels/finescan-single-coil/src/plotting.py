######################################################
#                                                    #
#       Script for plotting g4beamline output        #
#                                                    #
######################################################

########## Settings ##########

input_file = "singlecoil"        #name of the g4bl input file
use_channel = ["xoffset20"]          #name of single channel
#use_channel = None

import warnings

# Globally ignore SyntaxWarning
warnings.filterwarnings("ignore", category=SyntaxWarning)

# switch, save, show
plot_options = {
    'x vs. z': [0, 1, 1],
    'y vs. z': [0, 1, 1],
    'p vs. x': [0, 1, 1],
    'pz vs. z': [0, 1, 1],
    'px py vs. z': [0, 1, 1],
    'px+py vs. z': [0, 1, 1],
    'px py pz vs. z': [0, 1, 1],
    'ptsquared vs. z': [0, 1, 1],
    'psquared vs. z': [1, 1, 1],
    'p vs. z': [0, 1, 0],
    'Bx By vs. z': [0, 1, 1],
    'Bx By Bz vs. z': [0, 1, 1],
    'phi_r vs. phi_B': [0, 0, 1],
    'transverse plane r and B': [0, 0, 1],
    'ref test comparison': [0, 0, 1],
    'rB vs. r': [0, 0, 1],
    'rB vs. z': [0, 1, 1],
    'Lz vs. z': [0, 1, 1]
}

analysis_options = {
    'phase advance': 0,
    'net phase': 0,
    'numbers': 0,
    'write clean output': 0,
    'tof -- full length': 0,
    'tof -- pz': 0,
    't vs. z': 0,
    'tof vs. z': 0
}

multiplot_options = {
    'pz vs. z vary x-offset': [0, 1, 1],
    'p^2 vs. z vary x-offset': [0, 1, 1],
    'del p^2 vs. z vary x-offset': [0, 1, 1],
    '|del p^2| vs. z vary x-offset': [0, 1, 1]
}

channel_labels = {
    "xoffset20": "Beam at X=20mm, Y=0mm",
    "deltap0": "$\delta p = 0.0$",
    "nodet-xoffset000": "No detectors, beam at X=0mm, Y=0mm",
    "nodet-xoffset020": "No detectors, beam at X=+20mm, Y=0mm",
    "nodet-dp0p1-xoffset020": "No detectors, beam at X=+20mm, Y=0mm, and $\delta p = 0.1$",
    "det-dp0p1-xoffset020": "Detectors at 5000mm intervals, beam at X=+20mm, Y=0mm, and $\delta p = 0.1$",
    "no-offset": "No offsets"
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

#print(dfs.keys())

if use_channel != None:
    channels_ = channels
    channels = use_channel


solLength = float(extract_params("solLength")[0])
solPosition = 0
edges = [solPosition - solLength / 2, solPosition + solLength / 2]

lists = []
#### plot one channel at a time:
for channel in channels:
    df = dfs[channel]
    df = df[df["EventID"] == -1]
    #ref = df[df["EventID"] == -1]
    #test = df[df["EventID"] == 1]
    lbl = channel_labels["xoffset20"]
    #lbl = "Reference particle, no offsets"
    

    #=============== x vs. z ================
    switch, save, show = plot_options['x vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'x vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['x'])
        plt.xlabel('z (mm)')
        plt.ylabel('x (mm)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_x-vs-z.png', dpi=300)
        if show == 1:
            plt.show()


    #=============== y vs. z ================
    switch, save, show = plot_options['y vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'y vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['y'])
        plt.xlabel('z (mm)')
        plt.ylabel('y (mm)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_y-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== pi vs. xi ================
    switch, save, show = plot_options['p vs. x']
    if switch == 1:
        fig, axs = plt.subplots(1, 3, figsize=(12, 6))
        
        x, y = 'x', 'Px'
        axs[0].scatter(df[x], df[y], s=3)
        axs[0].plot(df[x], df[y], lw=1)
        axs[0].set_title(f'{labels[y]} vs. {labels[x]}')
        axs[0].set_xlabel(f'{labels[x]}')
        axs[0].set_ylabel(f'{labels[y]}')

        x, y = 'y', 'Py'
        axs[1].scatter(df[x], df[y], s=3)
        axs[1].plot(df[x], df[y], lw=1)
        axs[1].set_title(f'{labels[y]} vs. {labels[x]}')
        axs[1].set_xlabel(f'{labels[x]}')
        axs[1].set_ylabel(f'{labels[y]}')
        
        x, y = 'z', 'Pz'
        axs[2].plot(df[x], df[y], lw=1)
        axs[2].set_title(f'{labels[y]} vs. {labels[x]}')
        axs[2].set_xlabel(f'{labels[x]}')
        axs[2].set_ylabel(f'{labels[y]}')
        
        fig.suptitle(f'p vs. x -- {lbl}')

        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_p-vs-x.png', dpi=300)
        if show == 1:
            plt.show()

    #=============== pz vs. z ================
    switch, save, show = plot_options['pz vs. z']
    if switch == 1:
        #idx, idy = df[df['Px'] != 0].index[0], df[df['Py'] != 0].index[0]
        #print(df['z'][idx], df['z'][idy]) 
        
        plt.figure(figsize=(10, 5))
        plt.title(f'$p_z$ vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.plot(df['z'], df['Pz'], lw=1, label=f'{labels["Pz"]}')
        #plt.scatter(df['z'], df['Pz'], s=5, c='k')        
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('$p_z$ (MeV/c)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_pz-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== px+py vs. z ================
    switch, save, show = plot_options['px+py vs. z']
    if switch == 1:
        #idx, idy = df[df['Px'] != 0].index[0], df[df['Py'] != 0].index[0]
        #print(df['z'][idx], df['z'][idy]) 
        
        plt.figure(figsize=(10, 5))
        plt.title(f'$p_x + p_y$ vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k', label='Solenoid edges')
        #plt.scatter(df['z'], df['Px'], s=5)#, label=f'{labels["Px"]}')
        #plt.scatter(df['z'], df['Py'], s=5)#, label=f'{labels["Py"]}')
        plt.plot(df['z'], df['Px'] + df['Py'], label=f'$p_x + p_y$')
        plt.legend()
        #plt.xlim([-3000, 3000])   # not automated !!  
        plt.xlabel('z (mm)')
        plt.ylabel('p (MeV/c)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_px-plus-py-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== px py vs. z ================
    switch, save, show = plot_options['px py vs. z']
    if switch == 1:
        #idx, idy = df[df['Px'] != 0].index[0], df[df['Py'] != 0].index[0]
        #print(df['z'][idx], df['z'][idy]) 
        
        plt.figure(figsize=(8, 6))
        plt.title(f'p vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.scatter(df['z'], df['Px'], s=5)#, label=f'{labels["Px"]}')
        plt.scatter(df['z'], df['Py'], s=5)#, label=f'{labels["Py"]}')
        plt.plot(df['z'], df['Px'], label=f'{labels["Px"]}')
        plt.plot(df['z'], df['Py'], label=f'{labels["Py"]}')
        plt.legend()
        plt.xlim([-3000, 3000])   # not automated !!  
        plt.xlabel('z (mm)')
        plt.ylabel('p (MeV/c)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_pxpy-vs-z.png', dpi=300)
        if show == 1:
            plt.show()

    #=============== px py pz vs. z ================
    switch, save, show = plot_options['px py pz vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'p vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['Px'], label=f'{labels["Px"]}')
        plt.plot(df['z'], df['Py'], label=f'{labels["Py"]}')
        plt.plot(df['z'], df['Pz'], label=f'{labels["Pz"]}')
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('p (MeV/c)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_pxpypz-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== p_t^2 vs. z ================
    switch, save, show = plot_options['ptsquared vs. z']
    if switch == 1:
        plt.figure(figsize=(10, 6))
        plt.title(f'$p_T^2$ vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        #plt.axhline(40000.0, ls='--', lw=0.5, c='b') 
        #plt.axhline(40000.07857, ls='--', lw=0.5, c='b') 
        ptsquare = df['Px']**2 + df['Py']**2 
        #print(np.array(psquare)[-50])
        plt.plot(df['z'], ptsquare, label='$p^2 = p_x^2 + p_y^2$')
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('$p_T^2 (MeV^2/c^2)$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_ptsquare-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== p^2 vs. z ================
    switch, save, show = plot_options['psquared vs. z']
    if switch == 1:
        plt.figure(figsize=(12, 8))
        plt.title(f'$p^2$ vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=1, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=1, c='k')
        #plt.axhline(40000.0, ls='--', lw=0.5, c='b') 
        #plt.axhline(40000.07857, ls='--', lw=0.5, c='b') 
        psquare = df['Px']**2 + df['Py']**2 + df['Pz']**2
        maxval = np.array(psquare)[-50]
        print(maxval)
        #plt.axhline(maxval, ls='--', lw=0.5, c='b') 
        plt.plot(df['z'], psquare, label='$p^2 = p_x^2 + p_y^2 + p_z^2$')
        plt.legend(loc='lower left')
        plt.xlim([-1000, 1000])
        plt.xlabel('z (mm)')
        plt.ylabel('$p^2 (MeV^2/c^2)$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_psquarezoom-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== p vs. z ================
    switch, save, show = plot_options['p vs. z']
    if switch == 1:
        plt.figure(figsize=(10, 6))
        plt.title(f'$p$ vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.axhline(200.0, ls='--', lw=0.5, c='b') 
        plt.axhline(200.00019642, ls='--', lw=0.5, c='b') 
        plt.axhline(200.00021701, ls='--', lw=0.5, c='b') 
        #plt.axhline(40000.0, ls='--', lw=0.5, c='b') 
        #plt.axhline(40000.07857, ls='--', lw=0.5, c='b') 
        p = (df['Px']**2 + df['Py']**2 + df['Pz']**2)**0.5
        print(np.array(p)[-50])
        plt.plot(df['z'], p, label='$p = (p_x^2 + p_y^2 + p_z^2)^{0.5}$')
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('$p (MeV/c)$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_p-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== Bx By vs. z ================
    switch, save, show = plot_options['Bx By vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'B vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['Bx'], label=f'{labels["Bx"]}')
        plt.plot(df['z'], df['By'], label=f'{labels["By"]}')
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('B (T)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_bxby-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== Bx By Bz vs. z ================
    switch, save, show = plot_options['Bx By Bz vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'B vs. z -- {lbl}')
        plt.axvline(edges[0], ls='--', lw=0.5, c='k', label='Solenoid edges')
        plt.axvline(edges[1], ls='--', lw=0.5, c='k')
        plt.plot(df['z'], df['Bx'], label=f'{labels["Bx"]}')
        plt.plot(df['z'], df['By'], label=f'{labels["By"]}')
        plt.plot(df['z'], df['Bz'], label=f'{labels["Bz"]}')
        print(max(df['Bz']))
        plt.legend()
        plt.xlabel('z (mm)')
        plt.ylabel('B (T)')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_bxbybz-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== phi_r vs. phi_B   ================
    switch, save, show = plot_options['phi_r vs. phi_B']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'$\phi_r$ vs. $\phi_B$ -- {lbl}')
       
        x, y, Bx, By = df['x'], df['y'], df['Bx'], df['By']

        ### Check if B vector and r vector are in the same direction
        phi_r = np.arctan2(y, x)
        phi_B = np.arctan2(By, Bx)

        plt.scatter(phi_r, phi_B, s=5)

        #plt.plot(df['z'], df['Bx'], label=f'{labels["Bx"]}')
        #plt.plot(df['z'], df['By'], label=f'{labels["By"]}')
        
        plt.legend()
        plt.xlabel('$\phi_r$')
        plt.ylabel('$\phi_B$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_phir-vs-phiB.png', dpi=300)
        if show == 1:
            plt.show()

    #=============== transverse plane r and B ================
    switch, save, show = plot_options['transverse plane r and B']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'$\phi_r$ vs. $\phi_B$ -- {lbl}')
       
        x, y, Bx, By = df['x'], df['y'], df['Bx'], df['By']

        ### Check if B vector and r vector are in the same direction
        phi_r = np.arctan2(y, x)
        phi_B = np.arctan2(By, Bx)

        plt.scatter(phi_r, phi_B, s=5)

        #plt.plot(df['z'], df['Bx'], label=f'{labels["Bx"]}')
        #plt.plot(df['z'], df['By'], label=f'{labels["By"]}')
        
        plt.legend()
        plt.xlabel('$\phi_r$')
        plt.ylabel('$\phi_B$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_phir-vs-phiB.png', dpi=300)
        if show == 1:
            plt.show()
    

    #=============== rB vs. r  ================
    switch, save, show = plot_options['rB vs. r']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'$r_B$ vs. r -- {lbl}')
       
        #df = df[df['z'] < 1000]

        x, y, Bx, By = df['x'], df['y'], df['Bx'], df['By']

        ### Check if B vector and r vector are in the same direction
        phi_r = np.arctan2(y, x)
        phi_B = np.arctan2(By, Bx)

        r = np.sqrt(x**2 + y**2)
        rB = np.sqrt(Bx**2 + By**2)

        plt.scatter(r, rB, s=5)
        plt.plot(r, rB, lw=1)
        #plt.plot(df['z'], df['Bx'], label=f'{labels["Bx"]}')
        #plt.plot(df['z'], df['By'], label=f'{labels["By"]}')
        
        plt.legend()
        plt.xlabel('$r$')
        plt.ylabel('$r_B$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_rB-vs-r.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== rB vs. z  ================
    switch, save, show = plot_options['rB vs. z']
    if switch == 1:
        plt.figure(figsize=(10, 4))
        plt.title(f'$r_B$ vs. z -- {lbl}')
       
        #df = df[df['z'] < 1000]

        x, y, Bx, By = df['x'], df['y'], df['Bx'], df['By']
        z = df['z']
        ### Check if B vector and r vector are in the same direction
        phi_r = np.arctan2(y, x)
        phi_B = np.arctan2(By, Bx)

        r = np.sqrt(x**2 + y**2) 
        r = r / max(r)
        rB = np.sqrt(Bx**2 + By**2) 
        rB = rB / max(rB)

        plt.plot(z, r, lw=1, label='Position')
        plt.plot(z, rB, lw=1, label='B-field')
        #plt.plot(df['z'], df['Bx'], label=f'{labels["Bx"]}')
        #plt.plot(df['z'], df['By'], label=f'{labels["By"]}')
        
        plt.legend()
        plt.xlabel('$z$')
        plt.ylabel('$r_B$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_rB-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== Lz vs. z  ================
    switch, save, show = plot_options['Lz vs. z']
    if switch == 1:
        plt.figure(figsize=(8, 6))
        plt.title(f'$L_z$ vs. z -- {lbl}')
       
        x, y, px, py = df['x'], df['y'], df['Px'], df['Py']
        z = df['z']

        Lz = x * py - y * px

        plt.plot(z, Lz, lw=1)
        
        plt.legend()
        plt.xlabel('$z$')
        plt.ylabel('$L_z$')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{channel}_Lz-vs-z.png', dpi=300)
        if show == 1:
            plt.show()
    
    #=============== count tracks ================
    switch, save, show = plot_options['ref test comparison']
    if switch == 1:
        # got these values from checking manually what the duplicates were
        lists.append(np.unique(test['z']))
        z_vals = [-0.000500, 0.000500, 5000.0]
        for z in z_vals:
            index = ref[ref['z'] == z].index
            print(ref.iloc[index])
            index = test[test['z'] == z].index
            print(test.iloc[index])
#a, b = lists[0], lists[1]
#print(len(a), len(b))
#b = np.append(b, np.array([0,0,0]))


#z_values = pd.DataFrame({'Det': a, 'No Det': b})
#z_values.to_csv('../output/zvals_test.csv', index=False)  # index=False omits row numbers

##########################################################
#                         Analysis                       #
##########################################################

    if analysis_options['net phase'] == 1:
        z = df['z']
        print(min(z), max(z))
        x, y = df['x'], df['y']
        Bz = df['Bz']

        phi = np.array(np.arctan2(y, x))

        ##### SITUATION SPECIFIC NOT A GLOBAL FORMULA
        print(2*np.pi + np.abs(phi[-1]))

        #plt.scatter(z, phi, s=1)
        #plt.xlim([-5000, 10000])
        #plt.xlabel('z (mm)')
        #plt.show()

    if analysis_options['phase advance'] == 1:
        #e = 1.602176634e-19 #Coulombs
        e = 1
        m_mu = 105.7 #MeV/c^2
        cofactor = e / (2 * m_mu)
        c = 2.998e8 #m/s    

        Bz = max(df['Bz'])
        p = 200
        
        beta = p / np.sqrt(m_mu**2 + p**2)
        gamma = 1 / np.sqrt(1 - beta**2)

        print("Beta:", beta)

        mu = cofactor * Bz / (gamma * beta)

        print("Phase advance:", mu)

    if analysis_options['numbers'] == 1:
        z = np.array(df['z'])
        z0 = z[0]

        print(type(z0))


    if analysis_options['write clean output'] == 1:
        x, y = df['z'], df['Pz']
        out_df = pd.DataFrame({'z': df['z'], 'pz': df['Pz']})
        print(out_df.shape)
        out_df.to_csv(f'../output/{channel}-z-pz.csv', header=False, index=False)

    if analysis_options['tof -- full length'] == 1:
        maxStep = 5.00 #mm -- L z
        m = 105.7
        c = 3e8
        tof = []
        x, y, z = df['x'], df['y'], df['z']
        px, py, pz = df['Px'], df['Py'], df['Pz']
        L = []

        for i in range(len(df) - 1):
            x2, y2, z2 = x.iloc[i+1], y.iloc[i+1], z.iloc[i+1]
            x1, y1, z1 = x.iloc[i], y.iloc[i], z.iloc[i]
            l = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            L.append(l)

            px2, py2, pz2 = px.iloc[i+1], py.iloc[i+1], pz.iloc[i+1]
            px1, py1, pz1 = px.iloc[i], py.iloc[i], pz.iloc[i]

            vx2, vy2 = px2 / m, py2 / m  
            vx1, vy1 = px1 / m, py1 / m

            bz2 = pz2 / np.sqrt(m**2 + pz2**2)
            bz1 = pz1 / np.sqrt(m**2 + pz1**2)
            vz2, vz1 = bz2 * c, bz1 * c

            v2 = np.sqrt(vx2**2 + vy2**2 + vz2**2)
            v1 = np.sqrt(vx1**2 + vy1**2 + vz1**2)
            
            tof.append(l * ((1/v1) - (1/v2)))

        zz = z[1:]
        plt.scatter(z[1:], tof, s=4)
        plt.show()
    
    if analysis_options['tof -- pz'] == 1:
        maxStep = 5.00 #mm -- L z
        m = 105.7
        c = 3e8
        tof = []
        x, y, z = df['x'], df['y'], df['z']
        px, py, pz = df['Px'], df['Py'], df['Pz']
        L = []

        for i in range(len(df) - 1):

            px2, py2, pz2 = px.iloc[i+1], py.iloc[i+1], pz.iloc[i+1]
            px1, py1, pz1 = px.iloc[i], py.iloc[i], pz.iloc[i]

            vx2, vy2 = px2 / m, py2 / m  
            vx1, vy1 = px1 / m, py1 / m

            bz2 = pz2 / np.sqrt(m**2 + pz2**2)
            bz1 = pz1 / np.sqrt(m**2 + pz1**2)
            vz2, vz1 = bz2 * c, bz1 * c

            v2 = np.sqrt(vx2**2 + vy2**2 + vz2**2)
            v1 = np.sqrt(vx1**2 + vy1**2 + vz1**2)
            
            tof.append(maxStep * ((1/v1) - (1/v2)))

        zz = z[1:]
        plt.scatter(z[1:], tof, s=4)
        plt.show()

    if analysis_options['t vs. z'] == 1:
        t, z = df['t'], df['z']
        plt.scatter(z, t, s=3)
        plt.show()

    if analysis_options['tof vs. z'] == 1:
        t, z = df['t'], df['z']
        dt = []
        for i in range(len(df) - 1):
            delt = t.iloc[i+1] - t.iloc[i]
            dt.append(delt)

        plt.figure(figsize=(10, 5))
        plt.plot(z[1:], dt, lw=0.5)
        #plt.scatter(z[1:], dt, marker='.', s=1)
        plt.xlabel('z (mm)')
        plt.ylabel('$\Delta t$ (ns)')
        plt.ylim([0.01875, 0.019])
        #plt.savefig(f'../plots/tof-vs-z.png', dpi=300)
        plt.show()


##########################################################
#                    Multi-channel plots                 #
##########################################################


### Plot more than one channel at a time
#====================== pz vs. z =======================
#==== this one loops over different x-offset values ====
switch, save, show = multiplot_options['pz vs. z vary x-offset']
if switch == 1:
    x_vals = np.arange(0, 220, 20)
    files = sorted(glob.glob('../output/trace_nodet-xoffset*.txt'))
    plt.figure(figsize=(10, 5))
    plt.title('$p_z$ vs. z for different X')
    plt.axvline(edges[0], ls='--', lw=0.5, c='k')
    plt.axvline(edges[1], ls='--', lw=0.5, c='k')
    for i, file in enumerate(files):
        channel = re.search(r'trace_(.*)\.txt$', file).group(1)
        x_val = x_vals[i] 
        df = dfs[channel]
        df = df[df["EventID"] == -1]
        plt.plot(df['z'], df['Pz'], label=f'X=+{x_val}mm')
    plt.legend()
    plt.xlabel('z (mm)')
    plt.ylabel('$p_z$ (MeV/c)')
    plt.tight_layout()
    if save == 1:
        plt.savefig(f'../plots/x-offset_pz-vs-z.png', dpi=300)
    if show == 1:
        plt.show()


#===================== p^2 vs. z =======================
#==== this one loops over different x-offset values ====
switch, save, show = multiplot_options['p^2 vs. z vary x-offset']
if switch == 1:
    x_vals = np.arange(0, 220, 20)
    files = sorted(glob.glob('../output/trace_nodet-xoffset*.txt'))
    plt.figure(figsize=(10, 5))
    plt.title('$p^2$ vs. z for different X')
    plt.axvline(edges[0], ls='--', lw=0.5, c='k')
    plt.axvline(edges[1], ls='--', lw=0.5, c='k')
    for i, file in enumerate(files):
        channel = re.search(r'trace_(.*)\.txt$', file).group(1)
        x_val = x_vals[i] 
        df = dfs[channel]
        df = df[df["EventID"] == -1]
        psquare = df['Px']**2 + df['Py']**2 + df['Pz']**2
        plt.plot(df['z'], psquare, label=f'X=+{x_val}mm')
    plt.legend()
    plt.xlabel('z (mm)')
    plt.ylabel('$p^2 = p_x^2 + p_y^2 + p_z^2$ (MeV/c)')
    plt.tight_layout()
    if save == 1:
        plt.savefig(f'../plots/x-offset_psquare-vs-z.png', dpi=300)
    if show == 1:
        plt.show()

#===================== del p^2 vs. z =======================
#==== this one loops over different x-offset values ====
switch, save, show = multiplot_options['del p^2 vs. z vary x-offset']
if switch == 1:
    x_vals = np.arange(0, 220, 20)
    files = sorted(glob.glob('../output/trace_nodet-xoffset*.txt'))
    plt.figure(figsize=(10, 5))
    plt.title('$p_0^2 - p^2$ vs. z for different X')
    plt.axvline(edges[0], ls='--', lw=0.5, c='k')
    plt.axvline(edges[1], ls='--', lw=0.5, c='k')
    for i, file in enumerate(files):
        channel = re.search(r'trace_(.*)\.txt$', file).group(1)
        x_val = x_vals[i] 
        df = dfs[channel]
        df = df[df["EventID"] == -1]
        psquare = df['Px']**2 + df['Py']**2 + df['Pz']**2
        plt.plot(df['z'], 40000.0 - psquare, label=f'X=+{x_val}mm')
    plt.legend()
    plt.xlabel('z (mm)')
    plt.ylabel('$p_0^2 - p^2, p^2 = p_x^2 + p_y^2 + p_z^2$ (MeV/c)')
    plt.tight_layout()
    if save == 1:
        plt.savefig(f'../plots/x-offset_del-psquare-vs-z.png', dpi=300)
    if show == 1:
        plt.show()

#===================== |del p^2}| vs. z =======================
#==== this one loops over different x-offset values ====
switch, save, show = multiplot_options['|del p^2| vs. z vary x-offset']
if switch == 1:
    x_vals = np.arange(0, 220, 20)
    files = sorted(glob.glob('../output/trace_nodet-xoffset*.txt'))
    plt.figure(figsize=(10, 5))
    plt.title('$|p_0^2 - p^2|$ vs. z for different X')
    plt.axvline(edges[0], ls='--', lw=0.5, c='k')
    plt.axvline(edges[1], ls='--', lw=0.5, c='k')
    for i, file in enumerate(files):
        channel = re.search(r'trace_(.*)\.txt$', file).group(1)
        x_val = x_vals[i] 
        df = dfs[channel]
        df = df[df["EventID"] == -1]
        psquare = df['Px']**2 + df['Py']**2 + df['Pz']**2
        plt.plot(df['z'], np.abs(40000.0 - psquare), label=f'X=+{x_val}mm')
    plt.legend()
    plt.xlabel('z (mm)')
    plt.ylabel('$p_0^2 - p^2, p^2 = p_x^2 + p_y^2 + p_z^2$ (MeV/c)')
    plt.tight_layout()
    if save == 1:
        plt.savefig(f'../plots/x-offset_mod-del-psquare-vs-z.png', dpi=300)
    if show == 1:
        plt.show()
