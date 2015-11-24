from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

'''
Este script calcula la constante de Hubble a partir de
datos experimentales obtenidos en 1929 y su intervalo de
confianza al 95% mediante un ajuste lineal que minimiza
chi cuadrado.
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
S_vv = sum(x**2 for x in v)

# PRIMER CÁLCULO DE H
H1 = S_rv / S_rr
print(H1)

# SEGUNDO CÁLCULO DE H
H2 = S_vv / S_rv
print(H2)

# CÁLCULO FINAL DE H
H = (H1 + H2) / 2
print(H)

# INTERVALOS DE CONFIANZA
np.random.seed(1943)
Nboot = 1000
mean_values_1 = np.zeros(Nboot)
mean_values_2 = np.zeros(Nboot)
mean_final = np.zeros(Nboot)

for i in range(Nboot):
    s = np.random.randint(low=0, high=n, size=n)
    num1 = 0
    den1 = 0
    num2 = 0
    den2 = 0
    for j in s:
        num1 += v[j] * r[j]
        den1 += r[j]**2
        num2 += v[j]**2
        den2 += v[j] * r[j]
    mean_values_1[i] = np.mean(num1 / den1)
    mean_values_2[i] = np.mean(num2 / den2)
    mean_final[i] = (mean_values_1[i] + mean_values_2[i]) / 2

orden = np.sort(mean_final)
low = orden[int(Nboot * 0.025)]
high = orden[int(Nboot * 0.975)]
print "El intervalo de confianza al 95% es: [{}:{}]".format(low, high)
