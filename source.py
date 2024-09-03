import numpy as np
from scipy.optimize import curve_fit, minimize
from numpy import log, sqrt, exp, pi, e
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import os
from numba import njit
from iminuit import Minuit
from iminuit.cost import UnbinnedNLL

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
plt.rcParams['figure.constrained_layout.use'] = True

Lamc_m = 2.28646
Lamc_25_m = 2.5925
Lamc_26_m = 2.628
D_0_m = 1.86483
D_st_p_m = 2.01026
D_st_0_m = 2.00685
Pi_p_m = 0.13957
Pi_0_m = 0.13498
Ds_D_dif = 0.142014
K_s_m = 0.497611
K_p_m = 0.493677

x = np.array([1. , 2. ])
n = np.array([1, 2])

@njit(fastmath = True)
def eval_chebyt(n, x, a = 0, b = 0):
    if a == b:
        norm = 1
    else:
        if n == 0:
            norm = b - a
        elif n == 1:
            norm = (b**2 - a**2) / 2
        elif n == 2:
            norm = (2 * (b**3 - a**3) / 3 - (b - a)) / 2
        elif n == 3:
            norm = (4 * (b**4 - a**4) / 4 - 3 * (b**2 - a**2) / 2) / 4
        elif n == 4:
            norm = (8 * (b**5 - a**5) / 5 - 8 * (b**3 - a**3) / 3 + (b - a)) / 8
        elif n == 5:
            norm = (16 * (b**6 - a**6) / 6 - 20 * (b**4 - a**4) / 4 + 5 * (b**2 - a**2) / 2) / 16

    if n == 0:
        return np.ones_like(x)/norm
    elif n == 1:
        return x/norm
    elif n == 2:
        return (2 * np.power(x, 2) - 1)/norm
    elif n == 3:
        return (4 * np.power(x, 3) - 3 * x)/norm
    elif n == 4:
        return (8 * np.power(x, 4) - 8 * np.power(x, 2) + 1)//norm
    elif n == 5:
        return (16 * np.power(x, 5) - 20 * np.power(x, 3) + 5 * x)//norm

eval_chebyt(1, x)


@njit(fastmath = True)
def gaussian(x, mu, sigma): 
    sigma2 = np.power(sigma, 2)
    return np.power(sigma2*2*pi, -1/2) * np.exp(-np.power(x-mu, 2)/(2*sigma2))
gaussian(x, 1, 2)


@njit(fastmath = True)
def heaviside(x, d):
    return np.where(x >= d, 1.0, 0.0)
heaviside(x, 0)


@njit(fastmath = True)
def nois_log(x):
    return heaviside(x, 0)*np.log(x)
nois_log(x)

@njit(fastmath = True)
def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
factorial(1)


@njit(fastmath = True)
def factoriall(n):
    result = np.zeros_like(n)
    for i in range(n.size):
        result[i] = factorial(n[i])
    return result
factoriall(x)


@njit(fastmath = True)
def puasson(x, n):
    return np.exp(-x)*np.power(x, n)*np.power(factoriall(n), -1)
puasson(x, n)



@njit(fastmath=True)
def exp_dis(x, lam, a=0, b=0):
    if a == b:
        normalization_factor = 1
    else:
        normalization_factor = lam / (np.exp(lam * (b)) - np.exp(lam * (a)))
    return normalization_factor * np.exp(lam * x)
    



def normalization(counts, bin_edges):
    total_counts = np.sum(counts)
    bin_width = bin_edges[1] - bin_edges[0]
    return bin_width * total_counts

def rm(fname):
    if os.path.exists(fname):
        os.remove(fname)
    else:
        print("The file does not exist") 

from iminuit import Minuit

def max_bin_lik(f, bin_centers, counts, args0, des=False, norm=False, h=1e-7, bounds=None, normm=None, method='SLSQP'):
    # Poisson likelihood function
    def likelihoodn(x, n, norm, *args):
        return np.log(puasson(f(x, *args) / norm, n))
    
    # Normalize counts
    dx = bin_centers[1] - bin_centers[0]
    counts = counts / np.sum(counts) * dx
    
    # Define the negative log-likelihood function
    def df(*args0):
        normf = np.sum(f(bin_centers, *args0)) * dx
        return -np.sum(likelihoodn(bin_centers, counts, normf, *args0))
    
    # Initialize Minuit
    minuit = Minuit(df, *args0)
    if bounds != None:
        minuit.limits = bounds
    
    # Perform the minimization
    minuit.migrad()
    
    # Extract the results
    rez = minuit.values
    normf = np.sum(f(bin_centers, *rez)) * dx  # Note the change to `*rez` instead of `*rez.x`
    
    print(rez)
    
    # Return the parameters and normalization factor
    if normm is None:
        return rez, normf
    return rez, normf

#class CustomedAxes(Axes):
#    def errorhist(self, data, bins=10, fmt='.', color='dimgrey', err_func = np.sqrt, **kwargs):
#        counts, bin_edges = np.histogram(data, bins=bins, **kwargs)
#        bin_centers = bin_edges[:-1] + (bin_edges[1] - bin_edges[0]) / 2
#        self.errorbar(bin_centers, counts, yerr=err_func(counts), fmt=fmt, color=color, **kwargs)
#        return counts, bin_centers
#
#__subplot = plt.subplots
#
#def subplots(nrows=1, ncols=1, **kwargs):
#    fig, axes = __subplot(nrows=nrows, ncols=ncols, layout='constrained', **kwargs)
#    if isinstance(axes, np.ndarray):
#        custom_axes = []
#        for ax in axes.flat:
#            position = ax.get_position()
#            ax.remove() 
#            custom_ax = CustomedAxes(fig, position)
#            fig.add_axes(custom_ax)
#            custom_axes.append(custom_ax)
#        custom_axes = np.array(custom_axes).reshape(axes.shape)
#    else:
#        position = axes.get_position()
#        axes.remove()
#        custom_axes = CustomedAxes(fig, position)
#        fig.add_axes(custom_axes)
#    return fig, custom_axes
#
#plt.subplots = subplots


