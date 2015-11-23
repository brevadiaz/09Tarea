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
H_0 = S_rv / S_rr
print(H_0)

# INTERVALOS DE CONFIANZA
np.random.seed(1943)
Nboot = 1000
mean_values = np.zeros(Nboot)

for i in range(Nboot):
    s = np.random.randint(low=0, high=n, size=n)
    num = 0
    den = 0
    for j in s:
        num += v[j] * r[j]
        den += r[j]
    mean_values[i] = np.mean(num / den)

orden = np.sort(mean_values)
low = orden[int(Nboot * 0.025)]
high = orden[int(Nboot * 0.975)]
print "El intervalo de confianza al 95% es: [{}:{}]".format(low, high)
