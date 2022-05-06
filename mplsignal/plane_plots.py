#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "zplane",
    "splane",
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
    linewidth=0.2,
    linecolor='black',
    zeromarker='o',
    polemarker='x',
    unitcircle=True,
    markercolor=None,
    **kwargs,
):
    r"""
    Plot the z-plane of a discrete-time system

    Parameters
    ----------
    zeros : array-like, optional
        Zeros of transfer function.
    poles : array-like, optional
        Poles of transfer function.
    ax : `Axes`, optional
        Axes to plot in.
    adjust: int, optional. Default: 1
        Number of times to execute text adjustment. Set to 0 to disable.
    linewidth : float. Default: 0.2
        Line width of axes.
    linecolor : color
        Line color of axes.
    unitcircle : bool. Default: True
        If a unit circle is drawn.
    zeromarker : marker
        Marker to use for zeros. Default: 'o'
    polemarker : marker
        Marker to use for poles. Default: 'x'
    **kwargs
        Additional arguments.

    Returns
    -------
    None.

    """
    # if Axes not provided
    if ax is None:
        ax = plt.gca()
    ax.axvline(color=linecolor, linewidth=linewidth)
    ax.axhline(color=linecolor, linewidth=linewidth)
    if markercolor is None:
        markercolor = ax._get_lines.get_next_color()
    if unitcircle:
        ax.add_patch(
            plt.Circle(
                (0, 0), radius=1, fill=False, edgecolor=linecolor, linewidth=linewidth
            )
        )
    texts = _plot_plane(
        zeros,
        poles,
        zeromarker=zeromarker,
        polemarker=polemarker,
        markercolor=markercolor,
        ax=ax,
        **kwargs,
    )
    for _ in range(adjust):
        adjustText.adjust_text(texts)
    ax.axis('equal')
    return ax


def splane(
    zeros=None,
    poles=None,
    ax=None,
    **kwargs,
):
    return zplane(zeros=zeros, poles=poles, ax=ax, unitcircle=False, **kwargs)


def zplane_tf(num=None, den=None, **kwargs):
    zeros = None if num is None else np.roots(num)
    poles = None if den is None else np.roots(den)
    return zplane(zeros=zeros, poles=poles, **kwargs)


def _get_positions(items):
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


def _plot_plane(zeros, poles, zeromarker, polemarker, markercolor, ax=None, **kwargs):
    ret = []
    if zeros is not None:
        zeros_d = _get_multiples(zeros)
        xpos, ypos, texts_x, texts_y, texts = _get_positions(zeros_d)
        ax.plot(xpos, ypos, marker=zeromarker, ls='', color=markercolor, **kwargs)
        ret += [ax.text(x, y, text) for x, y, text in zip(texts_x, texts_y, texts)]

    if poles is not None:
        poles_d = _get_multiples(poles)
        xpos, ypos, texts_x, texts_y, texts = _get_positions(poles_d)
        ax.plot(xpos, ypos, marker=polemarker, ls='', color=markercolor, **kwargs)
        ret += [ax.text(x, y, text) for x, y, text in zip(texts_x, texts_y, texts)]

    return ret


def _is_close(x, y):
    return math.isclose(np.real(x), np.real(y)) and math.isclose(np.imag(x), np.imag(y))


def _get_multiples(x):
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
