# import necessary packages
# import pandas as pd
# import numpy as np
from sympy import *
#from sympy.plotting import plot
import matplotlib.pyplot as plt

# setup
data_filename = './data.csv'
points_count = 50
step = 8

def differentiate(X, Y):
    slopes = []
    for i in range(step, len(X)):
        slope = (Y[i] - Y[i - step]) / (X[i] - X[i - step])
        slopes.append(slope)
    return slopes

def simulate(l_0, l_1, l_2, l_3, filename1, filename2):
  # angle
  phi_1 = symbols('\phi_1')
  # links
  l0, l1, l2, l3 = symbols('l_0, l_1, l_2, l_3')
  # relative lengths
  r2, r3, r4 = l2 / l1, l3 / l1, l0 / l1

  # Equations of the angular coordinates of the links
  phi_b = sign(-sin(phi_1)) * acos((r4 - cos(phi_1)) / ( sqrt(1 + r4 ** 2 - 2 * r4 *  cos(phi_1))))

  phi_3 = phi_b +  acos((r2 ** 2 - r3 ** 2 - r4 ** 2 + 2 * r4 *  cos(phi_1) - 1) / (2 * r3 *  sqrt(1 + r4 ** 2 - 2 * r4 *  cos(phi_1))))

  phi_2 = phi_b +  acos((1 + r2 ** 2 - r3 ** 2 + r4 ** 2 - 2 * r4 *  cos(phi_1)) / (2 * r2 *  sqrt(1 + r4 ** 2 - 2 * r4 *  cos(phi_1))))

  # read link lengths
  # link_table = pd.read_csv(data_filename)
  # l_0, l_1, l_2, l_3 = link_table['l_0'][0], link_table['l_1'][0], link_table['l_2'][0], link_table['l_3'][0]

  # substitution
  phi_2 = phi_2.subs([(l0, l_0), (l1, l_1), (l2, l_2), (l3, l_3)]) 
  phi_3 = phi_3.subs([(l0, l_0), (l1, l_1), (l2, l_2), (l3, l_3)])
  # convert degrees to radians
  phi_2 = phi_2.subs(phi_1, phi_1 / 180 *  pi)
  phi_3 = phi_3.subs(phi_1, phi_1 / 180 *  pi)

  # generate points to plot
  pts_step = 360 / points_count
  X = [pts_step * x for x in range(points_count)]
  Y2 = [phi_2.subs(phi_1, x) for x in X]
  Y3 = [phi_3.subs(phi_1, x) for x in X]
  # convert to degrees
  Y2 = [y /  pi * 180 for y in Y2]
  Y3 = [y /  pi * 180 + 180 for y in Y3]

  # plot angles
  plt.clf()
  fg = plt.axes()
  fg.plot(X, Y2, color = 'blue', label = r'$\phi_2$')
  fg.plot(X, Y3, color = 'orange', label = r'$\phi_3$')
  fg.set_xlabel(r'$\phi_1$')
  fg.grid(which="major", linestyle='-')
  fg.grid(which="minor", linestyle=':')
  plt.legend()
  plt.savefig(filename1, dpi=300)

  # get angular velocities
  w2 = differentiate(X, Y2)
  w3 = differentiate(X, Y3)
  T = X[step:]

  # plot angular velocities
  plt.clf()
  fg = plt.axes()
  fg.plot(T, w2, color = 'blue', label = r'$\omega_2$')
  fg.plot(T, w3, color = 'orange', label = r'$\omega_3$')
  fg.set_xlabel(r'$t, s \quad \omega_1 = 1 rad / s$')
  fg.grid(which="major", linestyle='-')
  fg.grid(which="minor", linestyle=':')
  plt.legend()
  plt.savefig(filename2, dpi=300)

