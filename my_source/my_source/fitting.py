# my_package/fitting.py

import numpy as np
from scipy.optimize import minimize
from .math_functions import puasson

def normalization(counts, bin_edges):
    total_counts = np.sum(counts)
    bin_width = bin_edges[1] - bin_edges[0]
    return bin_width * total_counts

def max_bin_lik(f, bin_centers, counts, args0, des=False, norm=False, h=1e-7, bounds=None, normm=None, method='SLSQP'):
    likelihoodn = lambda x, n, norm, *args: np.log(puasson(f(x, *args) / norm, n))
    dx = bin_centers[1] - bin_centers[0]
    counts = counts / np.sum(counts) * dx

    def df(args0, bin_centers, counts): 
        normf = np.sum(f(bin_centers, *args0)) * dx
        return -np.sum(likelihoodn(bin_centers, counts, normf, *args0))

    rez = minimize(df, args0, args=(bin_centers, counts), method=method, options={'xatol': h, 'fatol': h}, bounds=bounds)
    normf = np.sum(f(bin_centers, *rez.x)) * dx
    print(rez)
    if normm is None:
        return rez.x, normf
    return rez.x, normf
