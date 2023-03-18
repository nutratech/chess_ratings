# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:56:29 2023

@author: shane
"""
import pytest

from chessdet.timecontrol import game_type


@pytest.mark.parametrize(
    "base_time,increment,category",
    [
        (1, 0, "UltraBullet"),
        (2, 1, "Bullet"),
        # Blitz
        (5, 4, "Blitz"),
        (10, 0, "Blitz"),
        # Rapid
        (7, 5, "Rapid"),
        (15, 10, "Rapid"),
        (20, 5, "Rapid"),
        # Classical
        (20, 15, "Classical"),
        (120, 60, "Classical"),
        (240, 180, "Classical"),
    ],
)
def test_game_type(base_time: int, increment: int, category: str) -> None:
    """Test that e.g. 15+10 is mapped to Rapid"""
    assert category == game_type(base_time, increment)


if __name__ == "__main__":
    pytest.main()
