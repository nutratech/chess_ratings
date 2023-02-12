# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:32:38 2023

@author: shane
"""
import argparse

from chessdet.argparser.funcs import parser_func_download, parser_func_rate


def test_parser_func_download() -> None:
    """Test "d" subcommand (download)"""
    exit_code, result = parser_func_download()
    assert exit_code == 0
    assert result is None


EMPTY_ARGPARSE_NAMESPACE = argparse.Namespace(skip_dl=True, matches=False, graph=True)


def test_parser_func_rate() -> None:
    """Test "r" subcommand (rate)"""
    # TODO: inject mock HTTP response, OR use test_data CSV
    exit_code, result = parser_func_rate(
        argparse.Namespace(skip_dl=True, matches=True, graph=True)
    )
    assert exit_code == 0
    assert result
