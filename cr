#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Created on Fri Feb 10 10:22:44 2023

@author: shane
"""
import sys

from chessdet.__main__ import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
