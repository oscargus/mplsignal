#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "freqz_tf",
    "freqz_zpk",
]

from ._tools import import_module

signal = import_module('scipy,signal')


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
        return signal.freqz(num, den, worN=w)
    else:
        raise ImportError("SciPy not installed.")


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
        return signal.freqz_zpk(zeros, poles, gain, worN=w)
    else:
        raise ImportError("SciPy not installed.")
