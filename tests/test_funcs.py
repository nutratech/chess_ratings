# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:32:38 2023

@author: shane
"""
import argparse

from chessdet.argparser.funcs import (
    parser_func_download,
    parser_func_match_ups,
    parser_func_rate,
)


def test_parser_func_download() -> None:
    """Test "d" subcommand (download)"""
    exit_code, result = parser_func_download()
    assert exit_code == 0
    assert result is None


EMPTY_ARGPARSE_NAMESPACE = argparse.Namespace(skip_dl=True, matches=False)


def test_parser_func_rate() -> None:
    """Test "r" subcommand (rate)"""
    exit_code, result = parser_func_rate(EMPTY_ARGPARSE_NAMESPACE)
    assert exit_code == 0
    assert result


def test_parser_func_match_ups() -> None:
    """Test "m" subcommand (match ups)"""
    exit_code, result = parser_func_match_ups(EMPTY_ARGPARSE_NAMESPACE)
    assert exit_code == 0
    assert result
