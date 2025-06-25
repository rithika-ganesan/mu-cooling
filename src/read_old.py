#-----------------------------------------------------------------

# Import g4bl trace .root files into Python with uproot and pandas

# This file can currently read 
#   (a) trace .root files from g4bl
#   (b) trace ascii files from g4bl

# To individual script file, add:

# from read import *
# args = parser.parse_args()
# paths = glob.glob(args.filepaths)
# data = read_files(paths)

#------------------------------------------------------------------

#======== Dependencies ========

import argparse
import uproot 
import awkward as ak
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.interpolate import CubicSpline
import glob
from PIL import Image
from pathlib import Path

# # Set default conversion to pandas dataframes
# # Can also be 'ak' for awkward arrays or 'np' for numpy
# uproot.default_library = 'pd'
# lib = 'pd'

# Parser set-up
parser = argparse.ArgumentParser()
parser.add_argument("filepaths", help="Path to root file(s)", type=str)

#===== Labels for the data columns =====

# All
tuple_labels=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight", "Bx", "By", "Bz", "Ex", "Ey", "Ez"]

# Integer variables
ip = ['PDGid', 'EventID', 'TrackID', 'ParentID', 'Weight']


#========  Functions ========

# Find if multiple files or single:
def multiple_files(paths):
    if len(paths) > 1:
        return True
    elif len(paths) == 1:
        return False
    elif len(paths) == 0:
        raise NameError("No files found.")

# Find if a given root file has one NTuple or multiple
def is_all_tracks(file):
    if 'Trace/AllTracks;1' in file.keys():
        return True
    else:
        return False
    
# Find if a given root file has reference and tune particles
def has_reference_particle(file):
    if 'Trace/ReferenceParticle;1' in file.keys():
        return True
    else:
        return False 
        
# Find if a given root file has individual event tracks and count them
def count_event_tracks(file):
    return sum([bool(re.match('Trace/Ev.*Trk.*', key)) for key in file.keys()])

# Get event ids and keys for a file that has individual event tracks
def get_event_ids(file):
    ids, keys = [], []
    for key in file.keys():
        match = re.match('Trace/Ev(.*)Trk.*', key)
        if match != None:
            ids.append(int(match.group(1)))
            keys.append(key)
    return ids, keys

# Get event iteration object
def get_event_iterator(path, eventkeys, lib=lib):
    return uproot.iterate(get_list_of_event_paths(path, eventkeys), library=lib)
    
# Get paths for events
def get_list_of_event_paths(path, eventkeys):
    return [f"{path}:" + key for key in eventkeys]

# Get events for a given trace file path
def get_file_events(path):
    events = {}
    with uproot.open(path=path) as file:
        if is_all_tracks(file) == True:
            tree = file['Trace/AllTracks'].arrays(library=lib)
            for eid in np.unique(tree["EventID"]).astype(int):
                events[eid] = tree[tree["EventID"] == eid]

        if has_reference_particle(file) == True:
            events[-2] = file['Trace/TuneParticle'].arrays(library=lib)
            events[-1] = file['Trace/ReferenceParticle'].arrays(library=lib)

        if count_event_tracks(file) != 0:
            eventids, eventkeys = get_event_ids(file)
            for event in get_event_iterator(path, eventkeys):
                events[int(max(event['EventID']))] = event
    
    return events

# Round to the nearest multiple
def m_round(arr, multiple):
    return np.round(arr / multiple) * multiple

# Get evenly distributed values between the minimum and maximum of an array 
def get_even_distr(vals, step):
    z = vals
    min_z, max_z = m_round(min(z), step), m_round(max(z), step)
    tot = np.abs(min_z) + np.abs(max_z)
    count = int(tot / step) + 1
    zs = np.linspace(min_z, max_z, count)
    return zs

# Get splined version of event
def get_splined_event(event, newvals, intcols=ip, basecol='z'):
    z = event[basecol]
    splined_cols = {}
    for l in event.columns.tolist():
        cs = CubicSpline(z, event[l])
        if l not in intcols:
            splined_cols[l] = cs(newvals)
        else: 
            splined_cols[l] = cs(newvals).astype(int)
    splined_event = pd.DataFrame(splined_cols)
    return splined_event

# Read for multiple files
def multiple(paths):
    files = {}
    for path in paths:
        files[path] = get_file_events(path)
    return paths, files

# Read for single file
def single(paths):
    path = paths[0]
    events = get_file_events(path)
    return path, events

# Read from path
def read_files(paths):
    if multiple_files(paths) == True:
        paths, files = multiple(paths)
        return paths, files
    elif multiple_files(paths) == False:
        path, events = single(paths)
        return path, events

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
def extract_params(match_word, filename_base, ext="in"):
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




#### Pseudo code


