import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

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

######### Plot ####################
plot_dir_path = directory + "/plots/" + "flipped"
os.makedirs(plot_dir_path, exist_ok=True)

for i, file in enumerate(files):
    df = read_ascii(file)
    z, bz = df['z'], df['Bz']
    eventid = df['EventID'][0]
    fig = plt.figure(figsize=(8, 5))
    plt.scatter(z, bz, marker='.', s=1, color='red')
    plt.xlabel('z (mm)')
    plt.ylabel('$B_z$ (T)')
    plt.title(f'$B_z$ vs. z (Event {i+1})')
    plt.savefig(f'{plot_dir_path}/bz_vs_z_{eventid}.png', dpi=300)


