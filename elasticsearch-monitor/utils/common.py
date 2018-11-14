#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
Author: Ligh
Mail: xiaohui920@sina.cn
File: __init__.py
Created Time: 11/13/18 16:41
"""

from traceback import print_exc

import yaml


def load_yaml_data(filename=None):
    try:
        with open(filename, 'r') as f:
            data = yaml.load(f)
            return data
    except IOError:
        print_exc()
