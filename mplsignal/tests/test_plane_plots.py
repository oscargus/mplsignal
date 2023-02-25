import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison

from mplsignal import plane_plots


@image_comparison(['zplane.png'], style="mpl20")
def test_zplane():
    fig, ax = plt.subplots()
    zeros = [0.5 + 0.5j, 0.5 - 0.5j]
    poles = [-0.5 + 0.5j, -0.5 - 0.5j]
    plane_plots.zplane(zeros, poles, ax=ax)


@image_comparison(['zplane_multiple.png'], remove_text=True, style="mpl20")
def test_zplane_multiple():
    fig, ax = plt.subplots()
    zeros = [0.5 + 0.5j, 0.5 - 0.5j] * 3
    poles = [-0.5 + 0.5j, -0.5 - 0.5j] * 2
    plane_plots.zplane(zeros, poles, ax=ax)
