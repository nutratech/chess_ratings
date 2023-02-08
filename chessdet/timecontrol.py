# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:13:36 2023

@author: shane
"""
import math

TIME_CONTROL_ULTRA_BULLET = ("UltraBullet", 30)
TIME_CONTROL_BULLET = ("Bullet", 180)
TIME_CONTROL_BLITZ = ("Blitz", 480)
TIME_CONTROL_RAPID = ("Rapid", 1500)
TIME_CONTROL_CLASSICAL = ("Classical", 8400)
TIME_CONTROL_CORRESPONDENCE = ("Correspondence", math.inf)

TIME_CONTROLS = [
    TIME_CONTROL_ULTRA_BULLET,
    TIME_CONTROL_BULLET,
    TIME_CONTROL_BLITZ,
    TIME_CONTROL_RAPID,
    TIME_CONTROL_CLASSICAL,
]


def game_type(base_time: int, increment: int) -> str:
    """
    Return the type of game based on base time and increment formula.
    (See: https://lichess.org/faq#time-controls)

    :param base_time: Starting time in seconds.
    :param increment: Increment in seconds.
    """

    game_duration = base_time + 40 * increment

    for _game_type, max_time in TIME_CONTROLS:
        if game_duration <= max_time:
            return _game_type

    return TIME_CONTROL_CORRESPONDENCE[0]
