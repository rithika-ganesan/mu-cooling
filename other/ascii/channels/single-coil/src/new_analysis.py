##################################################
#                                                #
#    Template file for analysis in g4beamline    #
#                                                #
##################################################

########## settings ##########

inp = "singlecoil"
filenametype = "trace_*.txt"
#use_channel = None
use_channel = "nodet-deltap0p1-xoffset20"

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

# Turn a single dataframe into a dictionary of multiple dataframes correspodning to each particle. 
def split_by_event(df):
    ids = np.unique(df["EventID"])
    print("Event IDs:", ids)
    d = {}
    for i in ids:
        d[i] = df[df["EventID"] == i].reset_index()
    return d

### For 2D vectors r and V of form r = np.array([x, y]),
### get components of V along r_hat and along phi_hat
### expressed in the same global coordinate system
def get_vector_components(r, V):
    r = np.array([x, y])
    r_hat = r / np.linalg.norm(r)
    phi_hat = np.array([-r_hat[1], r_hat[0]])
    
    V_r = np.dot(V, r_hat)
    V_phi = np.dot(V, phi_hat)
    return V_r, V_phi

# def compute_local_components(row):
#     r_vec = np.array([row['x'], row['y']])
#     V = np.array([row['Vx'], row['Vy']])
#     
#     # Normalize r̂
#     r_norm = np.linalg.norm(r_vec)
#     if r_norm == 0:
#         return pd.Series({'Vr': np.nan, 'Vphi': np.nan})  # avoid division by zero
# 
#     r_hat = r_vec / r_norm
#     phi_hat = np.array([-r_hat[1], r_hat[0]])  # 90° CCW rotation
#     
#     # Project V
#     Vr = np.dot(V, r_hat)
#     Vphi = np.dot(V, phi_hat)
#     
#     return pd.Series({'Vr': Vr, 'Vphi': Vphi})
# 
# 
# def add_local_components(df, x_col, y_col, vx_col, vy_col, vr_name='Vr', vphi_name='Vphi'):
#     def compute_components(row):
#         r_vec = np.array([row[x_col], row[y_col]])
#         v_vec = np.array([row[vx_col], row[vy_col]])
# 
#         norm = np.linalg.norm(r_vec)
#         if norm == 0:
#             return pd.Series({vr_name: np.nan, vphi_name: np.nan})
# 
#         r_hat = r_vec / norm
#         phi_hat = np.array([-r_hat[1], r_hat[0]])
# 
#         vr = np.dot(v_vec, r_hat)
#         vphi = np.dot(v_vec, phi_hat)
# 
#         return pd.Series({vr_name: vr, vphi_name: vphi})
# 
#     return df.join(df.apply(compute_components, axis=1))

# def add_local_vector_components(df, x_col, y_col, vx_col, vy_col,
#                                 vrx_name='Vr_x', vry_name='Vr_y',
#                                 vphix_name='Vphi_x', vphiy_name='Vphi_y'):
#     def compute_components(row):
#         r_vec = np.array([row[x_col], row[y_col]])
#         v_vec = np.array([row[vx_col], row[vy_col]])
# 
#         norm = np.linalg.norm(r_vec)
#         if norm == 0:
#             return pd.Series({vrx_name: np.nan, vry_name: np.nan,
#                               vphix_name: np.nan, vphiy_name: np.nan})
# 
#         r_hat = r_vec / norm
#         phi_hat = np.array([-r_hat[1], r_hat[0]])
# 
#         vr_mag = np.dot(v_vec, r_hat)
#         vphi_mag = np.dot(v_vec, phi_hat)
# 
#         vr_vec = vr_mag * r_hat
#         vphi_vec = vphi_mag * phi_hat
# 
#         return pd.Series({
#             vrx_name: vr_vec[0], vry_name: vr_vec[1],
#             vphix_name: vphi_vec[0], vphiy_name: vphi_vec[1]
#         })
# 
#     return df.join(df.apply(compute_components, axis=1))
# 

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

#print(deltap, p)

#########################################################

for channel in channels:

    ### Get data
    df_ = dfs[channel]
    ### Check that there are no copies
    #if len(ref) != len(test):
    #    raise ValueError(f"Extraneous data points! Reference: {len(ref)}, test: {len(test)} ")

    #### Getting radial and phi components
    for i, df in df_.iterrows():
    
        x, y, Px, Py, Bx, By = df['x'], df['y'], df['Px'], df['Py'], df['Bx'], df['By']

        r = np.sqrt(x**2 + y**2)
        Phi = np.arctan2(y, x)
        Phih = np.pi/2 + np.arctan2(y, x)

        P = np.array([Px, Py])
        B = np.array([Bx, By])

        R = np.array([[np.cos(Phi), -np.sin(Phi)], [np.sin(Phi), np.cos(Phi)]])
        Rh = np.array([[np.cos(Phih), -np.sin(Phih)], [np.sin(Phih), np.cos(Phih)]])

        Pr, Br = np.dot(R, P), np.dot(R, B)
        Pphi, Bphi = np.dot(Rh, P), np.dot(Rh, B)

        df['Pr'], df['Br'], df['Pphi'], df['Bphi'] = Pr, Br, Pphi, Bphi

   eventsdf = split_by_event(df_)
   ref, test = eventsdf[-1], eventsdf[1]



