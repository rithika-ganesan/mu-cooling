##################################################
#                                                #
#    Template file for analysis in g4beamline    #
#                                                #
##################################################

########## settings ##########

inp = "singlecoil"
running_from = "channel src"  
filenametype = "trace_*.txt"
#use_channel = None
use_channel = "nodet-deltap0p1-xoffset0"

######## dependencies ########

import pandas as pd
import numpy as np
import glob
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import re

########### labels ###########

# pandas column names:
tuple_labels_noEM=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]
tuple_labels=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight", "Bx", "By", "Bz", "Ex", "Ey", "Ez"]

# column units:
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

labels = {
    "x": "X",
    "y": "Y",
    "z": "Z",
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

######### functions ##########

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

def xy_scatter(x, y, df, units=units, show=True, save=False, legend="off", figsize=(8, 6), vlines=None, prefix=None):
    fig = plt.figure(figsize=figsize)
    plt.scatter(df[x], df[y], s=5, label=f"{y} vs. {x}")
    plt.xlabel(f"{x} ({units[x]})")
    plt.ylabel(f"{y} ({units[y]})")
    if legend == "on":
        plt.legend()
    plt.title(f"{y} ({units[y]}) vs. {x} ({units[x]})")
    if vlines != None:
        for vx in vlines:
            plt.axvline(x=vx, color='k', linestyle='--', linewidth=1, alpha=0.6)
    
    ### end plot

    if save == True:
        show = False
        if prefix == None:
            plt.savefig(f"../plots/{y}v{x}.png", dpi=300)
        else:
            plt.savefig(f"../plots/{prefix}_{y}v{x}.png", dpi=300)
    if show == True:
        plt.show()
    return None

def xy_plot(x, y, df, units=units, show=True, save=False, legend="off", figsize=(8, 6), vlines=None, prefix=None):
    fig = plt.figure(figsize=figsize)
    plt.plot(df[x], df[y], linewidth=2, label=f"{y} vs. {x}")
    plt.xlabel(f"{x} ({units[x]})")
    plt.ylabel(f"{y} ({units[y]})")
    if legend == "on":
        plt.legend()
    plt.title(f"{y} ({units[y]}) vs. {x} ({units[x]})")
    if vlines != None:
        for vx in vlines:
            plt.axvline(x=vx, color='k', linestyle='--', linewidth=1, alpha=0.6)
    
    ### end plot

    if save == True:
        show = False
        if prefix == None:
            plt.savefig(f"../plots/{y}v{x}.png", dpi=300)
        else:
            plt.savefig(f"../plots/{prefix}_{y}v{x}.png", dpi=300)
    if show == True:
        plt.show()
    return None

def extract_vals(filename_base, match_word, ext="in"):
    # Path to the current script's directory
    script_dir = Path(__file__).parent
    filepath = script_dir / f"{filename_base}.{ext}"

    pattern = re.compile(rf"\b{re.escape(match_word)}\s+\S+\s+val\s+(\S+)\b")
    vals = []

    with filepath.open('r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                vals.append(match.group(1))  # Extract the value after 'val'

    return vals

def extract_params(filename_base, match_word, ext="in"):
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

def to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return r, phi

def to_cartesian(r, phi):
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y

############ main ############

# 1. Get data:

##### Get path(s):
### Using Path(__file__) ensures that this script can be run from any working directory, but will look for output text files in the correct location.
### Relative to the script, the files are in ../output/textfile.txt
ROOT_DIR = Path(__file__).parent.parent         
file_ex = ROOT_DIR / 'output' /  filenametype   
files = sorted(glob.glob(f"{file_ex}"))

##### Load data:
### Since we might want to work with multiple .txt files, store them in a dictionary, with keys corresponding to the channel name. 
dfs = {}
for file in files:
    name = re.search(r'trace_(.*)\.txt$', file).group(1)
    df = read_ascii(file)
    dfs[name] = df

##### Select data:
channels = list(dfs.keys()) # Leaving this unchanged iterates over all available outputs in the directory.

if use_channel != None: # Alt to work with a single file, set this.
    channels = [use_channel]

# 2. Get channel parameters:

##### To plot the solenoid location:
solX, solY, solZ = 0, 0, 0

solLength = float(extract_params(inp, match_word="solLength")[0])
soliRad = float(extract_params(inp, match_word="solInner")[0])
solThickness = float(extract_params(inp, match_word="solThickness")[0])
soloRad = soliRad + solThickness

### These variable names are iffy 
edgesZ = [solZ - solLength / 2, solZ + solLength / 2]
edgesiX = [solX - soliRad, solX + soliRad]
edgesoX = [solX - soloRad, solX + soloRad]
edgesiY = [solY - soliRad, solY + soliRad]
edgesoY = [solY - soloRad, solY + soloRad]

##### Dispersion related values:
deltap = float(extract_params(inp, match_word="dp")[0]) 
p = float(extract_params(inp, match_word="p")[0])

print(deltap, p)

# 3. Get data to plot. Dispersion:

for channel in channels:
    df = dfs[channel]
    refp = df[df["EventID"] == -1].reset_index()   #Get reference particle data 
    testp = df[df["EventID"] == 1].reset_index()   #Get test particle data

    #print(len(refp), len(testp))

    z = refp['z']
    ind = []
    for i in range(len(refp) - 1):
        if z[i+1] == z[i]:
            ind.append(i+1)
    #refp = refp.drop(ind).reset_index(drop=True)

    z = testp['z']
    ind = []
    for i in range(len(testp) - 1):
        if z[i+1] == z[i]:
            ind.append(i+1)
    testp = testp.drop(ind).reset_index(drop=True)

     #print(len(refp), len(testp))
    rx, ry, rz = refp['x'], refp['y'], refp['z']
    tx, ty, tz = testp['x'], testp['y'], testp['z']

    #==== ref particle, test particle x vs z ====
    plotxvzrefptestp = 0
    show, save = 1, 0
    #save, show = 1, 0   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plotxvzrefptestp == 1:
        desc=f'xvz-refptestp-{channel}'
        fig = plt.figure(figsize=(8, 6))
        plt.plot(rz, rx, linewidth=1, label='Reference particle')
        plt.plot(tz, tx, linewidth=1, label='Test particle')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('x (mm)')
        plt.legend()
        plt.title(f'x vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()

    #==== ref particle, test particle x vs z ====
    plotyvzrefptestp = 0
    show, save = 1, 0
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plotyvzrefptestp == 1:
        desc=f'yvz-refptestp-{channel}'
        fig = plt.figure(figsize=(8, 6))
        plt.plot(rz, ry, linewidth=1, label='Reference particle')
        plt.plot(tz, ty, linewidth=1, label='Test particle')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('y (mm)')
        plt.legend()
        plt.title(f'y vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()

    #==== ref particle, test particle |p| vs z ====
    plot_magp_v_z_refptestp = 0
    show, save = 1, 1
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plot_magp_v_z_refptestp == 1:
        desc=f'magp-v-z_refptestp_{channel}'
        fig = plt.figure(figsize=(8, 6))
        rpx, rpy, rpz = refp['Px'], refp['Py'], refp['Pz']
        tpx, tpy, tpz = testp['Px'], testp['Py'], testp['Pz']

        rp = np.sqrt(rpx**2 + rpy**2 + rpz**2) 
        tp = np.sqrt(tpx**2 + tpy**2 + tpz**2) 

        plt.plot(rz, rp, linewidth=1, label='Reference particle $|p|$')
        plt.plot(rz, tp, linewidth=1, label='Test particle $|p|$')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('p (MeV/c)')
        plt.legend()
        plt.title(f'p vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
    
    #==== ref particle, test particle px py pz vs z ====
    plotpxpypzvzrefptestp = 0
    show, save = 1, 1
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plotpxpypzvzrefptestp == 1:
        desc=f'pxpypzvz-refptestp-{channel}'
        fig = plt.figure(figsize=(8, 6))
        rpx, rpy, rpz = refp['Px'], refp['Py'], refp['Pz']
        tpx, tpy, tpz = testp['Px'], testp['Py'], testp['Pz']
        plt.plot(rz, rpx, linewidth=1, label='Reference particle $p_x$')
        plt.plot(rz, rpy, linewidth=1, label='Reference particle $p_y$')
        plt.plot(rz, rpz, linewidth=1, label='Reference particle $p_z$')
        plt.plot(rz, tpx, linewidth=1, label='Test particle $p_x$')
        plt.plot(rz, tpy, linewidth=1, label='Test particle $p_y$')
        plt.plot(rz, tpz, linewidth=1, label='Test particle $p_z$')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('p (MeV/c)')
        plt.legend()
        plt.title(f'p vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
    
    #==== ref particle, test particle pz vs z ====
    plotpzvzrefptestp = 0
    show, save = 1, 0
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plotpzvzrefptestp == 1:
        desc=f'pzvz-refptestp-{channel}'
        fig = plt.figure(figsize=(8, 6))
        rpz = refp['Pz']
        tpz = testp['Pz']
        plt.plot(rz, rpz, linewidth=1, label='Reference particle $p_z$')
        plt.plot(rz, tpz, linewidth=1, label='Test particle $p_z$')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('$p_z$ (MeV/c)')
        plt.legend()
        plt.title(f'pz vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
        plt.clf()
    
    #==== ref particle px py vs z ====
    pxpy_v_z_refp = 0
    show, save = 1, 1
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if pxpy_v_z_refp == 1:
        desc=f'pxpy-v-z_refp_{channel}'
        fig = plt.figure(figsize=(8, 3))
        rpx, rpy = refp['Px'], refp['Py']
        plt.plot(rz, rpx, linewidth=1, label='Reference particle $p_x$')
        plt.plot(rz, rpy, linewidth=1, label='Reference particle $p_y$')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('p (MeV/c)')
        plt.legend()
        plt.title(f'p vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
            #plt.clf()
    
    #==== test particle px py vs z ====
    pxpy_v_z_testp = 0
    show, save = 1, 1
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if pxpy_v_z_testp == 1:
        desc=f'pxpy-v-z_testp-{channel}'
        fig = plt.figure(figsize=(8, 3))
        tpx, tpy = testp['Px'], testp['Py']
        plt.plot(rz, tpx, linewidth=1, label='Test particle $p_x$')
        plt.plot(rz, tpy, linewidth=1, label='Test particle $p_y$')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('p (MeV/c)')
        plt.legend()
        plt.title(f'p vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
            #plt.clf()

    #==== ref particle Bx By Bz vs z ====
    plot_bxbybz_v_z = 1
    show, save = 1, 0
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plot_bxbybz_v_z == 1:
        desc=f'bxbybz-v-z_{channel}'

        fig = plt.figure(figsize=(8, 6))

        z = refp['z']
        bx, by, bz = refp['Bx'], refp['By'], refp['Bz']
    
        print(max(bz)) 

        plt.plot(z, bx, linewidth=1, label='$B_x$')
        plt.plot(z, by, linewidth=1, label='$B_y$')
        plt.plot(z, bz, linewidth=1, label='$B_z$')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('B (T)')
        plt.legend()
        plt.title(f'B vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
    
    #==== ref Bx By vs x y | transverse plane ====
    plot_bxby_transverse = 1
    show, save = 1, 0
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plot_bxbybz_v_z == 1:
        desc=f'bxbybz-v-z_{channel}'

        fig = plt.figure(figsize=(8, 6))

        z = refp['z']
        bx, by, bz = refp['Bx'], refp['By'], refp['Bz']
    
        print(max(bz)) 

        plt.plot(z, bx, linewidth=1, label='$B_x$')
        plt.plot(z, by, linewidth=1, label='$B_y$')
        plt.plot(z, bz, linewidth=1, label='$B_z$')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('B (T)')
        plt.legend()
        plt.title(f'B vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
    

    #==== calculate dispersion ====
    s = np.sqrt((rx - tx)**2 + (ry - ty)**2)
    disp = s * p / deltap 
    rz = rz

    #==== s vs z ====
    plot_svz = 0
    show, save = 1, 1
    #save, show = 1, 0   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plot_svz == 1:
        desc=f'svz_{channel}'
        fig = plt.figure(figsize=(8, 6))
        plt.axvline(edgesZ[0], lw=0.5, c='k', linestyle='--')
        plt.axvline(edgesZ[1], lw=0.5, c='k', linestyle='--')
        plt.plot(rz, s, linewidth=1, label='Test particle')
        plt.xlabel('z (mm)')
        #plt.xlim([-2, 5])
        plt.ylabel('s (mm)')
        plt.title(f's vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
    

    #==== s vs z - solenoid scale ====
    plot_svz_sol = 0
    show, save = 1, 1
    #save, show = 1, 0   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plot_svz_sol == 1:
        desc=f'svz_sol_{channel}'
        fig = plt.figure(figsize=(8, 6))
        #plt.axhline(edgesiX[0], lw=0.5, c='k', linestyle='--')
        #plt.axhline(edgesiX[1], lw=0.5, c='k', linestyle='--')
        #plt.axhline(edgesoX[0], lw=0.5, c='k', linestyle='--')
        #plt.axhline(edgesoX[1], lw=0.5, c='k', linestyle='--')
        plt.axvline(edgesZ[0], lw=0.5, c='k', linestyle='--')
        plt.axvline(edgesZ[1], lw=0.5, c='k', linestyle='--')
        plt.plot(rz, s, linewidth=1, label='Test particle')
        plt.xlabel('z (mm)')
        plt.ylabel('s (mm)')
        plt.xlim([-500, 500])
        plt.title(f's vs. z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()

    #==== plot dispersion ====
    plottotaldispersion = 0
    plot_ = 1
    scatter_ = 1
    show, save = 1, 1
    #show, save = 0, 1   ##### COMMENT TO SHOW, UNCOMMENT TO SAVE
    if plottotaldispersion == 1:
        desc=f'totaldispersion-{channel}'
        plt.axvline(edgesZ[0], lw=0.5, c='k', linestyle='--')
        plt.axvline(edgesZ[1], lw=0.5, c='k', linestyle='--')
        if plot_ == 1: 
            plt.plot(rz, disp, linewidth=1)
        if scatter_ == 1:
            plt.scatter(rz, disp, s=3)
        plt.xlabel('z (mm)')
        plt.ylabel('Dispersion (mm)')
        plt.title(f'Total dispersion vs z -- {channel}')
        plt.tight_layout()
        if save == 1:
            plt.savefig(f'../plots/{desc}.png', dpi=300)
        if show == 1:
            plt.show()
        plt.clf()

################ Channel loops:

###### single plot

for channel in channels:
    df = dfs[channel]

    # basics -- uncomment to run:
    #print(df)
    #print(df.shape)

    # get solenoid params from file
    ### FOLLOWING CODE ASSUMES SOLENOID IS AT z=0
    #tiltx = float(extract_params(inp, match_word="tiltx")[0])
    #if tiltx < 1:
    #    tx = f'{tiltx}'
    #    txd = tx[-1]
    #    tiltx = f'0p{txd}'
    #tiltxlabel = f'xdegs_{tiltx}'


    # make some plots

    coordvscoord = 0 
    if coordvscoord == 1:
        #xy_scatter('z', 'x', df=df, vlines=edges, save=True, prefix=tiltxlabel)
        #xy_scatter('z', 'x', df=df, vlines=edges, save=True, prefix=tiltxlabel)
        xy_plot('z', 'x', df=df, vlines=edges, save=False, prefix=channel)
        xy_plot('z', 'y', df=df, vlines=edges, save=False, prefix=channel)
        #xy_scatter('z', 'Pz', df=df, vlines=edges)
        #xy_scatter('z', 'Px', df=df, vlines=edges)
        #xy_scatter('z', 'Py', df=df, vlines=edges)
        #xy_scatter('x', 'Px', df=df)
        #xy_scatter('y', 'Py', df=df)
        plt.close()

    ######## finding tranverse field:

    ##### MAGNETIC FIELDS vs. Z
    bfieldsvsz = 0 
    if bfieldsvsz == 1:
        z = df['z'] / 1000
        
        Bx, By = df['Bx'], df['By']
        Br, Bphi = to_polar(Bx, By)
        #r_Bx, r_By = to_cartesian(Br, Bphi)
        
        fig = plt.figure(figsize=(8, 6))
        #plt.plot(z, df['Bz'], linewidth=1, c='k', label="$B_z$")
        
        #plt.scatter(z, Br, s=1, label="$B_r$")
        #plt.scatter(z, Bphi, s=1, label="$B_\phi$")
        plt.plot(z, Br, linewidth=1, linestyle='--', label="$B_r$")
        plt.plot(z, Bphi, linewidth=1, linestyle='--', label="$B_\phi$")
        
        #plt.scatter(z, Bx, s=1, label="$B_x$")
        #plt.scatter(z, By, s=1, label="$B_y$")
        #plt.plot(z, Bx, linewidth=1, c='k', label="$B_x$")
        #plt.plot(z, By, linewidth=1, c='red', label="$B_y$")
        
        #plt.scatter(z, r_Bx, s=1, c='blue', label="$reco B_x$")
        #plt.scatter(z, r_By, s=1, c='orange', label="$reco B_y$")
        #plt.plot(z, r_Bx, linewidth=1, label="Reconstructed $B_x$")
        #plt.plot(z, r_By, linewidth=1, label="Reconstructed $B_y$")
        
        plt.xlabel('z (m)')
        plt.ylabel('B (t)')
        plt.title('Tranverse B-field components')
        plt.legend()
        plt.tight_layout()
        fig_name = f'../plots/{channel}_BrBphi_vs_z.png'
        plt.savefig(fig_name, dpi=300)
        print("Saved figure", fig_name)
        #plt.show()


    ##### R vs. Z
    rvsz = 0 
    if rvsz == 1:
        z = df['z'] / 1000
        
        x, y = df['x'], df['y']
        r = np.sqrt(x**2 + y**2)
 
        fig = plt.figure(figsize=(8, 6))
        
        plt.plot(z, r, linewidth=1, label="$B_r$")
        
        plt.xlabel('z (m)')
        plt.ylabel('r (mm)')
        plt.title('Change in radial position')
        #plt.legend()
        plt.tight_layout()
        fig_name = f'../plots/{channel}_rvsz.png'
        #plt.savefig(fig_name, dpi=300)
        #print("Saved figure", fig_name)
        plt.show()

    ##### MAGNETIC FIELDS vs. R
    bfieldsvsr = 0  
    if bfieldsvsr == 1:
        z = df['z'] / 1000
        
        x, y = df['x'], df['y']
        r = np.sqrt(x**2 + y**2)

        Bx, By, Bz = df['Bx'], df['By'], df['Bz']
        Br, Bphi = to_polar(Bx, By)
        
        fig = plt.figure(figsize=(8, 6))
        
        plt.plot(r, Br, linewidth=1, linestyle='--', label="$B_r$")
        #plt.plot(r, Bphi, linewidth=1, linestyle='--', label="$B_\phi$")
        #plt.plot(r, Bz, linewidth=1, linestyle='--', label="$B_z$")
        
        plt.xlabel('r (mm)')
        plt.ylabel('B (T)')
        plt.title('B-field components')
        plt.legend()
        plt.tight_layout()
        fig_name = f'../plots/{channel}_Bvsr.png'
        #plt.savefig(fig_name, dpi=300)
        #print("Saved figure", fig_name)
        plt.show()


#### multi:

multiplot = 0
x='z'
y='x'
vlines = edges 

prefix='all_tilts'

if multiplot == 1:
    fig = plt.figure(figsize=(10, 8))

    for channel in channels:
        df = dfs[channel]
        plt.plot(df[x], df[y], linewidth=1, label=f"{channel}")

    plt.xlabel(f"{x} ({units[x]})")
    plt.ylabel(f"{y} ({units[y]})")
    plt.legend()
    plt.title(f"{y} ({units[y]}) vs. {x} ({units[x]})")
    if vlines != None:
        for vx in vlines:
            plt.axvline(x=vx, color='k', linestyle='--', linewidth=1, alpha=0.6)
    
    ### end plot

    plt.savefig(f"../plots/{prefix}_{y}v{x}.png", dpi=300)
    #plt.show()

# code works but this plot doesn't really show anything useful
b_compare = 0
if b_compare == 1:
    channels = ['xtilt-0_xoffset-0', use_channel]

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # FULL B no offset:
    df = dfs[channels[0]]
        
    z = df['z'] / 1000
    
    Bx, By, Bz = df['Bx'], df['By'], df['Bz']
    Btotal = np.sqrt(Bx**2 + By**2 + Bz**2)
    Btransverse = np.sqrt(Bx**2 + By**2)

    Br, Bphi = to_polar(Bx, By)

    axs[0].plot(z, Btotal, lw=3, c='lightblue', label='Total B')
    axs[0].plot(z, Bz, lw=2, c='k', linestyle='--', label="$B_z$")
    axs[0].plot(z, Btransverse, lw=1, c='blue', linestyle='-', label="$B_T$")
    axs[0].plot()
    axs[0].set_xlabel('z (m)')
    axs[0].set_ylabel('B (T)')
    axs[0].set_title('B-fields for no offset')
    axs[0].legend()
    
    # FOR split B offset:
    df = dfs[channels[1]]
        
    z = df['z'] / 1000
    Bx, By, Bz = df['Bx'], df['By'], df['Bz']
    Btotal = np.sqrt(Bx**2 + By**2 + Bz**2)
    Btransverse = np.sqrt(Bx**2 + By**2)
    
    Br, Bphi = to_polar(Bx, By)

    axs[1].plot(z, Btotal, lw=3, c='blue', label='Total B')
    axs[1].plot(z, Bz, lw=2, c='k', linestyle='--', label="$B_z$")
    axs[1].plot(z, Btransverse, lw=1, c='blue', linestyle='-', label="$B_T$")
    axs[1].set_xlabel('z (m)')
    axs[1].set_ylabel('B (T)')
    axs[1].set_title('B-fields for x-offset=20mm')
    axs[1].legend()

    # DONE
    plt.show()

