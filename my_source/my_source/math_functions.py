# my_package/math_functions.py

import numpy as np
from numba import njit

@njit(fastmath=True)
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

@njit(fastmath=True)
def gaussian(x, mu, sigma):
    sigma2 = np.power(sigma, 2)
    return np.power(sigma2 * 2 * np.pi, -2) * np.exp(-np.power(x - mu, 2) / (2 * sigma2))

@njit(fastmath=True)
def heaviside(x, d):
    return np.where(x >= d, 1.0, 0.0)

@njit(fastmath=True)
def nois_log(x):
    return heaviside(x, 0) * np.log(x)

@njit(fastmath=True)
def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

@njit(fastmath=True)
def factoriall(n):
    result = np.zeros_like(n)
    for i in range(n.size):
        result[i] = factorial(n[i])
    return result

@njit(fastmath=True)
def puasson(x, n):
    return np.exp(-x) * np.power(x, n) * np.power(factoriall(n), -1)

@njit(fastmath=True)
def exponential_distribution(x, lam, a=0, b=0):
    if a == 0 and b == 0:
        normalization_factor = 1
    else:
        normalization_factor = lam / (np.exp(lam * a) - np.exp(lam * b))
    return normalization_factor * np.exp(-lam * x)
