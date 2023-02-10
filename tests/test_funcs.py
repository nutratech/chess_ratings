# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:32:38 2023

@author: shane
"""
from chessdet.argparser.funcs import parser_func_download, parser_func_rate


def test_parser_func_download() -> None:
    """Test "d" subcommand (download)"""
    exit_code, result = parser_func_download()
    assert exit_code == 0
    assert result is None


def test_parser_func_rate() -> None:
    """Test "r" subcommand (rate)"""
    exit_code, result = parser_func_rate()
    assert exit_code == 0
    assert result
