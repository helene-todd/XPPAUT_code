from matplotlib import cm, rcParams
import matplotlib.pyplot as plt
import numpy as np
import math as math
import random as rand
import os
import csv

rcParams.update({'figure.autolayout': True})

c = ['#aa3863', '#d97020', '#ef9f07', '#449775', '#3b7d86']

times = []
V1 = []
V2 = []

Vth = 1
Vr = -0

with open('gap_potential.dat', newline='') as file:
    datareader = csv.reader(file, delimiter=' ')
    for row in datareader:
        times.append(float(row[0]))
        V2.append(float(row[1]))

V1, V2 = np.array(V1), np.array(V2)
plt.figure(figsize=(11,4))

plt.plot(times, V2, alpha=0.75, color=c[0], linestyle='-', label='Voltage $V$')

plt.xlim(5,15)
plt.ylim(0,0.2)

plt.xlabel('time t ($10^{-2}$ seconds)')
plt.ylabel('voltage $V_k, k \in \{1,2\}$')
plt.title('Gap Potential with $\\beta=0.4$ and $\gamma=0.1$')

plt.legend(loc='upper right')
plt.savefig(f'gap_potential.png', dpi=600)
plt.show()
