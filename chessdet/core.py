# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:37:46 2023

@author: shane
"""
from typing import Dict, List, Tuple

from chessdet import CSV_GAMES_FILE_PATH
from chessdet.models import Club, Game, Player
from chessdet.sheetutils import build_csv_reader


def load_csv(
    csv_path: str = CSV_GAMES_FILE_PATH,
) -> Tuple[List[Game], Dict[str, Player], List[Club]]:
    """Load the CSV file into entity objects"""

    # Prep the lists
    games: List[Game] = []
    players: Dict[str, Player] = {}
    clubs: List[Club] = []

    # Read CSV
    reader = build_csv_reader(csv_path)
    # # TODO: do we want this duplicated in several places, or as a function?
    # # pylint: disable=consider-using-with
    # reader = csv.DictReader(open(csv_path, "r", encoding="utf-8"))
    # reader.fieldnames = [field.strip().lower() for field in reader.fieldnames or []]

    for row in reader:
        games.append(Game(row))

    return games, players, clubs
