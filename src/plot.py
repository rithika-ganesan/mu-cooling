#-----------------------------------------------------------------

# Plot figures relevant to g4bl 

#------------------------------------------------------------------

#============= Dependencies =============

import matplotlib.pyplot as plt
import numpy as np

#============== Functions ===============

# Initialize a plot along the z axis
def plot_long(x_axis, x=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.dpi = 300
    ax.set_xlabel('z (mm)')
    ax.set_ylabel(x_axis)
    return fig, ax

# Initialize a plot in the x-y plane
def plot_transverse(L=500, ticks='limits'):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.dpi = 300
    ax.axhline(0, lw=0.5, c='k')
    ax.axvline(0, lw=0.5, c='k')
    ax.set_xlim([-L, L])
    ax.set_ylim([-L, L])
    if ticks == 'limits':
        ax.set_xticks([-L, 0, L])
        ax.set_yticks([-L, 0, L])
    elif ticks == None:
        ax.set_xticks([])
        ax.set_yticks([])
    return fig, ax

# Add a position vector to the x-y plane
def add_vector(ax, x=None, y=None, r=None, phi=None, clr=None, label=None):
    if x != None and y != None:
        x, y = x, y
    elif r != None and phi != None:
        x = r * np.cos(phi)
        y = r * np.sin(phi)
    ax.plot([0, x], [0, y], lw=1, c=clr)
    ax.scatter([x], [y], s=5, c=clr, label=label)
    return ax

# Make histograms of different columns in a dataframe
# If saving plots, set save = path to directory to save in
# To modify individual axes, store plots dict in variable with show save both 0
def make_histograms(df, show=1, save=0, exclude=[None], title=None, bins=50):
    plots = {}
    for col in df.columns:
        if col not in exclude:
            vals = df[col]
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.dpi = 300
            ax.hist(vals, bins=bins, alpha=0.7)
            ax.set_xlabel(f'{col}')
            if title:
                ax.set_title(f'{title} {col}')
            fig.tight_layout()
            plots[col] = [fig, ax]
            if save != 0:
                plt.savefig(f'{save}/{col}.png')
            if show == 1:
                plt.show()
            if show == 0 and save == 0:
                plt.close(fig)
    
    return plots



