# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:48:37 2023

@author: shane
"""
from chessdet.core import process_csv
from tests import TEST_CSV_GAMES_FILE_PATH


def test_process_csv() -> None:
    """Test process_csv in core"""
    games, players, clubs = process_csv(TEST_CSV_GAMES_FILE_PATH)

    assert games
    assert players
    assert clubs
