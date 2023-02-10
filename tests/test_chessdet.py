# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 12:42:53 2023

@author: shane
"""
import argparse

from chessdet import CliConfig

# pylint: disable=invalid-name


def test_CliConfig() -> None:
    """Test the CLI_CONFIG() class instance"""
    # Test initial values
    CLI_CONFIG = CliConfig()
    assert not CLI_CONFIG.debug
    assert CLI_CONFIG.paging

    # Test ability to store & retrieve updated values
    CLI_CONFIG.set_flags(argparse.Namespace(debug=True, no_pager=True))

    assert CLI_CONFIG
    assert not CLI_CONFIG.paging
