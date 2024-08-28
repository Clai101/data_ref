# my_package/matplotlib_setup.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

class CustomedAxes(Axes):
    def errorhist(self, data, bins=10, fmt='.', color='dimgrey', err_func = np.sqrt, **kwargs):
        counts, bin_edges = np.histogram(data, bins=bins, **kwargs)
        bin_centers = bin_edges[:-1] + (bin_edges[1] - bin_edges[0]) / 2
        self.errorbar(bin_centers, counts, yerr=err_func(counts), fmt=fmt, color=color, capsize=5, **kwargs)
        return counts, bin_centers

__subplot = plt.subplots

def subplots(nrows=1, ncols=1, **kwargs):
    fig, axes = __subplot(nrows=nrows, ncols=ncols, **kwargs)
    if isinstance(axes, np.ndarray):
        custom_axes = []
        for ax in axes.flat:
            position = ax.get_position()
            ax.remove() 
            custom_ax = CustomedAxes(fig, position)
            fig.add_axes(custom_ax)
            custom_axes.append(custom_ax)
        custom_axes = np.array(custom_axes).reshape(axes.shape)
    else:
        position = axes.get_position()
        axes.remove()
        custom_axes = CustomedAxes(fig, position)
        fig.add_axes(custom_axes)
    return fig, custom_axes

plt.subplots = subplots

SMALL_SIZE = 12
MEDIUM_SIZE = 16
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)
plt.rc('axes', labelsize=BIGGER_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE) 
plt.rcParams['axes.titlesize'] = 22 