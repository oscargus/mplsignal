#!/usr/bin/env python

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "freqz_tf",
    "freqz_zpk",
]

try:
    import scipy.signal as signal
except ImportError:
    signal = None
import numpy as np


def freqz_tf(num, den, w):
    """
    Evaluate transfer function to determine frequency response.

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
    w : ndarray
        The angular frequencies at which *h* was computed.
    h : ndarray
        The frequency response.

    """
    if signal:
        return signal.freqz(num, den, worN=w)[1]
    else:
        wexp = np.exp(-1j * w)
        h = np.polynomial.polynomial.polyval(
            wexp, num, tensor=False
        ) / np.polynomial.polynomial.polyval(wexp, den, tensor=False)
        return h


def freqz_zpk(zeros, poles, gain, w):
    """
    Evaluate transfer function to determine frequency response.

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
    w : ndarray
        The angular frequencies at which *h* was computed.
    h : ndarray
        The frequency response.

    """
    if signal:
        return signal.freqz_zpk(zeros, poles, gain, worN=w)[1]
    else:
        wexp = np.exp(1j * w)
        h = np.polynomial.polynomial.polyvalfromroots(
            wexp, zeros
        ) / np.polynomial.polynomial.polyvalfromroots(wexp, poles)
        return h
