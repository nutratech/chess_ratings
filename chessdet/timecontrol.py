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
TIME_CONTROL_CLASSICAL = ("Classical", math.inf)
TIME_CONTROL_CORRESPONDENCE = ("Correspondence", -1)

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

    :param base_time: Starting time in MINUTES.
    :param increment: Increment in SECONDS.
    """

    game_duration = base_time * 60 + increment * 40

    if game_duration < TIME_CONTROL_ULTRA_BULLET[1]:
        return TIME_CONTROL_ULTRA_BULLET[0]
    if game_duration < TIME_CONTROL_BULLET[1]:
        return TIME_CONTROL_BULLET[0]
    if game_duration < TIME_CONTROL_BLITZ[1]:
        return TIME_CONTROL_BLITZ[0]
    if game_duration < TIME_CONTROL_RAPID[1]:
        return TIME_CONTROL_RAPID[0]
        #  else: game_duration < TIME_CONTROL_CLASSICAL[1]:
    return TIME_CONTROL_CLASSICAL[0]
