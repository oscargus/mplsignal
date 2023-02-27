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
        zeromarker=zeromarker,
        polemarker=polemarker,
        markercolor=markercolor,
        ax=ax,
        zerofillstyle=zerofillstyle,
        polefillstyle=polefillstyle,
        reallabel=reallabel,
        imaglabel=imaglabel,
        **kwargs,
    )
    if texts:
        for _ in range(adjust):
            # Fix for adjustText = 0.8
            ax.figure.draw_without_rendering()
            adjustText.adjust_text(texts, ax=ax)
    ax.axis('equal')
    return ax


def splane(
    zeros=None,
    poles=None,
    ax=None,
    **kwargs,
):
    """
    Plot the s-plane of a continuous-time system.

    Identical to :func:`zplane`, except that *unitcircle* is False.
    """
    return zplane(zeros=zeros, poles=poles, ax=ax, unitcircle=False, **kwargs)


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
    items

    Returns
    -------
    xpos
    ypos
    texts_x
    texts_y
    texts
    """
    xpos = []
    ypos = []
    texts_x = []
    texts_y = []
    texts = []
    for zero, mul in items.items():
        x = np.real(zero)
        y = np.imag(zero)
        xpos.append(x)
        ypos.append(y)
        if mul > 1:
            texts_x.append(x)
            texts_y.append(y)
            texts.append(f"{mul}")

    return xpos, ypos, texts_x, texts_y, texts


def _plot_plane(
    zeros,
    poles,
    zeromarker,
    polemarker,
    markercolor,
    zerofillstyle,
    polefillstyle,
    reallabel,
    imaglabel,
    ax=None,
    **kwargs,
):
    """
    Internal function for plotting poles and zeros.

    Parameters
    ----------
    zeros
    poles
    zeromarker
    polemarker
    markercolor
    zerofillstyle
    polefillstyle
    reallabel
    imaglabel
    ax
    **kwargs

    Returns
    -------
    List of texts.
    """
    ret = []
    if zeros is not None:
        zeros_d = _get_multiples(zeros)
        x_pos, y_pos, texts_x, texts_y, texts = _get_positions(zeros_d)
        ax.plot(
            x_pos,
            y_pos,
            marker=zeromarker,
            ls='none',
            fillstyle=zerofillstyle,
            color=markercolor,
            **kwargs,
        )
        ret += [ax.text(x, y, text) for x, y, text in zip(texts_x, texts_y, texts)]

    if poles is not None:
        poles_d = _get_multiples(poles)
        x_pos, y_pos, texts_x, texts_y, texts = _get_positions(poles_d)
        ax.plot(
            x_pos,
            y_pos,
            marker=polemarker,
            fillstyle=polefillstyle,
            ls='none',
            color=markercolor,
            **kwargs,
        )
        ret += [ax.text(x, y, text) for x, y, text in zip(texts_x, texts_y, texts)]

    ax.set_xlabel(reallabel)
    ax.set_ylabel(imaglabel)
    return ret


def _is_close(x, y):
    """Check if poles/zeros are close."""
    return math.isclose(np.real(x), np.real(y)) and math.isclose(np.imag(x), np.imag(y))


def _get_multiples(x):
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
