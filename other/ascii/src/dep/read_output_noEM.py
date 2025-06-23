# Read g4beamline ascii output from a single .txt file
# No B and E fields
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
tuple_labels=["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

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
    "Weight": None
}

###########  Main  #################
path = args.input_path 

df = pd.read_csv(f'{path}', comment='#', header=None, names=tuple_labels)

print(df.columns)
print("Length:", len(df))
