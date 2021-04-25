from matplotlib import cm, rcParams
import matplotlib.pyplot as plt
import numpy as np
import math
from shapely import geometry

""" ToDo : check if this is equivalent to the G-function for weak coupling """

c = ['#aa3863', '#d97020', '#ef9f07', '#449775', '#3b7d86']
rcParams.update({'figure.autolayout': True})

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


# Only makes sense if I > I_low (see bifurcation diagram code) !!!
I = 1.2
beta = 0.1
gammas = [0.4, 0.3, 0.2, 0.1, 0.01]

vector_x = []
vector_g = []

for gamma in gammas :

    xrange = np.linspace(0, 1, 10000) # phi
    yrange = np.linspace(0, 20, 10000) # T
    X, Y = np.meshgrid(xrange,yrange)

    phi = []
    T = []

    F = - np.exp(-(1+2*gamma)*X*Y)*u2(X,Y, gamma, beta) - u1(X,Y, gamma, beta) +1 - np.exp(-(1+2*gamma)*X*Y)*gamma*beta
    G = 2*I*(1-np.exp(-(1-X)*Y)) + u1(X,Y, gamma, beta)*np.exp(-(1-X)*Y) -1 -u2(X,Y, gamma, beta) +gamma*beta*np.exp(-(1-X)*Y)

    c1 = plt.contour(X, Y, F , [0], colors='blue')
    c2 = plt.contour(X, Y, G , [0], colors='red')

    # Closing the implicit function plots, but can be shown if wanted
    plt.clf()
    plt.close()

    # Since it's symmetric at phi=0.5, we only need values for one side !
    p1 = c1.collections[0].get_paths()[0]
    v1 = p1.vertices
    x1 = v1[:,0]
    y1 = v1[:,1]

    p2 = c2.collections[0].get_paths()[0]
    v2 = p2.vertices
    x2 = v2[:,0]
    y2 = v2[:,1]

    # The code below allows to easily deal with disreptancies in values between x1 and x2
    x = np.intersect1d(x1, x2)
    g = []
    for el in x :
        g.append(y2[np.where(x2 == el)[0][0]]-y1[np.where(x1 == el)[0][0]])
    g = np.array(g)

    # Function is discontinuous for phi in {0,1}
    x = np.insert(x, 0, 0.)
    x = np.insert(x, len(x)-1, 1.)
    g = np.insert(g, 0, 0)
    g = np.insert(g, len(g)-1, 0)

    vector_x.append(x)
    vector_g.append(g)

plt.figure(figsize=(8,5))
for k in range(len(vector_x)):
    plt.plot(vector_x[k], vector_g[k], color=c[k], label=f'$\gamma={gammas[k]}$')

plt.plot([0, 1], [0, 0], color='black', linestyle='--')

plt.xlabel('$\phi$')
#plt.ylabel('$G(\phi)$')
plt.title(f'G? function for $I={I}, \\beta=0.1$')

plt.legend(loc='upper left')
plt.savefig(f'T_function_range_gammas_I={I}.svg')
plt.show()
