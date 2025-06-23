#-----------------------------------------------------------

# Import g4bl trace .root files into Python with uproot

#-----------------------------------------------------------

#======== Dependencies ========

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

# Set default conversion to pandas dataframes
# Can also be 'ak' for awkward arrays or 'np' for numpy
uproot.default_library = 'pd'
lib = 'pd'
plot_params = {
    'landscape figsize': (8, 6),
    'labels': {
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
        "Ez": "$E_z$ (MV/m)",
        "Lz": "$L_z$"
    },
    'default plots': {
        'x-v-z': ['z', 'x'],
        'y-v-z': ['z', 'y'],
        'px-v-z': ['z', 'Px'],
        'py-v-z': ['z', 'Py'],
        'pz-v-z': ['z', 'Pz'],
        'Bx-v-z': ['z', 'Bx'],
        'By-v-z': ['z', 'By'],
        'Bz-v-z': ['z', 'Bz']
    },
    'dpi': 300 
}

# Integer variables
ip = ['PDGid', 'EventID', 'TrackID', 'ParentID', 'Weight']

#========  Functions      ========

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

# Initialize a 2d plot
def init_plot(x, y, figsize=plot_params['landscape figsize'], labels=plot_params['labels']):
    fig, ax = plt.subplots(figsize=figsize)
    fig.dpi = plot_params['dpi']
    fig.x_param = x
    fig.y_param = y
    ax.set_xlabel(labels[x])
    ax.set_ylabel(labels[y])
    return fig, ax

# Close out the plot
# If you want to save it, set save='pathname'
def fin_plot(fig, ax, show=1, save=0, store=0, no_legend=False):
    if len(ax.collections) != 0 or len(ax.lines) != 0:
        if no_legend != True:
            ax.legend()
    fig.tight_layout()
    if save != 0:
        plt.savefig(save)
    if show == 1:
        plt.show()
    if show == 0 and store == 0:
        plt.close()
    return fig, ax


# Initialize plot in x-y plane
def init_transverse_plot(event, innerradius=350, outerradius=500):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.dpi = 300
    ax.axvline(0, lw=0.5, c='k')
    ax.axhline(0, lw=0.5, c='k')

    inner = patches.Circle((0, 0), innerradius, lw=1, facecolor=(1.0, 1.0, 1.0), edgecolor=(1.0, 0.0, 0.0))
    outer = patches.Circle((0, 0), outerradius, lw=1, facecolor=(1.0, 0.0, 0.0), edgecolor=(1.0, 1.0, 1.0), alpha=0.3, label='RotSol')

    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.add_patch(outer)
    ax.add_patch(inner)

    return fig, ax

# Close plot in x-y plane
def fin_transverse_plot(fig, ax, title, show=1, save=0, store=0, no_legend=False):
    ax.set_title(title)
    if len(ax.collections) > 0 or len(ax.lines) > 0:
        if no_legend != True:
            ax.legend()
    fig.tight_layout()
    if save != 0:
        fig.savefig(save)
    if show == 1:
        plt.show()
    if show == 0 and store == 0:
        plt.close()

    return fig, ax

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


