from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

'''
Esta script encuentra la línea recta que mejor modela la
relación entre el flujo de la banda i y la banda z y su
intervalo de confianza al 95% mediante una simulación de
Montecarlo.
'''

# DATOS
datos = np.loadtxt("data/DR9Q.DAT", usecols=(80, 81, 82, 83))
banda_i = datos[:, 0] * 3.631
error_i = datos[:, 1] * 3.631
banda_z = datos[:, 2] * 3.631
error_z = datos[:, 3] * 3.631
n = len(banda_i)  # número de cuásares
N = 5000  # número de puntos de Montecarlo
slope = np.zeros(N)  # vector que guarda las pendientes
inter = np.zeros(N)  # vector que guarda coef. de posición

# SIMULACIÓN DE MONTECARLO
for i in range(N):
    r = np.random.normal(0, 1, size=n)
    muestra_i = banda_i + r * error_i
    muestra_z = banda_z + r * error_z
    slope[i], inter[i] = np.polyfit(muestra_i, muestra_z, 1)

m, n = np.polyfit(banda_i, banda_z, 1)
print(m)
print(n)

# INTERVALO DE CONFIANZA
slope_orden = np.sort(slope)
inter_orden = np.sort(inter)
low_slope = slope_orden[int(N * 0.025)]
high_slope = slope_orden[int(N * 0.975)]
low_inter = inter_orden[int(N * 0.025)]
high_inter = inter_orden[int(N * 0.975)]
print """El intervalo de confianza de la pendiente al 95% es:
       [{}:{}]""".format(low_slope, high_slope)
print """El intervalo de confianza del coef. de posicion al 95% es:
       [{}:{}]""".format(low_inter, high_inter)
