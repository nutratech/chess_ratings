# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:48:37 2023

@author: shane
"""
from chessdet.core import load_csv
from tests import TEST_CSV_GAMES_FILE_PATH

EXPECTED_FIELD_NAMES = [
    "date",
    "white",
    "black",
    "result",
    "outcome",
    "location",
    "time",
    "# of moves",
    "opening",
    "variant",
    "notes",
]


def test_load_csv() -> None:
    """Test load_csv in core"""
    load_csv(TEST_CSV_GAMES_FILE_PATH)
