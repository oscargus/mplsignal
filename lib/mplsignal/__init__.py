"""
mplsignal is a Matplotlib extension with some functions and classes aimed
at creating signal processing-related plots.
"""
# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.

# Must import __version__ first to avoid errors importing this file during the build
# process. See https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__
from .freq_plots import freqz, freqz_fir, freqz_tf, freqz_zpk
from .plane_plots import zplane, zplane_tf

__all__ = [
    '__version__',
    'freqz',
    'freqz_fir',
    'freqz_tf',
    'freqz_zpk',
    'zplane',
    'zplane_tf',
]
