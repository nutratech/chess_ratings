# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 12:49:16 2023

@author: shane
"""
import sys

import pytest

from chessdet import __title__
from chessdet.__main__ import build_arg_parser, main


def test_build_arg_parser() -> None:
    """Test the method to build the whole ArgParser()"""
    arg_parser = build_arg_parser()
    assert arg_parser.prog == __title__


def test_main() -> None:
    """Test the main method to prepare the builder"""
    # Empty out PyCharm's testing arguments
    sys.argv = []

    # Test without args
    exit_code = main()
    assert exit_code == 0

    # Test with args, "-v"
    with pytest.raises(SystemExit) as exc_info:
        main(args=["-v"])
    assert exc_info.value.code == 0

    # Test with "-h"
    with pytest.raises(SystemExit) as exc_info:
        main(args=["-h"])
    assert exc_info.value.code == 0


def test_with_debug() -> None:
    """Test with DEBUG=True"""
    exit_code = main(args=["-d"])
    assert exit_code == 0
