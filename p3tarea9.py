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

m, n = np.polyfit(banda_i, banda_z, 1)  # valores experimentales fiteados
print(m)
print(n)
m_calc = np.mean(slope)  # valor pendiente monte carlo
n_calc = np.mean(inter)  # valor coef. posición monte carlo
print(m_calc)
print(n_calc)

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

# HISTOGRAMA PENDIENTE
fig1 = plt.figure(1)
fig1.clf()
plt.hist(slope, bins=100, facecolor='c')
plt.axvline(m_calc, color='r', linewidth=3, label="Valor obtenido")
plt.axvline(low_slope, color='g', linewidth=3,
            label="Limites intervalo de confianza")
plt.axvline(high_slope, color='g', linewidth=3)
plt.xlabel("Pendiente")
plt.ylabel("Frecuencia")
plt.legend(loc=0, fontsize=9)
plt.draw()
plt.show()
plt.savefig('histslope.png')

# HISTOGRAMA COEFICIENTE DE POSICIÓN
fig2 = plt.figure(2)
fig2.clf()
plt.hist(inter, bins=100, facecolor='c')
plt.axvline(n_calc, color='r', linewidth=3, label="Valor obtenido")
plt.axvline(low_inter, color='g', linewidth=3,
            label="Limites intervalo de confianza")
plt.axvline(high_inter, color='g', linewidth=3)
plt.xlabel("Coeficiente de posicion")
plt.ylabel("Frecuencia")
plt.legend(loc=0, fontsize=9)
plt.draw()
plt.show()
plt.savefig('histinter.png')

# GRÁFICO
fig3 = plt.figure(3)
fig3.clf()
f_i = np.linspace(-100, 500, 10000)
f_z = m * f_i + n
plt.errorbar(banda_i, banda_z, xerr=error_i, yerr=error_z,
             fmt='o', color='c', label="Datos experimentales")
plt.plot(f_i, f_z, color='m', label="Ajuste Lineal")
plt.xlabel("Flujo banda i [$10^{-6}Jy$]")
plt.ylabel("Flujo banda z [$10^{-6}Jy$]")
plt.legend(loc=0, fontsize=9)
plt.draw()
plt.show()
plt.savefig('p3.png')
