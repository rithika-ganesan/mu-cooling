#-----------------------------------------------------------

# Import g4bl trace .root files into Python with uproot

#-----------------------------------------------------------

#======== Dependencies ========

import uproot 
import awkward as ak
import pandas as pd
import numpy as np
import argparse
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
        "Lz": 
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

# Parser set-up
parser = argparse.ArgumentParser()
parser.add_argument("filepaths", help="Path to root file(s)", type=str)
args = parser.parse_args()

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

#============ Main ============

paths = glob.glob(args.filepaths)

def multiple():
    files = {}
    for path in paths:
        files[path] = get_file_events(path)
    return paths, files

def single():
    path = paths[0]
    events = get_file_events(path)
    return path, events

if multiple_files(paths) == True:
    paths, files = multiple()
elif multiple_files(paths) == False:
    path, events = single()



############### Full longitudinal channel

long=1
if long == 1:
    fig, ax = init_plot('z', 'Lz', labels={'z': 'z (mm)', 'Bz': r'$B_z$', 'Lz': r'$L_z$'})
    ax.set_title(r'$B_z$ in the matching section')

    ax = add_element_patch(ax, "RFC0", 245, 300, 301, -425, 0, '#87ace8', 0.9)
    for z in [-175, 75, 325, 575]:
        ax = add_element_patch(ax, None, 245, 300, 301, z, 0, '#87ace8', 0.9)

    ax = add_element_patch(ax, "RFC", 245, 300, 301, 1075, 0, '#ce887a', 0.9)
    for z in [1325, 1775, 2025, 2475, 2725, 3175, 3425, 3875, 4125, 4575, 4825, 5275, 5525]:   
        ax = add_element_patch(ax, None, 245, 300, 301, z, 0, '#ce887a', 0.9)

    ax = add_element_patch(ax, "RotSol", 6000, 360, 500, -3000, 0, (1.0, 0.8, 1.0), 0.5)
    ax = add_element_patch(ax, "SolPos", 300, 420, 600, 500, 0, (1.0, 0.0, 0.0), 0.5)
    ax = add_element_patch(ax, "SolNeg", 300, 420, 600, 1200, 0, (0.0, 0.0, 1.0), 0.5)
    ax = add_element_patch(ax, None, 300, 420, 600, 1900, 0.08864577034195348, (1.0, 0.0, 0.0), 0.5) #solpos
    ax = add_element_patch(ax, None, 300, 420, 600, 2600, 0.12464581967694571, (0.0, 0.0, 1.0), 0.5) #solneg
    ax = add_element_patch(ax, None, 300, 420, 600, 3300, 0.08629462092385154, (1.0, 0.0, 0.0), 0.5) #solpos
    ax = add_element_patch(ax, None, 300, 420, 600, 4000, 0.08165184417494886, (0.0, 0.0, 1.0), 0.5) #solneg

    for i in [4200]: #no pitches !
        ax = add_element_patch(ax, "HFOFO SolPos", 300, 420, 600, 500+i, 0, (1.0, 0.0, 0.0), 0.95)
        ax = add_element_patch(ax, None, 300, 420, 600, 1200+i, 0, (0.0, 0.0, 1.0), 0.95)
        ax = add_element_patch(ax, None, 300, 420, 600, 1900+i, 0, (1.0, 0.0, 0.0), 0.95) #solpos
        ax = add_element_patch(ax, None, 300, 420, 600, 2600+i, 0, (0.0, 0.0, 1.0), 0.95) #solneg
        ax = add_element_patch(ax, None, 300, 420, 600, 3300+i, 0, (1.0, 0.0, 0.0), 0.95) #solpos
        ax = add_element_patch(ax, None, 300, 420, 600, 4000+i, 0, (0.0, 0.0, 1.0), 0.95) #solneg

    ax = add_element_patch(ax, "Pressure wall", 4, 0, 360, 850, 0, (0.1, 0.1, 0.1), 0.75)
    ax = add_element_patch(ax, "Absorber", 160, 500, 550, 850, 0, (0.1, 0.1, 0.1), 0.5)
    for z in [1550, 2250, 2950, 3650, 4350, 5050]:
        ax = add_element_patch(ax, None, 160, 500, 550, z, 0, (0.1, 0.1, 0.1), 0.5)

    for e in [-1]:
        event = events[e]
        #event = event[event['z'] < 100]

        z = event['z']
        x, y = event['x'], event['y']
        Px, Py, Pz = event['Px'], event['Py'], event['Pz']
        Bz = event['Bz']
        Lz = x * Py - y * Px
        if e == -1:
            ax.plot(z, Bz, lw=1, label='Reference particle')
        else:
            ax.plot(z, Bz, lw=1)

    ax.legend()
    ax.set_ylim([-5, 5])
    ax.set_xlim([-700, 5000])
    fig.tight_layout()
    #plt.show()
    fig.savefig(f'plots/fullmatching-Bz.png', dpi=300)

trans=0
if trans==1:
    folder = 'plots/refscanphaserotator'
    event = events[-1]
    event = event[event['z'] < 100]

    for i, row in event.iterrows():

        if i%1 == 0:

            fig, ax = init_transverse_plot(event)
            ax.set_title(f'z = {row['z']:.2f}mm')

            ax.set_ylim([-.15, .15])
            ax.set_xlim([-.15, .15])
            ax.plot(event['x'][:i+1], event['y'][:i+1], lw=0.5)
            ax.scatter(row['x'], row['y'], s=4)
            
            fig.tight_layout()
            plt.savefig(f'{folder}/{i:03d}.png',dpi=300)

        #fig, ax = fin_transverse_plot(fig, ax, f'z = {row['z']}mm', show=0, save=f'{folder}/{i:03d}.png')
        #fig, ax = fin_transverse_plot(fig, ax, row, save=f'./{folder}/{i:03d}.png', show=0)

    image_paths = sorted(glob.glob(f'{folder}/*.png'))
    images = [Image.open(p) for p in image_paths]

    images[0].save(
        f'{folder}/anim.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0
    )

##### smth else

# fig, ax = init_transverse_plot(ref, 0, 0)
# rB = np.sqrt(ref['Bx']**2 + ref['By']**2)
# phiB = np.arctan2(ref['By'], ref['Bx'])
# #ax.set_xlim([-60, 60])
# #ax.set_ylim([-60, 60])
# fig, ax = fin_transverse_plot(fig, ax, 'Transverse B-fields', no_legend=True)


#### Kinds of workflows

#### Iterate over multiple files
#### Iterate over events within a single file -> here rn
#### Iterate over z within a single event

############## Import events for a single file






# events = {}
# with uproot.open(path=path) as file:
#     if is_all_tracks(file) == True:
#         tree = file['Trace/AllTracks'].arrays(library=lib)
#         for eid in np.unique(tree["EventID"]).astype(int):
#             events[eid] = tree[tree["EventID"] == eid]

#     if has_reference_particle(file) == True:
#         events[-2] = file['Trace/TuneParticle'].arrays(library=lib)
#         events[-1] = file['Trace/ReferenceParticle'].arrays(library=lib)

#     if count_event_tracks != 0:
#         eventids, eventkeys = get_event_ids(file)
#         for event in get_event_iterator(path, eventkeys):
#             events[int(max(event['EventID']))] = event




