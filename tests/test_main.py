# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 12:49:16 2023

@author: shane
"""
import sys

import pytest
import requests.exceptions
from requests_mock import Mocker

from chessdet import __title__
from chessdet.__main__ import build_arg_parser, main
from chessdet.env import CSV_GAMES_URL


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


def test_func() -> None:
    """Test ability of __main__ to handle sub-commands (and DEBUG flag)"""
    main(args=["-d", "rank", "-s"])


def test_main_http_error_and_url_error(requests_mock: Mocker) -> None:
    """Test the HTTP / URL exceptions"""

    with pytest.raises(requests.exceptions.HTTPError):
        requests_mock.get(CSV_GAMES_URL, status_code=400)  # nosec: B113
        main(args=["-d", "fetch"])
