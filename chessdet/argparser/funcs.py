# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:26:28 2023

@author: shane
"""
from typing import Tuple

from chessdet.core import process_csv
from chessdet.sheetutils import cache_csv_games_file, get_google_sheet
from chessdet.utils import print_subtitle


def parser_func_download() -> Tuple[int, None]:
    """Default function for download parser"""
    cache_csv_games_file(_csv_bytes_output=get_google_sheet())
    return 0, None


def parser_func_rate() -> Tuple[int, tuple]:
    """Default function for rate parser"""
    games, players, clubs = process_csv()

    # WIP test stuff
    print_subtitle("Games")
    for game in games:
        print(game)
    print_subtitle("Players")
    for player in players.values():
        print(player)
    print_subtitle("Clubs")
    for club in clubs:
        print(club)

    return 0, (games, players, clubs)
