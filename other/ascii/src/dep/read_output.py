# Read g4beamline ascii output from a single .txt file
# Rithika Ganesan | May 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Get input path from parser
parser = argparse.ArgumentParser(description="Read g4bl ASCII output files")

parser.add_argument('--input_path', '-i', type=str, required=True, help='Input file path')
parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
  
args = parser.parse_args()

# if args.verbose:
#     print(f"Reading from: {args.input}")
#     print(f"Writing to: {args.output}")

# Data params
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

###########  Main  #################
path = args.input_path 

df = read_ascii(path=path)

print(df.columns)
print("Length:", len(df))
