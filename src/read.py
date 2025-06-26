#-----------------------------------------------------------------

# Import g4bl trace files into Python with uproot and pandas

# Usage:
# import read
# data, labels = read.read_trace(path)
# path can be a string or a list of strings

#------------------------------------------------------------------

#============= Dependencies =============

import uproot
import numpy as np
from pathlib import Path
import pandas as pd
import glob

#=============== Options ================

# Set default conversion to pandas dataframes
# Can also be 'ak' for awkward arrays or 'np' for numpy
uproot.default_library, lib = 'pd', 'pd'

# Tuple labels for reading ascii
tuple_labels=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight", "Bx", "By", "Bz", "Ex", "Ey", "Ez"]

#============== Functions ===============

# Check if a given root trace file has all tracks or separate tracks
def is_all_tracks_root(file):
    if 'Trace/AllTracks;1' in file.keys():
        return True
    else:
        return False
    
# Find if a given root file has reference and tune particles
def has_reference_particle_root(file):
    if 'Trace/ReferenceParticle;1' in file.keys():
        return True
    else:
        return False 

# Read a single root trace file that has AllTracks
def read_root_trace_alltracks(file):
    tree = file['Trace/AllTracks'].arrays(library=lib) 
    events = {}
    for eventid in np.unique(tree["EventID"]).astype(int):
        events[eventid] = tree[tree["EventID"] == eventid]
    return events

# Read a single root trace file from path that has separate tracks
def read_root_trace_septracks(file):
    events = {}
    for key in file.keys():
        if key != 'Trace;1':
            tree = file[key].arrays(library=lib)
            eventids = np.unique(tree["EventID"]).astype(int)
            if len(eventids) == 1:
                events[eventids[0]] = tree
            else:
                events["All"] = tree
    return events

# Read a single root trace file from path
def read_root_trace(path):
    with uproot.open(path=path) as file:
        if is_all_tracks_root(file) == True:
            return read_root_trace_alltracks(file)
        else:
            return read_root_trace_septracks(file)
        
# Read a single ascii trace file from path that has alltracks
def read_ascii_trace_alltracks(path, comment='#'):
    df = pd.read_csv(f'{path}', comment=comment, header=None, sep='\\s+')
    length = df.shape[1]
    df.columns = tuple_labels[:length]
    events = {"All": df}
    for eventid in np.unique(df["EventID"]).astype(int):
        events[eventid] = df[df["EventID"] == eventid]
    return events

# Read a single ascii trace file from path (directory) that has separate
def read_ascii_trace_septracks(path, comment='#'):
    print('Not configured yet!')
    return None

# Read a single root trace file from path
def read_ascii_trace(path, cmnt='#'):
    alltracks = 1
    if alltracks == True:
        return read_ascii_trace_alltracks(path, comment=cmnt)
    else:
        return read_ascii_trace_septracks(path)
        
# Check if file at given path is a root file
def is_root(path):
    p = Path(path)
    if p.suffix == '.root':
        return True
    else:
        return False
    
# Read a single trace file from path
def read_path_trace(path):
    if is_root(path) == True:
        return read_root_trace(path)
    else:
        return read_ascii_trace(path)
    
# Get the stem of a given path 
def path_label(path, n):
    p = Path(path)
    return p.stem
    
# Read multiple files (or a single file) from path using the path stem as the label
# Use a different function for diff labels
# Function has to have path and counter n both as positional arguments
def read_trace(filepaths, label_fn=path_label):
    if type(filepaths) == str:
        paths = sorted(glob.glob(filepaths))
    elif len(filepaths) >= 1:
        paths = sorted([glob.glob(path) for path in filepaths])
    else:
        raise ValueError("Unknown path type. Use a list of strings or a regex string.")

    data = {}
    for n, path in enumerate(paths):
        label = label_fn(path, n)
        data[label] = read_path_trace(path)

    labels = list(data.keys())

    if len(data) == 1:
        return data[labels[0]], labels[0]
    else:
        return data, labels
        







            
