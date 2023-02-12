# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:26:28 2023

@author: shane
"""
import argparse
from typing import Dict, List, Set, Tuple

from chessdet.core import func_rate, process_csv
from chessdet.models import Club, Game, Player
from chessdet.sheetutils import cache_csv_games_file, get_google_sheet


def parser_func_download() -> Tuple[int, None]:
    """Default function for download parser"""
    cache_csv_games_file(
        _csv_bytes_output=get_google_sheet(),
    )
    return 0, None


def parser_func_rate(
    args: argparse.Namespace,
) -> Tuple[int, Tuple[List[Game], Dict[str, Player], Set[Club]]]:
    """Default function for rate parser"""

    # FIXME: make this into an annotation function? Easily, neatly re-usable & testable.
    if not args.skip_dl:
        cache_csv_games_file(
            _csv_bytes_output=get_google_sheet(),
        )

    games, players, clubs = process_csv()

    func_rate(args, games=games, players=players, clubs=list(clubs))

    return 0, (games, players, clubs)
