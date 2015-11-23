from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

'''
Este script calcula la constante de Hubble a partir de
datos experimentales obtenidos en 1929.
'''

# DATOS
datos = np.loadtxt("data/hubble_original.dat")
r = datos[:, 0]
v = datos[:, 1]
n = len(r)  # número de galaxias

# ORGANIZACION DE DATOS
S_r = sum(r)
S_v = sum(v)
S_rr = sum(x**2 for x in r)
S_rv = sum(r[i] * v[i] for i in range(n))

# CÁLCULO DE a Y b
denom = n * S_rr - S_r**2
a = (S_rr * S_v - S_r * S_rv) / denom
b = (n * S_rv - S_r * S_v) / denom

# DESVIACIÓN ESTÁNDAR DE a Y b
sigma = np.sqrt(sum((v[i] - (a + b * r[i]))**2 for i in range(n)) / (n - 2))
sigma_a = np.sqrt((sigma**2 * S_rr) / denom)
sigma_b = np.sqrt((sigma**2 * n) / denom)

print(a)
print(b)
print(sigma_a)
print(sigma_b)

# INTERVALOS DE CONFIANZA
np.random.seed(1943)
Nboot = 10000
num = np.zeros(Nboot)
den = np.zeros(Nboot)
mean_values = np.zeros(Nboot)

for i in range(Nboot):
    s = np.random.randint(low=0, high=n, size=n)
    for j in s:
        num += n * r[j] * v[j] - r[j] * S_v
        den += n * r[j]**2 - r[j] * S_r
    mean_values[i] = np.mean(num / den)

orden = np.sort(mean_values)
low = orden[int(Nboot * 0.025)]
high = orden[int(Nboot * 0.975)]
print "El intervalo de confianza al 95% es: [{}:{}]".format(low, high)
