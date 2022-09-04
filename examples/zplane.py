"""
---------------------
``zplane_tf`` example
---------------------

A short example showcasing how to use :func:`~mplsignal.plane_plots.zplane_tf`.
"""

from mplsignal.plane_plots import zplane_tf

num = [1, 1, 1]
den = [1, -1.2, 0.5]
ax = zplane_tf(num=num, den=den)
ax.figure.show()
