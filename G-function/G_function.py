from matplotlib import cm, rcParams
import matplotlib.pyplot as plt
import numpy as np
import math as math
import random as rand

""" G(phi) function in Rinzel & Lewis' article (2003) under weak coupling """

c = ['#aa3863', '#d97020', '#ef9f07', '#449775', '#3b7d86']
rcParams.update({'figure.autolayout': True})

def T(I):
    return math.log(I/(I-1))

def G(phi, I, gamma):
    if phi != 0 and phi != 1:
        return gamma*(2/T(I))*(phi*math.sinh((1-phi)*T(I)) - (1-phi)*math.sinh(phi*T(I))) + gamma*(beta/(I*T(I)*T(I)))*(math.exp(phi*T(I)) - math.exp((1-phi)*T(I)))
    else :
        return 0

""" Varying Gamma """

gamma = [0.01, 0.1, 0.2, 0.4]
beta = 0.2


plt.figure(figsize=(8,5))
vector_phi = np.linspace(0,1,1000)
zero_line = np.zeros(len(vector_phi))
plt.plot(vector_phi, zero_line, linestyle='--', color='k')

k = 0
for g in gamma :
    vector_G = []
    for el in vector_phi:
        vector_G.append(G(el, 1.05, g))
    vector_G = np.array(vector_G)
    plt.plot(vector_phi, vector_G, label=f'$\gamma = {g}$', color = c[k])
    k += 1


plt.xlabel('$\phi$', size=14)
plt.ylabel('$G(\phi)$', size=14)
plt.title('G function for $I=1.05$')

zero_crossings = np.where(np.diff(np.sign(vector_G-zero_line)))[0]
print(zero_crossings)

plt.legend()
plt.savefig('G_function_range_gammas.png', dpi=600)
plt.show()
plt.close()

""" Varying I """
"""
gamma = 1
beta = 0.2
I = [1.15, 1.2, 1.4]

plt.figure(figsize=(8,5))
vector_phi = np.linspace(0,1,1000)
zero_line = np.zeros(len(vector_phi))
plt.plot(vector_phi, zero_line, linestyle='--', color='k')

k = 0
for current in I :
    vector_G = []
    for el in vector_phi:
        vector_G.append(G(el, current, gamma))
    vector_G = np.array(vector_G)
    plt.plot(vector_phi, vector_G, label=f'$I = {current}$', color = c[k])
    k += 1


plt.xlabel('$\phi$', size=14)
plt.ylabel('$G(\phi)$', size=14)

zero_crossings = np.where(np.diff(np.sign(vector_G-zero_line)))[0]
print(zero_crossings)

plt.legend()
plt.show()
"""
