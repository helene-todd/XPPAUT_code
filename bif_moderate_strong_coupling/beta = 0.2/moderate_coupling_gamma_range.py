import matplotlib.pyplot as plt
import numpy as np
import math
from shapely import geometry
import os

# TODO : write to file in xppaut style rather than like this.. or open weak coupling solution

c = ['#511845', '#900c3f', '#c70039', '#ff5733']
s = ['-', '--']

def findIntersection(contour1,contour2):
    p1 = contour1.collections[0].get_paths()[0]
    v1 = p1.vertices
    p2 = contour2.collections[0].get_paths()[0]
    v2 = p2.vertices

    if len(v1)> 1 and len(v2)>1 :
        poly1 = geometry.LineString(v1)
        poly2 = geometry.LineString(v2)
        intersection = poly1.intersection(poly2)
        return intersection

    else :
        return None

def u1(phi, T, gamma, beta) :
    return (np.exp((1-phi)*T)*(2-2*I) + 2*I)/(1 + np.exp(-2*gamma*(1-phi)*T)) - gamma*beta

def u2(phi, T, gamma, beta) :
    return (np.exp(phi*T)*(2-2*I) + 2*I)/(1 + np.exp(-2*gamma*phi*T)) - gamma*beta

def I_function(T, gamma, beta) :
    return -1/2*(beta*gamma*(math.exp((T*gamma + 1/2*T)) + math.exp((1/2*T))) - 2*math.exp((T*gamma + T)) + math.exp((T*gamma + 1/2*T)) - math.exp((1/2*T)))/(math.exp((T*gamma + T)) - math.exp((T*gamma + 1/2*T)) + math.exp((1/2*T)) - 1)

beta = 0.2
delta = 0.01

# must be moderate or strong gammas
gammas = [0.4]

for gamma in gammas :
    if not os.path.exists(f'gamma_{gamma}.dat'):
        os.mknod(f'gamma_{gamma}.dat')

xrange = np.arange(0., 1., delta) # phi
yrange = np.arange(0., 2., delta) # I
X, Y = np.meshgrid(xrange,yrange)

for gamma in gammas :

    f = open(f'gamma_{gamma}.dat', 'w')

    upper_fork = []
    lower_fork = []
    values_I = []

    # We begin by finding non-physical solution :
    # fixing phi = 0.5, we look for the smallest value T such that the equation is > 1
    # then we find which value of I this corresponds to.

    low_I = 0
    for T in np.linspace(0.1, 100, 1000):
        if (math.exp(T/2)*(2-2*I_function(T, gamma, beta)) + 2*I_function(T, gamma, beta))/(1+math.exp(-gamma*T)) > 1 :
            low_I = I_function(T, gamma, beta)
            break

    print(low_I)
    for I in np.linspace(low_I, 2, 10000) :
        print(I)
        F = - np.exp(-(1+2*gamma)*X*Y)*u2(X,Y, gamma, beta) - u1(X,Y, gamma, beta) +1 - np.exp(-(1+2*gamma)*X*Y)*gamma*beta
        G = 2*I*(1-np.exp(-(1-X)*Y)) + u1(X,Y, gamma, beta)*np.exp(-(1-X)*Y) -1 -u2(X,Y, gamma, beta) +gamma*beta*np.exp(-(1-X)*Y)

        c1 = plt.contour(X, Y, F , [0], colors='blue')
        c2 = plt.contour(X, Y, G , [0], colors='red')

        intersection_points = findIntersection(c1,c2)
        #print(intersection_points)

        # For a single point value : if isinstance(intersection_points, geometry.point.Point)
        if isinstance(intersection_points, geometry.multipoint.MultiPoint) :
            #print(round(I, 4), round(intersection_points[0].x, 4))
            values_I.append(round(I, 7))
            lower_fork.append(round(intersection_points[0].x, 7))
            upper_fork.append(round(intersection_points[2].x, 7))

    # We kind of "cheat" a little here to get the fork to intersect with phi = 0.5 in the plot
    values_I.append(max(values_I))
    lower_fork.append(0.5)
    upper_fork.append(0.5)

    for I in np.linspace(2, max(values_I), 200):
        f.write(f'{round(I, 7)} 0.5 0.5 2 1 0\n')

    for I in np.linspace(max(values_I), low_I, 200):
        f.write(f'{round(I, 7)} 0.5 0.5 1 1 0\n')

    for I in np.linspace(low_I, 1, 200):
        f.write(f'{round(I, 7)} 0.5 0.5 2 1 0\n')

    for k in range(len(values_I)-1, -1, -1):
        f.write(f'{values_I[k]} {upper_fork[k]} {upper_fork[k]} 2 2 0\n')

    for k in range(len(values_I)-1, -1, -1):
        f.write(f'{values_I[k]} {lower_fork[k]} {lower_fork[k]} 2 2 0\n')

f.close()
