from matplotlib import cm
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import math as math
import random as rand
import os
import csv

rcParams.update({'figure.autolayout': True})

c = ['#20639B', '#ED553B', '#3CAEA3', '#7C5295']
# blue, red, green, pruple

times_plot1 = []
V1_plot1 = []
V2_plot1 = []

times_plot2 = []
V1_plot2 = []
V2_plot2 = []

Vth = 1
Vr = -0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4), sharey=True)

with open('asynchro_sol.dat', newline='') as file:
    datareader = csv.reader(file, delimiter=' ')
    for row in datareader:

        if float(row[0]) <= 10 :
            times_plot1.append(float(row[0]))
            V1_plot1.append(float(row[1]))
            V2_plot1.append(float(row[2]))

        if float(row[0]) >= 990 :
            times_plot2.append(float(row[0]))
            V1_plot2.append(float(row[1]))
            V2_plot2.append(float(row[2]))

ax1.plot(times_plot1, V1_plot1, alpha=0.75, color=c[0], linestyle='-')
ax1.plot(times_plot1, V2_plot1, alpha=0.75, color=c[1], linestyle='-')

ax2.plot(times_plot2, V1_plot2, alpha=0.75, color=c[0], linestyle='-', label='$V_1$')
ax2.plot(times_plot2, V2_plot2, alpha=0.75, color=c[1], linestyle='-', label='$V_2$')

# A spike occurs iff there was a reset
spike_times_V1_plot1 = [times_plot1[i] for i in range(1,len(V1_plot1)) if abs(V1_plot1[i]-V1_plot1[i-1]) > (Vth-Vr)/2]
spike_times_V2_plot1 = [times_plot1[i] for i in range(1,len(V2_plot1)) if abs(V2_plot1[i]-V2_plot1[i-1]) > (Vth-Vr)/2]

for t in spike_times_V1_plot1:
    ax1.plot([t, t], [Vth, Vth+0.5], alpha=0.75, color=c[0])

for t in spike_times_V2_plot1:
    ax1.plot([t, t], [Vth, Vth+0.5], alpha=0.75, color=c[1])

# A spike occurs iff there was a reset
spike_times_V1_plot2 = [times_plot2[i] for i in range(1,len(V1_plot2)) if abs(V1_plot2[i]-V1_plot2[i-1]) > (Vth-Vr)/2]
spike_times_V2_plot2 = [times_plot2[i] for i in range(1,len(V2_plot2)) if abs(V2_plot2[i]-V2_plot2[i-1]) > (Vth-Vr)/2]

for t in spike_times_V1_plot2:
    ax2.plot([t, t], [Vth, Vth+0.5], alpha=0.75, color=c[0])

for t in spike_times_V2_plot2:
    ax2.plot([t, t], [Vth, Vth+0.5], alpha=0.75, color=c[1])

ax1.set_xlabel('Time ($10^{-2}$ seconds)')
ax2.set_xlabel('Time ($10^{-2}$ seconds)')
ax1.set_ylabel('Voltage $V_k, k \in \{1,2\}$')

fig.suptitle('Example of Asynchronous Solution')
plt.legend()

plt.savefig('asynchronous_example.png', dpi=600)
plt.show()
