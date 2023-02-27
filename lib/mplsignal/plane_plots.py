# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.
"""
Functions for pole-zero plots.
"""

__all__ = [
    "zplane",
    "zplane_tf",
    "splane",
    "splane_tf",
]

import math

import adjustText
import matplotlib.pyplot as plt
import numpy as np


def zplane(
    zeros=None,
    poles=None,
    ax=None,
    adjust=1,
    spinelinewidth=0.2,
    spinecolor='black',
    zeromarker='o',
    polemarker='x',
    unitcircle=True,
    markercolor=None,
    zerofillstyle='none',
    polefillstyle='none',
    reallabel=None,
    imaglabel=None,
    zero_props=None,
    pole_props=None,
    multiplicity_props=None,
    **kwargs,
):
    r"""
    Plot the z-plane of a discrete-time system.

    Parameters
    ----------
    zeros : array-like, optional
        Zeros of transfer function.

    poles : array-like, optional
        Poles of transfer function.

    ax : :class:`~matplotlib.axes.Axes`, optional
        Axes to plot in.

    adjust : int, optional, default: 1
        Number of times to execute text adjustment. Set to 0 to disable.

    spinelinewidth : float, default: 0.2
        Line width of spines.

    spinecolor : color, default: 'black'
        Line color of spines.

    unitcircle : bool, default: True
        If a unit circle is drawn.

    zeromarker : marker, default: 'o'
        Marker to use for zeros.

    polemarker : marker, default: 'x'
        Marker to use for poles.

    markercolor : color
        Color to use for pole and zero markers, default: None

    zerofillstyle : fill style, default: 'none'
        Fill style to use for zeros.

    polefillstyle : fill style, default: 'none'
        Fill style to use for poles.

    reallabel : str, optional
        Label for real axis. None gives "Real part".

    imaglabel : str, optional
        Label for imaginary axis. None gives "Imaginary part".

    zero_props : dict, optional
        Additional arguments for the zero markers when calling
        :meth:`~matplotlib.Axes.plot`. This can be used instead of *zeromarker*
        ('marker'), *markercolor* ('color'), and/or *zerofillstyle* ('fillstyle'),
        but also for all other arguments of :meth:`~matplotlib.Axes.plot`.
        Any arguments provided here will override other arguments.

        .. versionadded:: 0.2.0

    pole_props : dict, optional
        Additional arguments for the zero markers when calling
        :meth:`~matplotlib.Axes.plot`. This can be used instead of *polemarker*
        ('marker'), *markercolor* ('color'), and/or *polefillstyle* ('fillstyle'),
        but also for all other arguments of :meth:`~matplotlib.Axes.plot`.
        Any arguments provided here will override other arguments.

        .. versionadded:: 0.2.0

    multiplicity_props : dict, optional
        Arguments to :meth:`~matplotlib.Axes.text` for changing the
        properties of the texts showing multiplicity.

        .. versionadded:: 0.2.0

    **kwargs
        Additional arguments passed to :meth:`matplotlib.Axes.plot`.

    Returns
    -------
    None.
    """
    # if Axes not provided
    if ax is None:
        ax = plt.gca()
    ax.axvline(color=spinecolor, linewidth=spinelinewidth)
    ax.axhline(color=spinecolor, linewidth=spinelinewidth)
    if markercolor is None:
        markercolor = ax._get_lines.get_next_color()
    if reallabel is None:
        reallabel = "Real part"
    if imaglabel is None:
        imaglabel = "Imaginary part"

    # Update zero properties
    if zero_props is None:
        zero_props = {}
    if "marker" not in zero_props:
        zero_props["marker"] = zeromarker
    if "fillstyle" not in zero_props:
        zero_props["fillstyle"] = zerofillstyle
    if "color" not in zero_props:
        zero_props["color"] = markercolor
    if "ls" not in zero_props and "linestyle" not in zero_props:
        zero_props["ls"] = 'none'

    # Update pole properties
    if pole_props is None:
        pole_props = {}
    if "marker" not in pole_props:
        pole_props["marker"] = polemarker
    if "fillstyle" not in pole_props:
        pole_props["fillstyle"] = polefillstyle
    if "color" not in pole_props:
        pole_props["color"] = markercolor
    if "ls" not in pole_props and "linestyle" not in pole_props:
        pole_props["ls"] = 'none'

    if unitcircle:
        ax.add_patch(
            plt.Circle(
                (0, 0),
                radius=1,
                fill=False,
                edgecolor=spinecolor,
                linewidth=spinelinewidth,
            )
        )
    texts = _plot_plane(
        zeros,
        poles,
        ax=ax,
        reallabel=reallabel,
        imaglabel=imaglabel,
        zero_props=zero_props,
        pole_props=pole_props,
        multiplicity_props=multiplicity_props,
        **kwargs,
    )
    if texts:
        for _ in range(adjust):
            # Fix for adjustText = 0.8
            ax.figure.draw_without_rendering()
            adjustText.adjust_text(texts, ax=ax)
    ax.axis('equal')
    return ax


def splane(zeros=None, poles=None, **kwargs):
    """
    Plot the s-plane of a continuous-time system.

    Identical to :func:`zplane`, except that *unitcircle* is False.
    """
    return zplane(zeros=zeros, poles=poles, unitcircle=False, **kwargs)


def zplane_tf(num=None, den=None, **kwargs):
    """
    Plot the z-plane of a discrete-time system represented as a transfer function.

    Parameters
    ----------
    num : array-like, optional
        Numerator of transfer function.
    den : array-like, optional
        Denominator of transfer function.
    **kwargs
        Additional arguments passed to :func:`zplane`.
    """
    zeros = None if num is None else np.roots(num)
    poles = None if den is None else np.roots(den)
    return zplane(zeros=zeros, poles=poles, **kwargs)


def splane_tf(num=None, den=None, **kwargs):
    """
    Plot the s-plane of a continuous-time system represented as a transfer function.

    Parameters
    ----------
    num : array-like, optional
        Numerator of transfer function.
    den : array-like, optional
        Denominator of transfer function.
    **kwargs
        Additional arguments passed to :func:`splane`.
    """
    zeros = None if num is None else np.roots(num)
    poles = None if den is None else np.roots(den)
    return splane(zeros=zeros, poles=poles, **kwargs)


def _get_positions(items):
    """
    Convert complex poles and zeros to x- and y-positions.

    For poles and zeros with multiplicity, add multiplicity strings
    and x- and y-positions.

    Parameters
    ----------
    items : list
        List of complex positions.

    Returns
    -------
    pos_x : list
        List with x-positions for *items*.
    pos_x : list
        List with y-positions for *items*.
    texts : list
        List with (x, y, multiplicity-string)-tuples for items with multiplicity > 1.
    """
    pos_x = []
    pos_y = []
    texts = []
    for zero, mul in items.items():
        x = np.real(zero)
        y = np.imag(zero)
        pos_x.append(x)
        pos_y.append(y)
        if mul > 1:
            texts.append((x, y, f"{mul}"))

    return pos_x, pos_y, texts


def _plot_plane(
    zeros,
    poles,
    reallabel,
    imaglabel,
    ax=None,
    zero_props=None,
    pole_props=None,
    multiplicity_props=None,
    **kwargs,
):
    """
    Internal function for plotting poles and zeros.

    Parameters
    ----------
    zeros
    poles
    reallabel
    imaglabel
    ax
    zero_props
    pole_props
    multiplicity_props
    **kwargs

    Returns
    -------
    List of texts.
    """
    ret = []
    if multiplicity_props is None:
        multiplicity_props = {}
    if zeros is not None:
        zeros_d = _get_multiplicities(zeros)
        x_pos, y_pos, texts = _get_positions(zeros_d)
        ax.plot(
            x_pos,
            y_pos,
            **zero_props,
            **kwargs,
        )
        ret += [ax.text(x, y, text, **multiplicity_props) for x, y, text in texts]

    if poles is not None:
        poles_d = _get_multiplicities(poles)
        x_pos, y_pos, texts = _get_positions(poles_d)
        ax.plot(
            x_pos,
            y_pos,
            **pole_props,
            **kwargs,
        )
        ret += [ax.text(x, y, text, **multiplicity_props) for x, y, text in texts]

    ax.set_xlabel(reallabel)
    ax.set_ylabel(imaglabel)
    return ret


def _is_close(x, y):
    """Check if poles/zeros are close."""
    return math.isclose(np.real(x), np.real(y)) and math.isclose(np.imag(x), np.imag(y))


def _get_multiplicities(x):
    """Turn list of poles/zeros into a dict with location and multiplicity."""
    res = dict()
    for val in x:
        existed = False
        for ref in res:
            if _is_close(val, ref):
                res[ref] += 1
                existed = True
                continue
        if not existed:
            res[val] = 1
    return res
