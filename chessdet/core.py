# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:37:46 2023

@author: shane
"""
from typing import Dict, List, Set, Tuple

from chessdet import BLACK, CSV_GAMES_FILE_PATH, WHITE
from chessdet.glicko2 import glicko2
from chessdet.models import Club, Game, Player
from chessdet.sheetutils import build_csv_reader
from chessdet.utils import get_or_create_player_by_name


def update_players_ratings(players: Dict[str, Player], game: Game) -> None:
    """Update two players' ratings, based on a game outcome together"""

    def do_game(player1: Player, player2: Player, drawn: bool = False) -> None:
        """NOTE: player1 is winner by default, unless drawn (then it doesn't matter)"""
        _new_rating_player1, _new_rating_player2 = glicko.rate_1vs1(
            player1.rating, player2.rating, drawn=drawn
        )

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

    return games, players, clubs
