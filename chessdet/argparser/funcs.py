# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:26:28 2023

@author: shane
"""
import math
from typing import Dict, List, Set, Tuple

from tabulate import tabulate

from chessdet.core import process_csv
from chessdet.glicko2 import glicko2
from chessdet.models import Club, Game, Player
from chessdet.sheetutils import cache_csv_games_file, get_google_sheet
from chessdet.utils import print_title


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
    print_title(
        f"Rankings ({len(games)} games, {len(players)} players, {len(clubs)} clubs)"
    )
    print(_table)

    # Print the rating progress charts
    print_title("Rating progress charts")
    for p in players.values():
        print()
        print(p)
        p.graph_ratings()

    return 0, (games, players, clubs)


def parser_func_match_ups() -> Tuple[int, tuple]:
    """Default function for rate parser"""

    def match_up(player1: Player, player2: Player) -> tuple:
        """Yields an individual match up for the table data"""
        glicko = glicko2.Glicko2()

        delta_rating = round(player1.rating.mu - player2.rating.mu)
        rd_avg = int(
            round(
                math.sqrt((player1.rating.phi**2 + player2.rating.phi**2) / 2),
                -1,
            )
        )
        win_probability = round(
            glicko.expect_score(
                glicko.scale_down(player1.rating),
                glicko.scale_down(player2.rating),
                glicko.reduce_impact(
                    glicko.scale_down(player2.rating),
                ),
            ),
            2,
        )
        loss_probability = round(
            glicko.expect_score(
                glicko.scale_down(player2.rating),
                glicko.scale_down(player1.rating),
                glicko.reduce_impact(
                    glicko.scale_down(player1.rating),
                ),
            ),
            2,
        )
        draw_probability = round(
            glicko.quality_1vs1(
                glicko.scale_down(player1.rating),
                glicko.scale_down(player2.rating),
            ),
            2,
        )
        return (
            player1.username,
            player2.username,
            delta_rating,
            rd_avg,
            win_probability,
            loss_probability,
            draw_probability,
        )

    games, players, clubs = process_csv()
    players_list = list(players.values())

    match_ups = []
    # pylint: disable=invalid-name,consider-using-enumerate
    for i1 in range(len(players_list)):
        p1 = players_list[i1]
        for i2 in range(i1 + 1, len(players)):
            p2 = players_list[i2]
            match_ups.append(match_up(p1, p2))

    print_title("Match ups")
    _table = tabulate(
        match_ups,
        headers=["Player 1", "Player 2", "Δμ", "RD", "P(w)", "P(l)", "P(d)"],
    )
    print(_table)

    return 0, (games, players, clubs)
