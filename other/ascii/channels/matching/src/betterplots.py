import matplotlib.pyplot as plt
import matplotlib as mpl

# This function initializes a figure and axes if they do not already exist. 
def plot_init(fig, ax, figsize=(10, 7)):

    if bool(fig) != bool(ax):
        raise Exception("Only figure or axes given. Add both or initialize new.")
    
    if fig == None and ax == None:
        fig, ax = plt.subplots(figsize=figsize)
        fig.tight_layout()

    return fig, ax

def plot_complete(fig, ax):

    if ax.get_legend() == None:
        ax = legend_init(ax)

    return fig, ax

def legend_init(ax):

    number = len(ax.collections) + len(ax.lines) + len(ax.patches)
    if number > 1:
        ax.legend()

    return ax

def lineplot(x, y, 
        fig=None, 
        ax=None,
        figsize=(10, 7)
    ):

    fig, ax = plot_init(fig, ax)



    return fig, ax





