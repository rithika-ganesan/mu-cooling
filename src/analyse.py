#-----------------------------------------------------------------

# Perform manipulations on g4bl output with pandas and numpy

# Script assumes data, labels of form produced by read.read_trace()
# All functions for one particular dataframe

#------------------------------------------------------------------

#============== Temporary ===============

# from read import read_trace

# path1 = '../output/solshapel2000.root'
# path2 = '../other/ascii/channels/matching/src/solenoids-2.root'
# path3 = '../other/ascii/channels/matching/src/solenoids-3.root'
# path2p5 = '../other/ascii/channels/matching/src/solenoids-*.root'

# path = path1

# data, labels = read_trace(path1)

# data = data[-1]

# #print(labels)


#============= Dependencies =============

import pandas as pd
import numpy as np


#============== Functions ===============

# Get the rms of a number of numpy vectors
def vecnorm(list):
    sum = (list[0])**2
    for el in list[1:]:
        sum += el**2 
    return np.sqrt(sum)

# Rotation matrix for some angle phi
def rot_mat(phi):
    return np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])

# Get vectors for a pair of coordinates
def get_2d_vec(a, b):
    N = len(a)
    if len(a) != len(b):
        raise ValueError
    a, b = a.to_numpy(), b.to_numpy()
    a, b = a.reshape(1, N), b.reshape(1, N)
    return np.concatenate([a, b])

# Get particle position in polar coordinates
def get_polar_coordinates(df):
    x, y = df['x'], df['y']
    df['rho'] = vecnorm([x, y])
    df['phi'] = np.arctan2(y, x)
    return df

# # Get transverse magnetic field in polar coordinates
# def get_polar_transverse_B(df):
#     if 'rho' not in df.columns and 'phi' not in df.columns:
#         df = get_polar_coordinates(df)

# Get the total momentum
def get_total_p(df):
    df['p total'] = vecnorm([df['Px'], df['Py'], df['Pz']])
    return df

# Get angular momentum in z
def get_Lz(df):
    df['Lz'] = (df['x'] * df['Py']) - (df['y'] * df['Px'])
    return df

# Iterate to get polar transverse field components
def get_Bt(df):
    if 'rho' not in df.columns and 'phi' not in df.columns:
        df = get_polar_coordinates(df)

    bxp, byp = [], []
    for i, row in df.iterrows():
        primed = rot_mat(row['phi']) @ np.array([row['Bx'], row['By']])
        bxp.append(primed[0])
        byp.append(primed[1])

    df['Bx primed'], df['By primed'] = bxp, byp

    return df

    


# a b cos theta

# a  b sin theta 