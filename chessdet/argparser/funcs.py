# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:26:28 2023

@author: shane
"""
from typing import Dict, List, Set, Tuple

from tabulate import tabulate

from chessdet.core import process_csv
from chessdet.models import Club, Game, Player
from chessdet.sheetutils import cache_csv_games_file, get_google_sheet


def parser_func_download() -> Tuple[int, None]:
    """Default function for download parser"""
    cache_csv_games_file(
        _csv_bytes_output=get_google_sheet(),
    )
    return 0, None


def parser_func_rate() -> Tuple[int, Tuple[List[Game], Dict[str, Player], Set[Club]]]:
    """Default function for rate parser"""
    games, players, clubs = process_csv()

    # Print the rankings table
    # pylint: disable=invalid-name
    p: Player  # noqa: F842
    table_series_players = [
        (
            p.username,
            p.str_rating(),
            p.str_wins_draws_losses(),
            round(max(x.mu for x in p.ratings)),
            p.avg_opponent(),
            p.best_win(),
            p.best_win(mode="draws"),
            p.home_club(),
        )
        for p in players.values()
    ]
    _table = tabulate(
        table_series_players,
        headers=[
            "Username",
            "Glicko 2",
            "Record",
            "Top",
            "Avg opp",
            "B win",
            "B draw",
            "Club",
        ],
    )
    print(_table)

    return 0, (games, players, clubs)
