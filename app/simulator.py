# import necessary packages
#import pandas as pd
import numpy as np
import sympy as sp
#from sympy.plotting import plot
import matplotlib.pyplot as plt

# setup
data_filename = './data.csv'
points_count = 50

def simulate(l_0, l_1, l_2, l_3, filename):
  # angle
  phi_1 = sp.symbols('\phi_1')
  # links
  l0, l1, l2, l3 = sp.symbols('l_0, l_1, l_2, l_3')
  # relative lengths
  r2, r3, r4 = l2 / l1, l3 / l1, l0 / l1

  # Equations of the angular coordinates of the links
  phi_b = sp.sign(-sp.sin(phi_1)) * sp.acos((r4 - sp.cos(phi_1)) / (sp.sqrt(1 + r4 ** 2 - 2 * r4 * sp.cos(phi_1))))

  phi_3 = phi_b + sp.acos((r2 ** 2 - r3 ** 2 - r4 ** 2 + 2 * r4 * sp.cos(phi_1) - 1) / (2 * r3 * sp.sqrt(1 + r4 ** 2 - 2 * r4 * sp.cos(phi_1))))

  phi_2 = phi_b + sp.acos((1 + r2 ** 2 - r3 ** 2 + r4 ** 2 - 2 * r4 * sp.cos(phi_1)) / (2 * r2 * sp.sqrt(1 + r4 ** 2 - 2 * r4 * sp.cos(phi_1))))

  # read link lengths
  # link_table = pd.read_csv(data_filename)
  # l_0, l_1, l_2, l_3 = link_table['l_0'][0], link_table['l_1'][0], link_table['l_2'][0], link_table['l_3'][0]

  # substitution
  phi_2 = phi_2.subs([(l0, l_0), (l1, l_1), (l2, l_2), (l3, l_3)]) 
  phi_3 = phi_3.subs([(l0, l_0), (l1, l_1), (l2, l_2), (l3, l_3)])
  # convert degrees to radians
  phi_2 = phi_2.subs(phi_1, phi_1 / 180 * sp.pi)
  phi_3 = phi_3.subs(phi_1, phi_1 / 180 * sp.pi)

  # generate points to plot
  X = np.linspace(0, 360, points_count)
  Y2 = [phi_2.subs(phi_1, x) for x in X]
  Y3 = [phi_3.subs(phi_1, x) for x in X]
  # convert to degrees
  Y2 = [y / sp.pi * 180 for y in Y2]
  Y3 = [y / sp.pi * 180 + 180 for y in Y3]

  fg = plt.axes()
  fg.plot(X, Y2, color = 'blue', label = r'$\phi_2$')
  fg.plot(X, Y3, color = 'orange', label = r'$\phi_3$')
  fg.set_xlabel(r'$\phi_1$')
  fg.grid(which="major", linestyle='-')
  fg.grid(which="minor", linestyle=':')
  plt.legend()
  plt.savefig(filename, dpi=300)

