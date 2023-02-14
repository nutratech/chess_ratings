# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:32:38 2023

@author: shane
"""
import argparse

from chessdet.argparser.funcs import parser_func_download, parser_func_rank


def test_parser_func_download() -> None:
    """Test "d" subcommand (download)"""
    exit_code, result = parser_func_download()
    assert exit_code == 0
    assert result is None


def test_parser_func_rank() -> None:
    """Test "r" subcommand (rank)"""
    # TODO: inject mock HTTP response, OR use test_data CSV
    exit_code, result = parser_func_rank(
        argparse.Namespace(skip_dl=True, matches=True, graph=True, abbrev_titles=True)
    )
    assert exit_code == 0
    assert result
