#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.


import pytest
import matplotlib.pyplot as plt
from mplsignal import freqz


def test_freqz():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den)
    assert len(fig.axes) == 2


def test_freqz_twin():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den, style='twin')
    assert len(fig.axes) == 2


def test_freqz_magnitude():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den, style='magnitude')
    assert len(fig.axes) == 1


def test_freqz_phase():
    plt.figure()
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den, style='phase')
    assert len(fig.axes) == 1
