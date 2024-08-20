import numpy as np
from scipy.optimize import curve_fit, minimize
from numpy import log, sqrt, exp, pi, e
import os
from numba import njit

Lamc_m = 2.28646
Lamc_25_m = 2.5925
Lamc_26_m = 2.628
D_0_m = 1.86483
D_st_p_m = 2.01026
D_st_0_m = 2.00685
Pi_p_m = 0.13957
Pi_0_m = 0.13498
K_s_m = 0.497611
K_p_m = 0.493677

x = np.array([1. , 2. ])
n = np.array([1, 2])

@njit(fastmath = True)
def eval_chebyt(n, x):
    if n == 0:
        return np.ones_like(x)
    elif n == 1:
        return x
    elif n == 2:
        return 2 * np.power(x, 2) - 1
    elif n == 3:
        return 4 * np.power(x, 3) - 3 * x
    elif n == 4:
        return 8 * np.power(x, 4) - 8 * np.power(x, 2) + 1
    elif n == 5:
        return 16 * np.power(x, 5) - 20 * np.power(x, 3) + 5 * x

eval_chebyt(1, x)


@njit(fastmath = True)
def gaussian(x, mu, sigma): 
    sigma2 = np.power(sigma, 2)
    return np.power(sigma2*2*pi, -2) * np.exp(-np.power(x-mu, 2)/(2*sigma2))
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



@njit(fastmath = True)
def exponential_distribution(x, lam, a = 0, b = 0):
    if a == 0 and b == 0:
        normalization_factor = 1
    else:
        normalization_factor = lam / (np.exp(lam * a) - np.exp(lam * b))
    return normalization_factor * np.exp(-lam * x)


def normalization(counts, bin_edges):
    total_counts = np.sum(counts)
    bin_width = bin_edges[1] - bin_edges[0]
    return bin_width * total_counts

def rm(fname):
    if os.path.exists(fname):
        os.remove(fname)
    else:
        print("The file does not exist") 

def max_bin_lik(f, bin_centers, counts, args0, des = False, norm = False, h = 1e-7, bounds = None, normm = None, method='SLSQP'):
    likelihoodn = lambda x, n, norm, *args: np.log(puasson(f(x, *args)/norm, n))
    dx = bin_centers[1] - bin_centers[0]
    counts = counts/np.sum(counts)*dx
    def df(args0, bin_centers, counts): 
        normf = np.sum(f(bin_centers, *args0))*dx
        return -np.sum(likelihoodn(bin_centers, counts, normf, *args0))
    rez = minimize(df, args0, args=(bin_centers, counts), method = method, options={'xatol': h, 'fatol': h}, bounds=bounds)
    normf = np.sum(f(bin_centers, *rez.x))*dx
    print(rez)
    if normm == None:
        return rez.x, normf
    return rez.x, normf

