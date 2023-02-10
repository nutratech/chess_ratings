# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 20:11:45 2023

@author: shane
"""
from chessdet.models import Player
from chessdet.utils import get_or_create_player_by_name, print_subtitle, print_title


def test_print_title() -> None:
    """Test printing titles"""
    print_title("Test title")


def test_print_subtitle() -> None:
    """Test printing titles"""
    print_subtitle("Test subtitle")


def test_get_or_create_player_by_name() -> None:
    """Test the ability to store and retrieve players on the dictionary"""

    players = {f"id_{x}": Player(f"id_{x}") for x in range(0, 4)}

    # Check ability to retrieve existing player
    result1 = get_or_create_player_by_name(players, "id_0")
    assert result1 == players["id_0"]

    # Check ability to add new player
    new_id = "id_4"
    assert new_id not in players
    result2 = get_or_create_player_by_name(players, new_id)
    assert new_id in players
    assert result2 == players[new_id]
