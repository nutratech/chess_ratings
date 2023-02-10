# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:11:07 2023

@author: shane
"""
import csv

import pytest

from chessdet.glicko2 import glicko2
from chessdet.models import Club, Game, Player
from tests import TEST_CSV_GAMES_FILE_PATH

# pylint: disable=invalid-name


def test_Club() -> None:
    """Test the Club() class"""

    clubs = set()

    club_name_raw = "Royal Oak (Methodist Church)"
    club_name_abbrev = "Royal Oak"

    club = Club(club_name_raw)

    # Test str() operator, and CLUB_DICT assignment
    assert str(club) == club_name_abbrev

    # Test hash() operator (uniqueness)
    clubs.add(club)
    clubs.add(club)
    assert club in clubs

    # Test eq() operator
    assert club == Club(club_name_raw)


def test_Game() -> None:
    """Test the Game() class with a normal CSV (happy path)"""

    # pylint: disable=consider-using-with
    reader = csv.DictReader(open(TEST_CSV_GAMES_FILE_PATH, "r", encoding="utf-8"))
    reader.fieldnames = [field.strip().lower() for field in reader.fieldnames or []]

    for row in reader:
        game = Game(row)
        print(game)


def test_Game_validate_fields() -> None:
    """Test field validation on Game entity"""

    def _default_row_builder() -> dict:
        return {
            "date": "2023-01-01",
            "white": "shane j",
            "black": "berto z",
            "result": "Black",
            "outcome": "Resignation",
            "location": "Royal Oak (Methodist Church)",
            "time": "15|10",
            "# of moves": "37",
            "opening": "B37",
            "variant": "",
            "notes": "",
        }

    # Result (not for coverage, just code sanity)
    with pytest.raises(KeyError):
        row = _default_row_builder()
        row["result"] = "INVALID_RESULT"
        Game(row)

    # Outcome
    with pytest.raises(ValueError):
        row = _default_row_builder()
        row["outcome"] = "INVALID_OUTCOME"
        Game(row)

    # Variant
    with pytest.raises(ValueError):
        row = _default_row_builder()
        row["variant"] = "INVALID_VARIANT"
        Game(row)

    # Usernames
    with pytest.raises(ValueError):
        row = _default_row_builder()
        row["white"] = ""
        Game(row)


def test_Player() -> None:
    """Test Player() class (happy path)"""

    # Basic test
    player = Player("id_0")
    print(player)

    # clubs(), home_club()
    club_name_abbrev = "Royal Oak"
    player.club_appearances[club_name_abbrev] = 2
    assert [club_name_abbrev] == player.clubs()
    assert club_name_abbrev == player.home_club()

    # W/L
    assert "0-0" == player.str_win_losses()

    # avg_opponent(), best_win()
    player.opponent_ratings = {"wins": [], "losses": [1500]}
    assert 1500 == player.avg_opponent()
    assert None is player.best_win()

    player.opponent_ratings["wins"] = [1500]
    assert 1500 == player.best_win()

    # graph_ratings()
    player.ratings.append(glicko2.Glicko2().create_rating(mu=1650))
    ratings = player.graph_ratings()
    assert 2 == len(ratings)
