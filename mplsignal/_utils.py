#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "freqz_tf", "freqz_zpk",
]
import numpy as np
from scipy import signal


def freqz_tf(num, den, w):
    """


    Parameters
    ----------
    num : array-like
        Numerator.
    den : array-like
        Denominator.
    w : array-like
        Frequency-points.

    Returns
    -------
    ndarray with complex frequency response.

    """
    return signal.freqz(num, den, w)


def freqz_zpk(zeros, poles, gain, w):
    """


    Parameters
    ----------
    zeros : array-like
        Zeros.
    poles : array-like
        Poles.
    gain : float
        Gain.
    w : array-like
        Frequency-points.

    Returns
    -------
    ndarray with complex frequency response.

    """
