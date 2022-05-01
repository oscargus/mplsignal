#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Oscar Gustafsson.
# Distributed under the terms of the Modified BSD License.


def import_module(module):
    levels = module.split(".")
    try:
        mod = __import__(levels[0])
        if len(levels) == 1:
            return mod
        return mod.__dict__[levels[1]]
    except ImportError:
        return
