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
    unitcircle=True,
    **kwargs,
):
    r"""
    Plot the frequency response of a discrete-time system.

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
    unitcircle: bool. Default: True
        If a unit circle is drawn.
    **kwargs
        Additional arguments.

    Returns
    -------
    None.

    """
    # if Axes not provided
    if ax is None:
        ax = plt.gca()
    linewidth = 0.2
    color = "black"
    ax.axvline(color=color, linewidth=linewidth)
    ax.axhline(color=color, linewidth=linewidth)
    if unitcircle:
        ax.add_patch(
            plt.Circle(
                (0, 0), radius=1, fill=False, edgecolor=color, linewidth=linewidth
            )
        )
    texts = _plot_plane(zeros, poles, ax=ax, **kwargs)
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
    unitcircle = kwargs.pop('unitcircle', False)
    return zplane(zeros=zeros, poles=poles, ax=ax, unitcircle=unitcircle, **kwargs)


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


def _plot_plane(zeros, poles, ax=None, **kwargs):
    ret = []
    if zeros is not None:
        zeros_d = _get_multiples(zeros)
        xpos, ypos, texts_x, texts_y, texts = _get_positions(zeros_d)
        ax.scatter(xpos, ypos, marker='o')
        ret += [ax.text(x, y, text) for x, y, text in zip(texts_x, texts_y, texts)]

    if poles is not None:
        poles_d = _get_multiples(poles)
        xpos, ypos, texts_x, texts_y, texts = _get_positions(poles_d)
        ax.scatter(xpos, ypos, marker='x')
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
