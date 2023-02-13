# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:37:46 2023

@author: shane
"""
import math
from typing import Dict, List, Set, Tuple

from tabulate import tabulate

from chessdet import BLACK, CSV_GAMES_FILE_PATH, WHITE
from chessdet.glicko2 import glicko2
from chessdet.models import Club, Game, Player
from chessdet.sheetutils import build_csv_reader
from chessdet.utils import get_or_create_player_by_name, print_title


def update_players_ratings(players: Dict[str, Player], game: Game) -> None:
    """Update two players' ratings, based on a game outcome together"""

    def do_game(player1: Player, player2: Player, drawn: bool = False) -> None:
        """NOTE: player1 is winner by default, unless drawn (then it doesn't matter)"""

        # Add opponent ratings
        if drawn:
            player1.opponent_ratings["draws"].append(player2.rating.mu)
            player2.opponent_ratings["draws"].append(player1.rating.mu)
        else:
            player1.opponent_ratings["wins"].append(player2.rating.mu)
            player2.opponent_ratings["losses"].append(player1.rating.mu)

        # Add clubs
        player1.add_club(game.location.name)
        player2.add_club(game.location.name)

        # Update ratings
        _new_rating_player1, _new_rating_player2 = glicko.rate_1vs1(
            player1.rating, player2.rating, drawn=drawn
        )
        player1.ratings.append(_new_rating_player1)
        player2.ratings.append(_new_rating_player2)

    # Create the rating engine
    glicko = glicko2.Glicko2()

    # Extract (or create) player_white & player_black from Players Dict
    player_white = get_or_create_player_by_name(players, game.username_white)
    player_black = get_or_create_player_by_name(players, game.username_black)

    # Run the helper methods
    if game.result == WHITE:
        do_game(player_white, player_black)
    elif game.result == BLACK:
        do_game(player_black, player_white)
    else:
        # NOTE: already validated in: self.score = DICT_OUTCOME_TO_SCORE[self.result]
        do_game(player_white, player_black, drawn=True)


def process_csv(
    csv_path: str = CSV_GAMES_FILE_PATH,
) -> Tuple[List[Game], Dict[str, Player], Set[Club]]:
    """Load the CSV file into entity objects"""

    # Prep the lists
    games: List[Game] = []
    players: Dict[str, Player] = {}
    clubs: Set[Club] = set()

    # Read CSV
    reader = build_csv_reader(csv_path)

    for row in reader:
        game = Game(row)
        games.append(game)
        clubs.add(game.location)

        # Update players stats and ratings
        update_players_ratings(players, game)

    # Sort players by ratings
    sorted_players = sorted(
        players.values(), key=lambda x: float(x.rating.mu), reverse=True
    )
    players = {p.username: p for p in sorted_players}

    return games, players, clubs


def func_rank(
    games: List[Game],
    players: Dict[str, Player],
    clubs: List[Club],
) -> None:
    """Rank function used by rank sub-parser"""

    # Print the rankings table
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
            "Best W",
            "Best D",
            "Club",
        ],
    )
    print_title(
        f"Rankings ({len(games)} games, {len(players)} players, {len(clubs)} clubs)"
    )
    print(_table)


def func_match_ups(
    players: Dict[str, Player],
) -> Tuple[int, List[Tuple[str, str, int, int, float]]]:
    """Print match ups (used by rank sub-parser)"""

    def match_up(player1: Player, player2: Player) -> Tuple[str, str, int, int, float]:
        """Yields an individual match up for the table data"""
        glicko = glicko2.Glicko2()

        delta_rating = round(player1.rating.mu - player2.rating.mu)
        rd_avg = int(
            round(
                math.sqrt((player1.rating.phi**2 + player2.rating.phi**2) / 2),
                -1,
            )
        )
        expected_score = round(
            glicko.expect_score(
                glicko.scale_down(player1.rating),
                glicko.scale_down(player2.rating),
                glicko.reduce_impact(
                    glicko.scale_down(player2.rating),
                ),
            ),
            2,
        )
        return (
            player1.username,
            player2.username,
            delta_rating,
            rd_avg,
            expected_score,
        )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Main match up method
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    players_list = list(players.values())

    match_ups = []
    n_players = len(players)

    # pylint: disable=invalid-name,consider-using-enumerate
    for i1 in range(len(players_list)):
        p1 = players_list[i1]
        for i2 in range(i1 + 1, len(players)):
            p2 = players_list[i2]
            match_ups.append(match_up(p1, p2))

    _n_pairs = math.comb(n_players, 2)
    _n_top = min(100, _n_pairs)
    print_title(f"Match ups (top {_n_top}, {n_players}C2={_n_pairs} possible)")
    _table = tabulate(
        match_ups,
        headers=["Player 1", "Player 2", "ΔR", "RD", "E"],
    )
    print(_table)

    return 0, match_ups
