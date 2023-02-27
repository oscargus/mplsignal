#!/usr/bin/env python
# coding: utf-8

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


def group_delay(num, den, w):
    """
    Evaluate transfer function to determine group delay.

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
    gd : ndarray
        The group delay.

    """
    if signal:
        return signal.group_delay((num, den), w=w)[1]
    else:
        # TODO: compute actual group delay
        gd, _ = group_delay_from_h(w, freqz_tf(num, den, w))
        gd.append(0)
        return gd


def group_delay_from_h(w, h):
    """
    Estimate group delay from frequency response.

    Parameters
    ----------
    w : array-like
        Frequency-points.
    h : array-like
        Frequency response.

    Returns
    -------
    gd : ndarray
        The estimated group delay.
    w : ndarray
        The frequency points where the group delay is estimated.
    """
    angle = np.unwrap(np.angle(h))
    angle_diff = np.diff(angle)
    angle_diff[np.abs(angle_diff) > 3] = np.nan
    w_diff = np.diff(w)
    w_new = w[0:-1] + w_diff / 2
    gd = -angle_diff / w_diff
    return gd, w_new
