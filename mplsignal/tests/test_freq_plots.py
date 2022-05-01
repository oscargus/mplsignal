#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.


import pytest
from mplsignal import freqz


@pytest.mark.mpl_image_compare(filename="test_example.png")
def test_freqz():
    num = [1, 2, 1]
    den = [1, -1.5, 0.5]
    fig = freqz(num=num, den=den)
    return fig
