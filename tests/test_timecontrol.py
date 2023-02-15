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
        (0.25, 0, "UltraBullet"),
        (0.5, 0, "Bullet"),
        (2, 1, "Bullet"),
        (3, 0, "Blitz"),
        (5, 3, "Blitz"),
        (5, 5, "Rapid"),
        (10, 0, "Rapid"),
        (15, 10, "Rapid"),
        (30, 0, "Classical"),
        (120, 60, "Classical"),
        (240, 180, "Classical"),
    ],
)
def test_game_type(base_time: int, increment: int, category: str) -> None:
    """Test that e.g. 15+10 is mapped to Rapid"""
    assert category == game_type(base_time, increment)


# @pytest.mark.parametrize(
#     "base_time,increment,category",
#     [
#         (0.25, 0, "UltraBullet"),
#         (0.5, 0, "Bullet"),
#         (2, 1, "Bullet"),
#         (3, 0, "Blitz"),
#         (5, 3, "Blitz"),
#         (5, 5, "Rapid"),
#         (10, 0, "Rapid"),
#         (15, 10, "Rapid"),
#         (30, 0, "Classical"),
#         (120, 60, "Classical"),
#         (240, 180, "Classical"),
#     ],
# )
# def test_game_type_correspondence(
#     base_time: int, increment: int, category: str
# ) -> None:
#     """Test that e.g. 15+10 is mapped to Rapid"""
#     assert category == game_type(base_time, increment)
#
#
# @pytest.mark.parametrize(
#     "base_time,increment,category",
#     [
#         (0.25, 0, "UltraBullet"),
#         (0.5, 0, "Bullet"),
#         (2, 1, "Bullet"),
#         (3, 0, "Blitz"),
#         (5, 3, "Blitz"),
#         (5, 5, "Rapid"),
#         (10, 0, "Rapid"),
#         (15, 10, "Rapid"),
#         (30, 0, "Classical"),
#         (120, 60, "Classical"),
#         (240, 180, "Classical"),
#     ],
# )
# def test_game_type_invalid_throws_value_error(
#     base_time: str, increment: int, category: str
# ) -> None:
#     """Test that invalid time controls throw errors"""
#     with pytest.raises(ValueError):
#         game_type(base_time, increment)


if __name__ == "__main__":
    pytest.main()
