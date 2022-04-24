# -*- coding: utf-8 -*-
import os

__author__ = 'mc'


def configuration_file(name: str):
    filename = name + ".conf"
    if os.path.isfile(os.path.join(os.path.abspath(os.path.dirname('__file__')), 'templates', filename)):
        return filename
    else:
        return False

