# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 15:22:46 2023

@author: shane
"""
import os
from typing import Dict

from chessdet.models import Player


def get_or_create_player_by_name(players: Dict[str, Player], username: str) -> Player:
    """Adds a player"""
    if username in players:
        return players[username]

    _player = Player(username)
    players[username] = _player
    return _player


def print_title(title: str) -> None:
    """Prints a neat and visible header to separate tables"""
    print(os.linesep)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(title)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()


def print_subtitle(subtitle: str) -> None:
    """Print a subtitle"""
    print()
    print(subtitle)
    print("~" * len(subtitle))
    print()


def add_club(_player: Player, club: str) -> None:
    """Adds a club tally to the club appearances dictionary"""
    _appearances = _player.club_appearances

    if club in _appearances:
        _appearances[club] += 1
    else:
        _appearances[club] = 1


# def cache_ratings_csv_file(sorted_players: List[Player]) -> None:
#     """Saves the ratings in a CSV file, so we can manually calculate match ups"""
#     headers = ["username", "mu", "phi", "sigma", "history", "clubs"]
#     rows = [
#         (
#             p.username,
#             p.rating_singles.mu,
#             p.rating_singles.phi,
#             p.rating_singles.sigma,
#             " ".join(str(round(x.mu)) for x in p.rating),
#             "|".join(p.clubs()),
#         )
#         for p in sorted_players
#     ]
#
#     # Write the rows
#     with open(CSV_RATINGS_FILE_PATH, "w", encoding="utf-8") as _f:
#         csv_writer = csv.writer(_f)
#
#         csv_writer.writerow(headers)
#         csv_writer.writerows(rows)
