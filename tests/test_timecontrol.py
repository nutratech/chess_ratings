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
        (30, 0, "UltraBullet"),
        (15 * 60, 10, "Rapid"),
        (30 * 60, 0, "Classical"),
        (60 * 60, 180, "Correspondence"),
    ],
)
def test_categories(base_time: int, increment: int, category: str) -> None:
    """Test that e.g. 15|10 is mapped to Rapid"""
    assert category == game_type(base_time, increment)


if __name__ == "__main__":
    pytest.main()
