# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 20:11:45 2023

@author: shane
"""
from chessdet.core import (
    add_club,
    get_or_create_player_by_name,
    print_subtitle,
    print_title,
)
from chessdet.models import Player


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


def test_add_club() -> None:
    """Test the ability to track club appearances"""
    player = Player("Guy")
    club = "Home"

    # Initialize new club
    add_club(player, club)
    assert club in player.club_appearances
    assert 1 == player.club_appearances[club]

    # Add tally to existing club
    add_club(player, club)
    assert 2 == player.club_appearances[club]
