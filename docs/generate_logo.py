#!/usr/bin/env python3
"""
Created on Thu Mar  9 10:53:13 2023

@author: oscgu95
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.text import Text

fig = plt.figure()
y = np.linspace(0, 2 * np.pi, 100)
x = np.sin(y)

fp = {'size': 25, 'weight': 'bold'}
t1 = Text(0.0, 0.05, "mpl", fontproperties=fp)
t2 = Text(0.19, 0.05, "ignal", fontproperties=fp)

line = Line2D(0.155 + 0.03 * x, 0.05 + 0.01 * y, lw=5)
fig.add_artist(t1)
fig.add_artist(t2)
fig.add_artist(line)
fig.savefig("_static/mplsignal_logo.svg", bbox_inches='tight', transparent=True)

t1.set_c('w')
t2.set_c('w')

fig.savefig("_static/mplsignal_logo_dark.svg", bbox_inches='tight', transparent=True)
