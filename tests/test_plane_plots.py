import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from mplsignal.plane_plots import splane, splane_tf, zplane, zplane_tf


@image_comparison(['zplane.png'], style="mpl20")
def test_zplane():
    fig, ax = plt.subplots()
    zeros = [0.5 + 0.5j, 0.5 - 0.5j]
    poles = [-0.5 + 0.5j, -0.5 - 0.5j]
    zplane(zeros, poles, ax=ax)


@image_comparison(['zplane_multiple.png'], remove_text=True, style="mpl20")
def test_zplane_multiple():
    fig, ax = plt.subplots()
    zeros = [0.5 + 0.5j, 0.5 - 0.5j] * 3
    poles = [-0.5 + 0.5j, -0.5 - 0.5j] * 2
    zplane(zeros, poles, ax=ax)


@image_comparison(
    ['zplane_multiplicity_properties.png'], remove_text=True, style="mpl20"
)
def test_zplane_multiplicity_properties():
    fig, ax = plt.subplots()
    zeros = [0.2 + 0.8j, 0.2 - 0.8j] * 3
    poles = [-0.7 + 0.3j, -0.7 - 0.3j] * 2
    props = {'color': 'b', 'fontsize': 20, 'backgroundcolor': 'g', 'rotation': 45}
    zplane(zeros, poles, ax=ax, multiplicity_props=props)


@check_figures_equal(extensions=["png"])
def test_pole_zero_properties(fig_test, fig_ref):
    zeros = [0.2 + 0.8j, 0.2 - 0.8j]
    poles = [-0.7 + 0.3j, -0.7 - 0.3j]
    ax_test = fig_test.add_subplot()
    zplane(
        zeros,
        poles,
        ax=ax_test,
        zeromarker='s',
        zerofillstyle='top',
        markercolor='r',
        polemarker='*',
        polefillstyle='left',
    )

    ax_ref = fig_ref.add_subplot()
    zero_props = {'marker': 's', 'color': 'r', 'fillstyle': 'top'}
    pole_props = {'marker': '*', 'color': 'r', 'fillstyle': 'left'}
    zplane(zeros, poles, ax=ax_ref, zero_props=zero_props, pole_props=pole_props)


@image_comparison(['splane.png'], style="mpl20")
def test_splane():
    fig, ax = plt.subplots()
    zeros = [0.5j, -0.5j]
    poles = [-0.5 + 0.5j, -0.5 - 0.5j]
    splane(zeros, poles, ax=ax)


@image_comparison(['zplane_tf.png'], style="mpl20")
def test_zplane_tf():
    fig, ax = plt.subplots()
    num = [1, 1, 0]
    den = [1, -1.2, 0.5]
    zplane_tf(num, den, ax=ax)


@image_comparison(['splane_tf.png'], style="mpl20")
def test_splane_tf():
    fig, ax = plt.subplots()
    num = [1, 0, 1]
    den = [1, 1.2, 0.5]
    splane_tf(num, den, ax=ax)
