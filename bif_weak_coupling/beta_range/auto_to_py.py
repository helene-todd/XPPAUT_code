from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import math as math
import random as rand
import os
import csv
import argparse

# TO DO : Rewrite this code to make it more readable.
# USAGE : Run in terminal "python auto_to_py.py beta_0.05.dat beta_0.1.dat beta_0.15.dat beta_0.2.dat line.dat stable1.dat stable2.dat".

p = argparse.ArgumentParser()
p.add_argument('files', type=str, nargs='*')
args = p.parse_args()

def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for _ in in_file)

c = ['#511845', '#900c3f', '#c70039', '#ff5733']
s = ['-', '--']

I = [[]]
phi = [[]]
stability = []

for filename in args.files :
    with open(filename, newline='') as file:
        datareader = csv.reader(file, delimiter=' ')

        last_line_nb = row_count(filename)

        last_I = -999
        last_phi = -999
        last_stability = 0

        # seperate by checking if two consecutive values are duplicates
        for row in datareader:

            # this last condition avoids a list with one value when two consecutive values are duplicates
            if last_I == float(row[0]) and len(I[-1]) > 1 :
                I.append([])
                phi.append([])
                if last_stability != 0 :
                    stability.append(last_stability)

            if last_I != -999 :
                I[-1].append(last_I)
                phi[-1].append(last_phi)

            if last_stability != int(row[3]) and len(I[-1]) > 1:
                I.append([])
                phi.append([])
                if last_stability != 0 :
                    stability.append(last_stability)

            # if at last line, then stop checking for consecutive values and just add the remaining data
            if last_line_nb == datareader.line_num:
                I[-1].append(last_I)
                phi[-1].append(last_phi)
                stability.append(last_stability)

            last_I = float(row[0])
            last_phi = float(row[1])
            last_stability = int(row[3])

plt.figure(figsize=(8,6))
b = [0.05, 0.1, 0.15, 0.2]
for k in range(len(I)) :
    if k < 8 :
        plt.plot(I[k], phi[k], color=c[int(k/2)], linestyle=s[stability[k]-1], label=f'$\\beta={b[int(k/2)]}$')

    else :
        if stability[k] == 1 :
            plt.plot(I[k], phi[k], color='black', linestyle=s[stability[k]-1])
        if stability[k] == 2 :
            plt.plot(I[k], phi[k], color='black', linestyle=s[stability[k]-1])

plt.title('Bifurcation diagram for two weakly coupled neurons', fontsize=13)
plt.xlabel('Current $I$', fontsize=12)
plt.ylabel('Phase Difference $\phi$', fontsize=12)

# remove duplicate legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1, 0.95))

plt.savefig('beta_range.png', dpi=600)
plt.show()
